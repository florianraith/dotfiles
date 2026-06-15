---
name: anki-card-finetuning
description: Refine an overgenerated anki.txt file into roughly 60-70 high-value Anki cards, using presentation.pdf as source context and Exam/Parsed/index.md plus its linked exam Markdown files to prioritize exam-relevant concepts.
---

# Anki Card Finetuning

## Purpose

Use this skill when `anki.txt` contains too many generated cards and needs to be reduced to a compact, exam-focused set.

The skill must preserve broad coverage of the course material while prioritizing concepts that recur in the parsed exam corpus. The presentation remains the factual source of truth. The exam index and linked task Markdown are relevance signals, not independent sources for new course content.

## Inputs

Read these files before editing:

- `./anki.txt`: the flashcard set to refine.
- `./presentation.pdf`: the source material used to verify terminology, claims, and slide references.
- `./Exam/Parsed/index.md`: the topic and technical-term index for the parsed exams.
- Markdown files linked from `./Exam/Parsed/index.md`: the full exam tasks, subtasks, and solutions needed to understand each indexed reference.

If `./Exam/Parsed/index.md` or its linked Markdown files do not exist, use the corresponding exam and solution PDFs under `./Exam/` as a fallback.

## Output

Rewrite `./anki.txt` in place unless the user requests another output path.

The final file should normally contain about 60-70 cards. Treat this as a target range rather than an absolute rule: preserve a few extra cards if removing them would create an important coverage gap, and use fewer cards when the source material does not justify more.

Preserve the existing card syntax and ordering conventions. Do not renumber retained cards merely to close gaps.

## Core Principles

1. Use `presentation.pdf` as the factual authority.
2. Use `Exam/Parsed/index.md` to discover potentially exam-relevant concepts.
3. Follow index references into the linked Markdown before assigning importance.
4. Judge relevance from the actual task, subtask, and solution context rather than from an isolated index term.
5. Prefer cards that test reusable understanding over cards that test incidental wording.
6. Preserve broad course coverage instead of selecting only historically examined material.
7. Merge overlap before deleting distinct concepts.
8. Keep cards atomic enough to review effectively.
9. Do not add facts found only in the exam corpus.

## Workflow

### 1. Inspect the Existing Deck

Read all of `anki.txt` and determine:

- the card format;
- the current number of cards;
- the numbering scheme;
- major topic groups;
- duplicate or near-duplicate cards;
- cards with overloaded answers;
- cards that appear unsupported, trivial, or too narrow.

Do not change the file until its structure is understood.

### 2. Verify the Course Structure

Read `presentation.pdf` with the `pdf` skill and build a compact outline of the course:

- major chapters;
- foundational definitions;
- processes and methods;
- models and architectures;
- quality attributes and principles;
- comparisons and trade-offs;
- diagrams or relationships that are central to the course.

Use this outline to ensure the refined deck does not omit an entire major area.

### 3. Read the Exam Index

Read all of `Exam/Parsed/index.md`, including both the topic section and the word or terminology section.

Record:

- broad topics and their exercise references;
- technical terms, abbreviations, named methods, tools, standards, and models;
- repeated references across distinct exams;
- references to exact subtasks;
- spelling variants, German and English equivalents, abbreviations, and closely related terminology.

The index is a retrieval map. Do not infer the meaning or importance of a reference from its entry alone.

### 4. Resolve Relevant References

For every concept represented in `anki.txt`, search the index for:

- the exact term;
- singular and plural forms;
- abbreviations and expanded forms;
- German and English variants;
- common spelling variants;
- broader parent topics;
- directly related technical terms.

Follow every relevant reference to the linked exam Markdown file. Read the complete referenced exercise or subtask and its corresponding solution section.

Determine:

- what knowledge the question actually tests;
- whether the concept is central or merely incidental;
- whether recall, explanation, comparison, application, modeling, or evaluation is required;
- which presentation concept the task corresponds to;
- whether the same concept recurs independently in other exams.

Do not count multiple index entries pointing to the same task as independent evidence.

### 5. Build a Relevance Map

Create an internal mapping from each candidate card or concept to:

- presentation chapter;
- supporting slide or slide range;
- matching index terms and topics;
- linked exam file and task or subtask;
- number of distinct exams containing a substantive match;
- depth of examination;
- conceptual importance;
- overlap with other cards.

Use the linked task wording and solution context to distinguish genuine matches from superficial term occurrences.

### 6. Score Candidate Cards

Score each card using these factors:

#### Exam recurrence

- High: substantively tested in several distinct exams.
- Medium: tested once or twice, or appears as a meaningful part of a larger task.
- Low: only mentioned incidentally or absent from the parsed exam corpus.

#### Conceptual centrality

- High: foundational definition, principle, process, architecture, model, or relationship.
- Medium: useful supporting detail.
- Low: isolated fact, list fragment, or implementation trivia.

#### Coverage value

- High: the card is the only good representative of a major course area.
- Medium: it supports a covered area without being unique.
- Low: several retained cards already test the same knowledge.

#### Card quality

- High: clear, atomic, accurate, and directly answerable.
- Medium: useful but needs tightening or merging.
- Low: ambiguous, redundant, overloaded, or unsupported.

Prioritize cards with strong combined value. A card absent from the index may still be retained when it is foundational or needed for broad coverage.

### 7. Merge Redundant Cards

Before deleting cards, look for opportunities to merge:

- duplicate definitions;
- a definition and a separate card listing the same properties;
- multiple cards that divide one short coherent process unnecessarily;
- synonymous concepts expressed with different terminology;
- cards that test the same distinction from nearly identical angles.

A merged card must remain reviewable. Do not create a large answer containing several unrelated concepts merely to reduce the count.

When merging:

- retain the best existing card number;
- combine only closely related information;
- preserve the most precise wording;
- verify the result against `presentation.pdf`;
- preserve or correct the slide reference.

### 8. Remove Low-Value Cards

Remove cards that are:

- exact or near duplicates;
- unsupported by the presentation;
- excessively narrow;
- obvious from another retained card;
- focused on incidental examples rather than transferable knowledge;
- poorly phrased and not worth repairing;
- redundant list fragments;
- based on a term that appears in the index but is not substantively tested in the linked task.

Do not remove a card solely because its concept does not occur in the index.

### 9. Repair Retained Cards

For every retained or merged card:

- verify the answer against `presentation.pdf`;
- correct terminology and grammar;
- keep the question unambiguous;
- keep the answer concise but complete;
- retain useful context needed to distinguish similar concepts;
- verify the slide reference;
- preserve the established Anki formatting.

Do not silently introduce claims that cannot be traced to the presentation.

### 10. Check Coverage and Count

After the first reduction pass:

1. Count the remaining cards.
2. Compare them against the presentation outline.
3. Confirm that major exam-index topics are represented where the presentation supports them.
4. Confirm that foundational topics absent from the index were not accidentally removed.
5. Review overrepresented topics for further consolidation.
6. Review underrepresented topics for harmful gaps.
7. Adjust toward the target of roughly 60-70 cards.

### 11. Preserve Numbering and Order

Keep cards in their existing conceptual or slide order.

- Do not renumber retained cards.
- When inserting a necessary new card between existing cards, append a decimal to the preceding card number, such as `15.1`.
- Place inserted cards in the correct chronological position.
- Do not append inserted cards arbitrarily to the end.

New cards should be rare during finetuning and should only repair a clear coverage gap supported by the presentation.

## Exam-Index Search Strategy

Search broadly enough to avoid missing relevant references:

- Start with the exact concept named in a card.
- Expand abbreviations and search both forms.
- Search related terminology used in the presentation.
- Check the broad topic section when no exact word match exists.
- Check the word section for precise subtask references.
- Follow links and inspect the full task context.
- Read the corresponding solution directly below the task.
- Track recurrence by distinct exam and substantive task, not raw link count.

Examples:

- A card about the Single Responsibility Principle should also be checked under `SRP`, `SOLID`, responsibility, and design principles.
- A card about web services may require searches for `SOAP`, `WSDL`, service-oriented architecture, interface, and protocol.
- A card about software components may require searches for component, interface, connector, Palladio, and architecture.

These expansions are for retrieval only. Keep a match only when the linked task actually tests the concept.

## Required Final Summary

After editing, report:

- original card count;
- final card count;
- number of removed cards;
- number of merged card groups;
- number of newly added cards, if any;
- whether the exam index and linked Markdown were used successfully;
- any important coverage decisions;
- any limitations such as missing index entries, broken links, or incomplete task or solution Markdown.

## Constraints

- Do not generate a replacement deck from scratch when the existing deck can be refined.
- Do not use the index as a substitute for reading the linked task.
- Do not treat every indexed term as equally important.
- Do not create cards for exam topics unsupported by `presentation.pdf`.
- Do not discard important presentation topics merely because they are absent from the index.
- Do not change the established Anki file format.
- Do not renumber the deck solely for cosmetic consistency.
