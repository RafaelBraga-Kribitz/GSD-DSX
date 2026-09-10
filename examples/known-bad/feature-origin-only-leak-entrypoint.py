# Paired entrypoint for feature-origin-only-leak-ANALYSIS-SPEC.yaml (Phase 27).
# Nothing here is ever executed by the gate: the entrypoint check
# (dsx/checks/code.py) reads it as text; the reproducibility check tests only
# that the declared path exists.
#
# This entrypoint is DELIBERATELY CLEAN. It performs a temporal split, fits the
# whole pipeline on the training fold only, and never forms or tests a hypothesis
# against the target before the split. There is no full-frame imputation, no
# scaler fitted on the full frame after the split, and no statistical test that
# references the target before the split — so none of DSX-CODE-020/021/030 has
# anything to match. The defect this fixture measures does not live in this file's
# text at all: it lives in how `account_health_index` was constructed upstream
# (recomputed nightly from activity that includes the outcome window), which no
# scan of the entrypoint source can see.

import pandas as pd
import lightgbm
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Pre-joined warehouse extract: one row per account per nightly as-of date, with
# the outcome label `churned_90d` already attached by the upstream join.
data = pd.read_csv("account_churn_features.csv", parse_dates=["as_of_date"])
data = data.sort_values("as_of_date").reset_index(drop=True)

feature_cols = [
    "tenure_days",
    "plan_tier",
    "monthly_charges",
    "support_ticket_count",
    "num_logins_30d",
    "account_health_index",
    "region",
]

# --- temporal split (declared train_period strictly before test_period): the
#     last fold of a forward-chaining TimeSeriesSplit holds out the most recent
#     rows, so no future row ever lands in training. The split precedes the fit. ---
splitter = TimeSeriesSplit(n_splits=5)
train_idx, test_idx = list(splitter.split(data))[-1]
train, test = data.iloc[train_idx], data.iloc[test_idx]

X_train, y_train = train[feature_cols], train["churned_90d"]
X_test, y_test = test[feature_cols], test["churned_90d"]

# --- pipeline fitted on the training fold only (scaler included in the pipeline,
#     so its statistics are learned from X_train alone, never the full frame) ---
pipeline = Pipeline(
    [
        ("scale", StandardScaler()),
        ("model", lightgbm.LGBMClassifier(random_state=42)),
    ]
)
pipeline.fit(X_train, y_train)

train_score = pipeline.score(X_train, y_train)
test_score = pipeline.score(X_test, y_test)
