# STEP 20 — Model Explainability + Feature Importance

## Objective
Add a reproducible explainability layer to the cybersecurity dashboard so model predictions can be interpreted and the most influential features can be inspected.

## Scope
- Document the explainability contract and expected outputs.
- Keep explainability deterministic and compatible with the existing CI pipeline.
- Prefer model-native feature importance when available, with a documented fallback for supported estimators.
- Expose feature names and importance values in a machine-readable format for dashboard integration.

## Validation
STEP 20 must preserve the existing application/test behavior and keep GitHub Actions CI green.
