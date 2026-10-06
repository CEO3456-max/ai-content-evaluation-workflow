# AI-Assisted Web Content Evaluation Workflow

A practical, transparent Python workflow for evaluating web content against a search intent using explicit, human-readable criteria.

> **Portfolio project:** This is an independently created technical project for demonstrating software engineering, evaluation methodology, and responsible AI practices. It is not presented as an official industry benchmark, conference publication, or production search-ranking system.

## Overview

Search and content-evaluation tasks often require several judgments at once:

- Does the result match the user's intent?
- Is the information useful?
- Is the source sufficiently credible for the task?
- Is the content current enough?
- Is the result high quality and readable?

This project turns those qualitative questions into a small, reproducible scoring workflow.

The evaluator accepts structured JSON records and produces criterion scores, a weighted overall score, a qualitative label, human-readable reasoning, and basic validation.

## Evaluation model

| Criterion | Weight |
|---|---:|
| Relevance | 30% |
| Usefulness | 20% |
| Accuracy / support | 20% |
| Source quality | 15% |
| Freshness | 10% |
| Clarity | 5% |

Each criterion is scored from **0 to 5**. The weighted score is normalized to 0–100.

The model is intentionally simple and explainable. It does **not** claim that a numeric score is an objective measure of truth or search-engine ranking quality.

## Quick start

### Requirements

- Python 3.9+
- No third-party packages are required.

### Run

```bash
python src/evaluator.py examples/sample_evaluations.json
```

### Test

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
ai-content-evaluation-workflow/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   └── technical-writeup.md
├── src/
│   ├── __init__.py
│   └── evaluator.py
├── examples/
│   └── sample_evaluations.json
└── tests/
    ├── __init__.py
    └── test_evaluator.py
```

## Design principles

### Explainability
Every score is explicit and the calculation is visible.

### Separation of judgment and calculation
Human or upstream evaluation supplies criterion scores; the program validates, weights, normalizes, and reports them.

### Reproducibility
The same structured input produces the same output.

### Responsible AI
The system does not pretend a numeric score can automatically establish factual truth. Accuracy scores should be based on evidence available to the evaluator.

### Privacy
The example data contains no personal information. Production deployments should minimize unnecessary collection.

## Limitations

This is a portfolio-scale reference implementation. It does not crawl websites, independently verify factual claims, determine authority automatically, replace trained human evaluation, model proprietary search ranking, or detect every form of bias and misinformation.

## Future improvements

Potential extensions include configurable scoring profiles, CSV/database input, an API layer, evidence extraction, inter-rater agreement analysis, reviewer calibration, audit logs, dashboard visualization, and model-assisted explanations with human review.

## Author

**Ian Kipkorir**

This repository is intended as a technical portfolio project demonstrating structured evaluation, Python development, testing, documentation, and responsible AI-oriented workflow design.
