# Ordinal-operand correlation readout (known-bad control)

**Audience:** executive
**Status:** calibration fixture — encodes a declared routing defect, not a measured result.

## Headline

The bundle recommender raises average order value by $1.85
(95% CI $0.92 to $2.78) per completed order in the test window.

The numbers above are illustrative and pinned; they are not asserted as a real
measured effect. The fixture exists so the gate has a live, dedicated example of
the ordinal-scale routing defect to catch.

## What is wrong

Pearson's r assumes a linear, interval-or-better scale. An ordinal operand with
more than two ordered levels calls for a monotone rank measure (Spearman's rho or
Kendall's tau-b), not Pearson r.

## Limitations

A calibration control. It carries no decision weight and reports no real finding
about any product.
