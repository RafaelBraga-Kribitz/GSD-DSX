# Weighted-kappa readout (clean negative control)

**Audience:** VP Merchandising
**Status:** calibration control — a correctly-declared weighted kappa that the
gate should pass silently.

## Headline

The bundle recommender raises average order value by $1.85
(95% CI $0.92 to $2.78) per completed order in the test window.

The numbers above are illustrative and pinned. This spec exists as a clean
negative control: it declares a weighted kappa with a recognised weighting scheme
(quadratic) and both p_pos and p_neg companions, so the weighted-kappa-weights
and kappa-companions gates reach their branches and stay silent.

## Limitations

A calibration control. It carries no decision weight and reports no real finding
about any product.
