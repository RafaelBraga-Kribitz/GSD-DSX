# Weighted-kappa readout (known-bad control)

**Audience:** executive
**Status:** calibration fixture — encodes a declared routing defect, not a measured result.

## Headline

The bundle recommender raises average order value by $1.85
(95% CI $0.92 to $2.78) per completed order in the test window.

The numbers above are illustrative and pinned; they are not asserted as a real
measured effect. The fixture exists so the gate has a live, dedicated example of
the weighted-kappa-without-weights routing defect to catch.

## What is wrong

A weighted kappa needs a declared weighting scheme — linear or quadratic, or an
explicit weight matrix. Without one it is not a weighted kappa at all; an
unweighted kappa is a different statistic (declare cohens_kappa instead).

## Limitations

A calibration control. It carries no decision weight and reports no real finding
about any product.
