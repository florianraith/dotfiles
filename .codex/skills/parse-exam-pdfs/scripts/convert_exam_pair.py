#!/usr/bin/env python3
"""Create a structured Markdown draft from one exam/solution PDF pair."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


DEFAULT_VISUAL_WORDS = (
    "figure", "diagram", "table", "schema", "code", "illustrated", "image",
    "Abbildung", "Diagramm", "Tabelle", "Schema", "Quelltext", "Grafik",
)


@dataclass(frozen=True)
class Pair:
    slug: str
    exam: Path
    solution: Path
    language: str
    title: str | None
    visual_keywords: tuple[str, ...]
    ocr_languages: str
    force_ocr: bool


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)


def extracted_text(pdf: Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8", errors="replace")


def usable(text: str) -> bool:
    letters = sum(character.isalpha() for character in text)
    return letters >= 200


def prepare_text(pdf: Path, temp: Path, languages: str, force: bool) -> str:
    text = extracted_text(pdf)
    if usable(text) and not force:
        return text
    if not shutil.which("ocrmypdf"):
        raise RuntimeError(f"{pdf} needs OCR, but ocrmypdf is unavailable")
    ocr_pdf = temp / f"{pdf.stem}-ocr.pdf"
    command = [
        "ocrmypdf", "--force-ocr" if force else "--skip-text",
        "--deskew", "--rotate-pages", "--language", languages,
        "--output-type", "pdf", str(pdf), str(ocr_pdf),
    ]
    run(command)
    return extracted_text(ocr_pdf)


def clean_page(page: str) -> str:
    page = (
        page.replace("\u00ad", "")
        .replace("\ufb00", "ff")
        .replace("\ufb01", "fi")
        .replace("\ufb02", "fl")
        .replace("\ufffd", "")
    )
    lines: list[str] = []
    for line in page.splitlines():
        stripped = line.strip()
        if stripped in {
            "LÖ", "SU", "NG", "LÖSUNG", "SOLUTION",
            "Solu", "tion", "So", "lutio", "lu", "tio",
        }:
            continue
        if re.match(r"^(Name|Matrikelnummer|Student ID|Candidate Number)\s*:", stripped, re.I):
            continue
        if re.match(
            r"^(Erst|Zweit|Nach|Haupt)?klausur\b.*"
            r"(Wintersemester|Sommersemester|Winter Term|Summer Term)\b",
            stripped,
            re.I,
        ):
            continue
        if re.search(r"\b(Page|Seite)\s+\d+(\s+(of|von)\s+\d+)?\s*$", stripped, re.I):
            line = re.sub(
                r"\s*\b(Page|Seite)\s+\d+(\s+(of|von)\s+\d+)?\s*$",
                "",
                line,
                flags=re.I,
            ).rstrip()
            if not line.strip():
                continue
        lines.append(line.rstrip())
    text = "\n".join(lines)
    text = re.sub(r"(?<=\w)-\n[ \t]+(?=\w)", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def pages(text: str) -> list[str]:
    return [clean_page(page) for page in text.split("\f")]


def task_pattern(words: list[str]) -> re.Pattern[str]:
    alternatives = "|".join(re.escape(word) for word in words)
    return re.compile(rf"(?m)^({alternatives})\s+(\d+)\s*:\s*(.+)$")


def split_tasks(text: str, pattern: re.Pattern[str]) -> dict[int, tuple[str, str]]:
    matches = []
    seen: set[int] = set()
    for match in pattern.finditer(text):
        number = int(match.group(2))
        if number in seen:
            break
        seen.add(number)
        matches.append(match)
    result: dict[int, tuple[str, str]] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[int(match.group(2))] = (
            f"{match.group(1)} {match.group(2)}: {match.group(3).strip()}",
            text[match.end():end].strip(),
        )
    return result


def markdown_body(body: str, number: int) -> str:
    body = re.sub(
        r"(?m)^[ \t]*([a-z])\)\s+",
        lambda match: f"\n### {number} {match.group(1)})\n\n",
        body,
    )
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def task_pages(source_pages: list[str], pattern: re.Pattern[str]) -> dict[int, list[int]]:
    starts: list[tuple[int, int]] = []
    seen: set[int] = set()
    for page_number, page in enumerate(source_pages, 1):
        for match in pattern.finditer(page):
            number = int(match.group(2))
            if number in seen:
                return ranges(starts, len(source_pages))
            seen.add(number)
            starts.append((number, page_number))
    return ranges(starts, len(source_pages))


def ranges(starts: list[tuple[int, int]], count: int) -> dict[int, list[int]]:
    result: dict[int, list[int]] = {}
    for index, (number, start) in enumerate(starts):
        end = starts[index + 1][1] if index + 1 < len(starts) else count + 1
        result[number] = list(range(start, max(start + 1, end)))
    return result


def render_assets(
    pair: Pair,
    pdf: Path,
    source_pages: list[str],
    ranges_by_task: dict[int, list[int]],
    kind: str,
    assets: Path,
) -> dict[int, list[str]]:
    pattern = re.compile(
        "|".join(re.escape(word) for word in pair.visual_keywords),
        re.I,
    )
    links: dict[int, list[str]] = {}
    for number, page_numbers in ranges_by_task.items():
        for page_number in page_numbers:
            if not pattern.search(source_pages[page_number - 1]):
                continue
            name = f"{pair.slug}-{kind}-p{page_number:02d}.png"
            destination = assets / name
            run([
                "pdftoppm", "-f", str(page_number), "-l", str(page_number),
                "-r", "150", "-singlefile", "-png", str(pdf),
                str(destination.with_suffix("")),
            ])
            links.setdefault(number, []).append(f"assets/{name}")
    return links


def make_pair(raw: dict, root: Path) -> Pair:
    return Pair(
        slug=raw["slug"],
        exam=root / raw["exam"],
        solution=root / raw["solution"],
        language=raw.get("language", "en"),
        title=raw.get("title"),
        visual_keywords=tuple(DEFAULT_VISUAL_WORDS) + tuple(raw.get("visual_keywords", [])),
        ocr_languages=raw.get("ocr_languages", "eng"),
        force_ocr=raw.get("force_ocr", False),
    )


def convert(config: dict, raw_pair: dict) -> Path:
    root = Path(config.get("root", ".")).resolve()
    output = root / config.get("output_dir", "Exam/Parsed")
    temp = root / config.get("temp_dir", "tmp/exam-pdfs")
    assets = output / "assets"
    output.mkdir(parents=True, exist_ok=True)
    temp.mkdir(parents=True, exist_ok=True)
    assets.mkdir(parents=True, exist_ok=True)
    pair = make_pair(raw_pair, root)
    pattern = task_pattern(config.get("task_words", ["Aufgabe", "Task", "Exercise"]))

    exam_pages = pages(prepare_text(pair.exam, temp, pair.ocr_languages, pair.force_ocr))
    solution_pages = pages(prepare_text(pair.solution, temp, pair.ocr_languages, pair.force_ocr))
    exam_tasks = split_tasks("\n\n".join(exam_pages), pattern)
    solution_tasks = split_tasks("\n\n".join(solution_pages), pattern)
    exam_assets = render_assets(
        pair, pair.exam, exam_pages, task_pages(exam_pages, pattern), "exam", assets
    )
    solution_assets = render_assets(
        pair, pair.solution, solution_pages,
        task_pages(solution_pages, pattern), "solution", assets
    )

    title = pair.title or config.get("course_title", pair.slug)
    headings = config.get("solution_headings", {})
    solution_template = headings.get(
        pair.language,
        "Lösung zur Aufgabe {number}" if pair.language == "de" else "Solution for Task {number}",
    )
    lines = [
        f"# {title} - {pair.slug}",
        "",
        f"- Exam: `{raw_pair['exam']}`",
        f"- Solution: `{raw_pair['solution']}`",
        "",
    ]
    for number in sorted(exam_tasks):
        heading, body = exam_tasks[number]
        lines.extend([f"## {heading}", "", markdown_body(body, number), ""])
        for link in exam_assets.get(number, []):
            lines.extend([f"![{heading}]({link})", ""])
        solution_body = solution_tasks.get(number, ("", "[Solution not detected]"))[1]
        lines.extend([
            f"## {solution_template.format(number=number)}",
            "",
            markdown_body(solution_body, number),
            "",
        ])
        for link in solution_assets.get(number, []):
            lines.extend([f"![Solution {number}]({link})", ""])

    destination = output / f"{pair.slug}.md"
    destination.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--slug")
    selection.add_argument("--all", action="store_true")
    args = parser.parse_args()
    config = json.loads(args.manifest.read_text(encoding="utf-8"))
    pairs = config["pairs"]
    if args.slug:
        pairs = [pair for pair in pairs if pair["slug"] == args.slug]
        if not pairs:
            raise SystemExit(f"Unknown slug: {args.slug}")
    for raw_pair in pairs:
        print(convert(config, raw_pair))


if __name__ == "__main__":
    main()
