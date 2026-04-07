from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"
EXEC = UNIVERSE / "00_EXECUTIVE_DIGEST"
CANON = UNIVERSE / "00_EDITION_CANONIQUE_FINALE"
PUBLIC = UNIVERSE / "00_PUBLIC_BRIEF"


def load_json(path: Path) -> dict:
 return json.loads(path.read_text(encoding="utf-8"))


def build_public_brief(step10: dict, step9: dict) -> str:
 stats = step10.get("stats", {})
 return "\n".join(
 [
 "# PUBLIC BRIEF",
 "",
 "## Vision",
 "Le corpus a ete organise en une architecture fractale et chiastique pour rendre une masse documentaire dense plus lisible, plus navigable et plus transmissible.",
 "",
 "## Ce Qui A Ete Produit",
 "- Une structure chiastique globale de consultation.",
 "- Des versions reinterpretees de textes, JSON, PDF et manuscrits.",
 "- Un index maitre de correspondance entre sources et sorties.",
 "- Une carte visuelle et une edition canonique finale.",
 "",
 "## Chiffres Publics",
 f"- Sources uniques organisees : `{stats.get('unique_sources', 0)}`",
 f"- Entrees reliees dans l'index maitre : `{stats.get('total_entries', 0)}`",
 f"- Axe de lecture : `{' -> '.join(stats.get('chiastic_axis', []))}`",
 "",
 "## Lire En Premier",
 "- `00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md`",
 "- `00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md`",
 "- `00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md`",
 "",
 "## Usage",
 "Cette version est destinee a une lecture externe rapide: presentation, orientation, consultation ou demonstration.",
 ]
 ) + "\n"


def build_presentation(step10: dict) -> str:
 stats = step10.get("stats", {})
 return "\n".join(
 [
 "# PRESENTATION PUBLIQUE",
 "",
 "Le depot a ete replie en une forme fractale et chiastique pour transformer un ensemble documentaire complexe en parcours de lecture clair.",
 "",
 "L'architecture suit un axe simple : fondation, preuves, noyau de memoire, gouvernance, archives.",
 "",
 "En pratique, cela donne :",
 f"- `{stats.get('unique_sources', 0)}` sources organisees",
 f"- `{stats.get('total_entries', 0)}` relations tracees dans l'index maitre",
 "- un portail canonique central",
 "- une carte visuelle de navigation",
 "- une synthese executive de lecture rapide",
 "",
 "Point d'entree recommande :",
 "- `../00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md`",
 "",
 "Cette presentation est la couche la plus courte, la plus accessible et la plus directement partageable du dispositif.",
 ]
 ) + "\n"


def build_manifest(step10: dict, step9: dict) -> dict:
 return {
 "stage": "step_11_public_brief",
 "public_root": str(PUBLIC.relative_to(ROOT)).replace("\\", "/"),
 "inputs": {
 "executive_digest": "FRACTAL_CHIASTE/00_EXECUTIVE_DIGEST/manifest_step10_executive_digest.json",
 "canonical_edition": "FRACTAL_CHIASTE/00_EDITION_CANONIQUE_FINALE/manifest_step9_canonical_edition.json",
 },
 "outputs": {
 "public_brief": "FRACTAL_CHIASTE/00_PUBLIC_BRIEF/PUBLIC_BRIEF.md",
 "presentation": "FRACTAL_CHIASTE/00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md",
 "manifest": "FRACTAL_CHIASTE/00_PUBLIC_BRIEF/manifest_step11_public_brief.json",
 },
 "public_stats": {
 "unique_sources": step10.get("stats", {}).get("unique_sources", 0),
 "total_entries": step10.get("stats", {}).get("total_entries", 0),
 "chiastic_axis": step10.get("stats", {}).get("chiastic_axis", []),
 },
 }


def main() -> None:
 PUBLIC.mkdir(parents=True, exist_ok=True)
 step10 = load_json(EXEC / "manifest_step10_executive_digest.json")
 step9 = load_json(CANON / "manifest_step9_canonical_edition.json")

 (PUBLIC / "PUBLIC_BRIEF.md").write_text(
 build_public_brief(step10, step9),
 encoding="utf-8",
 )
 (PUBLIC / "PRESENTATION_PUBLIQUE.md").write_text(
 build_presentation(step10),
 encoding="utf-8",
 )
 (PUBLIC / "manifest_step11_public_brief.json").write_text(
 json.dumps(build_manifest(step10, step9), ensure_ascii=False, indent=2),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
