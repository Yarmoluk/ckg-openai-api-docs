# Evaluation

## Twenty-question diagnostic review

Questions and checklists were frozen before retrieval. The same agent wrote and reviewed answers using the top five graph results.

| Author-reviewed outcome | Initial graph | Revised graph |
|---|---:|---:|
| Complete supported answer | 16 | 19 |
| Partial answer | 1 | 0 |
| Insufficient retrieved evidence | 2 | 0 |
| Correct evidence-limited abstention | 1 | 1 |

Repairs supplied async result-item types and request schemas for organization-group creation and organization-admin-key pagination.

The abstention question asks for Astra's exact retirement date. The reviewed answer says that the retrieved evidence does not establish a date. It does not claim to prove that no announcement exists anywhere.

## Reproduce the retrieval check

```bash
python3 scripts/evaluate.py
```

The repository contains the initial graph, revised graph, frozen questions, rubric, manually authored answers and citations. The script runs the same lexical retrieval on both graphs and checks that the cited nodes occur in the returned results.

**It does not independently generate or score model answers.** Manual entailment judgments remain author judgments. Private retained evidence locators are not part of the public export.

## Other checks

The candidate passed source-capture integrity checks, graph structure validation, a minimum public-content screen, isolated compilation, the host repository's 12 accepted regression cases and production-ranker parity before export. The standalone package adds its own export checksum and public-content checks.

The host regression suite protects unrelated retrieval behavior; it is not an evaluation of OpenAI API answer correctness.

## What has not been demonstrated

- Independent human agreement with the answer scores.
- Better coding outcomes than direct documentation lookup.
- Superiority over RAG, another graph or an unassisted model.
- Token or cost savings.
- Complete representation of every source assertion or schema field.

The graph remains unbenchmarked. A future quality study should freeze real coding tasks, hold out examples, repeat runs under matched conditions and retain both failures and human scores.
