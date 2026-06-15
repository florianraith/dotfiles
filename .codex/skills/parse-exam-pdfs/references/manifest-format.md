# Manifest Format

```json
{
  "root": ".",
  "output_dir": "Exam/Parsed",
  "temp_dir": "tmp/exam-pdfs",
  "course_title": "Software Engineering II",
  "task_words": ["Aufgabe", "Task", "Exercise"],
  "solution_headings": {
    "de": "Lösung zur Aufgabe {number}",
    "en": "Solution for Task {number}"
  },
  "pairs": [
    {
      "slug": "course-ws2324",
      "exam": "Exam/Old Exams/exam.pdf",
      "solution": "Exam/Solutions/solution.pdf",
      "language": "de"
    }
  ]
}
```

Paths are relative to `root`. `slug` becomes `<output_dir>/<slug>.md`.

Optional pair fields:

- `title`: Override the document title.
- `visual_keywords`: Additional words that indicate a page should be rendered.
- `ocr_languages`: Tesseract languages such as `deu+eng`.
- `force_ocr`: OCR even if a PDF contains an unusable text layer.
