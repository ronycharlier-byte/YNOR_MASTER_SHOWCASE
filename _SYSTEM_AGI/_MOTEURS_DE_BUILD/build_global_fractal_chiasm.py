from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "FRACTAL_CHIASTE"

TEXT_EXTENSIONS = {
 ".md",
 ".txt",
 ".json",
 ".yaml",
 ".yml",
 ".toml",
 ".py",
 ".ps1",
 ".bat",
 ".sh",
 ".tex",
 ".html",
 ".css",
 ".js",
 ".ts",
 ".tsx",
 ".jsx",
 ".xml",
 ".csv",
 ".gitignore",
 ".env",
 ".template",
}

NODES = [
 {
 "order": "01",
 "key": "A",
 "title": "FONDATION",
 "mirror": "A_PRIME",
 "role": "Ouverture, configuration, cadre initial",
 "paths": [
 "README.md",
 "MDL_Ynor_Framework/.env",
 "MDL_Ynor_Framework/.env.template",
 "MDL_Ynor_Framework/.gitignore",
 "MDL_Ynor_Framework/docker-compose.yml",
 "MDL_Ynor_Framework/Dockerfile",
 "MDL_Ynor_Framework/environment.yml",
 "MDL_Ynor_Framework/pyproject.toml",
 "MDL_Ynor_Framework/README.md",
 "MDL_Ynor_Framework/requirements.txt",
 "MDL_Ynor_Framework/uv.lock",
 "MDL_Ynor_Framework/YNOR_FULL_CORPUS_FORMAL_SPEC_V2.3.md",
 "MDL_Ynor_Framework/YNOR_FULL_CORPUS_FORMAL_SPEC_V2.3.pdf",
 "MDL Ynor Constitution",
 ],
 },
 {
 "order": "02",
 "key": "B",
 "title": "THEORIE_ET_PREUVES",
 "mirror": "B_PRIME",
 "role": "Developpement theorique et preuve formelle",
 "paths": [
 "MDL_Ynor_Framework/_01_THEORY_AND_PAPERS",
 "MDL_Ynor_Framework/_02_RESEARCH_GRAPHS",
 "MDL_Ynor_Framework/_PREUVES_ET_RAPPORTS",
 "_RELEASES/GOLDEN_MASTER_PHASE_III",
 "_RELEASES/GOLDEN_MASTER_PHASE_III_SOUVERAINE",
 ],
 },
 {
 "order": "03",
 "key": "C",
 "title": "MOTEURS_ET_DEPLOIEMENT",
 "mirror": "C_PRIME",
 "role": "Moteurs actifs, APIs et tableaux de bord",
 "paths": [
 "MDL_Ynor_Framework/_03_CORE_AGI_ENGINES",
 "MDL_Ynor_Framework/_04_DEPLOYMENT_AND_API",
 "MDL_Ynor_Framework/_06_SCRIPTS_AND_DASHBOARDS",
 "MDL_Ynor_Framework/_ASSETS_UI",
 "MDL_Ynor_Framework/.github",
 ],
 },
 {
 "order": "04",
 "key": "X",
 "title": "NOYAU_MEMOIRE",
 "mirror": "X",
 "role": "Centre chiastique de connaissance, memoire et intelligence",
 "paths": [
 "MDL_Ynor_Framework/_05_DATA_AND_MEMORY",
 "MDL_Ynor_Framework/_10_YNOR_AI_KNOWLEDGE_BASE_SOURCES",
 "MDL_Ynor_Framework/mdl_intelligence_report.json",
 "MDL_Ynor_Framework/logs",
 ],
 },
 {
 "order": "05",
 "key": "C_PRIME",
 "title": "VALIDATION_ET_TESTS",
 "mirror": "C",
 "role": "Retour miroir par validation, stress et reproductibilite",
 "paths": [
 "MDL_Ynor_Framework/tests",
 "MDL_Ynor_Framework/.pytest_cache",
 "MDL_Ynor_Framework/.uv-cache",
 "MDL_Ynor_Framework/.venv",
 "MDL_Ynor_Framework/_08_EXPERIMENTS_AND_DEMOS",
 "MDL_Ynor_Framework/_11_GEOMAGNETISM_AND_WMM",
 "MDL_Ynor_Framework/_12_QUANT_FINANCE_MDL",
 "MDL_Ynor_Framework/_12_QUANT_FINANCE_MODERN",
 ],
 },
 {
 "order": "06",
 "key": "B_PRIME",
 "title": "GOUVERNANCE_ET_DIFFUSION",
 "mirror": "B",
 "role": "Reprise normative, securitaire, commerciale et de soumission",
 "paths": [
 "MDL_Ynor_Framework/_05_MARKETING_AND_PITCH",
 "MDL_Ynor_Framework/_07_ADMIN_LEGAL_GOVERNANCE",
 "MDL_Ynor_Framework/_09_SECURITY_AND_AUDIT",
 "_SUBMISSIONS",
 ],
 },
 {
 "order": "07",
 "key": "A_PRIME",
 "title": "ARCHIVES_ET_RELEASES",
 "mirror": "A",
 "role": "Cloture recursive par archives, commandes et distributions",
 "paths": [
 "MDL_Ynor_Framework/_00_DISTS_AND_RELEASES",
 "MDL_Ynor_Framework/_00_YNOR_COMMAND_CENTER",
 "MDL_Ynor_Framework/_ARCHIVES_LOGIQUE_MDL",
 "MDL_Ynor_Framework/mdl_ynor_framework.egg-info",
 "_RELEASES/MDL_YNOR_SOVEREIGN_ARCH_GOLDEN_MASTER_2026.zip",
 ],
 },
]


def file_sha256(path: Path) -> str:
 digest = hashlib.sha256()
 with path.open("rb") as handle:
 for chunk in iter(lambda: handle.read(1024 * 1024), b""):
 digest.update(chunk)
 return digest.hexdigest()


def is_textual(path: Path) -> bool:
 suffix = path.suffix.lower()
 return suffix in TEXT_EXTENSIONS or path.name in {".gitignore", ".env", ".env.template"}


def read_text(path: Path) -> str | None:
 for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
 try:
 return path.read_text(encoding=encoding)
 except Exception:
 continue
 return None


def materialize_file(source: Path, destination: Path) -> None:
 destination.parent.mkdir(parents=True, exist_ok=True)
 if destination.exists():
 destination.unlink()
 try:
 os.link(source, destination)
 except Exception:
 shutil.copy2(source, destination)


def render_text_mirror(source: Path, mirror_path: Path, rel_path: str) -> dict:
 mirror_path.parent.mkdir(parents=True, exist_ok=True)
 text = read_text(source)
 metadata = {
 "source": rel_path,
 "size_bytes": source.stat().st_size,
 "sha256": file_sha256(source),
 "kind": "text" if text is not None else "binary_descriptor",
 }
 if text is None:
 descriptor = "\n".join(
 [
 f"# DESCRIPTEUR BINAIRE - {source.name}",
 "",
 f"Source : {rel_path}",
 f"Taille : {metadata['size_bytes']} octets",
 f"SHA256 : {metadata['sha256']}",
 "",
 "Contenu non textualisable automatiquement dans ce miroir.",
 ]
 )
 mirror_path.with_suffix(mirror_path.suffix + ".md").write_text(descriptor, encoding="utf-8")
 return metadata

 payload = "\n".join(
 [
 f"# MIROIR TEXTUEL - {source.name}",
 "",
 f"Source : {rel_path}",
 f"Taille : {metadata['size_bytes']} octets",
 f"SHA256 : {metadata['sha256']}",
 "",
 "```text",
 text,
 "```",
 ]
 )
 mirror_path.with_suffix(mirror_path.suffix + ".md").write_text(payload, encoding="utf-8")
 return metadata


def iter_files(path: Path):
 if path.is_file():
 yield path
 return
 for file_path in path.rglob("*"):
 if file_path.is_file():
 if OUTPUT in file_path.parents:
 continue
 yield file_path


def main() -> None:
 OUTPUT.mkdir(parents=True, exist_ok=True)
 root_manifest = {
 "title": "FRACTAL_CHIASTE",
 "order": "A -> B -> C -> X -> C' -> B' -> A'",
 "nodes": [],
 }

 md_lines = [
 "# FRACTAL CHIASTE",
 "",
 "Ordre chiastique global : A -> B -> C -> X -> C' -> B' -> A'",
 "",
 "Chaque noeud contient :",
 "- 01_SOURCE_IMPLANTEE : implantation materielle des fichiers",
 "- 02_MIROIR_TEXTUEL : contenu textuel ou descripteur du fichier",
 "- 03_RECURSION : regle fractale locale",
 "- 04_INDEX : inventaire et hash",
 "",
 ]

 for node in NODES:
 node_name = f"{node['order']}_{node['key']}_{node['title']}"
 node_root = OUTPUT / node_name
 source_root = node_root / "01_SOURCE_IMPLANTEE"
 mirror_root = node_root / "02_MIROIR_TEXTUEL"
 recursion_root = node_root / "03_RECURSION"
 index_root = node_root / "04_INDEX"
 for folder in (source_root, mirror_root, recursion_root, index_root):
 folder.mkdir(parents=True, exist_ok=True)

 inventory = []
 for raw_path in node["paths"]:
 source_path = ROOT / raw_path
 if not source_path.exists():
 inventory.append({"source": raw_path, "status": "missing"})
 continue

 for file_path in iter_files(source_path):
 rel_source = file_path.relative_to(ROOT)
 source_dest = source_root / rel_source
 materialize_file(file_path, source_dest)
 mirror_target = mirror_root / rel_source
 metadata = render_text_mirror(file_path, mirror_target, str(rel_source))
 inventory.append(metadata)

 recurse_note = "\n".join(
 [
 f"Noeud : {node['key']} / {node['title']}",
 f"Miroir : {node['mirror']}",
 "Regle fractale : chaque fichier est replie en source, miroir textuel et index.",
 "Regle chiastique : tout noeud renvoie a son miroir et au centre X.",
 ]
 )
 (recursion_root / "RECURSION.txt").write_text(recurse_note, encoding="utf-8")

 node_index = {
 "node": node_name,
 "key": node["key"],
 "mirror": node["mirror"],
 "role": node["role"],
 "inventory_count": len(inventory),
 "inventory": inventory,
 }
 (index_root / "index.json").write_text(
 json.dumps(node_index, ensure_ascii=False, indent=2),
 encoding="utf-8",
 )
 node_md = "\n".join(
 [
 f"# {node_name}",
 "",
 f"Role : {node['role']}",
 f"Miroir : {node['mirror']}",
 f"Inventaire : {len(inventory)} elements indexes",
 ]
 )
 (node_root / "00_NODE.md").write_text(node_md, encoding="utf-8")

 root_manifest["nodes"].append(
 {
 "node": node_name,
 "role": node["role"],
 "mirror": node["mirror"],
 "inventory_count": len(inventory),
 }
 )
 md_lines.append(f"- {node_name} -> {node['role']} -> miroir {node['mirror']}")

 (OUTPUT / "MANIFESTE_FRACTAL_CHIASTE.md").write_text(
 "\n".join(md_lines),
 encoding="utf-8",
 )
 (OUTPUT / "manifeste_fractal_chiaste.json").write_text(
 json.dumps(root_manifest, ensure_ascii=False, indent=2),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
