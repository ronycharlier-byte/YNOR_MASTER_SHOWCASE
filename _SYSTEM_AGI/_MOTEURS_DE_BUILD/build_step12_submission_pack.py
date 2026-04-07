from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"
PUBLIC = UNIVERSE / "00_PUBLIC_BRIEF"
EXEC = UNIVERSE / "00_EXECUTIVE_DIGEST"
CANON = UNIVERSE / "00_EDITION_CANONIQUE_FINALE"
PACK = UNIVERSE / "00_SUBMISSION_PACK"


def load_json(path: Path) -> dict:
 return json.loads(path.read_text(encoding="utf-8"))


def build_cover_letter(step11: dict, step10: dict, step9: dict) -> str:
 stats = step10.get("stats", {})
 return "\n".join(
 [
 "# LETTRE DE COUVERTURE",
 "",
 "Madame, Monsieur,",
 "",
 "Le present depot a ete organise en une architecture fractale et chiastique destinee a rendre un corpus dense plus lisible, plus navigable et plus transmissible.",
 "",
 "La livraison comprend :",
 "- une couche publique de presentation,",
 "- une couche executive de synthese rapide,",
 "- une edition canonique finale de consultation,",
 "- un index maitre et une carte visuelle de navigation,",
 "- des projections fractales et chiastiques des textes, JSON, PDF et manuscrits sources.",
 "",
 "Ordre de grandeur de la livraison :",
 f"- sources uniques organisees : `{stats.get('unique_sources', 0)}`",
 f"- relations documentees dans l'index maitre : `{stats.get('total_entries', 0)}`",
 f"- axe de lecture : `{' -> '.join(stats.get('chiastic_axis', []))}`",
 "",
 "Point d'entree recommande :",
 "- `../00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md`",
 "- `../00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md`",
 "- `../00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md`",
 "",
 "Cette soumission est concue pour permettre une lecture rapide a l'exterieur, tout en conservant une profondeur documentaire complete pour l'examen detaille.",
 "",
 "Veuillez recevoir l'expression de ma consideration distinguee.",
 ]
 ) + "\n"


def build_submission_summary(step11: dict, step10: dict, step9: dict) -> str:
 stats = step10.get("stats", {})
 return "\n".join(
 [
 "# RESUME DE SOUMISSION",
 "",
 "## Objet",
 "Presentation et remise d'un corpus restructure en architecture fractale et chiastique.",
 "",
 "## Contenu",
 "- Presentation publique courte",
 "- Digest executif",
 "- Portail canonique final",
 "- Index maitre",
 "- Carte visuelle de navigation",
 "- Manifests des etapes 2 a 11",
 "",
 "## Chiffres",
 f"- Sources uniques : `{stats.get('unique_sources', 0)}`",
 f"- Entrees indexees : `{stats.get('total_entries', 0)}`",
 f"- Etapes realisees : `{len(stats.get('stage_counts', {}))}`",
 "",
 "## Ordre De Lecture Recommande",
 "1. Presentation publique",
 "2. Executive digest",
 "3. Portail canonique",
 "4. Index maitre",
 "5. Carte visuelle",
 "",
 "## Finalite",
 "Offrir une structure de consultation, de demonstration, d'analyse et de transmission plus stable que la dispersion documentaire initiale.",
 ]
 ) + "\n"


def build_delivery_map(step11: dict, step10: dict, step9: dict) -> str:
 return "\n".join(
 [
 "# STRUCTURE DE LIVRAISON",
 "",
 "## Niveaux",
 "- Niveau 1 : `../00_PUBLIC_BRIEF`",
 "- Niveau 2 : `../00_EXECUTIVE_DIGEST`",
 "- Niveau 3 : `../00_EDITION_CANONIQUE_FINALE`",
 "- Niveau 4 : `../01_A_FONDATION` a `../07_A_PRIME_ARCHIVES_ET_RELEASES`",
 "",
 "## Fichiers De Reference",
 "- `../00_PUBLIC_BRIEF/PUBLIC_BRIEF.md`",
 "- `../00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md`",
 "- `../00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md`",
 "- `../00_EXECUTIVE_DIGEST/FICHE_UNE_PAGE.md`",
 "- `../00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md`",
 "- `../00_EDITION_CANONIQUE_FINALE/01_DOCUMENTS_CENTRAUX/INDEX_MAITRE_FRACTAL_CHIASTIQUE.md`",
 "- `../00_EDITION_CANONIQUE_FINALE/01_DOCUMENTS_CENTRAUX/CARTE_VISUELLE_FRACTALE_CHIASTIQUE.md`",
 "",
 "## Usage",
 "Cette structure permet une remise graduelle: lecture externe, lecture executive, puis audit canonique complet.",
 ]
 ) + "\n"


def build_manifest(step11: dict, step10: dict, step9: dict) -> dict:
 return {
 "stage": "step_12_submission_pack",
 "submission_root": str(PACK.relative_to(ROOT)).replace("\\", "/"),
 "inputs": {
 "public_brief": "FRACTAL_CHIASTE/00_PUBLIC_BRIEF/manifest_step11_public_brief.json",
 "executive_digest": "FRACTAL_CHIASTE/00_EXECUTIVE_DIGEST/manifest_step10_executive_digest.json",
 "canonical_edition": "FRACTAL_CHIASTE/00_EDITION_CANONIQUE_FINALE/manifest_step9_canonical_edition.json",
 },
 "outputs": {
 "cover_letter": "FRACTAL_CHIASTE/00_SUBMISSION_PACK/LETTRE_DE_COUVERTURE.md",
 "submission_summary": "FRACTAL_CHIASTE/00_SUBMISSION_PACK/RESUME_DE_SOUMISSION.md",
 "delivery_map": "FRACTAL_CHIASTE/00_SUBMISSION_PACK/STRUCTURE_DE_LIVRAISON.md",
 "manifest": "FRACTAL_CHIASTE/00_SUBMISSION_PACK/manifest_step12_submission_pack.json",
 },
 "stats": step10.get("stats", {}),
 }


def main() -> None:
 PACK.mkdir(parents=True, exist_ok=True)
 step11 = load_json(PUBLIC / "manifest_step11_public_brief.json")
 step10 = load_json(EXEC / "manifest_step10_executive_digest.json")
 step9 = load_json(CANON / "manifest_step9_canonical_edition.json")

 (PACK / "LETTRE_DE_COUVERTURE.md").write_text(
 build_cover_letter(step11, step10, step9),
 encoding="utf-8",
 )
 (PACK / "RESUME_DE_SOUMISSION.md").write_text(
 build_submission_summary(step11, step10, step9),
 encoding="utf-8",
 )
 (PACK / "STRUCTURE_DE_LIVRAISON.md").write_text(
 build_delivery_map(step11, step10, step9),
 encoding="utf-8",
 )
 (PACK / "manifest_step12_submission_pack.json").write_text(
 json.dumps(build_manifest(step11, step10, step9), ensure_ascii=False, indent=2),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
