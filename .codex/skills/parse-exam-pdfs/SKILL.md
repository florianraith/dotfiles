---
name: parse-exam-pdfs
description: Convert collections of exam PDFs and matching solution PDFs into faithful, structured Markdown files with task/subtask headings, solutions placed directly after each task, and linked extracted or rendered visual assets. Use for digitizing old exams, sample solutions, scanned/OCR exams, bilingual exams, or building a searchable exam corpus for any class. Always use the pdf skill alongside this skill.
---

# Parse Exam PDFs

Use the `pdf` skill for every PDF operation. Preserve the source wording and language.

## Workflow

1. Inspect repository instructions and locate exam and solution PDFs.
2. Inventory every PDF with `pdfinfo` and first-page text. Map each exam to its solution by term, date, title, task count, and points.
3. Choose collision-free output slugs. Prefer the repository's requested naming convention; otherwise use `<course>-wsYYZZ` and `<course>-ssYY`.
4. Create a JSON manifest from [manifest-format.md](references/manifest-format.md).
5. Process exactly one exam/solution pair at a time:
   - Extract existing text layers with `pdftotext -layout`.
   - If extraction is empty or unusable, create an OCR working copy with `ocrmypdf`; never modify source PDFs.
   - Render pages with `pdftoppm` when diagrams, tables, code, handwriting, redactions, or layout affect meaning.
   - Run `scripts/convert_exam_pair.py` to create the Markdown draft and visual assets.
   - Compare the draft with both rendered PDFs page by page.
   - Correct OCR, ligatures, hyphenation, headers, watermarks, tables, symbols, and task boundaries.
   - Preserve source grammar unless an obvious OCR/parsing defect caused it.
   - Finish and verify this pair before starting the next pair.
6. Use this hierarchy:
   - `## Aufgabe 4: ...` or `## Task 4: ...`
   - `### 4 a)`, `### 4 b)`, and so on
   - `## Lösung zur Aufgabe 4` or `## Solution for Task 4`
7. Place each solution directly after its corresponding task.
8. Store visual assets under `<output>/assets/` and link them relatively.
9. Validate all pairs:
   - Task and solution counts match.
   - Every expected subtask is present.
   - Every asset link resolves.
   - No replacement characters, page furniture, OCR watermark fragments, or duplicate translated exam sections remain.

## Commands

Use the repository's required Python environment. Otherwise use the active Python environment.

```bash
python scripts/convert_exam_pair.py manifest.json --slug course-ws2324
```

Run once per pair to preserve the iterative workflow. Use `--all` only after the manifest and conversion quality have already been verified.

```bash
python scripts/convert_exam_pair.py manifest.json --all
```

## Quality Rules

- Treat OCR as a draft, never as ground truth.
- Prefer the exam PDF for task wording and the solution PDF for answers.
- Link a rendered page whenever text cannot faithfully represent a diagram, schema, code layout, handwritten annotation, or graphical answer.
- Do not silently omit blacked-out, illegible, or unavailable content. Preserve the usable source and link the page.
- For bilingual PDFs, keep the language requested by the user and stop at the repeated task sequence in the other language.
- Keep source PDFs untouched and intermediates outside final output.

Read [verification-checklist.md](references/verification-checklist.md) before final delivery.
