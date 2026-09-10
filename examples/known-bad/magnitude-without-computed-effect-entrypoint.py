# Paired entrypoint for magnitude-without-computed-effect-ANALYSIS-SPEC.yaml
# (Phase 28 known-bad corpus fixture). Nothing here is ever executed by the gate:
# the entrypoint check (dsx/checks/code.py) reads it as text; the reproducibility
# check (DSX-REP-030/031) tests only that the declared path resolves. No CSV is
# required.
#
# This is a plain descriptive-statistics readout: it groups the book of customers by
# how many products they hold and reports each group's churn share and two other
# metrics over the 2026-Q2 window. There is NO model, NO train/test split, NO scaler,
# and NO statistical test that references an outcome before a split — so none of the
# code-defect idioms DSX-CODE-020/021/030 scans for have anything to match.
#
# The defect this fixture measures does not live in this file's text. It lives in the
# spec's claim: a churn magnitude (27% vs 18%) is quoted for a metric NO results.tests
# entry computes; the two computed tests are on OTHER metrics (revenue_per_user and
# activation_rate) whose reported effects happen to coincide with 27 and 18 via the
# 100x proportion bridge, so the numeric-overlap gate (DSX-CLM-033) clears on its full
# union-membership logic while nothing verifies that any test measured churn.

import pandas as pd

# Observational warehouse extract: one row per customer, 2026-Q2, with the products
# held, the churn flag, and the two computed metrics already joined upstream.
book = pd.read_csv("book_2026q2.csv")

book["few_products"] = book["products_held"] < 2

# --- descriptive churn share by product-holding segment (the claim's headline) ---
churn_by_segment = book.groupby("few_products")["churned"].mean()

# --- the two metrics that were actually tested, reported for the record ---
revenue_per_user = book["revenue_per_user"].mean()
activation_rate = book["activated"].mean()

summary = {
    "n_customers": int(len(book)),
    "churn_few_products": float(churn_by_segment.get(True, float("nan"))),
    "churn_rest": float(churn_by_segment.get(False, float("nan"))),
    "revenue_per_user": float(revenue_per_user),
    "activation_rate": float(activation_rate),
}

print(summary)
