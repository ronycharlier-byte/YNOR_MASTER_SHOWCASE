from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"


def load_json(path: Path) -> dict:
 return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
 step7 = load_json(UNIVERSE / "manifest_step7_master_index.json")
 step14 = load_json(UNIVERSE / "00_MASTER_FINAL" / "manifest_step14_master_final.json")

 recap = "\n".join(
 [
 "# RECAPITULATION FINALE",
 "",
 "## Etat",
 "Le corpus a ete transforme en une architecture fractale et chiastique complete, reliee de la fondation jusqu'au manifeste terminal.",
 "",
 "## Chiffres Cles",
 f"- Sources uniques : `{step7.get('unique_sources', 0)}`",
 f"- Entrees unifiees : `{step7.get('total_entries', 0)}`",
 f"- Axe chiastique : `{' -> '.join(step7.get('chiastic_axis', []))}`",
 "",
 "## Niveaux Disponibles",
 "- Homepage : `00_HOMEPAGE/HOMEPAGE_DU_CORPUS.md`",
 "- Public : `00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md`",
 "- Executive : `00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md`",
 "- Canonique : `00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md`",
 "- Soumission : `00_SUBMISSION_PACK/RESUME_DE_SOUMISSION.md`",
 "- Terminal : `00_MASTER_FINAL/MASTER_FINAL.md`",
 "",
 "## Cohérence Globale",
 "- Les étapes 1 à 14 sont reliées.",
 "- Les couches publique, executive, canonique et soumission sont en place.",
 "- Les branches internes B, X, B' et A' sont peuplées et navigables.",
 "",
 "## Point D'entree Recommande",
 "- `00_MASTER_FINAL/MASTER_FINAL.md`",
 "",
 "## Centre",
 "Le centre chiastique final est maintenant la consultation unifiée : un seul point d'entree, plusieurs profondeurs de lecture, une seule arche documentaire.",
 ]
 ) + "\n"

 (UNIVERSE / "RECAPITULATION_FINALE.md").write_text(recap, encoding="utf-8")


if __name__ == "__main__":
 main()
