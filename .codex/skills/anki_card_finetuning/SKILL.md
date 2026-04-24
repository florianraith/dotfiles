---
name: anki_card_finetuning
description: Refine an overgenerated anki.txt file by reducing it to around 60–70 high-value Anki cards, using presentation.pdf as source context and older exams in ./Exam to prioritize exam-relevant cards.
---

# Anki Card Finetuning

## Purpose

Use this skill to reduce an over-generated set of Anki flashcards into a compact, high-value exam-preparation deck.

The input deck was generated from a presentation and may contain hundreds of cards per slide. Your job is to select, merge, rewrite, and prioritize the most useful cards, aiming for approximately 60–70 final cards total unless the user specifies a different target.

The skill must preserve coverage of the presentation while strongly prioritizing concepts that appear in older exams.

## Inputs

The working directory contains:

- `./anki.txt` — the generated Anki cards. This is the only allowed source for final card content.
- `./presentation.pdf` — the presentation that the cards were generated from. Use it to understand context and verify whether cards are grounded in the presentation.
- `./Exam/` — a directory containing older exams and solutions from previous years for the same class.

The exams may contain topics that are not covered by the presentation or the generated Anki cards. Do **not** generate new cards from the exams unless the relevant content is already present in `./anki.txt`.

## Core Rule

Only keep, rewrite, merge, or delete cards that already exist in `./anki.txt`.

Do **not** introduce new factual content from `./Exam/` that is not represented in the generated cards.

The exams are used only to estimate importance, not to expand the deck.

## Goal

Produce a refined `anki.txt` containing roughly 60–70 high-value cards.

The final cards should be:

- Exam-relevant.
- Conceptually important.
- Atomic.
- Non-redundant.
- Clear without referencing slide numbers.
- Focused on definitions, mechanisms, contrasts, formulas, assumptions, and typical exam-style questions.

## High-Level Workflow

1. Read `./anki.txt` and parse all generated cards.
2. Read `./presentation.pdf` to understand the intended topic scope.
3. Read all files in `./Exam/`, including solutions if available.
4. Identify which concepts from the generated cards appear in past exams.
5. Score each card based on importance, exam recurrence, conceptual centrality, and redundancy.
6. Remove low-value, duplicate, overly specific, trivial, or common-sense cards.
7. Merge overlapping cards where appropriate.
8. Rewrite selected cards for clarity and atomicity.
9. Output the refined card list back to `./anki.txt`, unless instructed otherwise.

## Card Selection Criteria

Prioritize cards that ask about:

- Definitions of central terms.
- Core concepts repeatedly used throughout the presentation.
- Differences or comparisons between related concepts.
- Algorithms, models, architectures, or workflows.
- Formulas, metrics, evaluation methods, or assumptions.
- Limitations, advantages, disadvantages, or trade-offs.
- Concepts that appear in previous exams or solutions.
- Concepts required to answer likely exam questions.

Keep cards that are strongly connected to previous exams even if they seem slightly less central in the slides.

## Exam-Based Importance

When reading `./Exam/`, look for semantic overlap with existing cards, not only exact wording.

Examples of valid overlap:

- A card asks for the definition of “precision,” and an exam asks students to compute or explain precision.
- A card asks about the difference between stemming and lemmatization, and an exam solution mentions that distinction.
- A card asks about an algorithm’s main idea, and an exam asks students to apply that algorithm.

Exam occurrence should increase a card’s priority when:

- The concept appears in exam questions.
- The concept appears in official solutions.
- The concept appears across multiple years.
- The concept is needed to solve a calculation, explanation, or comparison task.

Do not create a new card just because an exam covers a related topic. Only use exam content to rank cards already present in `./anki.txt`.

## Low-Value Card Criteria

Remove cards that are primarily:

- Common sense.
- Too obvious from general background knowledge.
- Purely administrative.
- About slide structure rather than content.
- Too specific to an example unless the example is exam-relevant.
- Repetitive duplicates of better cards.
- Overly broad and vague.
- Too detailed for exam preparation.
- Asking for isolated facts that do not support understanding.
- Asking about wording, phrasing, or incidental slide details.

Examples of weak cards:

- “What does the slide introduce?”
- “Why is this topic important?” when the answer is generic.
- “What is shown in the figure?” without a deeper concept.
- “What is an example of X?” when X itself is already covered and the example is not exam-relevant.
- “What does this bullet point say?”

## Redundancy Handling

If multiple cards cover the same idea, keep the strongest one.

Prefer:

- A definition card over several shallow example cards.
- A contrast card over two separate isolated fact cards.
- A mechanism card over a memorization-only wording card.
- An exam-aligned card over a non-exam-aligned duplicate.

Merge cards only when the result remains atomic enough for Anki.

Do not merge unrelated concepts into one large card.

## Scoring Heuristic

Use the following internal scoring model when deciding what to keep.

### Exam relevance

- 3 points: concept appears in multiple past exams or is central to an exam task.
- 2 points: concept appears in one past exam or solution.
- 1 point: concept is indirectly useful for solving exam tasks.
- 0 points: no detected exam relevance.

### Conceptual importance

- 3 points: core definition, formula, algorithm, model, or principle.
- 2 points: important supporting concept.
- 1 point: minor but useful detail.
- 0 points: incidental detail.

### Card quality

- 2 points: clear, atomic, and directly testable.
- 1 point: useful but needs rewriting.
- 0 points: vague, redundant, or poorly scoped.

### Penalties

Subtract points for:

- Redundancy with another stronger card.
- Common-sense content.
- Excessive specificity.
- Slide-only wording.
- Content not grounded in `./anki.txt`.

Prefer cards with the highest total score until the target deck size is reached.

## Target Deck Size

Aim for 60–70 cards total.

If the generated deck covers very little material, fewer cards are acceptable.

If the presentation is unusually broad and many cards are clearly exam-relevant, slightly exceed 70 only when necessary. Do not exceed 80 unless explicitly instructed.

If there are far more than 70 apparently useful cards, keep the most exam-relevant and foundational ones.

## Rewriting Rules

Rewrite cards to improve clarity, but do not add unsupported information.

Each final card should:

- Ask exactly one main thing.
- Be understandable without seeing the slide.
- Avoid phrases like “according to the slide,” “in this presentation,” or “as shown above.”
- Use precise terminology.
- Prefer concise answers.
- Include short examples only when they materially improve understanding or exam preparation.

Good formats:

```text
Front: 
What is [concept]?
Back: 
[Concise definition].
```

```text
Front: 
How does [method] differ from [related method]?
Back: 
[Key distinction].
```

```text
Front: 
Why is [assumption] important for [method]?
Back: 
[Reason].
```

```text
Front: 
What are the main steps of [algorithm/process]?
Back: 
[Short ordered list].
```

## Output Format

Overwrite or create the final `./anki.txt` using this exact style unless the existing file uses a clearly different user-required format:

```text
1. Card
Front: 
...
Back: 
...

2. Card
Front: 
...
Back: 
...
```

Do not use Markdown bullets inside the final file unless they are needed inside an answer.

Do not include analysis, scoring notes, or explanations in `./anki.txt`.

## Required Final Summary

After writing the refined file, report briefly:

- How many cards were in the original deck.
- How many cards remain.
- Whether past exams were used successfully.
- Any limitations, such as unreadable scans or missing solutions.

Do not include the full card list in the chat unless the user asks for it.

## Handling PDFs and Scans

When reading `./presentation.pdf` and files in `./Exam/`:

- Extract text directly when possible.
- If a PDF page appears to be scanned or image-only, use OCR only when necessary.
- If OCR is unreliable, state this in the final summary.
- Prefer official solutions over guessed interpretations.

## Important Constraints

- Do not generate new content from exams.
- Do not create cards for exam topics absent from `./anki.txt`.
- Do not keep cards solely because they match an exam if the card is factually unsupported by the generated deck.
- Do not preserve all slide details.
- Do not optimize for maximum coverage at the expense of usefulness.
- Do not exceed the target size unless clearly justified.

## Quality Checklist

Before finishing, verify:

- The final deck has roughly 60–70 cards.
- No card depends on seeing a slide.
- No card asks trivial/common-sense questions.
- Duplicate cards were removed or merged.
- Exam-relevant concepts were prioritized.
- No new content was introduced from the exams.
- Final output is written to `./anki.txt`.
