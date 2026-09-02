Changelog

All notable changes to this project will be documented in this file.

The format follows the principles of Keep a Changelog, and this project uses Semantic Versioning.

---

[3.1.0] - 2026-09-02

Added

- Bounded CSV parsing with UTF-8 validation and row, column, cell, and field-length limits.
- Runtime artifact SHA256 identity enforcement against the committed artifact manifest before production artifact loading.
- Adversarial tests for runtime artifact tampering and malformed or resource-abusive CSV inputs.
- CI privilege-contract validation for normal and privileged workflows.
- Deterministic model-native explainability with a linear-coefficient fallback.

Changed

- Replaced the STEP 31-B placeholder marker test with executable security contract assertions.
- Utility CSV loading now uses the same bounded parser and upload-size boundary as untrusted CSV inputs.
- Feature-importance extraction now rejects NaN and infinite values before persistence.
- Repository documentation now reflects the actual workflows, tests, scripts, and committed runtime artifacts.

Security

- Runtime prediction fails closed when any expected artifact is missing, empty, or byte-level SHA256-inconsistent with `models/artifact_manifest.json`.
- Untrusted CSV input is rejected when it exceeds configured structural or resource limits.
- Explainability artifacts cannot contain non-finite feature-importance values.

---

[3.0.0] - 2026-07-18

Added

- Initial release of the AI-Powered Cybersecurity Dashboard.
- Interactive Streamlit dashboard architecture.
- Modular project structure.
- Dashboard home page.
- Dataset Explorer module.
- Exploratory Data Analysis (EDA) dashboard.
- Cybersecurity incident prediction interface.
- Feature Importance visualization page.
- Model Performance dashboard.
- Configuration management.
- Utility functions.
- Model loading module.
- Prediction module.
- Visualization utilities.
- Logging support.
- Responsive dashboard layout.
- Downloadable prediction results.
- GitHub-ready documentation.
- MIT License.
- Production-ready project structure.

Planned

- Real-time prediction support.
- Explainable AI using SHAP.
- Interactive filtering and search.
- Authentication and user management.
- Model version management.
- REST API integration.
- Docker support.
- Cloud deployment (AWS, Azure, or Google Cloud).
- Performance monitoring dashboard.
- Dark mode support.

---

Version Summary

Version| Description
3.1.0| Security, runtime artifact integrity, bounded CSV, explainability, and CI hardening
3.0.0| Initial release of the AI-Powered Cybersecurity Dashboard

---

Notes

Version 3.1.0 documents the repository's implemented security and CI hardening. SHAP-based explainability remains planned; the current implementation uses deterministic model-native feature importance with a linear-coefficient fallback.
