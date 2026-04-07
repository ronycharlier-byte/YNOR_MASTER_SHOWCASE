from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

def build_node(node_name: str, key: str, title: str, mirror: str, role: str, subfolders_to_absorb: list[str]):
 node_root = ROOT / node_name
 source_root = node_root / "01_SOURCE_IMPLANTEE"
 mirror_root = node_root / "02_MIROIR_TEXTUEL"
 recursion_root = node_root / "03_RECURSION"
 index_root = node_root / "04_INDEX"
 
 for folder in (source_root, mirror_root, recursion_root, index_root):
 folder.mkdir(parents=True, exist_ok=True)
 
 for sub in subfolders_to_absorb:
 sub_path = ROOT / sub
 if sub_path.exists() and sub_path.is_dir() and sub_path != node_root:
 dest = source_root / sub
 if not dest.exists():
 shutil.move(str(sub_path), str(dest))
 
 inventory = []
 
 for file_path in source_root.rglob("*"):
 if file_path.is_file():
 rel_source = file_path.relative_to(source_root)
 mirror_target = mirror_root / rel_source
 mirror_target.parent.mkdir(parents=True, exist_ok=True)
 
 try:
 text = file_path.read_text(encoding="utf-8")
 kind = "text"
 payload = f"# MIROIR TEXTUEL - {file_path.name}\n\n```text\n{text}\n```"
 except Exception:
 text = None
 kind = "binary_descriptor"
 payload = f"# DESCRIPTEUR BINAIRE - {file_path.name}\n\nContenu binaire."
 
 digest = hashlib.sha256()
 with file_path.open("rb") as handle:
 for chunk in iter(lambda: handle.read(1024 * 1024), b""):
 digest.update(chunk)
 sha256 = digest.hexdigest()
 
 mirror_target.with_suffix(mirror_target.suffix + ".md").write_text(payload, encoding="utf-8")
 
 inventory.append({
 "source": str(rel_source),
 "size_bytes": file_path.stat().st_size,
 "sha256": sha256,
 "kind": kind
 })
 
 recurse_note = f"Noeud : {key} / {title}\nMiroir : {mirror}\nRole : {role}\nLe systeme est structurellement ferme et recroise toutes les dimensions."
 (recursion_root / "RECURSION.txt").write_text(recurse_note, encoding="utf-8")
 
 node_index = {
 "node": node_name,
 "key": key,
 "mirror": mirror,
 "role": role,
 "inventory_count": len(inventory),
 "inventory": inventory,
 }
 (index_root / "index.json").write_text(json.dumps(node_index, ensure_ascii=False, indent=2), encoding="utf-8")
 
 node_md = f"# {node_name}\n\nRole : {role}\nMiroir : {mirror}\nInventaire : {len(inventory)} elements indexes\n"
 (node_root / "00_NODE.md").write_text(node_md, encoding="utf-8")

def main():
 # Absorbing all 00_ and 01_TECHNICAL, 02_PUBLIC into 00
 stray_00 = [d.name for d in ROOT.iterdir() if d.is_dir() and (d.name.startswith("00_") or d.name.startswith("01_T") or d.name.startswith("02_P")) and d.name != "00_OMEGA_PORTAIL_ET_EDITION"]
 build_node(
 "00_OMEGA_PORTAIL_ET_EDITION",
 "",
 "PORTAIL_ET_EDITION",
 "OMEGA_PRIME",
 "Enveloppe matricielle externe, face d'entree structurelle.",
 stray_00
 )
 
 # Absorbing 08_ into 08_OMEGA_PRIME
 stray_08 = [d.name for d in ROOT.iterdir() if d.is_dir() and d.name.startswith("08_") and d.name != "08_OMEGA_PRIME_API_REFERENCE"]
 build_node(
 "08_OMEGA_PRIME_API_REFERENCE",
 "OMEGA_PRIME",
 "API_REFERENCE_CLOTURE",
 "",
 "Enveloppe de reference finale, API technique et cloture du systeme.",
 stray_08
 )
 
if __name__ == "__main__":
 main()
