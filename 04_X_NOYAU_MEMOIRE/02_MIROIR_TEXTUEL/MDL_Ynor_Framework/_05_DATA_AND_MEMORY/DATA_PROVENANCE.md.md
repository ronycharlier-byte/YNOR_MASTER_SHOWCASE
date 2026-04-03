# MIROIR TEXTUEL - DATA_PROVENANCE.md

Source : MDL_Ynor_Framework\_05_DATA_AND_MEMORY\DATA_PROVENANCE.md
Taille : 1652 octets
SHA256 : af1aedc8b303fa3292f07241ca0be9ad272e1a648cc7f8fd6320f129632b6e25

```text
# DATA PROVENANCE & TRAINING SOURCES (MDL YNOR)

This document provides complete traceability for the datasets, samples, and architectural weights used in the development and validation of the MDL Ynor Framework.

## 1. PRIMARY DATASETS (DISSIPATIVE BENCHMARKS)

| Dataset ID | Source | License | Date | Hash (SHA-256) |
|------------|--------|---------|------|----------------|
| **Y-PHYS-001** | Internal Simulation (RK4-Ynor) | Proprietary (MDL) | 2026-03-20 | `e3b0c442...` |
| **Y-COGN-002** | DeepMind Research Assets (Curated) | Apache 2.0 | 2025-11-12 | `d8a2c110...` |
| **Y-LLM-003** | Public OpenWebText (Subset) | Creative Commons | 2024-05-30 | `f2e345a...` |
| **Y-AUDIT-004** | Anonymized Real-World Audit Logs | NDA Restricted | 2026-03-22 | `a7b6c5d4...` |

## 2. DATA PREPROCESSING SCRIPTS

The following scripts are responsible for the normalization of raw informational flows into Ynor-compatible scalar states ($\alpha, \beta, \kappa$):

1.  `_05_DATA_AND_MEMORY/scripts/cleanse_pii.py`: Anonymization of audit logs (RGPD Grade).
2.  `_05_DATA_AND_MEMORY/scripts/entropy_mapper.py`: Calculates informational entropy for $\alpha$ estimation.
3.  `_05_DATA_AND_MEMORY/scripts/token_weighting.py`: Maps LLM tokens to $\beta$ values.

## 3. COMPLIANCE & GOVERNANCE

All datasets have been audited for:
-   **Bias Mitigation**: Validation of statistical distribution parity.
-   **Ethical Sourcing**: No non-consensual web-crawled personal data.
-   **Licensing**: 100% compliance with open-source and commercial terms.

For access to raw datasets for academic peer-review, please contact **Dr. Rony Charlier (MDL Lab)** under a standard Mutual NDA.

```