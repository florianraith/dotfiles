---
name: anki_generator
description: Generate high-quality Anki flashcards from presentation.pdf using a structured 3-phase process (knowledge extraction, flashcard generation, contextual examples).
---

# Anki Generator from Presentation

## Purpose

This skill generates high-quality Anki flashcards from a presentation (`presentation.pdf`) using a structured multi-phase approach. The output is written to `anki.txt`.

---

## Inputs

- `./presentation.pdf`

---

## Phase 1 — Knowledge Extraction (INTERNAL ONLY)

Read the presentation carefully and extract all individual knowledge units.

This includes:

- definitions
- terminology
- rules
- classifications
- comparisons
- structural explanations
- mechanisms
- relationships between concepts
- central ideas or principles

### Rules

- Break content into the smallest independent units possible.
- Treat examples as supporting context, not primary knowledge.
- Do NOT output anything from this phase.

---

## Phase 2 — Flashcard Generation

Convert each knowledge unit into an Anki flashcard.

### Goal

Efficient memorization of core concepts.

---

### Core Rules

- Each card = exactly **one atomic fact**
- Prefer **many small cards** over large ones
- Split complex ideas into multiple cards
- Cards must be **independent and self-contained**

---

### Preferred Question Types

Use active recall:

- What is ...?
- Which ...?
- Why ...?
- What does ... mean?
- What is the difference between ...?

---

### Prioritization (VERY IMPORTANT)

Focus on:

1. Core idea of a concept  
2. Definitions  
3. Mechanisms (how something works)  
4. Differences / contrasts  
5. Relationships between concepts  

Avoid:

- trivial descriptive details
- non-essential facts

---

### Strict Constraints

#### No Acronym Introduction
- Do not introduce new acronyms
- If used, write full term first

#### No Example-Based Questions
- Do NOT ask for examples

#### No Slide References
- No phrasing like:
  - "according to the slide"
  - "shown on the slide"

---

### Quality Checklist (MANDATORY)

Each card must satisfy:

1. Atomic (single fact)
2. Clear and unambiguous
3. Minimal answer length
4. Active recall focused
5. No redundancy
6. Independent
7. No long answers (split if needed)

---

### Slide Number Requirement

- Use slide number printed on slide (NOT PDF page)
- If spanning slides → use range (e.g. page 12-13)

---

### Output Format (STRICT)

- Plain text only
- No markdown
- No explanations
- No additional text

Format exactly:

1. Card (page x)
Front:
<Question>
Back:
<Answer>


2. Card (page y-z)
Front:
<Question>
Back:
<Answer>

---

### Output Target

Write output to:

`./anki.txt`

---

## Phase 3 — Add Contextual Examples

Read `anki.txt` and enrich cards with examples.

---

### Process

For each card:

- Identify relevant examples from slides
- Select up to 2 useful examples

---

### Rules

- DO NOT modify question
- DO NOT modify main answer
- Append examples to answer

---

### Format

Add directly after answer:

```
Example: <Example 1>, <Example 2>
```

- Max 2 examples
- If none → leave unchanged

---

### Final Output

Rewrite:

`./anki.txt`

with appended examples.

---

## Constraints Across All Phases

- No hallucinated content
- No adding new knowledge not present in slides
- No restructuring outside defined format
- Strict adherence to output format
