---
name: paper-explainer
description: Explainer PDF for an academic paper, tailored to one reader's background and goals. Use when asked to explain, summarise for understanding, or make a readable/intuitive PDF of a paper.
---

Turn one paper into a printable A4 LaTeX/PDF explainer for a specific reader. The reader's profile decides everything: which background gets a primer, which analogies bridge to what they already know, what gets left out. The paper is the source of truth; the explainer adds intuition, not new claims.

## Steps

1. **Locate the paper.** Get the PDF path (or download it after asking). `pdftotext -layout` it into `tmp/<slug>/paper.txt`. Read it end to end, including tables and the appendix. Render pages with figures or formulas the text dump mangles (`pdftoppm -r 80 -png`) and look at them. Done when you can state the problem, method, evidence and limitations in one sentence each.

2. **Interview the reader.** Send one chat message with these six questions, each pre-filled with your best guess from the conversation, CLAUDE.md/AGENTS.md and the project, so the user can confirm or correct instead of writing from scratch:
   - **Scope**: whole paper, or specific sections/aspects?
   - **Wants to know**: the questions the explainer must answer (e.g. "what is the model", "why does it matter", "how was it evaluated").
   - **Does not want**: depth to skip (e.g. proofs, derivations, implementation details).
   - **Already knows**: fields and concepts to build on (these become the analogy domain).
   - **Does not know**: fields and concepts that need a primer.
   - **Context**: why they read it (course, project, thesis), and directories or documents with more context.
   
   Also confirm language and output location (default: next to the paper PDF as `<paper name> - Explainer.pdf`). Wait for the answer. Done when every question has an answer or an accepted default.

3. **Read the context.** Read every directory and document the user named, enough to know what the reader's project needs from this paper. Done when you can write the "why this matters for you" section without guessing.

4. **Write** `tmp/<slug>/<slug>.tex` from [`template.tex`](template.tex), using the structure and writing rules below.

5. **Verify.** Every number, claim and result in the explainer is traced to a page, table or section of the paper; recheck each against `paper.txt`. Every own example is recomputed with `python3 -I` (scripts in `tmp/verify/`). Done when every stated number has been checked, including table rows.

6. **Compile.** `cd tmp/<slug> && tectonic --keep-logs <slug>.tex`. Fix every error and every `Overfull \hbox` (long title or author lines and long inline math are the usual culprits).

7. **Inspect.** Render all pages to `tmp/render/`, view every page with a figure or table, and build a contact sheet (`pdftoppm -r 30 -png`, then `montage c-*.png -tile 5x -geometry +4+4 grid.png`). Check TikZ labels for overlap with lines and other labels. Done when no page except the last is mostly empty and no element overflows or collides.

8. **Deliver.** Copy the PDF to the output location, keep the `.tex` in `tmp/<slug>/`, delete `tmp/render/` and `tmp/verify/`. Report concisely: path, page count, what was verified and how, what is own material (examples, interpretation), anything uncertain in the paper.

## Structure

Sections in this order; drop any the profile makes irrelevant:

1. **The paper in one page**: the question, the idea, the evidence, the result, and a `takeaway` box with the one sentence summary.
2. **Primers**, one per "does not know" topic the paper takes for granted: just enough to follow the paper, no more. Say that the primer is general background, not paper specific.
3. **Baselines and prior work**: the methods the paper improves on, and why they fall short.
4. **The method**: intuition first, then the minimum notation needed to name the moving parts. Explain *why* each design choice was made (what breaks without it). Skip what the reader excluded.
5. **Evaluation**: setup, metrics (explained), one `booktabs` table of the key numbers with the source table cited in the caption, and how to read it.
6. **Pitfalls**: a `pitfall` box listing the ways a reader would most plausibly over-read or misread the results.
7. **Strengths and limitations**, including the paper's own future work.
8. **Why this matters for you**: links to the reader's context, marked once as own interpretation.
9. **Glossary** of every term the reader did not know before.
10. **Summary** as a numbered list.

## Writing rules

- Write for the reader profile: everything in "already knows" is used without explanation and is the source of analogies; everything in "does not know" is explained the first time it appears.
- Each technical section gets an analogy box (`analogy` environment, titled after the reader's home field, e.g. `\begin{analogy}{ML analogy}`), mapping the paper's concept to one the reader knows.
- At least one small worked toy example of the core mechanism (`example` box), small enough to follow by hand, with numbers computed in step 5. Title it `(own toy example)`.
- At least one TikZ figure showing the central idea, when the idea has a spatial or temporal shape.
- Prose over bullet fragments. Plain words for every equation shown: what each term does.
- Own material (examples, analogies beyond the paper, the relevance section) is labelled as such; everything else must be in the paper.
- Layout is printable and compact: content flows continuously from title and TOC onward. Use sections only (`\chapter` forces a page break in `scrreprt` even with the redeclared style); the template already does this.
