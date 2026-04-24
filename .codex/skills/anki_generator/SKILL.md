---
name: anki_generator
description: Generate high-quality Anki flashcards from presentation.pdf using a structured 3-phase process (knowledge extraction, flashcard generation, contextual examples).
---

# Anki Generator from Presentation

## Purpose

This skill generates high-quality Anki flashcards from a presentation (`presentation.pdf`) using a structured multi-phase approach. The output is written to `anki.txt`.

## Inputs

- `./presentation.pdf`

## Phase 1 — Knowledge Extraction (INTERNAL ONLY)

Carefully read the slides and extract all individual pieces of knowledge contained in them.

This includes:

- definitions
- terminology
- rules
- classifications
- comparisons
- structural explanations
- mechanisms
- relationships between concepts
- central ideas or principles behind concepts

### Rules

- Break the content into the smallest possible independent knowledge units.
- Examples contained in the slides should be treated as supporting information that clarifies concepts, not as primary facts to memorize.
- Do NOT output this phase. It is only used internally.

## Phase 2 - Flashcard Generation

Convert each extracted knowledge unit into an Anki flashcard.

### Goal

Create flashcards that enable efficient memorization of the key concepts from the slides.

### Guidelines

- Each card must contain exactly one atomic fact or concept.
- Cards must be concise and optimized for recall.
- Prefer creating many small cards instead of fewer large cards.
- If a slide contains multiple facts, create multiple cards.
- If information is complex or long, split it into several smaller cards.
- Each card must be understandable independently and must not rely on knowledge of the slides.
- Prefer questions on the front and short answers on the back.

### Preferred Question Types

Prefer Active Recall Questions
Prefer questions such as:

- What is ...?
- Which ...?
- Why ...?
- What does ... mean?
- What is the difference between ...?

### Preferred Knowledge Type (VERY IMPORTANT)

When creating cards, prioritize testing the underlying idea behind a concept.

Prefer cards about:

1. The main idea of a concept
2. Definitions of terms
3. Mechanisms (how something works)
4. Contrasts or differences between concepts
5. Structural relationships between concepts

Avoid:

- trivial descriptive details
- non-essential facts

### Strict Constraints

#### No Acronym Introduction

- Do not introduce acronyms that are not used in the slides.
- If an acronym is used, write the full term first and optionally place the acronym in parentheses afterward.

#### No Example-Based Questions

- Do NOT create questions that ask for specific examples.

#### No Slide References

- Questions must not refer to slides or slide content directly.
- Avoid phrasing such as:
  - "... according to the slide?"
  - "... mentioned on the slide?"
  - "... highlighted on the slide?"
  - "... named on the slide?"
  - "... shown on the slide?"
- Questions must be answerable without knowing the lecture slides.

### Card Quality Checklist (MANDATORY)

Each card must satisfy:

1. Atomicity
   The card tests exactly one piece of knowledge.
2. Clarity
   The question must be unambiguous and understandable without additional context.
3. Minimal Answer
   The back should contain the shortest possible correct answer.
4. Active Recall
   Prefer recall-based questions rather than recognition.
5. No Redundancy
   Avoid repeating the same fact unless testing a different aspect.
6. Independent Cards
   Each card must make sense without relying on other cards.
7. Avoid Long Text
   If an answer would be long, split it into multiple cards.

### Slide Number Requirement

- Every card must include the slide number it was derived from.
- The slide number must be the number shown on the slide itself, typically located at the bottom-left corner of the slide.
- Do NOT use the PDF page number.
- If the slide numbering starts later due to title or intro slides, use the numbering printed on the slide.
- If a card is based on information spanning multiple slides, specify a range (example: page 12-13).

### Output Format (STRICT)

- Output only the cards. Do not include explanations or additional text.
- The output must be plain raw text suitable for a .txt file.
- Do not use markdown formatting.
- Use only normal characters commonly used in programming such as ', ", -, :, (, ), etc.

Required Output Structure:

```
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
```

Continue numbering sequentially.

### Output 

Write the cards into a file named "anki.txt".

## Phase 3 - Add Contextual Examples

Read the previously generated cards from "anki.txt" and enrich cards with examples.

### Process

For each card:

- Identify examples from the slides that illustrate the concept tested by the card.
- Choose at most two examples that provide the most helpful context for understanding the concept.

### Rules

- Do NOT modify the question.
- Do NOT modify the main answer text.
- Append the examples after the answer on a new line.
- The line must start with "Example: ".
- Include at most two examples.
- If no suitable examples exist, leave the card unchanged.

### Format

```
Front: 
<Question>
Back: 
<Answer>

Example: <Example 1>, <Example 2>
```

### Output

Rewrite the file "anki.txt" so that each card includes the contextual examples appended to the answer when applicable.
