# Reproduction of "The AI Data Scientist" (arXiv:2508.18113v1, Akimov, Nwadike,
# Iklassov and Takac), Section 2.1 (Data Cleaning Subagent), Section 2.2
# (Hypothesis Subagent, Table 1) and Section 2.3 (Preprocessing Subagent,
# Table 2). Paired with
# examples/known-bad/full-frame-cleaning-ANALYSIS-SPEC.yaml (REQ-P11.1-07) and
# examples/known-bad/full-frame-cleaning-POSTMORTEM.md.
#
# Nothing in this file is ever executed by the gate: the entrypoint check
# (dsx/checks/code.py) reads it as text, and the reproducibility check
# (dsx/checks/repro.py) tests only that the declared path exists. The stages
# below are transcribed in the paper's own order — clean, form and test a
# hypothesis, split, then preprocess — because that ordering is the entire
# point of this fixture: it is the shape that passed the gate before Phase
# 11.1's DSX-CODE-020/021/030 checks existed.

import pandas as pd
import sklearn.model_selection
from scipy.stats import chi2_contingency
from sklearn.preprocessing import StandardScaler

data = pd.read_csv("bank_churn.csv")

# --- Data Cleaning Subagent (Section 2.1): "the Subagent applies imputation
# techniques such as the mean or median when missing values are relatively
# simple and randomly distributed." Full-frame, before any split.
data['Age'] = data['Age'].fillna(data['Age'].mean())

# --- Data Cleaning Subagent (Section 2.1): "the Subagent applies statistical
# checks such as z-score thresholds and interquartile range (IQR) analysis"
# to identify outliers. A spread-based row filter, also full-frame, also
# before any split.
data = data[data['Balance'] < data['Balance'].quantile(0.99)]

# --- Hypothesis Subagent (Section 2.2, Table 1): "Proportion Comparison —
# Chi-Square Test — Check if category proportions differ between groups."
less_products = data['NumOfProducts'] < 2
contingency_table = pd.crosstab(less_products, data['Exited'])
chi2, p_value, _, _ = chi2_contingency(contingency_table)

# --- a legitimate split ---
X = data.drop(columns=['Exited'])
y = data['Exited']
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
    X, y, test_size=0.2, random_state=1
)

# --- Preprocessing Subagent (Section 2.3, Table 2): "standardized_Age —
# Standardized Age using StandardScaler" — fitted on the full frame, after
# the split, instead of on X_train.
scaler = StandardScaler()
data['standardized_Age'] = scaler.fit_transform(data[['Age']])
