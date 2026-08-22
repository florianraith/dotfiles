---
name: anki-custom-examples
description: "Add concise self-authored examples to existing Anki text decks, labeling additions exactly `Example*:` while preserving source-derived `Example:` lines. Use when Codex is asked to enrich existing anki.txt cards with custom examples; do not use for generating a new deck."
---

# Anki Custom Examples

Add selective examples that clarify existing answers without changing the knowledge being tested. The asterisk marks examples authored by Codex rather than taken from the slides or source material.

## Workflow

1. Read the complete target file. Default to `./anki.txt` when no path is given.
2. Record the card count, numbering, structure, and counts of existing `Example:` and `Example*:` lines.
3. Select only cards whose answers become easier to understand through a concrete scenario, contrast, or small numerical illustration.
4. Add one concise example after the answer, following the deck's established spacing and formatting.
5. Rewrite the target file in place unless the user requests another output path.

## Example Rules

- Prefix every self-authored example exactly with `Example*: `.
- Keep slide- or source-derived examples labeled `Example:`. Preserve their wording and label.
- Make each example directly demonstrate the answer's concept and independently understandable.
- Prefer a minimal concrete case. Use numbers only when they illuminate a metric, calculation, or comparison.
- Skip cards that are already concrete, have a sufficient example, or would gain only redundant detail.
- Add at most one custom example per card unless the user explicitly requests more.
- Preserve the deck's existing mathematical notation and valid Anki MathJax tags.

Use this form:

```text
Back:
Precision is the proportion of selected items that are relevant.

Example*: If 8 of 10 selected documents are relevant, precision is 0.8.
```

Do not introduce variants such as `Example: (*)`, `Example (*)`, or `*Example:`.

## Preservation

Preserve card headers, page references, numbering, fronts, answers, existing examples, and formatting. Do not add, remove, merge, or reorder cards. A custom example may clarify an answer but must not introduce an unsupported claim or imply that it came from the source material.

## Validation

Before finishing:

1. Confirm the original card count, numbering, headers, fronts, answers, source examples, and page references remain intact.
2. Confirm every added example starts with exactly `Example*:` and no malformed marker was introduced.
3. Confirm the number of new `Example*:` lines equals the number of examples added.
4. Review every new example for correctness, relevance, brevity, and duplication.
5. Report the number of custom examples added and any cards intentionally skipped because an example would not improve understanding.
