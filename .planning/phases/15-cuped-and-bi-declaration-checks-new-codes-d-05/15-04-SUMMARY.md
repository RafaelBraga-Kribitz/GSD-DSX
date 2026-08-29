---
phase: 15-cuped-and-bi-declaration-checks-new-codes-d-05
plan: 04
status: complete
requirements: [REQ-P15-02]
---

# 15-04 SUMMARY — DSX-EXP-070 CUPED post-treatment gate check + off-path arithmetic

## What shipped
- **`dsx/mathx.py`** — added `cuped_theta(cov_xy, var_x)` (θ = Cov/Var, ValueError on var_x=0) and
  `cuped_variance_reduction(rho)` (ρ², ValueError outside [-1,1]), each with a `Citation:` (Deng, Xu,
  Kohavi & Walker 2013 WSDM, DOI 10.1145/2433396.2433413) + `Reference value:` docstring pinning
  ρ=0.5 → ρ²=0.25 (variance ratio 0.75). Pure, stdlib-only, imported by no check.
- **`dsx/checks/design.py`** — imported `CUPED_COVARIATE_TIMINGS` from `..spec` (NOT the CUPED math);
  added `_check_cuped(design, spec, report)`, dispatched from the **always-run tail** of `check()` after
  `_check_identification`. Runs only when `normalize(design.variance_adjustment) == "cuped"`; fires
  **DSX-EXP-070** (CRITICAL) when `design.cuped.covariate_timing` is not `pre_experiment` (recognised
  post_treatment, unrecognised, or absent — each with an honest detail, trap #4/#11); `pre_experiment` →
  report.ok. Fixed literal message `CUPED declared with a covariate that is not pre-experiment`;
  `where="spec.design.cuped.covariate_timing"`. Computes nothing; cites Deng 2013 WSDM (not the Unified
  playbook). No GATE_THRESHOLDS/GATE_PROFILES edit.
- **`tests/test_cuped.py`** (new, `# D-05: DSX-EXP-070`) — 8 tests: the WSDM ρ²=0.25 worked value; EXP-070
  firing on post_treatment/absent/unrecognised and silence on pre_experiment / non-cuped; the **`dsx gate
  plan` exit_code 0→1 flip** over the good fixture via the real `run_checks` engine at `GATE_THRESHOLDS['plan']`;
  and design.py's non-import of the CUPED math.

## Gate evidence (all re-run by the orchestrator, brief §5)
- `python -m unittest tests.test_cuped` → 8 OK (incl. the gate-plan exit flip).
- AST verify: one `report.add` (`DSX-EXP-070`, `CRITICAL`, fixed literal); Deng Citation + Structural
  criterion docstring; dispatched from `check()`; `CUPED_COVARIATE_TIMINGS` imported; design.py names
  neither CUPED math function. `git status --porcelain -- dsx/cli.py` empty. Catalogue stale until 15-06.
