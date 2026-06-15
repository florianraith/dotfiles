---
name: index-exam-markdown
description: Build a detailed Markdown index over parsed exam and solution files, with broad topic categories linked to whole exercises and normalized technical terms linked to exact tasks or subtasks. Use for creating or refreshing searchable exam indexes, agent retrieval pages, course knowledge maps, terminology concordances, or search-engine-friendly navigation for any class.
---

# Index Exam Markdown

Index the parsed Markdown corpus, not the original PDFs. If Markdown is missing or unreliable, use `parse-exam-pdfs` first.

## Workflow

1. Inventory all parsed exam files and confirm their heading structure.
2. Count files, exercises, and subtasks before indexing.
3. Create a JSON configuration from [config-format.md](references/config-format.md).
4. Categorize every complete exercise into one broad topic:
   - Use task titles as the strongest signal.
   - Read the full task and solution when the title is generic.
   - Assign mixed knowledge exercises to a cross-topic fundamentals category.
   - Ensure every exercise appears exactly once in Topics.
5. Build the Words index from both task and solution text:
   - Include domain-specific words, named methods, laws, models, patterns, principles, quality attributes, abbreviations, notation, process roles/artifacts, and bilingual aliases.
   - Normalize aliases into one canonical term.
   - Link to the most specific subtask containing the term; use task-level links only for task introductions.
   - Exclude people, application-domain nouns, variable names, ordinary words, OCR fragments, and accidental capitalized tokens unless course-relevant.
6. Run `scripts/build_exam_index.py`.
7. Make at least three vocabulary passes:
   - Pass 1: headline concepts and recurring terminology.
   - Pass 2: secondary vocabulary in solutions, diagrams, tables, and parenthetical translations.
   - Pass 3: long-tail named laws/authors, subtypes, process artifacts, notation, quality attributes, security principles, and abbreviations.
8. Validate:
   - Every exercise appears once in Topics.
   - Canonical terms are unique.
   - References are deduplicated.
   - Every relative file and anchor exists.
   - No OCR-generated abbreviations or generic words pollute the index.

## Command

```bash
python scripts/build_exam_index.py config.json
```

The script writes the configured index and fails on missing exercise coverage or broken anchors.

## Index Shape

```markdown
# Course Exam Index

## Topics

### Requirements Engineering

- [WS 23/24, Aufgabe 2](course-ws2324.md#aufgabe-2-...)

## Words

### P

- **Palladio Component Model (PCM)**: [SS 25, Task 1 b)](course-ss25.md#1-b)
```

Use [candidate-mining.md](references/candidate-mining.md) during the second and third passes.
