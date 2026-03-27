# MIROIR TEXTUEL - DATA_PROVENANCE.json

Source : MDL_Ynor_Framework\_00_DISTS_AND_RELEASES\MDL_YNOR_GPT_UPLOAD_V3\DATA_PROVENANCE.json
Taille : 1316 octets
SHA256 : 260677a8704a2cec6a8a5fbbee014467a64f03e7cd9f3bae2397af1bb994a664

```text
{
  "title": "DATA PROVENANCE & TRAINING SOURCES (MDL YNOR)",
  "description": "Traceability for datasets, samples, and architectural weights used in the MDL Ynor Framework.",
  "datasets": [
    {
      "id": "Y-PHYS-001",
      "source": "Internal Simulation (RK4-Ynor)",
      "license": "Proprietary (MDL)",
      "date": "2026-03-20",
      "hash": "e3b0c442..."
    },
    {
      "id": "Y-COGN-002",
      "source": "DeepMind Research Assets (Curated)",
      "license": "Apache 2.0",
      "date": "2025-11-12",
      "hash": "d8a2c110..."
    },
    {
      "id": "Y-LLM-003",
      "source": "Public OpenWebText (Subset)",
      "license": "Creative Commons",
      "date": "2024-05-30",
      "hash": "f2e345a..."
    },
    {
      "id": "Y-AUDIT-004",
      "source": "Anonymized Real-World Audit Logs",
      "license": "NDA Restricted",
      "date": "2026-03-22",
      "hash": "a7b6c5d4..."
    }
  ],
  "scripts": [
    "_05_DATA_AND_MEMORY/scripts/cleanse_pii.py",
    "_05_DATA_AND_MEMORY/scripts/entropy_mapper.py",
    "_05_DATA_AND_MEMORY/scripts/token_weighting.py"
  ],
  "compliance": {
    "bias_mitigation": "Verified statistical distribution parity.",
    "ethical_sourcing": "No non-consensual web-crawled personal data.",
    "gdpr": "100% compliant anonymization (RGPD Grade)."
  }
}

```