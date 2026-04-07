from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"
CANON = UNIVERSE / "00_EDITION_CANONIQUE_FINALE"

SOURCE_FILES = [
 UNIVERSE / "MANIFESTE_FRACTAL_CHIASTE.md",
 UNIVERSE / "manifeste_fractal_chiaste.json",
 UNIVERSE / "INDEX_MAITRE_FRACTAL_CHIASTIQUE.md",
 UNIVERSE / "manifest_step7_master_index.json",
 UNIVERSE / "CARTE_VISUELLE_FRACTALE_CHIASTIQUE.md",
 UNIVERSE / "manifest_step8_visual_navigation.json",
 UNIVERSE / "manifest_step2_bulk_rewrite.json",
 UNIVERSE / "manifest_step3_json_rewrite.json",
 UNIVERSE / "manifest_step4_pdf_latex_augmented.json",
 UNIVERSE / "manifest_step5_constitution_pdf_augmented.json",
 UNIVERSE / "manifest_step6_legal_admin_pdf_augmented.json",
]


def load_json(path: Path) -> dict:
 return json.loads(path.read_text(encoding="utf-8"))


def copy_sources() -> list[str]:
 copied = []
 for source in SOURCE_FILES:
 if not source.exists():
 continue
 target = CANON / "01_DOCUMENTS_CENTRAUX" / source.name
 target.parent.mkdir(parents=True, exist_ok=True)
 shutil.copy2(source, target)
 copied.append(str(target.relative_to(ROOT)).replace("\\", "/"))
 return copied


def build_portal(master: dict, navigation: dict, copied: list[str]) -> str:
 lines = [
 "# PORTAIL CANONIQUE FINAL",
 "",
 "Cette edition canonique rassemble les artefacts centraux des etapes 1 a 8 dans un seul point de consultation.",
 "",
 "## Noyau",
 f"- Entrees unifiees : `{master.get('total_entries', 0)}`",
 f"- Sources uniques : `{master.get('unique_sources', 0)}`",
 f"- Axe chiastique : `{' -> '.join(master.get('chiastic_axis', []))}`",
 "",
 "## Documents Cles",
 "- `01_DOCUMENTS_CENTRAUX/MANIFESTE_FRACTAL_CHIASTE.md`",
 "- `01_DOCUMENTS_CENTRAUX/INDEX_MAITRE_FRACTAL_CHIASTIQUE.md`",
 "- `01_DOCUMENTS_CENTRAUX/CARTE_VISUELLE_FRACTALE_CHIASTIQUE.md`",
 "",
 "## Navigation Rapide",
 "- A : fondation textuelle et README chiastiques.",
 "- B : preuves, corpus formels, PDF constitutionnels et mathematiques.",
 "- X : memoire, intelligence et JSON reinterpretes.",
 "- B' : droit, doctrine, prospectus et diffusion.",
 "- A' : archives, releases et editions augmentees.",
 "",
 "## Comptage Par Etape",
 ]
 for stage, count in sorted(master.get("stage_counts", {}).items()):
 lines.append(f"- {stage} : `{count}`")

 lines.extend(
 [
 "",
 "## Comptage Par Noeud",
 ]
 )
 for node, count in sorted(master.get("node_counts", {}).items()):
 label = navigation.get("node_titles", {}).get(node, node)
 lines.append(f"- {label} : `{count}`")

 lines.extend(
 [
 "",
 "## Table Canonique",
 ]
 )
 for path in copied:
 lines.append(f"- `{path}`")

 lines.extend(
 [
 "",
 "## Centre",
 "Le centre chiastique de cette edition finale est la consultation : tout converge ici pour etre lu, cartographie et transmis sans perdre l'arche source.",
 ]
 )
 return "\n".join(lines) + "\n"


def build_readme_json(master: dict, navigation: dict, copied: list[str]) -> dict:
 return {
 "stage": "step_9_canonical_edition",
 "canonical_root": str(CANON.relative_to(ROOT)).replace("\\", "/"),
 "copied_documents": copied,
 "total_entries": master.get("total_entries", 0),
 "unique_sources": master.get("unique_sources", 0),
 "chiastic_axis": master.get("chiastic_axis", []),
 "node_counts": master.get("node_counts", {}),
 "stage_counts": master.get("stage_counts", {}),
 "primary_portal": "FRACTAL_CHIASTE/00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md",
 "visual_map": "FRACTAL_CHIASTE/00_EDITION_CANONIQUE_FINALE/01_DOCUMENTS_CENTRAUX/CARTE_VISUELLE_FRACTALE_CHIASTIQUE.md",
 "master_index": "FRACTAL_CHIASTE/00_EDITION_CANONIQUE_FINALE/01_DOCUMENTS_CENTRAUX/INDEX_MAITRE_FRACTAL_CHIASTIQUE.md",
 "navigation_manifest": "FRACTAL_CHIASTE/00_EDITION_CANONIQUE_FINALE/01_DOCUMENTS_CENTRAUX/manifest_step8_visual_navigation.json",
 }


def main() -> None:
 CANON.mkdir(parents=True, exist_ok=True)
 copied = copy_sources()
 master = load_json(UNIVERSE / "manifest_step7_master_index.json")
 navigation = load_json(UNIVERSE / "manifest_step8_visual_navigation.json")

 portal = build_portal(master, navigation, copied)
 (CANON / "PORTAIL_CANONIQUE_FINAL.md").write_text(portal, encoding="utf-8")

 manifest = build_readme_json(master, navigation, copied)
 (CANON / "manifest_step9_canonical_edition.json").write_text(
 json.dumps(manifest, ensure_ascii=False, indent=2),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
