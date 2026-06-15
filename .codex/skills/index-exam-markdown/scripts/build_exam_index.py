#!/usr/bin/env python3
"""Build and validate a topic/term index for structured exam Markdown."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


TASK_RE = re.compile(r"^## (Aufgabe|Task|Exercise) (\d+):\s*(.*)$", re.M)
SOLUTION_RE = re.compile(
    r"^## (?:Lösung zur Aufgabe|Solution for (?:Task|Exercise)) (\d+)\s*$",
    re.M,
)
SUBTASK_RE = re.compile(r"^### (\d+) ([a-z])\)\s*$", re.M)


def slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"[\s_-]+", "-", text).strip("-")


def label(path: Path) -> str:
    stem = path.stem.upper()
    winter = re.search(r"WS(\d{2})(\d{2})", stem)
    summer = re.search(r"SS(\d{2})", stem)
    if winter:
        return f"WS {winter.group(1)}/{winter.group(2)}"
    if summer:
        return f"SS {summer.group(1)}"
    return path.stem


@dataclass(frozen=True)
class Ref:
    file: str
    exam: str
    number: int
    unit: str
    heading: str
    subtask: str | None = None

    @property
    def anchor(self) -> str:
        return f"{self.number}-{self.subtask}" if self.subtask else slug(self.heading)

    @property
    def markdown(self) -> str:
        detail = f" {self.subtask})" if self.subtask else ""
        return f"[{self.exam}, {self.unit} {self.number}{detail}]({self.file}#{self.anchor})"


@dataclass
class Segment:
    ref: Ref
    text: str


@dataclass
class Exercise:
    ref: Ref
    title: str
    segments: list[Segment]


def clean(text: str) -> str:
    text = re.sub(r"!\[[^\]]*]\([^)]*\)", " ", text)
    text = re.sub(r"`[^`]*`", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def subtasks(text: str, base: Ref) -> tuple[str, dict[str, str]]:
    matches = list(SUBTASK_RE.finditer(text))
    intro = text[: matches[0].start() if matches else len(text)].strip()
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        if int(match.group(1)) != base.number:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(2)] = text[match.end():end]
    return intro, result


def parse(path: Path) -> list[Exercise]:
    text = path.read_text(encoding="utf-8")
    matches = list(TASK_RE.finditer(text))
    result: list[Exercise] = []
    for index, match in enumerate(matches):
        number = int(match.group(2))
        solution = SOLUTION_RE.search(text, match.end())
        if not solution or int(solution.group(1)) != number:
            raise ValueError(f"{path}: no matching solution for exercise {number}")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        heading = match.group(0).removeprefix("## ")
        base = Ref(path.name, label(path), number, match.group(1), heading)
        prompt_intro, prompt_parts = subtasks(text[match.end():solution.start()], base)
        answer_intro, answer_parts = subtasks(text[solution.end():end], base)
        segments = []
        intro = clean(prompt_intro + "\n" + answer_intro)
        if intro:
            segments.append(Segment(base, intro))
        for letter in sorted(set(prompt_parts) | set(answer_parts)):
            ref = Ref(path.name, label(path), number, match.group(1), heading, letter)
            segments.append(
                Segment(ref, clean(prompt_parts.get(letter, "") + "\n" + answer_parts.get(letter, "")))
            )
        result.append(Exercise(base, match.group(3).strip(), segments))
    return result


def alias_pattern(alias: str) -> re.Pattern[str]:
    escaped = re.escape(alias)
    if re.fullmatch(r"[\w -]+", alias, re.UNICODE):
        return re.compile(rf"(?<!\w){escaped}(?!\w)", re.I)
    return re.compile(escaped, re.I)


def unique(refs: list[Ref]) -> list[Ref]:
    seen = set()
    result = []
    for ref in sorted(refs, key=lambda item: (item.exam, item.number, item.subtask or "")):
        key = (ref.file, ref.number, ref.subtask)
        if key not in seen:
            seen.add(key)
            result.append(ref)
    return result


def anchors(path: Path) -> set[str]:
    result: set[str] = set()
    seen: Counter[str] = Counter()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+)$", line)
        if not match:
            continue
        base = slug(match.group(1))
        count = seen[base]
        result.add(base if count == 0 else f"{base}-{count}")
        seen[base] += 1
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    input_dir = Path(config["input_dir"])
    output = Path(config["output"])
    excluded = set(config.get("exclude", ["index.md"]))
    files = [
        path for path in sorted(input_dir.glob(config.get("file_glob", "*.md")))
        if path.name not in excluded
    ]
    exercises = [exercise for path in files for exercise in parse(path)]

    topics: dict[str, list[Ref]] = defaultdict(list)
    overrides = config.get("topic_overrides", {})
    for exercise in exercises:
        override_key = f"{exercise.ref.file}#{exercise.ref.number}"
        topic = overrides.get(override_key)
        if topic is None:
            topic = config.get("fallback_topic", "Other Course Topics")
            for rule in config["topic_rules"]:
                if any(re.search(pattern, exercise.title, re.I) for pattern in rule["patterns"]):
                    topic = rule["topic"]
                    break
        topics[topic].append(exercise.ref)

    terms: dict[str, list[Ref]] = defaultdict(list)
    for canonical, aliases in config["terms"].items():
        patterns = [alias_pattern(alias) for alias in aliases]
        for exercise in exercises:
            for segment in exercise.segments:
                if any(pattern.search(segment.text) for pattern in patterns):
                    terms[canonical].append(segment.ref)

    lines = [
        f"# {config.get('title', 'Exam Index')}",
        "",
        "Topic references point to complete exercises. Word references point to the",
        "most specific task or subtask containing the term.",
        "",
        "## Topics",
        "",
    ]
    for topic in sorted(topics, key=str.casefold):
        lines.extend([
            f"### {topic}", "",
            "- " + ", ".join(ref.markdown for ref in unique(topics[topic])), "",
        ])
    lines.extend(["## Words", ""])
    grouped: dict[str, list[str]] = defaultdict(list)
    for term in terms:
        first = unicodedata.normalize("NFKD", term)[0].upper()
        grouped[first if first.isalnum() else "#"].append(term)
    for first in sorted(grouped):
        lines.extend([f"### {first}", ""])
        for term in sorted(grouped[first], key=str.casefold):
            refs = unique(terms[term])
            if refs:
                lines.append(f"- **{term}**: " + ", ".join(ref.markdown for ref in refs))
        lines.append("")
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    topic_refs = [ref for refs in topics.values() for ref in unique(refs)]
    expected = {(exercise.ref.file, exercise.ref.number) for exercise in exercises}
    actual = {(ref.file, ref.number) for ref in topic_refs}
    if actual != expected or len(topic_refs) != len(expected):
        raise SystemExit("Topic coverage is incomplete or duplicated")
    anchor_map = {path.name: anchors(path) for path in files}
    broken = [
        (ref.file, ref.anchor)
        for refs in list(topics.values()) + list(terms.values())
        for ref in unique(refs)
        if ref.anchor not in anchor_map.get(ref.file, set())
    ]
    if broken:
        raise SystemExit(f"Broken anchors: {broken[:10]}")
    print(
        f"Wrote {output}: {len(exercises)} exercises, "
        f"{sum(bool(unique(refs)) for refs in terms.values())} terms"
    )


if __name__ == "__main__":
    main()
