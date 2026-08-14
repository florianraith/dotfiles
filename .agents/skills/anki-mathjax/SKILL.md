---
name: anki-mathjax
description: Convert mathematical notation in Anki text decks to Anki-compatible MathJax tags while preserving card wording, equations, examples, numbering, and formatting. Use when Codex is asked to mathify anki.txt or another plain-text Anki deck, wrap formulas or variables in MathJax, repair raw mathematical notation, or standardize inline and block equations for Anki.
---

# Anki MathJax

Convert mathematical notation in an Anki text deck without changing the knowledge being tested.

## Workflow

1. Read the complete target file. Default to `./anki.txt` when no path is given.
2. Record the card count and established card structure before editing.
3. Identify mathematical notation in `Front:`, `Back:`, and `Example:` content. Do not modify card headers or page references.
4. Convert short notation embedded in prose to inline MathJax:

   `<anki-mathjax>...</anki-mathjax>`

5. Convert a standalone or long equation to block MathJax on its own line:

   `<anki-mathjax block="true">...</anki-mathjax>`

6. Rewrite raw notation as valid LaTeX inside the tags. Examples:

   - `p_model(x)` becomes `<anki-mathjax>p_{\mathrm{model}}(x)</anki-mathjax>`
   - `R^(3 x h x w)` becomes `<anki-mathjax>\mathbb{R}^{3 \times h \times w}</anki-mathjax>`
   - `F(G(x)) approximates x` becomes `<anki-mathjax>F(G(x)) \approx x</anki-mathjax>`

7. Preserve every equation's full mathematical meaning. Do not omit objectives, parameters, conditions, sampling distributions, indices, constants, or terms merely to shorten an expression. When source material is available, verify the equation against it.
8. Preserve all non-mathematical wording unless a minimal grammar adjustment is required around a tag. Do not add, remove, merge, or renumber cards.
9. Rewrite the target file in place unless the user requests another output path.

## Conversion Rules

- Wrap mathematical variables when they function as notation, including symbols such as `x`, `z`, `G`, and `D` in mathematical statements.
- Wrap equations, probability distributions, objectives, expectations, matrix or vector expressions, dimensions, inequalities, and function compositions.
- Keep ordinary prose, model names, acronyms, dates, page numbers, and incidental numbers outside MathJax.
- Use `\mathrm{...}` for textual subscripts, `\mathbb{E}` for expectations, `\mathbb{R}` for real spaces, `\times` for mathematical dimensions, `\mid` for conditioning, and `\approx` for approximation.
- Do not nest MathJax tags.
- Preserve valid existing MathJax tags. Repair them only when syntax or mathematical content is incomplete.
- Use `&nbsp;` around inline tags only when needed to preserve visible spacing in the target Anki template.

## Full-Equation Example

Use a complete GAN objective rather than abbreviated expectations:

`<anki-mathjax block="true">\min_G \max_D V(D,G) = \mathbb{E}_{x \sim p_{\mathrm{data}}(x)}\!\left[\log D(x)\right] + \mathbb{E}_{z \sim p_z(z)}\!\left[\log\!\left(1-D(G(z))\right)\right]</anki-mathjax>`

## Validation

Before finishing:

1. Confirm opening and closing MathJax tag counts match.
2. Confirm every block tag has `block="true"` and occupies its own content line.
3. Search for remaining raw equation patterns and classify each match before changing it.
4. Confirm the original card count, numbering, headers, questions, answers, examples, and page references remain intact.
5. Report the number of inline and block expressions converted and any ambiguous notation intentionally left unchanged.
