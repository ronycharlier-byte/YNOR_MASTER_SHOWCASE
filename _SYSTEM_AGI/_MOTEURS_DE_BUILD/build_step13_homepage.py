from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"
PUBLIC = UNIVERSE / "00_PUBLIC_BRIEF"
EXEC = UNIVERSE / "00_EXECUTIVE_DIGEST"
CANON = UNIVERSE / "00_EDITION_CANONIQUE_FINALE"
SUBMISSION = UNIVERSE / "00_SUBMISSION_PACK"
HOMEPAGE = UNIVERSE / "00_HOMEPAGE"


def load_json(path: Path) -> dict:
 return json.loads(path.read_text(encoding="utf-8"))


def build_homepage(step7: dict) -> str:
 stats = {
 "entries": step7.get("total_entries", 0),
 "sources": step7.get("unique_sources", 0),
 "axis": " -> ".join(step7.get("chiastic_axis", [])),
 }
 return "\n".join(
 [
 "# HOMEPAGE DU CORPUS",
 "",
 "## Vision",
 "Bienvenue dans la version fractale et chiastique du corpus. Cette page sert de porte d'entree principale pour parcourir l'ensemble sans se perdre dans la masse documentaire.",
 "",
 "## En Bref",
 f"- Sources organisees : `{stats['sources']}`",
 f"- Relations indexees : `{stats['entries']}`",
 f"- Axe chiastique : `{stats['axis']}`",
 "",
 "## Parcours Recommande",
 "1. Lire la presentation publique pour comprendre l'intention generale.",
 "2. Ouvrir le digest executif pour une vue rapide des couches.",
 "3. Entrer dans le portail canonique pour la navigation complete.",
 "4. Utiliser l'index maitre et la carte visuelle pour explorer en profondeur.",
 "",
 "## Portes D'entree",
 "- Public : `../00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md`",
 "- Executive : `../00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md`",
 "- Canonique : `../00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md`",
 "- Soumission : `../00_SUBMISSION_PACK/RESUME_DE_SOUMISSION.md`",
 "",
 "## Branches",
 "- A : fondation et textes d'ouverture",
 "- B : theorie, preuves, corpus formels et PDF mathematiques",
 "- X : memoire, intelligence, JSON reinterpretes",
 "- B' : gouvernance, juridique, prospectus, doctrine",
 "- A' : archives, releases, manuscrits et editions augmentees",
 "",
 "## Lire Maintenant",
 "- `../00_PUBLIC_BRIEF/PUBLIC_BRIEF.md`",
 "- `../00_EXECUTIVE_DIGEST/FICHE_UNE_PAGE.md`",
 "- `../00_EDITION_CANONIQUE_FINALE/01_DOCUMENTS_CENTRAUX/CARTE_VISUELLE_FRACTALE_CHIASTIQUE.md`",
 "- `../00_SUBMISSION_PACK/STRUCTURE_DE_LIVRAISON.md`",
 "",
 "## Centre",
 "Le centre chiastique de cette homepage est l'orientation : permettre a tout lecteur de savoir ou entrer, quoi lire et comment descendre dans la profondeur du corpus.",
 ]
 ) + "\n"


def build_sitemap() -> str:
 return "\n".join(
 [
 "# SITE MAP",
 "",
 "- `00_HOMEPAGE/HOMEPAGE_DU_CORPUS.md`",
 "- `00_HOMEPAGE/SITE_MAP.md`",
 "- `00_PUBLIC_BRIEF/`",
 "- `00_EXECUTIVE_DIGEST/`",
 "- `00_EDITION_CANONIQUE_FINALE/`",
 "- `00_SUBMISSION_PACK/`",
 "- `01_A_FONDATION/`",
 "- `02_B_THEORIE_ET_PREUVES/`",
 "- `03_C_MOTEURS_ET_DEPLOIEMENT/`",
 "- `04_X_NOYAU_MEMOIRE/`",
 "- `05_C_PRIME_VALIDATION_ET_TESTS/`",
 "- `06_B_PRIME_GOUVERNANCE_ET_DIFFUSION/`",
 "- `07_A_PRIME_ARCHIVES_ET_RELEASES/`",
 ]
 ) + "\n"


def build_manifest(step7: dict) -> dict:
 return {
 "stage": "step_13_homepage",
 "homepage_root": str(HOMEPAGE.relative_to(ROOT)).replace("\\", "/"),
 "inputs": {
 "master_index": "FRACTAL_CHIASTE/manifest_step7_master_index.json",
 "public_brief": "FRACTAL_CHIASTE/00_PUBLIC_BRIEF/manifest_step11_public_brief.json",
 "executive_digest": "FRACTAL_CHIASTE/00_EXECUTIVE_DIGEST/manifest_step10_executive_digest.json",
 "canonical_edition": "FRACTAL_CHIASTE/00_EDITION_CANONIQUE_FINALE/manifest_step9_canonical_edition.json",
 "submission_pack": "FRACTAL_CHIASTE/00_SUBMISSION_PACK/manifest_step12_submission_pack.json",
 },
 "outputs": {
 "homepage": "FRACTAL_CHIASTE/00_HOMEPAGE/HOMEPAGE_DU_CORPUS.md",
 "site_map": "FRACTAL_CHIASTE/00_HOMEPAGE/SITE_MAP.md",
 "manifest": "FRACTAL_CHIASTE/00_HOMEPAGE/manifest_step13_homepage.json",
 },
 "stats": {
 "total_entries": step7.get("total_entries", 0),
 "unique_sources": step7.get("unique_sources", 0),
 "chiastic_axis": step7.get("chiastic_axis", []),
 },
 }


def main() -> None:
 HOMEPAGE.mkdir(parents=True, exist_ok=True)
 step7 = load_json(UNIVERSE / "manifest_step7_master_index.json")

 (HOMEPAGE / "HOMEPAGE_DU_CORPUS.md").write_text(
 build_homepage(step7),
 encoding="utf-8",
 )
 (HOMEPAGE / "SITE_MAP.md").write_text(
 build_sitemap(),
 encoding="utf-8",
 )
 (HOMEPAGE / "manifest_step13_homepage.json").write_text(
 json.dumps(build_manifest(step7), ensure_ascii=False, indent=2),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
