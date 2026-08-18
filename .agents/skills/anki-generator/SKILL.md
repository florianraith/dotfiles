---
name: anki-generator
description: Generate concise, independently gradable Anki flashcards from presentation.pdf, including conceptual, contrastive, and slide-supported application cards, then audit cue quality, interference, and formatting.
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

- Extract independent knowledge units, then group only facts retrieved through one coherent operation.
- Examples contained in the slides should be treated as supporting information that clarifies concepts, not as primary facts to memorize.
- Do NOT output this phase. It is only used internally.

## Phase 2 - Flashcard Generation

Convert each extracted knowledge unit into an Anki flashcard.

### Goal

Create flashcards that enable efficient memorization of the key concepts from the slides.

### Guidelines

- Test one retrieval operation per card. A formula, a contrast pair, or a short ordered sequence may contain several facts when they form one retrievable chunk.
- Make every card concise and independently gradable.
- Split unrelated facts and answers that require a pause between independently recalled parts.
- Treat more than three unordered items or roughly 25 substantive answer words as repair triggers, not automatic failures.
- Each card must be understandable independently and must not rely on knowledge of the slides.
- Put a question on the front and a short, verbalizable answer on the back.

### Preferred Question Types

Prefer diagnostic active-recall questions such as:

- What is ...?
- Which ...?
- Why ...?
- What does ... mean?
- What is the difference between ...?
- Why does ... cause ...?
- What breaks if ...?
- Given ..., which method applies and why?
- Given ..., what value results?

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

#### Abbreviation Handling

- Use only abbreviations that appear in the slides.
- Classify each abbreviation by how the slides use it:
  1. **Topic-introduced abbreviation:** If the slides introduce the abbreviation as a concept, model, or method and provide its meaning, create an introduction card at the first relevant position:
     - Front: `What is <ABBREVIATION>?`
     - Back: `<Full term> (<ABBREVIATION>): <concise explanation of the concept>.`
     After this card, use the abbreviation alone without repeatedly expanding it.
  2. **Assumed-known abbreviation:** If the slides use an abbreviation without introducing its topic or expansion, treat it as prior knowledge and reuse it without expansion. Do not create an expansion-only card. Examples can include RGB, API, and LLM when the slides merely reuse them.
- Do not infer or invent an expansion that the slides do not provide.
- Place every abbreviation-introduction card before later cards that use that abbreviation.

#### Examples and Application

- Do not ask learners to reproduce incidental examples from the slides.
- Create a constrained application card when a central slide-supported concept is naturally applied:
  - formula: compute or interpret a result;
  - principle: identify a violation or consequence;
  - method or pattern: choose it for a situation;
  - trade-off: predict what improves or breaks under stated conditions.
- Use scenarios only to test slide-supported knowledge. Do not introduce external facts.
- Make scenario cues specific enough to have one defensible answer.

#### No Slide References

- Questions must not refer to slides or slide content directly.
- Avoid phrasing such as:
  - "... according to the slide?"
  - "... mentioned on the slide?"
  - "... highlighted on the slide?"
  - "... named on the slide?"
  - "... shown on the slide?"
- Questions must be answerable without knowing the lecture slides.

#### Source-Artifact Independent Questions

- Questions must not depend on presentation artifacts or the learning context.
- Do NOT phrase questions with terms such as:
  - "in this lecture"
  - "in the presentation"
  - "on the slide"
  - "in the diagram"
  - "shown in the diagram"
  - "shown in the lecture"
  - "according to the lecture"
  - "according to the diagram"
- If a generated question contains source-artifact wording, rewrite it so it asks about the concept directly.
- It is acceptable to use slide numbers only in the card header, never in the question text.

### Card Quality Checklist (MANDATORY)

Each card must satisfy:

1. One retrieval operation
   Require one clear grading decision. Split compound prompts and unrelated answer parts.
2. Unique cue
   Ask whether a knowledgeable learner could give another correct answer. If so, add the framework, answer type, count, or other diagnostic scope.
3. Typed answer
   Signal whether the answer is a name, count, formula, mechanism, consequence, comparison, or trade-off. A formula question must include the formula in text; a why-question must state the cause.
4. Diagnostic verb
   Use a verb that constrains the answer. Replace load-bearing uses of vague verbs such as identify, formalize, synthesize, define, play a role, is used for, and is important with the precise relationship being tested.
5. Minimal, verbalizable answer
   Put the shortest complete answer in text. Images may illustrate an answer but must not carry it alone.
6. Bounded sets and sequences
   For more than three unordered items, use semantic groups of at most three, invert into discriminating member cards, or keep only a count-and-group scaffold. For a long pipeline, teach local links first; keep a full-chain card only when reproducing the chain is itself useful.
7. Independence and active recall
   Make the card understandable without other cards or the slides, and require recall rather than recognition.
8. Nonredundancy and interference
   Avoid duplicate facts, identical backs, and parallel cues that differ only in a small label. Prefer explicit contrasts or wording whose differing terms determine the answer.
9. Source-Artifact Independence
   The question must not mention standalone source-artifact words such as lecture, presentation, slide, deck, figure, or diagram, or phrases such as shown, mentioned, named, or highlighted there when they refer to the source material or learning context. Whole-word matching is required; terms like representation are allowed. Before rewriting a flagged question, classify whether the flagged word is actually valid domain/content terminology. Keep it when it names a domain concept from the source content rather than the source artifact itself, such as "presentation layer" in enterprise application architecture.

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
- Prefer one example of at most roughly 20 words. Include a second only when it adds a useful contrast.
- Do not append an example to a scenario card unless it adds distinct explanatory value.
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

## Final Validation

Run the bundled script by its resolved skill path: `python3 <anki-generator-skill-directory>/scripts/audit_cards.py anki.txt`. Treat structural findings as failures and inspect every heuristic warning. Repair each true positive and record why any false positive is safe to retain internally.

Then perform the semantic checks below, which the script cannot decide reliably.

Before finishing, scan all question text for source-artifact wording using whole-word matching, such as "lecture", "presentation", "slide", "deck", "figure", "diagram", "shown", "mentioned", "named", or "highlighted".

For each match, first classify the usage:

- Rewrite it if it refers to the source artifact, learning context, or visual placement, such as "in the presentation", "on the slide", "shown in the diagram", "mentioned in the lecture", or "highlighted there".
- Keep it if it is valid domain/content terminology from the source material and the question is still independent of the source artifact. For example, keep "presentation layer" when the topic is enterprise application architecture, because it names a domain layer rather than the lecture presentation.
- Do not flag substrings inside valid technical terms; for example, "representation" is allowed.

Rewrite only the questions whose matched wording refers to the source artifact while preserving the slide number in the card header.

Validate abbreviation handling:

- every abbreviation occurs in the slides;
- every topic-introduced abbreviation has an earlier `What is ...?` card with its expansion and explanation;
- later cards use the shorthand without repeatedly expanding it;
- assumed-known abbreviations are not expanded or given synthetic introduction cards;
- no expansion was inferred beyond the slides.

Validate cue and answer quality:

- every card has one verbalizable pass criterion;
- every answer matches the type requested by its question;
- every unordered set larger than three has been grouped, inverted, or justified as one chunk;
- no card asks for unconstrained recall of an entire architecture or process;
- identical backs and highly similar fronts have been merged, contrasted, differentiated, or deliberately justified;
- applicable central concepts include a slide-supported computation, choice, diagnosis, or explanation card where doing so improves transfer;
- incidental implementation details remain only when conceptually important.
