#!/usr/bin/env python3
"""Audit the plain-text Anki card format used by the Anki skills."""

from __future__ import annotations

import argparse
import html
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


HEADER_RE = re.compile(r"(?m)^(\d+)\. Card \(page ([^)]+)\)\s*$")
VAGUE_RE = re.compile(
    r"\b(identify|identifies|formalize|formalizes|synthesize|synthesizes|"
    r"define|defines|play(?:s)? a role|is used for|are used for|is important|are important)\b",
    re.IGNORECASE,
)
ARTIFACT_RE = re.compile(
    r"\b(lecture|presentation|slide|deck|figure|diagram|shown|mentioned|named|highlighted)\b",
    re.IGNORECASE,
)
FORMULA_RE = re.compile(
    r"\b(formula|equation|calculate|calculation)\b|\bcompute\s+(?:the|a|an|this|that)\b",
    re.IGNORECASE,
)
TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_+-]*")
STOPWORDS = {
    "a", "an", "and", "are", "does", "for", "how", "in", "is", "of", "on",
    "the", "to", "what", "when", "which", "why", "with",
}


@dataclass
class Card:
    number: int
    page: str
    front: str
    back: str


def parse_cards(text: str) -> tuple[list[Card], list[str]]:
    matches = list(HEADER_RE.finditer(text))
    errors: list[str] = []
    cards: list[Card] = []
    if not matches:
        return [], ["No card headers found."]
    if text[: matches[0].start()].strip():
        errors.append("Text appears before the first card header.")

    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end].strip()
        parts = re.split(r"(?m)^Back:\s*$", body, maxsplit=1)
        if len(parts) != 2 or not re.search(r"(?m)^Front:\s*$", parts[0]):
            errors.append(f"Card {match.group(1)}: missing Front:/Back: structure.")
            continue
        front = re.split(r"(?m)^Front:\s*$", parts[0], maxsplit=1)[1].strip()
        cards.append(Card(int(match.group(1)), match.group(2).strip(), front, parts[1].strip()))
    return cards, errors


def visible_text(value: str) -> str:
    value = re.sub(r"!\[[^]]*\]\([^)]*\)", " ", value)
    value = re.sub(r"<img\b[^>]*>", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def main_answer(back: str) -> str:
    return re.split(r"(?m)^Example:\s*", back, maxsplit=1)[0].strip()


def normalized(value: str) -> str:
    return " ".join(TOKEN_RE.findall(visible_text(value).lower()))


def content_tokens(value: str) -> set[str]:
    return {token for token in TOKEN_RE.findall(value.lower()) if token not in STOPWORDS and len(token) > 1}


def warn_list_shape(card: Card, answer: str) -> str | None:
    bullets = re.findall(r"(?m)^\s*[-*]\s+\S", answer)
    if len(bullets) > 3:
        return f"Card {card.number}: answer has {len(bullets)} bullet items; inspect as an unbounded set."
    if answer.count(",") >= 3 and not re.search(r"[=/]", answer):
        return f"Card {card.number}: comma-heavy answer may contain more than three independent items."
    return None


def audit(cards: list[Card], args: argparse.Namespace) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    numbers = [card.number for card in cards]
    expected = list(range(1, len(cards) + 1))
    if numbers != expected:
        errors.append(f"Card numbering is not sequential: expected 1..{len(cards)}.")
    if args.min_cards is not None and len(cards) < args.min_cards:
        warnings.append(f"Deck has {len(cards)} cards, below target minimum {args.min_cards}.")
    if args.max_cards is not None and len(cards) > args.max_cards:
        warnings.append(f"Deck has {len(cards)} cards, above target maximum {args.max_cards}.")

    by_back: dict[str, list[int]] = defaultdict(list)
    front_tokens: list[set[str]] = []
    for card in cards:
        answer = main_answer(card.back)
        front_visible = visible_text(card.front)
        answer_visible = visible_text(answer)
        if not front_visible:
            errors.append(f"Card {card.number}: empty front.")
        if not answer_visible:
            errors.append(f"Card {card.number}: empty or image-only main answer.")
        if card.front.count("?") > 1:
            warnings.append(f"Card {card.number}: multiple question marks suggest a compound prompt.")
        if VAGUE_RE.search(front_visible):
            warnings.append(f"Card {card.number}: cue contains a potentially vague load-bearing verb.")
        if ARTIFACT_RE.search(front_visible):
            warnings.append(f"Card {card.number}: inspect possible source-artifact wording.")
        word_count = len(TOKEN_RE.findall(answer_visible))
        if word_count > args.max_answer_words:
            warnings.append(
                f"Card {card.number}: main answer has {word_count} words (trigger: {args.max_answer_words})."
            )
        list_warning = warn_list_shape(card, answer)
        if list_warning:
            warnings.append(list_warning)
        if FORMULA_RE.search(front_visible) and not re.search(r"[=/×÷]|\\(?:approx|frac|sum|prod)\b", answer_visible):
            warnings.append(f"Card {card.number}: formula-like cue has no formula-like text answer.")
        back_key = normalized(answer)
        if back_key:
            by_back[back_key].append(card.number)
        front_tokens.append(content_tokens(front_visible))

    for key, card_numbers in by_back.items():
        if len(card_numbers) > 1:
            warnings.append(f"Cards {card_numbers}: identical normalized main answers: {key[:80]!r}.")

    for left in range(len(cards)):
        for right in range(left + 1, len(cards)):
            a, b = front_tokens[left], front_tokens[right]
            if min(len(a), len(b)) < 3:
                continue
            similarity = len(a & b) / len(a | b)
            if similarity >= args.similarity and normalized(cards[left].back) != normalized(cards[right].back):
                warnings.append(
                    f"Cards {cards[left].number} and {cards[right].number}: similar fronts "
                    f"({similarity:.0%}) with different answers; inspect for cue collision."
                )
                if len(warnings) >= args.max_warnings:
                    warnings.append("Warning limit reached; rerun with --max-warnings to inspect more.")
                    return errors, warnings
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path)
    parser.add_argument("--min-cards", type=int)
    parser.add_argument("--max-cards", type=int)
    parser.add_argument("--max-answer-words", type=int, default=25)
    parser.add_argument("--similarity", type=float, default=0.60)
    parser.add_argument("--max-warnings", type=int, default=200)
    parser.add_argument("--strict", action="store_true", help="Return nonzero when warnings remain.")
    args = parser.parse_args()

    cards, parse_errors = parse_cards(args.deck.read_text(encoding="utf-8"))
    errors, warnings = audit(cards, args) if cards else ([], [])
    errors = parse_errors + errors
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")
    print(f"Audited {len(cards)} cards: {len(errors)} errors, {len(warnings)} warnings.")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
