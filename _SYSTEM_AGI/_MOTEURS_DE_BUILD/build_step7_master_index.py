from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"

MANIFEST_FILES = [
 UNIVERSE / "manifeste_fractal_chiaste.json",
 UNIVERSE / "manifest_step2_bulk_rewrite.json",
 UNIVERSE / "manifest_step3_json_rewrite.json",
 UNIVERSE / "manifest_step4_pdf_latex_augmented.json",
 UNIVERSE / "manifest_step5_constitution_pdf_augmented.json",
 UNIVERSE / "manifest_step6_legal_admin_pdf_augmented.json",
]

STEP1_ENTRIES = [
 {
 "source": "README.md",
 "node": "01_A_FONDATION",
 "output": "FRACTAL_CHIASTE/01_A_FONDATION/05_REECRITURE_CHIASTIQUE/README_RACINE_FRACTAL_CHIASTIQUE.md",
 },
 {
 "source": "MDL_Ynor_Framework/README.md",
 "node": "01_A_FONDATION",
 "output": "FRACTAL_CHIASTE/01_A_FONDATION/05_REECRITURE_CHIASTIQUE/README_FRAMEWORK_FRACTAL_CHIASTIQUE.md",
 },
 {
 "source": "MDL_Ynor_Framework/YNOR_FULL_CORPUS_FORMAL_SPEC_V2.3.md",
 "node": "02_B_THEORIE_ET_PREUVES",
 "output": "FRACTAL_CHIASTE/02_B_THEORIE_ET_PREUVES/05_REECRITURE_CHIASTIQUE/YNOR_FULL_CORPUS_FORMAL_SPEC_V2_3_FRACTAL_CHIASTIQUE.md",
 },
 {
 "source": "_RELEASES/GOLDEN_MASTER_PHASE_III/Sovereign_Scientific_White_Paper_v3.md",
 "node": "02_B_THEORIE_ET_PREUVES",
 "output": "FRACTAL_CHIASTE/02_B_THEORIE_ET_PREUVES/05_REECRITURE_CHIASTIQUE/SOVEREIGN_SCIENTIFIC_WHITE_PAPER_V3_FRACTAL_CHIASTIQUE.md",
 },
 {
 "source": "_SUBMISSIONS/SUBMISSION_CHECKLIST.md",
 "node": "06_B_PRIME_GOUVERNANCE_ET_DIFFUSION",
 "output": "FRACTAL_CHIASTE/06_B_PRIME_GOUVERNANCE_ET_DIFFUSION/05_REECRITURE_CHIASTIQUE/SUBMISSION_CHECKLIST_FRACTAL_CHIASTIQUE.md",
 },
 {
 "source": "_RELEASES/GOLDEN_MASTER_PHASE_III/SOVEREIGN_MASTER_PROMPT_V3.txt",
 "node": "07_A_PRIME_ARCHIVES_ET_RELEASES",
 "output": "FRACTAL_CHIASTE/07_A_PRIME_ARCHIVES_ET_RELEASES/05_REECRITURE_CHIASTIQUE/SOVEREIGN_MASTER_PROMPT_V3_FRACTAL_CHIASTIQUE.md",
 },
]

NODE_LABELS = {
 "01_A_FONDATION": "A",
 "02_B_THEORIE_ET_PREUVES": "B",
 "03_C_MOTEURS_ET_DEPLOIEMENT": "C",
 "04_X_NOYAU_MEMOIRE": "X",
 "05_C_PRIME_VALIDATION_ET_TESTS": "C'",
 "06_B_PRIME_GOUVERNANCE_ET_DIFFUSION": "B'",
 "07_A_PRIME_ARCHIVES_ET_RELEASES": "A'",
}


def load_json(path: Path):
 if not path.exists():
 return None
 return json.loads(path.read_text(encoding="utf-8"))


def infer_node_from_path(path_str: str) -> str:
 normalized = path_str.replace("\\", "/")
 for node in NODE_LABELS:
 if f"/{node}/" in f"/{normalized}/":
 return node
 return "04_X_NOYAU_MEMOIRE"


def register_entry(table: list[dict], source: str, stage: str, node: str, outputs: list[str], mode: str | None = None, family: str | None = None) -> None:
 table.append(
 {
 "source": source.replace("\\", "/"),
 "stage": stage,
 "node": node,
 "chiastic_symbol": NODE_LABELS.get(node, "X"),
 "outputs": [output.replace("\\", "/") for output in outputs],
 "mode": mode,
 "family": family,
 }
 )


def build_master_index() -> dict:
 entries: list[dict] = []
 stage_counts: Counter = Counter()
 node_counts: Counter = Counter()
 family_counts: Counter = Counter()
 source_to_entries: defaultdict[str, list[dict]] = defaultdict(list)

 base_manifest = load_json(MANIFEST_FILES[0]) or {}
 for item in base_manifest.get("items", []):
 source = item.get("source", "")
 implanted = item.get("implanted_path")
 mirror = item.get("mirror_path")
 node = item.get("node", infer_node_from_path(implanted or mirror or source))
 register_entry(entries, source, "base_universe", node, [p for p in [implanted, mirror] if p])

 for item in STEP1_ENTRIES:
 register_entry(
 entries,
 item["source"],
 "step_1_curated_text",
 item["node"],
 [item["output"]],
 )

 step2_manifest = load_json(MANIFEST_FILES[1]) or {}
 for item in step2_manifest.get("items", []):
 rewrite = item.get("rewrite") or item.get("output")
 source = item.get("source", "")
 node = infer_node_from_path(rewrite or source)
 register_entry(entries, source, "step_2_bulk_text", node, [rewrite] if rewrite else [])

 step3_manifest = load_json(MANIFEST_FILES[2]) or {}
 for item in step3_manifest.get("items", []):
 rewrite = item.get("rewrite")
 source = item.get("source", "")
 node = item.get("node") or infer_node_from_path(rewrite or source)
 register_entry(entries, source, "step_3_json", node, [rewrite] if rewrite else [], mode=item.get("mode"))

 step4_manifest = load_json(MANIFEST_FILES[3]) or {}
 for item in step4_manifest.get("items", []):
 source = item.get("source", "")
 tex = item.get("augmented_tex")
 pdf = item.get("companion_pdf")
 node = infer_node_from_path(tex or pdf or source)
 register_entry(entries, source, "step_4_latex_pdf", node, [p for p in [tex, pdf] if p])

 step5_manifest = load_json(MANIFEST_FILES[4]) or {}
 for item in step5_manifest.get("items", []):
 source = item.get("source", "")
 md = item.get("markdown_rewrite")
 pdf = item.get("companion_pdf")
 node = infer_node_from_path(md or pdf or source)
 register_entry(entries, source, "step_5_constitution_pdf", node, [p for p in [md, pdf] if p], family=item.get("family"))

 step6_manifest = load_json(MANIFEST_FILES[5]) or {}
 for item in step6_manifest.get("items", []):
 source = item.get("source", "")
 md = item.get("markdown_rewrite")
 pdf = item.get("companion_pdf")
 node = infer_node_from_path(md or pdf or source)
 register_entry(entries, source, "step_6_legal_pdf", node, [p for p in [md, pdf] if p], family=item.get("family"))

 for entry in entries:
 stage_counts[entry["stage"]] += 1
 node_counts[entry["node"]] += 1
 if entry.get("family"):
 family_counts[entry["family"]] += 1
 source_to_entries[entry["source"]].append(entry)

 source_correspondence = []
 for source, linked_entries in sorted(source_to_entries.items()):
 source_correspondence.append(
 {
 "source": source,
 "stages": [entry["stage"] for entry in linked_entries],
 "nodes": sorted({entry["node"] for entry in linked_entries}),
 "outputs": [output for entry in linked_entries for output in entry["outputs"]],
 }
 )

 return {
 "stage": "step_7_master_index",
 "chiastic_axis": ["A", "B", "C", "X", "C'", "B'", "A'"],
 "node_labels": NODE_LABELS,
 "total_entries": len(entries),
 "unique_sources": len(source_to_entries),
 "stage_counts": dict(stage_counts),
 "node_counts": dict(node_counts),
 "family_counts": dict(family_counts),
 "entries": entries,
 "source_correspondence": source_correspondence,
 }


def build_markdown(master: dict) -> str:
 lines = [
 "# INDEX MAITRE FRACTAL ET CHIASTIQUE",
 "",
 "Axe chiastique global : A -> B -> C -> X -> C' -> B' -> A'",
 "",
 "## Vue D'ensemble",
 f"- Entrees totales : `{master['total_entries']}`",
 f"- Sources uniques : `{master['unique_sources']}`",
 "",
 "## Comptage Par Etape",
 ]
 for stage, count in sorted(master["stage_counts"].items()):
 lines.append(f"- {stage} : `{count}`")

 lines.extend(
 [
 "",
 "## Comptage Par Noeud",
 ]
 )
 for node, count in sorted(master["node_counts"].items()):
 symbol = master["node_labels"].get(node, "X")
 lines.append(f"- {symbol} | {node} : `{count}`")

 if master["family_counts"]:
 lines.extend(
 [
 "",
 "## Comptage Par Famille",
 ]
 )
 for family, count in sorted(master["family_counts"].items()):
 lines.append(f"- {family} : `{count}`")

 lines.extend(
 [
 "",
 "## Table Centrale Des Correspondances",
 ]
 )
 for row in master["source_correspondence"][:80]:
 stages = ", ".join(row["stages"])
 nodes = ", ".join(row["nodes"])
 lines.append(f"- Source : `{row['source']}`")
 lines.append(f" Stages : {stages}")
 lines.append(f" Noeuds : {nodes}")
 if row["outputs"]:
 lines.append(f" Sorties : {row['outputs'][0]}")

 lines.extend(
 [
 "",
 "## Centre",
 "Le centre chiastique de l'index maitre est la correspondance : chaque source retrouve sa place, son miroir et sa fermeture dans l'arche.",
 ]
 )
 return "\n".join(lines) + "\n"


def main() -> None:
 master = build_master_index()
 (UNIVERSE / "manifest_step7_master_index.json").write_text(
 json.dumps(master, ensure_ascii=False, indent=2),
 encoding="utf-8",
 )
 (UNIVERSE / "INDEX_MAITRE_FRACTAL_CHIASTIQUE.md").write_text(
 build_markdown(master),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
