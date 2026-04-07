from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"
CANON = UNIVERSE / "00_EDITION_CANONIQUE_FINALE"
EXEC = UNIVERSE / "00_EXECUTIVE_DIGEST"


def load_json(path: Path) -> dict:
 return json.loads(path.read_text(encoding="utf-8"))


def build_executive_summary(step7: dict, step8: dict, step9: dict) -> str:
 return "\n".join(
 [
 "# EXECUTIVE DIGEST",
 "",
 "## En Une Phrase",
 "Le depot a ete replie en une architecture fractale et chiastique complete, consultable depuis un portail canonique unique.",
 "",
 "## Chiffres Cles",
 f"- Entrees unifiees : `{step7.get('total_entries', 0)}`",
 f"- Sources uniques : `{step7.get('unique_sources', 0)}`",
 f"- Axe chiastique : `{' -> '.join(step7.get('chiastic_axis', []))}`",
 f"- Noeuds actifs : `{len(step7.get('node_counts', {}))}`",
 "",
 "## Etapes Realisees",
 "- 1 : reecritures structurantes manuelles",
 "- 2 : reecriture bulk des textes majeurs",
 "- 3 : reinterpretation chiastique des JSON",
 "- 4 : editions LaTeX/PDF augmentees souveraines",
 "- 5 : projection des PDF constitutionnels et mathematiques",
 "- 6 : projection des PDF juridiques et administratifs",
 "- 7 : index maitre de correspondance",
 "- 8 : carte visuelle et navigation centrale",
 "- 9 : edition canonique finale",
 "",
 "## Portes D'entree",
 "- Fondation : README et textes de base",
 "- Theorie : corpus formels, preuves, PDF mathematiques",
 "- Memoire : JSON, connaissance, intelligence",
 "- Gouvernance : droit, doctrine, prospectus, depot",
 "- Releases : manuscrits, archives, versions augmentees",
 "",
 "## Fichiers A Lire En Premier",
 "- `00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md`",
 "- `00_EDITION_CANONIQUE_FINALE/01_DOCUMENTS_CENTRAUX/INDEX_MAITRE_FRACTAL_CHIASTIQUE.md`",
 "- `00_EDITION_CANONIQUE_FINALE/01_DOCUMENTS_CENTRAUX/CARTE_VISUELLE_FRACTALE_CHIASTIQUE.md`",
 "",
 "## Centre",
 "Le centre chiastique de cette version executive est la lisibilite immediate : rendre l'ensemble navigable en quelques minutes sans perdre la profondeur de l'architecture.",
 ]
 ) + "\n"


def build_one_page(step7: dict) -> str:
 node_counts = step7.get("node_counts", {})
 stage_counts = step7.get("stage_counts", {})
 return "\n".join(
 [
 "# FICHE UNE PAGE",
 "",
 "## Structure",
 "- A : Fondation",
 f"- B : Theorie et preuves ({node_counts.get('02_B_THEORIE_ET_PREUVES', 0)})",
 f"- X : Memoire ({node_counts.get('04_X_NOYAU_MEMOIRE', 0)})",
 f"- B' : Gouvernance et diffusion ({node_counts.get('06_B_PRIME_GOUVERNANCE_ET_DIFFUSION', 0)})",
 f"- A' : Archives et releases ({node_counts.get('07_A_PRIME_ARCHIVES_ET_RELEASES', 0)})",
 "",
 "## Volume Par Etape",
 f"- Etape 1 : {stage_counts.get('step_1_curated_text', 0)}",
 f"- Etape 2 : {stage_counts.get('step_2_bulk_text', 0)}",
 f"- Etape 3 : {stage_counts.get('step_3_json', 0)}",
 f"- Etape 4 : {stage_counts.get('step_4_latex_pdf', 0)}",
 f"- Etape 5 : {stage_counts.get('step_5_constitution_pdf', 0)}",
 f"- Etape 6 : {stage_counts.get('step_6_legal_pdf', 0)}",
 "",
 "## Lire Maintenant",
 "- Portail canonique",
 "- Index maitre",
 "- Carte visuelle",
 "",
 "## Usage",
 "Cette fiche sert de vue immediate pour un lecteur, un evaluateur ou un integrateur qui veut comprendre rapidement la forme finale du corpus.",
 ]
 ) + "\n"


def build_manifest(step7: dict, step8: dict, step9: dict) -> dict:
 return {
 "stage": "step_10_executive_digest",
 "executive_root": str(EXEC.relative_to(ROOT)).replace("\\", "/"),
 "inputs": {
 "master_index": "FRACTAL_CHIASTE/manifest_step7_master_index.json",
 "visual_navigation": "FRACTAL_CHIASTE/manifest_step8_visual_navigation.json",
 "canonical_edition": "FRACTAL_CHIASTE/00_EDITION_CANONIQUE_FINALE/manifest_step9_canonical_edition.json",
 },
 "outputs": {
 "executive_digest": "FRACTAL_CHIASTE/00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md",
 "one_page": "FRACTAL_CHIASTE/00_EXECUTIVE_DIGEST/FICHE_UNE_PAGE.md",
 "manifest": "FRACTAL_CHIASTE/00_EXECUTIVE_DIGEST/manifest_step10_executive_digest.json",
 },
 "stats": {
 "total_entries": step7.get("total_entries", 0),
 "unique_sources": step7.get("unique_sources", 0),
 "chiastic_axis": step7.get("chiastic_axis", []),
 "stage_counts": step7.get("stage_counts", {}),
 "node_counts": step7.get("node_counts", {}),
 },
 }


def main() -> None:
 EXEC.mkdir(parents=True, exist_ok=True)
 step7 = load_json(UNIVERSE / "manifest_step7_master_index.json")
 step8 = load_json(UNIVERSE / "manifest_step8_visual_navigation.json")
 step9 = load_json(CANON / "manifest_step9_canonical_edition.json")

 (EXEC / "EXECUTIVE_DIGEST.md").write_text(
 build_executive_summary(step7, step8, step9),
 encoding="utf-8",
 )
 (EXEC / "FICHE_UNE_PAGE.md").write_text(
 build_one_page(step7),
 encoding="utf-8",
 )
 (EXEC / "manifest_step10_executive_digest.json").write_text(
 json.dumps(build_manifest(step7, step8, step9), ensure_ascii=False, indent=2),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
