from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"
MASTER_FINAL = UNIVERSE / "00_MASTER_FINAL"

STEP_MANIFESTS = {
 "step_7_master_index": UNIVERSE / "manifest_step7_master_index.json",
 "step_8_visual_navigation": UNIVERSE / "manifest_step8_visual_navigation.json",
 "step_9_canonical_edition": UNIVERSE / "00_EDITION_CANONIQUE_FINALE" / "manifest_step9_canonical_edition.json",
 "step_10_executive_digest": UNIVERSE / "00_EXECUTIVE_DIGEST" / "manifest_step10_executive_digest.json",
 "step_11_public_brief": UNIVERSE / "00_PUBLIC_BRIEF" / "manifest_step11_public_brief.json",
 "step_12_submission_pack": UNIVERSE / "00_SUBMISSION_PACK" / "manifest_step12_submission_pack.json",
 "step_13_homepage": UNIVERSE / "00_HOMEPAGE" / "manifest_step13_homepage.json",
}


def load_json(path: Path) -> dict:
 return json.loads(path.read_text(encoding="utf-8"))


def build_terminal_portal(step7: dict, manifests: dict[str, dict]) -> str:
 return "\n".join(
 [
 "# MASTER FINAL",
 "",
 "## Statut",
 "Cette page ferme la chaine complete des etapes 1 a 13 et sert de point d'entree terminal unique.",
 "",
 "## Totaux",
 f"- Sources uniques : `{step7.get('unique_sources', 0)}`",
 f"- Entrees unifiees : `{step7.get('total_entries', 0)}`",
 f"- Axe chiastique : `{' -> '.join(step7.get('chiastic_axis', []))}`",
 "",
 "## Parcours Integral",
 "1. Homepage",
 "2. Public brief",
 "3. Executive digest",
 "4. Edition canonique",
 "5. Submission pack",
 "6. Branches fractales internes",
 "",
 "## Points D'entree Absolus",
 "- `../00_HOMEPAGE/HOMEPAGE_DU_CORPUS.md`",
 "- `../00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md`",
 "- `../00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md`",
 "- `../00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md`",
 "- `../00_SUBMISSION_PACK/RESUME_DE_SOUMISSION.md`",
 "",
 "## Etapes Referencees",
 ]
 + [f"- {name}" for name in STEP_MANIFESTS]
 + [
 "",
 "## Centre",
 "Le centre chiastique du master final est la fermeture: toutes les couches convergent en un seul point de consultation, de preuve et de transmission.",
 ]
 ) + "\n"


def build_terminal_manifest(step7: dict, loaded: dict[str, dict]) -> dict:
 return {
 "stage": "step_14_master_final",
 "master_final_root": str(MASTER_FINAL.relative_to(ROOT)).replace("\\", "/"),
 "stats": {
 "unique_sources": step7.get("unique_sources", 0),
 "total_entries": step7.get("total_entries", 0),
 "chiastic_axis": step7.get("chiastic_axis", []),
 "stage_counts": step7.get("stage_counts", {}),
 "node_counts": step7.get("node_counts", {}),
 },
 "linked_steps": {
 name: str(path.relative_to(ROOT)).replace("\\", "/")
 for name, path in STEP_MANIFESTS.items()
 },
 "primary_entrypoints": {
 "homepage": "FRACTAL_CHIASTE/00_HOMEPAGE/HOMEPAGE_DU_CORPUS.md",
 "public_brief": "FRACTAL_CHIASTE/00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md",
 "executive_digest": "FRACTAL_CHIASTE/00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md",
 "canonical_portal": "FRACTAL_CHIASTE/00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md",
 "submission_summary": "FRACTAL_CHIASTE/00_SUBMISSION_PACK/RESUME_DE_SOUMISSION.md",
 "master_final": "FRACTAL_CHIASTE/00_MASTER_FINAL/MASTER_FINAL.md",
 },
 }


def main() -> None:
 MASTER_FINAL.mkdir(parents=True, exist_ok=True)
 step7 = load_json(UNIVERSE / "manifest_step7_master_index.json")
 loaded = {name: load_json(path) for name, path in STEP_MANIFESTS.items()}

 (MASTER_FINAL / "MASTER_FINAL.md").write_text(
 build_terminal_portal(step7, loaded),
 encoding="utf-8",
 )
 (MASTER_FINAL / "manifest_step14_master_final.json").write_text(
 json.dumps(build_terminal_manifest(step7, loaded), ensure_ascii=False, indent=2),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
