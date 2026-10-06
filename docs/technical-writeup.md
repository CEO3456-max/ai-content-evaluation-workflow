# Building a Transparent AI-Assisted Web Content Evaluation Workflow

**Author:** Ian Kipkorir  
**Project type:** Independent technical portfolio project  
**Status:** Reference implementation

## Abstract

Evaluating web content is a multi-dimensional task. A result can be relevant to a query while still being outdated, difficult to use, poorly supported, or published by a low-quality source.

This project implements a small Python-based evaluation workflow that converts these dimensions into an explicit scoring model. The design separates evaluator judgment from deterministic calculation: a reviewer supplies scores for predefined criteria, while the software validates those scores, applies configurable weights, normalizes the result, and generates a concise report.

The goal is not to reproduce a commercial search engine or claim that the resulting score represents objective truth. Instead, the project demonstrates how a qualitative content-review process can be made more consistent, auditable, and reproducible.

## 1. Problem Statement

A content evaluator may need to answer several questions about a search result:

1. Does the result satisfy the intent behind the query?
2. Does it provide useful information?
3. Are its claims sufficiently supported?
4. Is the source appropriate for the topic?
5. Is the information reasonably current?
6. Is the content clear and understandable?

When these judgments are made without an explicit framework, different reviewers may apply different standards.

A lightweight scoring model can improve consistency by giving reviewers a common vocabulary and a repeatable calculation method.

## 2. Goals

The implementation has five primary goals:

- Define a small set of understandable evaluation criteria.
- Make criterion weights explicit.
- Validate all incoming scores.
- Produce a deterministic weighted score.
- Keep human judgment visible rather than hiding it behind an opaque model.

## 3. Non-Goals

The project deliberately does not attempt to:

- rank the entire web;
- determine absolute factual truth automatically;
- scrape arbitrary websites;
- infer a user's private preferences;
- reproduce proprietary search algorithms;
- make high-stakes decisions without human review.

## 4. Evaluation Criteria

Each criterion receives a score from 0 to 5.

### Relevance — 30%

Measures how closely the content addresses the user's query and likely intent.

### Usefulness — 20%

Measures whether the content helps the user accomplish the task implied by the query.

### Accuracy / Support — 20%

Measures how well the information appears to be supported by evidence available to the evaluator.

This score is not an automatic fact-check. A reviewer should use appropriate evidence and should avoid treating unsupported assertions as verified facts.

### Source Quality — 15%

Measures whether the publisher is reasonably appropriate and trustworthy for the subject.

### Freshness — 10%

Measures whether the content appears sufficiently current for the task.

Freshness is highly task-dependent.

### Clarity — 5%

Measures readability, organization, and whether the user can easily understand and use the information.

## 5. Scoring Formula

Let:

- `s_i` be a criterion score between 0 and 5.
- `w_i` be its percentage weight.

The normalized overall score is:

```text
overall = Σ ((s_i / 5) × w_i)

Because the weights sum to 100, the result is on a 0–100 scale.

For example:

Relevance       = 5
Usefulness      = 4
Accuracy        = 4
Source quality  = 4
Freshness       = 3
Clarity         = 5

The resulting weighted score is:

85/100

The implementation calculates this programmatically.

6. Architecture

The reference implementation has three conceptual layers:

Structured evaluation input
          |
          v
     Validation layer
          |
          v
 Weighted scoring engine
          |
          v
 Human-readable report

The evaluator does not fetch external pages. This is intentional: source inspection and scoring remain separate from the deterministic calculation component.

7. Input Format

The evaluator accepts a JSON array of records.

Example:

[
  {
    "query": "best places to visit in Nairobi Kenya",
    "title": "Top places to visit in Nairobi",
    "url": "https://example.com/nairobi-guide",
    "scores": {
      "relevance": 5,
      "usefulness": 4,
      "accuracy": 4,
      "source_quality": 4,
      "freshness": 3,
      "clarity": 5
    },
    "notes": "Directly addresses the query and provides practical visitor information."
  }
]
8. Validation Strategy

The evaluator rejects malformed records rather than silently producing questionable results.

Validation includes:

required top-level fields;
basic URL structure;
presence of every scoring criterion;
numeric score values;
score range from 0 through 5;
no unknown scoring criteria;
non-empty titles and queries.
9. Implementation

The core implementation uses Python's standard library only.

Important functions include:

validate_evaluation() — checks input structure and score ranges.
calculate_score() — applies criterion weights.
classify_score() — maps the numerical result to a qualitative label.
evaluate_record() — combines validation and calculation.
format_report() — produces a readable terminal report.

Keeping these functions small makes the project easier to test and extend.

10. Testing

The test suite uses Python's built-in unittest framework.

Tests cover:

a perfect score;
a zero score;
weighted-score calculation;
invalid score ranges;
missing criteria;
unknown criteria;
empty required fields;
basic URL validation;
rating classification.

Run the tests with:

python -m unittest discover -s tests -v
11. Responsible AI Considerations

An evaluation workflow can create a false impression of precision if a numerical score is treated as objective truth.

This project addresses that risk through:

Explicit Criteria

The criteria and weights are visible rather than hidden.

Human-in-the-Loop Design

The reviewer remains responsible for interpreting evidence and assigning criterion scores.

No Automatic Truth Claim

The accuracy field represents an evaluation judgment based on available evidence; it is not a universal truth score.

Auditability

The input scores and notes can be inspected to understand how an overall score was produced.

Privacy Minimization

The example dataset contains only task-relevant information. A production implementation should avoid storing personal data unless necessary.

12. Bias and Consistency

A scoring framework can reduce some inconsistency while still introducing its own biases.

For example:

A weight of 30% for relevance reflects a design choice.
Different topics may require different standards.
Reviewers may interpret the same criterion differently.
A source's reputation can be difficult to assess objectively.

A more advanced implementation should therefore support reviewer calibration and measure inter-rater agreement.

13. Security Considerations

The reference implementation treats input as data rather than executable code.

It does not:

execute URLs;
run downloaded content;
evaluate arbitrary Python;
require external credentials.

If future versions add web crawling or model APIs, additional protections would be required, including URL allow/deny policies, request limits, content sanitization, secret management, and logging controls.

14. Performance

For the current implementation, scoring is computationally inexpensive. Each record requires a fixed number of arithmetic operations, making the core scoring complexity effectively linear in the number of evaluation records.

The main performance cost in a future end-to-end system would likely come from external activities such as web retrieval, document parsing, or model inference rather than the scoring function itself.

15. Example Result

For the included sample data, the evaluator produces reports containing:

Query: best places to visit in Nairobi Kenya
Title: Top Places to Visit in Nairobi
URL: https://example.com/nairobi-guide
Overall score: 85.00/100
Rating: Excellent
16. Future Work

Potential improvements include:

Reviewer calibration with shared scoring examples.
Configurable rubrics for different content types.
Evidence tracking for accuracy judgments.
Human-reviewed AI assistance.
Score-distribution and disagreement analytics.
API integration.
17. Conclusion

This project demonstrates a practical approach to making web-content evaluation more structured and reproducible.

Its central design decision is simple:

Use automation for consistent calculation while keeping substantive evaluation decisions visible to a human reviewer.

That separation makes the system easier to understand, test, audit, and adapt.

Repository: ai-content-evaluation-workflow
Author: Ian Kipkorir
