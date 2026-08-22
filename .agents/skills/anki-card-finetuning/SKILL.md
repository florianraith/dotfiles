---
name: anki-card-finetuning
description: Analyze and refine an overgenerated anki.txt into an exam-focused, efficiently reviewable deck by proposing a source-specific target card range for user approval, verifying presentation content, resolving exam references, repairing cue and interference problems, and matching card operations to assessed tasks.
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

First produce a target-range proposal without modifying `anki.txt`. Rewrite `./anki.txt` in place only after the user explicitly approves that range, supplies a replacement range, or specifies an exact target count.

Treat the user-selected target as authoritative. Finish within an approved range, or at the exact count when the user selects one. If satisfying it would require removing required coverage or creating low-quality cards, stop and ask the user to revise the target instead of silently deviating.

Preserve the existing card syntax and ordering conventions. After the final card selection is complete, renumber all cards sequentially from 1 without gaps.

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
10. Preserve concept learning order: retain or create one introduction card for each retained newly introduced concept, including topic-introduced abbreviations, before its detail cards.
11. Optimize one retrieval operation per card, not the smallest possible fact fragment.
12. Match the card operation to the exam operation when the presentation supports it.
13. Derive the target range from the current source and obtain explicit user approval before changing the deck.

## Concept and Abbreviation Introduction

For every retained named topic, concept, model, method, architecture, metric, or process that the slides newly introduce:

- Retain or create exactly one first card with front `What is <canonical concept name>?`.
- Use a one-sentence answer that states the concept's category and distinguishing idea without listing its later details.
- Allow the answer to refer to concepts introduced earlier, including relational definitions such as `An extension of <earlier concept> that adds <feature>.`
- Place prerequisite introduction cards before dependent introductions, then place finer-grained Why, Which, How, comparison, mechanism, trade-off, and application cards afterward.
- Treat the minimal definition and distinct detail cards as an intentional scaffold, not redundancy.
- Do not create introduction cards for incidental names or prerequisites the slides use without explaining.

If all cards for a concept are intentionally removed, its introduction card may also be removed. If any detail card remains, preserve or restore its introduction card even when this causes a modest count overrun; remove lower-value detail cards before required introductions.

Treat abbreviation introduction as a special case of this rule:

- Use only abbreviations that appear in the slides.
- Classify each abbreviation from the way the slides present it:
  1. **Topic-introduced abbreviation:** If the slides introduce the abbreviation as a concept, model, or method and provide its meaning, retain or create an introduction card before later shorthand use:
     - Front: `What is <ABBREVIATION>?`
     - Back: `<Full term> (<ABBREVIATION>): <concise explanation of the concept>.`
     Later cards may use the abbreviation alone without repeating its expansion.
  2. **Assumed-known abbreviation:** If the slides use an abbreviation without introducing its topic or expansion, treat it as prior knowledge and reuse it without expansion. Do not create an expansion-only card. Examples can include RGB, API, and LLM when the slides merely reuse them.
- Do not infer or invent an expansion that the slides do not provide.
- Do not remove the only required introduction card when later cards depend on that abbreviation.
- When the abbreviation and full term name the same concept, retain one abbreviation introduction card rather than a duplicate full-term introduction card.

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
- vague, under-specified, or compound cues;
- unordered sets larger than three and answers longer than roughly 25 substantive words;
- formula, mechanism, or comparison prompts whose answers have the wrong type;
- empty or image-only text backs;
- identical normalized answers and highly similar fronts with competing answers;
- newly introduced concepts, their introduction cards, prerequisite order, and any detail cards lacking an earlier introduction;
- abbreviation use, classification, and introduction order;
- questions that depend on source artifacts or learning context, especially wording such as "in this lecture", "in the presentation", "on the slide", "in the diagram", "shown in the diagram", "shown in the lecture", "according to the lecture", or "according to the diagram".

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

### 5. Propose a Target Range and Get Approval

Keep `anki.txt` unchanged while sizing the deck. Derive a defensible range by triangulating all four signals below rather than applying a universal card count:

1. **Slide volume:** Count total slides and content-bearing slides. Exclude title pages, agendas, section dividers, bibliographies, near-empty slides, and repeated administrative material.
2. **Content complexity:** Classify content-bearing slides or coherent slide groups as low, medium, or high complexity. Low-complexity material presents one simple definition or example; medium-complexity material presents several related claims, a comparison, or a short process; high-complexity material presents formulas, multi-stage mechanisms, dense architectures, interacting concepts, or application procedures. Account for concepts developed across several slides as one unit instead of multiplying cards by slide count.
3. **Existing-deck yield:** Start from the current card count, then estimate how many distinct supported retrieval operations remain after obvious duplicates, unsupported trivia, and redundant fragments are removed and necessary introductions, splits, or application cards are added. This is an estimate only; do not rewrite cards to obtain it.
4. **Exam coverage:** Count distinct exams and substantive tasks, the major presentation areas they cover, recurring concepts, and the assessed operations they require. Increase space for independently recurring or application-heavy concepts; avoid increasing it for repeated index links to the same task or incidental mentions.

Establish a **coverage floor** from the required concept introductions, at least one strong representative for each major course area, and distinct exam-assessed operations that need separate cards. Establish a **useful ceiling** from the supported, non-redundant retrieval operations justified by the slides and exam evidence. Reconcile these bounds with slide volume, complexity, and the current deck's estimated yield. Prefer a reasonably narrow range that communicates a real study-load choice; widen it only when missing or ambiguous source material creates genuine uncertainty.

Present the proposal to the user with:

- current card count;
- total and content-bearing slide counts;
- complexity profile and the main reasons for it;
- exam corpus size, recurrence, breadth, and application depth;
- estimated coverage floor and useful ceiling;
- proposed minimum and maximum card counts;
- the main trade-off at the lower versus upper end;
- any uncertainty or missing inputs that materially affect the estimate.

Ask the user to approve the proposed range, provide a replacement range, or specify an exact target card count based on the proposal. Stop after asking: do not merge, remove, add, repair, renumber, or write any card until a subsequent user message explicitly selects a target. A request to run this skill is not itself approval of the proposed range. Record the selection as the **approved target** and use it throughout the remaining workflow. For an exact target, set the approved minimum and maximum to that same count.

### 6. Build a Relevance Map

Create an internal mapping from each candidate card or concept to:

- presentation chapter;
- supporting slide or slide range;
- matching index terms and topics;
- linked exam file and task or subtask;
- number of distinct exams containing a substantive match;
- depth of examination;
- conceptual importance;
- overlap with other cards.
- whether the card is a required concept introduction or a detail card in that concept's cluster;
- retrieval operation: recall, explain, compare, compute, choose, diagnose, model, or evaluate;
- card-shape risks: ambiguous cue, unbounded set, compound prompt, long prose, answer-type mismatch, image-only answer, or interference cluster;

Use the linked task wording and solution context to distinguish genuine matches from superficial term occurrences.

### 7. Score Candidate Cards

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

- High: the card is a required introduction for a retained concept or the only good representative of a major course area.
- Medium: it supports a covered area without being unique.
- Low: several retained cards already test the same knowledge.

#### Card quality

- High: unique cue, one retrieval operation, concise verbalizable answer, binary grading criterion, and exam-appropriate operation.
- Medium: valuable but needs splitting, tightening, contrast, or type repair.
- Low: ambiguous, redundant, overloaded, unsupported, image-only, or strongly confusable with another card.

Prioritize cards with strong combined value. A card absent from the index may still be retained when it is foundational or needed for broad coverage.

### 8. Merge Redundant Cards

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
- do not merge away the only required introduction card for an abbreviation used by later cards.
- do not merge a required `What is ...?` introduction into a detail card;
- do not treat minimal definition/detail overlap as redundancy when the detail card tests a distinct operation;
- do not merge cards when the result requires more than one independent retrieval operation;
- do not merge merely to reach the target count.

### 9. Transform High-Cost Card Shapes

Repair valuable but inefficient cards before considering deletion:

- **Large unordered set:** group it semantically into sets of at most three, invert it into cards keyed by distinguishing properties, or retain only a count-and-group scaffold.
- **Long process or architecture:** create cards for diagnostic links or stages; retain a full-chain card only when reproducing the complete chain is exam-relevant.
- **Parallel siblings:** ask which concept has a distinguishing property or create an explicit contrast instead of repeating nearly identical stems.
- **Vague cue:** state the framework, requested answer type, count, or relationship that makes one answer uniquely correct.
- **Missing introduction:** add `What is <canonical concept name>?` before retained detail cards and define the concept briefly using only earlier introduced or assumed-known terminology.
- **Compound prompt:** split it so each resulting card has one pass criterion.
- **Type mismatch:** make the text answer supply the requested formula, name, mechanism, cause, or trade-off.
- **Image-only answer:** add the minimum verbalizable text answer; use media only as support.

Treat more than three unordered items or roughly 25 substantive answer words as repair triggers, not automatic failures. Preserve coherent formulas, contrast pairs, and short ordered chunks.

### 10. Remove Low-Value Cards

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

### 11. Repair Retained Cards

For every retained or merged card:

- verify the answer against `presentation.pdf`;
- correct terminology and grammar;
- keep the question unambiguous;
- make the expected answer type explicit and ensure a knowledgeable learner cannot give a different correct answer;
- preserve `What is <canonical concept name>?` for introduction cards; on detail cards, replace load-bearing vague verbs such as identify, formalize, synthesize, define, play a role, is used for, and is important with the precise tested relationship;
- require one grading decision and a verbalizable text answer per card;
- rewrite questions so they are source-artifact independent and do not mention standalone source-artifact words such as lecture, presentation, slide, deck, figure, or diagram, or phrases such as shown, mentioned, named, or highlighted there; use whole-word matching so terms like representation are allowed;
- keep the answer concise but complete;
- retain useful context needed to distinguish similar concepts;
- apply the concept and abbreviation introduction policy, ensure each required introduction precedes its detail cards, and remove forward references to concepts introduced later;
- verify the slide reference;
- preserve the established Anki formatting.

Do not silently introduce claims that cannot be traced to the presentation.

When linked exam tasks require application, preserve or create at least one card with the same supported operation: compute, choose, diagnose, model, explain, or evaluate. Exam material may determine the task shape but not introduce unsupported course facts.

### 12. Check Coverage and Count

After the first reduction pass:

1. Count the remaining cards.
2. Compare them against the presentation outline.
3. Confirm that major exam-index topics are represented where the presentation supports them.
4. Confirm that foundational topics absent from the index were not accidentally removed.
5. Review overrepresented topics for further consolidation.
6. Review underrepresented topics for harmful gaps.
7. Scan every question for forbidden source-artifact wording using whole-word matching, and repair any match before finalizing. Do not flag substrings inside valid technical terms; for example, representation is allowed.
8. Validate concept and abbreviation classification, introduction coverage, dependency order, and learning order.
9. Confirm that every retained detail-card cluster has exactly one earlier `What is ...?` introduction and that its definition does not merely duplicate a detail card.
10. Confirm that substantively examined application-level concepts use the relevant retrieval operation where supported.
11. Run the bundled script by its resolved skill path, substituting the approved bounds: `python3 <anki-card-finetuning-skill-directory>/scripts/audit_cards.py anki.txt --min-cards <approved-min> --max-cards <approved-max>`. For an exact target, pass the same value to both options. Repair every structural finding, inspect all warnings, and justify internally any safe exception.
12. Adjust to the approved target without removing required introduction cards or sacrificing quality and coverage. If those requirements conflict, pause and request a revised target.

### 13. Preserve Order and Renumber Sequentially

Keep cards in their existing conceptual or slide order.

- During selection and merging, you may keep original card numbers temporarily to track provenance.
- Before writing the final `anki.txt`, renumber all cards sequentially as `1. Card`, `2. Card`, `3. Card`, and so on without gaps.
- Place inserted cards in the correct chronological position.
- Order concept prerequisites before dependent introductions and place each introduction before its detail cards.
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

- proposed target range and the user-selected range or exact count;
- original card count;
- final card count;
- number of removed cards;
- number of merged card groups;
- number of newly added cards, if any;
- number of repaired cues, split list or process cards, and resolved collision groups;
- number of retained or added application cards;
- number of concept-introduction cards retained, restored, newly added, and removed with an excluded concept;
- whether the exam index and linked Markdown were used successfully;
- whether the source-artifact wording scan passed after repairs;
- whether the audit script passed and which warnings, if any, were deliberately retained;
- any important coverage decisions;
- any limitations such as missing index entries, broken links, or incomplete task or solution Markdown.

## Constraints

- Do not generate a replacement deck from scratch when the existing deck can be refined.
- Do not use the index as a substitute for reading the linked task.
- Do not treat every indexed term as equally important.
- Do not create cards for exam topics unsupported by `presentation.pdf`.
- Do not invent abbreviation expansions absent from the slides.
- Do not remove the required introduction card while retaining detail cards for that concept.
- Do not discard important presentation topics merely because they are absent from the index.
- Do not change the established Anki file format.
- Do not leave gaps or decimal card numbers in the final deck; final card numbers must be sequential integers.
- Do not edit `anki.txt` before the user explicitly selects a proposed range, replacement range, or exact count.
- Do not use the approved target to justify a compound card, an unbounded list, or a cue collision.
