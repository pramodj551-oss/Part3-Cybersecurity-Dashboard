# STEP 31-B — CSV/Input Resource-Abuse Security

Implemented on `feature/step31b-csv-resource-abuse`.

Security boundary: upload byte-size check → bounded strict CSV parser → DataFrame → prediction schema/numeric validation → preprocessing → model.

Guardrails: 100 MB upload size, 100,000 data rows, 100 columns, 1,000,000 cells, and 1,000,000-character field/name limit. Strict UTF-8 with BOM support, strict CSV quoting, duplicate/inconsistent columns rejection, and safe parser errors are covered by adversarial tests.
