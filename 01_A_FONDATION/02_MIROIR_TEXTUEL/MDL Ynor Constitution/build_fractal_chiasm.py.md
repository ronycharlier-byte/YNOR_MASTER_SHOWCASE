# MIROIR TEXTUEL - build_fractal_chiasm.py

Source : MDL Ynor Constitution\build_fractal_chiasm.py
Taille : 7902 octets
SHA256 : 034258a8a15a94ed58d23403a7d088d38a25cdd87674d4207dc0db6cac2a30d5

```text
from __future__ import annotations

import json
import shutil
from pathlib import Path


def copy_item(source: Path, destination: Path) -> None:
    if source.is_dir():
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def main() -> None:
    constitution_root = Path(__file__).resolve().parent
    output_root = constitution_root / "FRACTAL_CHIASME_MDL_YNOR"
    output_root.mkdir(parents=True, exist_ok=True)

    nodes = [
        {
            "order": "01",
            "key": "A",
            "title": "AXIOMATIQUE_MINIMALE",
            "role": "Ouverture fondatrice",
            "mirror": "A_PRIME",
            "summary": "Le point d'entree du systeme. Les axiomes minimaux ouvrent la forme fractale.",
            "sources": [
                constitution_root / "MDL Ynor MATH" / "Chapitre I — Formalisation axiomatique minimale.pdf",
            ],
        },
        {
            "order": "02",
            "key": "B",
            "title": "THEOREMES_DE_LA_MARGE",
            "role": "Premier arc de dissipation",
            "mirror": "B_PRIME",
            "summary": "Le premier developpement porte la marge dissipative comme loi de propagation.",
            "sources": [
                constitution_root / "MDL Ynor — Théorèmes fondamentaux de la marge dissipative.pdf",
            ],
        },
        {
            "order": "03",
            "key": "C",
            "title": "THEORIE_STRUCTURELLE",
            "role": "Arc structural amont",
            "mirror": "C_PRIME",
            "summary": "La theorie structurelle prepare le renversement chiastique vers le noyau.",
            "sources": [
                constitution_root / "MDL Ynor — Théorie Structurelle des Systèmes Dissipatifs à Amplification Bornée.pdf",
            ],
        },
        {
            "order": "04",
            "key": "X",
            "title": "NOYAU_INTEGRAL",
            "role": "Centre chiastique",
            "mirror": "X",
            "summary": "Le centre integre les formulations mathematiques du noyau. Tout converge ici puis repart en reflet.",
            "sources": [
                constitution_root / "MDL Ynor MATH" / "Chapitre XVI — Formalisation mathématique intégrale du noyau MDL Ynor.pdf",
                constitution_root / "Chapitre I — Formalisation mathématique intégrale du noyau MDL Ynor.pdf",
            ],
        },
        {
            "order": "05",
            "key": "C_PRIME",
            "title": "CONSTITUTION_STRUCTURELLE",
            "role": "Arc structural aval",
            "mirror": "C",
            "summary": "La constitution structurelle rejoue la theorie en forme inverse et plus normative.",
            "sources": [
                constitution_root / "MDL Ynor — Constitution Structurelle des Systèmes Dissipatifs à Amplification Bornée.pdf",
            ],
        },
        {
            "order": "06",
            "key": "B_PRIME",
            "title": "TRAITE_DYNAMIQUE",
            "role": "Second arc de dissipation",
            "mirror": "B",
            "summary": "Le traite reprend la dynamique au retour du centre et ferme l'enveloppe theorique.",
            "sources": [
                constitution_root / "MDL Ynor — Traité des dynamiques dissipatives et de la stabilité structurelle.pdf",
            ],
        },
        {
            "order": "07",
            "key": "A_PRIME",
            "title": "ARCHITECTURE_RECURSIVE",
            "role": "Cloture architecturale",
            "mirror": "A",
            "summary": "La cloture se fait par l'architecture, qui replie le corpus sur lui-meme et ouvre la recursion fractale.",
            "sources": [
                constitution_root / "MDL Ynor Archtecture_",
            ],
        },
    ]

    manifest_lines = [
        "# MANIFESTE FRACTAL CHIASTIQUE MDL YNOR",
        "",
        "Ordre chiastique : A -> B -> C -> X -> C' -> B' -> A'",
        "",
        "Centre : X / NOYAU_INTEGRAL",
        "",
        "Principe fractal : chaque noeud contient trois strates repetees.",
        "- 01_SOURCE : le document ou corpus source",
        "- 02_REFLET : son role miroir dans l'axe",
        "- 03_RECURSION : la regle de retour vers le centre et vers la paire",
        "",
    ]
    json_nodes = []

    for node in nodes:
        node_folder_name = f"{node['order']}_{node['key']}_{node['title']}"
        node_root = output_root / node_folder_name
        source_root = node_root / "01_SOURCE"
        mirror_root = node_root / "02_REFLET"
        recursion_root = node_root / "03_RECURSION"
        source_root.mkdir(parents=True, exist_ok=True)
        mirror_root.mkdir(parents=True, exist_ok=True)
        recursion_root.mkdir(parents=True, exist_ok=True)

        copied_names: list[str] = []
        for source in node["sources"]:
            if not source.exists():
                continue
            destination = source_root / source.name
            copy_item(source, destination)
            copied_names.append(source.name)

        node_readme = "\n".join(
            [
                f"# {node['key']} - {node['title']}",
                "",
                f"Role : {node['role']}",
                "",
                f"Miroir chiastique : {node['mirror']}",
                "",
                f"Resume : {node['summary']}",
                "",
                "Contenu source :",
                *[f"- {name}" for name in copied_names],
                "",
                "Implementation fractale :",
                "- 01_SOURCE contient le document ou le sous-corpus original.",
                "- 02_REFLET designe la paire miroir dans la structure chiastique.",
                "- 03_RECURSION rappelle le retour vers le centre X.",
            ]
        )
        (node_root / "00_NODE.md").write_text(node_readme, encoding="utf-8")

        mirror_note = "\n".join(
            [
                f"Noeud : {node['key']}",
                f"Paire miroir : {node['mirror']}",
                "Centre : X / NOYAU_INTEGRAL",
                "Mouvement : aller -> centre -> retour",
            ]
        )
        (mirror_root / "MIROIR.txt").write_text(mirror_note, encoding="utf-8")

        recursion_note = "\n".join(
            [
                f"Recursion fractale du noeud {node['key']}",
                "",
                "Regle 1 : lire la source.",
                f"Regle 2 : identifier son miroir chiastique ({node['mirror']}).",
                "Regle 3 : revenir au centre X.",
                "Regle 4 : rejouer la meme logique a l'interieur du corpus local.",
            ]
        )
        (recursion_root / "RECURSION.txt").write_text(recursion_note, encoding="utf-8")

        manifest_lines.append(
            f"- {node_folder_name} -> {node['role']} -> miroir {node['mirror']}"
        )
        json_nodes.append(
            {
                "order": node["order"],
                "key": node["key"],
                "title": node["title"],
                "role": node["role"],
                "mirror": node["mirror"],
                "summary": node["summary"],
                "sources": copied_names,
            }
        )

    manifest_lines.extend(
        [
            "",
            "Resultat : les fichiers demandes sont reorientes dans une arche documentaire fractale et chiastique sans toucher aux originaux.",
        ]
    )
    (output_root / "MANIFESTE_FRACTAL_CHIASTIQUE.md").write_text(
        "\n".join(manifest_lines),
        encoding="utf-8",
    )
    (output_root / "manifeste_fractal_chiastique.json").write_text(
        json.dumps(json_nodes, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

```