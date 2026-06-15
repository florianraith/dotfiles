# Candidate Mining

Use several independent searches and review candidates manually.

## Parenthetical translations

Search for bilingual or expanded technical terms:

```bash
rg -n '\([^()]{2,80}\)' Exam/Parsed/*.md
```

## Named concepts

Search capitalized multiword phrases, acronyms, laws, models, patterns, principles, standards, and authors. Reject OCR fragments and application-specific names.

## Suffix families

Search words ending in:

- architecture, pattern, principle, model
- requirement, quality, semantics, syntax
- process, review, test, scheduling
- interface, service, repository, factory
- entity, aggregate, context, inheritance

## Solution-only vocabulary

Review solution sections for:

- Lists of valid answers
- Named subtypes and variants
- Layer names and roles
- Security and quality principles
- Scheduling algorithms
- Test doubles and review forms
- Bilingual aliases and abbreviations

## Quality filter

Include a candidate if it helps locate course knowledge. Exclude it if it is merely:

- A person or organization in an exam scenario
- A class/variable name unique to one example
- A generic programming keyword
- Page furniture or OCR noise
- A broad everyday word without course-specific meaning
