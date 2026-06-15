# Configuration Format

```json
{
  "input_dir": "Exam/Parsed",
  "output": "Exam/Parsed/index.md",
  "title": "Course Exam Index",
  "file_glob": "*.md",
  "exclude": ["index.md"],
  "topic_rules": [
    {
      "topic": "Requirements Engineering",
      "patterns": ["Requirement", "Anforderung"]
    },
    {
      "topic": "Cross-Topic Fundamentals",
      "patterns": ["General Knowledge", "Wissensfragen", "Verschiedenes"]
    }
  ],
  "fallback_topic": "Other Course Topics",
  "topic_overrides": {
    "course-ws2324.md#1": "Cloud Computing",
    "course-ss25.md#6": "Enterprise Architecture"
  },
  "terms": {
    "Palladio Component Model (PCM)": [
      "Palladio",
      "PCM"
    ],
    "Software component": [
      "software component",
      "Softwarekomponente"
    ]
  }
}
```

Topic rules are evaluated in order. Put more specific rules before broad rules.

Use `topic_overrides` when a generic title such as "General Knowledge" or
"Miscellaneous" actually belongs to a specific broad topic. Keys use
`<filename>#<exercise-number>`.

The parser recognizes:

- `## Aufgabe N: ...`
- `## Task N: ...`
- `## Exercise N: ...`
- `## Lösung zur Aufgabe N`
- `## Solution for Task N`
- `## Solution for Exercise N`
- `### N a)`

File names should encode a useful exam label. The script recognizes `wsYYZZ` and `ssYY`; otherwise it uses the stem.
