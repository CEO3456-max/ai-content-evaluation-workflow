"""
AI-Assisted Web Content Evaluation Workflow

A small, deterministic scoring engine for evaluating web content
using explicit, human-assigned criteria.

Author: Ian Kipkorir
Project: ai-content-evaluation-workflow
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_WEIGHTS = {
    "relevance": 30,
    "usefulness": 20,
    "accuracy": 20,
    "source_quality": 15,
    "freshness": 10,
    "clarity": 5,
}

REQUIRED_FIELDS = {
    "query",
    "title",
    "url",
    "scores",
}

REQUIRED_CRITERIA = set(DEFAULT_WEIGHTS.keys())


class EvaluationError(ValueError):
    """Raised when an evaluation record is invalid."""


def validate_evaluation(record: Dict[str, Any]) -> None:
    """Validate a single evaluation record."""

    if not isinstance(record, dict):
        raise EvaluationError("Evaluation record must be a dictionary.")

    missing_fields = REQUIRED_FIELDS - set(record.keys())
    if missing_fields:
        raise EvaluationError(
            f"Missing required fields: {', '.join(sorted(missing_fields))}"
        )

    if not isinstance(record["query"], str) or not record["query"].strip():
        raise EvaluationError("Query must be a non-empty string.")

    if not isinstance(record["title"], str) or not record["title"].strip():
        raise EvaluationError("Title must be a non-empty string.")

    if not isinstance(record["url"], str) or not record["url"].startswith(
        ("http://", "https://")
    ):
        raise EvaluationError("URL must start with http:// or https://.")

    scores = record["scores"]

    if not isinstance(scores, dict):
        raise EvaluationError("Scores must be provided as a dictionary.")

    missing_criteria = REQUIRED_CRITERIA - set(scores.keys())
    if missing_criteria:
        raise EvaluationError(
            f"Missing scoring criteria: {', '.join(sorted(missing_criteria))}"
        )

    unknown_criteria = set(scores.keys()) - REQUIRED_CRITERIA
    if unknown_criteria:
        raise EvaluationError(
            f"Unknown scoring criteria: {', '.join(sorted(unknown_criteria))}"
        )

    for criterion, score in scores.items():
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise EvaluationError(
                f"Score for '{criterion}' must be numeric."
            )

        if not 0 <= score <= 5:
            raise EvaluationError(
                f"Score for '{criterion}' must be between 0 and 5."
            )


def calculate_score(
    scores: Dict[str, float],
    weights: Dict[str, float] = DEFAULT_WEIGHTS,
) -> float:
    """Calculate a weighted score on a 0-100 scale."""

    if set(scores.keys()) != set(weights.keys()):
        raise EvaluationError(
            "Scores and weights must contain the same criteria."
        )

    weight_total = sum(weights.values())

    if weight_total <= 0:
        raise EvaluationError("Weight total must be greater than zero.")

    weighted_total = sum(
        (scores[criterion] / 5) * weight
        for criterion, weight in weights.items()
    )

    return round((weighted_total / weight_total) * 100, 2)


def classify_score(score: float) -> str:
    """Convert a numerical score into a qualitative rating."""

    if score >= 90:
        return "Outstanding"
    if score >= 80:
        return "Excellent"
    if score >= 70:
        return "Good"
    if score >= 60:
        return "Acceptable"
    if score >= 50:
        return "Needs Improvement"
    return "Poor"


def evaluate_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and evaluate a single content record."""

    validate_evaluation(record)

    overall_score = calculate_score(record["scores"])

    return {
        "query": record["query"],
        "title": record["title"],
        "url": record["url"],
        "scores": record["scores"],
        "overall_score": overall_score,
        "rating": classify_score(overall_score),
        "notes": record.get("notes", ""),
    }


def format_report(result: Dict[str, Any]) -> str:
    """Create a human-readable evaluation report."""

    lines = [
        f"Query: {result['query']}",
        f"Title: {result['title']}",
        f"URL: {result['url']}",
        f"Overall score: {result['overall_score']:.2f}/100",
        f"Rating: {result['rating']}",
    ]

    if result.get("notes"):
        lines.append(f"Notes: {result['notes']}")

    return "\n".join(lines)


def load_records(file_path: str) -> List[Dict[str, Any]]:
    """Load evaluation records from a JSON file."""

    path = Path(file_path)

    if not path.exists():
        raise EvaluationError(f"File not found: {file_path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise EvaluationError(
            f"Invalid JSON: {exc}"
        ) from exc

    if not isinstance(data, list):
        raise EvaluationError("Input JSON must contain an array of records.")

    return data


def main() -> int:
    """Run the command-line interface."""

    if len(sys.argv) != 2:
        print(
            "Usage: python src/evaluator.py "
            "examples/sample_evaluations.json"
        )
        return 1

    try:
        records = load_records(sys.argv[1])

        for index, record in enumerate(records, start=1):
            try:
                result = evaluate_record(record)
                print(f"\nEvaluation #{index}")
                print("-" * 60)
                print(format_report(result))
            except EvaluationError as exc:
                print(f"\nEvaluation #{index} failed: {exc}")

        return 0

    except EvaluationError as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
