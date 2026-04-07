from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"
MASTER_INDEX = UNIVERSE / "manifest_step7_master_index.json"

NODE_TITLES = {
 "01_A_FONDATION": "A | Fondation",
 "02_B_THEORIE_ET_PREUVES": "B | Theorie et preuves",
 "03_C_MOTEURS_ET_DEPLOIEMENT": "C | Moteurs et deploiement",
 "04_X_NOYAU_MEMOIRE": "X | Noyau memoire",
 "05_C_PRIME_VALIDATION_ET_TESTS": "C' | Validation et tests",
 "06_B_PRIME_GOUVERNANCE_ET_DIFFUSION": "B' | Gouvernance et diffusion",
 "07_A_PRIME_ARCHIVES_ET_RELEASES": "A' | Archives et releases",
}

NODE_ORDER = [
 "01_A_FONDATION",
 "02_B_THEORIE_ET_PREUVES",
 "03_C_MOTEURS_ET_DEPLOIEMENT",
 "04_X_NOYAU_MEMOIRE",
 "05_C_PRIME_VALIDATION_ET_TESTS",
 "06_B_PRIME_GOUVERNANCE_ET_DIFFUSION",
 "07_A_PRIME_ARCHIVES_ET_RELEASES",
]


def load_master() -> dict:
 return json.loads(MASTER_INDEX.read_text(encoding="utf-8"))


def build_mermaid(master: dict) -> str:
 node_counts = master.get("node_counts", {})
 stage_counts = master.get("stage_counts", {})
 lines = [
 "flowchart LR",
 ' A["A | Fondation\\n' + str(node_counts.get("01_A_FONDATION", 0)) + ' entrees"]',
 ' B["B | Theorie et preuves\\n' + str(node_counts.get("02_B_THEORIE_ET_PREUVES", 0)) + ' entrees"]',
 ' C["C | Moteurs et deploiement\\n' + str(node_counts.get("03_C_MOTEURS_ET_DEPLOIEMENT", 0)) + ' entrees"]',
 ' X["X | Noyau memoire\\n' + str(node_counts.get("04_X_NOYAU_MEMOIRE", 0)) + ' entrees"]',
 ' CP["C\' | Validation et tests\\n' + str(node_counts.get("05_C_PRIME_VALIDATION_ET_TESTS", 0)) + ' entrees"]',
 ' BP["B\' | Gouvernance et diffusion\\n' + str(node_counts.get("06_B_PRIME_GOUVERNANCE_ET_DIFFUSION", 0)) + ' entrees"]',
 ' AP["A\' | Archives et releases\\n' + str(node_counts.get("07_A_PRIME_ARCHIVES_ET_RELEASES", 0)) + ' entrees"]',
 "",
 " A --> B --> C --> X --> CP --> BP --> AP",
 " A -. miroir .-> AP",
 " B -. miroir .-> BP",
 " C -. miroir .-> CP",
 "",
 ' S1["Etape 1\\n' + str(stage_counts.get("step_1_curated_text", 0)) + '"] --> A',
 ' S2["Etape 2\\n' + str(stage_counts.get("step_2_bulk_text", 0)) + '"] --> B',
 ' S3["Etape 3\\n' + str(stage_counts.get("step_3_json", 0)) + '"] --> X',
 ' S4["Etape 4\\n' + str(stage_counts.get("step_4_latex_pdf", 0)) + '"] --> AP',
 ' S5["Etape 5\\n' + str(stage_counts.get("step_5_constitution_pdf", 0)) + '"] --> B',
 ' S6["Etape 6\\n' + str(stage_counts.get("step_6_legal_pdf", 0)) + '"] --> BP',
 ]
 return "\n".join(lines) + "\n"


def top_sources_for_node(master: dict, node: str, limit: int = 8) -> list[str]:
 rows = []
 for row in master.get("source_correspondence", []):
 if node in row.get("nodes", []):
 rows.append(row["source"])
 return rows[:limit]


def build_navigation_markdown(master: dict) -> str:
 lines = [
 "# CARTE VISUELLE ET PLAN CENTRAL DE NAVIGATION",
 "",
 "## Carte Mermaid",
 "```mermaid",
 build_mermaid(master).rstrip(),
 "```",
 "",
 "## Portes D'entree",
 "- A : lire la fondation textuelle et les README chiastiques.",
 "- B : entrer par les preuves, les corpus formels et les PDF constitutionnels/mathematiques.",
 "- X : entrer par la memoire et les JSON reinterpretes.",
 "- B' : entrer par les corpus juridiques, prospectus, doctrines et soumissions.",
 "- A' : entrer par les releases, manuscrits souverains et versions augmentees LaTeX/PDF.",
 "",
 "## Plan Central",
 ]

 for node in NODE_ORDER:
 title = NODE_TITLES[node]
 count = master.get("node_counts", {}).get(node, 0)
 lines.append(f"- {title} : `{count}` entrees")
 for source in top_sources_for_node(master, node):
 lines.append(f" {source}")

 lines.extend(
 [
 "",
 "## Centre",
 "Le centre chiastique de la navigation est le passage d'une source a son miroir, puis a sa branche complementaire dans l'axe A -> B -> C -> X -> C' -> B' -> A'.",
 ]
 )
 return "\n".join(lines) + "\n"


def build_navigation_json(master: dict) -> dict:
 return {
 "stage": "step_8_visual_navigation",
 "chiastic_axis": master.get("chiastic_axis", []),
 "node_titles": NODE_TITLES,
 "node_counts": master.get("node_counts", {}),
 "stage_counts": master.get("stage_counts", {}),
 "navigation": {
 node: {
 "title": NODE_TITLES[node],
 "count": master.get("node_counts", {}).get(node, 0),
 "top_sources": top_sources_for_node(master, node),
 }
 for node in NODE_ORDER
 },
 "mermaid_path": "FRACTAL_CHIASTE/CARTE_VISUELLE_FRACTALE_CHIASTIQUE.md",
 }


def main() -> None:
 master = load_master()
 md = build_navigation_markdown(master)
 navigation = build_navigation_json(master)

 (UNIVERSE / "CARTE_VISUELLE_FRACTALE_CHIASTIQUE.md").write_text(
 md,
 encoding="utf-8",
 )
 (UNIVERSE / "manifest_step8_visual_navigation.json").write_text(
 json.dumps(navigation, ensure_ascii=False, indent=2),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
