# Fictional ticket evaluation

Split: **test**. Tickets: **20**.

| Method | Correct | Accuracy | Coverage | Accepted accuracy | Review recall |
| --- | ---: | ---: | ---: | ---: | ---: |
| keyword | 13/20 | 65.0% | 50.0% | 90.0% | 80.0% |
| semantic | 18/20 | 90.0% | 75.0% | 93.3% | 80.0% |

Accuracy includes correct review decisions. Coverage is the fraction assigned a supported category. Accepted accuracy measures only those assignments. Review recall measures how many expected-review tickets were sent to review.

This small, balanced, synthetic dataset does not establish production accuracy or time savings. Thresholds are provisional. Inspect predictions.csv for errors; metrics.json includes confusion matrices and run metadata.

## Incorrect outcomes

- keyword, T02: expected Authentication; got Other / needs review.
- keyword, T06: expected Performance; got Other / needs review.
- keyword, T07: expected Performance; got Other / needs review.
- keyword, T09: expected Performance; got Other / needs review.
- keyword, T13: expected Integration; got Other / needs review.
- keyword, T14: expected Integration; got Other / needs review.
- keyword, T20: expected Other / needs review; got Integration.
- semantic, T13: expected Integration; got Other / needs review.
- semantic, T20: expected Other / needs review; got Performance.
