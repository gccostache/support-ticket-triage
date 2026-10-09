# Fictional ticket evaluation

Split: **development**. Tickets: **20**.

| Method | Correct | Accuracy | Coverage | Accepted accuracy | Review recall |
| --- | ---: | ---: | ---: | ---: | ---: |
| keyword | 16/20 | 80.0% | 75.0% | 86.7% | 60.0% |
| semantic | 18/20 | 90.0% | 85.0% | 88.2% | 60.0% |

Accuracy includes correct review decisions. Coverage is the fraction assigned a supported category. Accepted accuracy measures only those assignments. Review recall measures how many expected-review tickets were sent to review.

This small, balanced, synthetic dataset does not establish production accuracy or time savings. Thresholds are provisional. Inspect predictions.csv for errors; metrics.json includes confusion matrices and run metadata.

## Incorrect outcomes

- keyword, D07: expected Performance; got Other / needs review.
- keyword, D14: expected Integration; got Other / needs review.
- keyword, D19: expected Other / needs review; got Integration.
- keyword, D20: expected Other / needs review; got Performance.
- semantic, D19: expected Other / needs review; got Authentication.
- semantic, D20: expected Other / needs review; got Authentication.
