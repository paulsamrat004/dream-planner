# Test Evidence

The automated suite contains 24 tests.

| # | Scenario | Expected |
|---|---|---|
| 1 | Inflation configuration | 6% (`0.06`) |
| 2 | One-year inflation | 100000 -> 106000 |
| 3 | Five-year inflation | Compound at 6% annually |
| 4 | Timeline 0 | Reject |
| 5 | Timeline 51 | Reject |
| 6 | Saving -1% | Reject |
| 7 | Saving 101% | Reject |
| 8 | Salary 0 | Reject |
| 9 | Case-insensitive city | Accept |
| 10 | Unknown city | Reject |
| 11 | Unknown area | Reject |
| 12 | Achievable | Achievable |
| 13 | Challenging | Challenging |
| 14 | Highly Challenging | Highly Challenging |
| 15 | Entered salary 40000 | Exactly 40000 is used |
| 16 | Three goals | Marriage, Car, Home |
| 17 | Investment calculation | Positive |
| 18 | Salary dataset | Required columns |
| 19 | Model comparison | 3 models, MAE/R², no Random Forest |
| 20 | RAG retrieval | Local guidance returned |
| 21 | Unknown RAG | No grounded result |
| 22 | Prompt injection | Not executed |
| 23 | RAG documents | At least 3 |
| 24 | Expected return | Positive |

Run `pytest -q` and record the actual output in `docs/test_results.txt`.
