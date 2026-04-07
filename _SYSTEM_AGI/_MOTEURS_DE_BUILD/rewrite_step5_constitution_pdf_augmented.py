from __future__ import annotations

import json
import re
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"
OUT_ROOT = UNIVERSE / "02_B_THEORIE_ET_PREUVES" / "09_PDF_CONSTITUTION_MATH_AUGMENTES"

def resolve_targets() -> list[Path]:
 constitution_root = ROOT / "MDL Ynor Constitution"
 found: list[Path] = []
 seen: set[Path] = set()

 buckets = [
 constitution_root / "MDL Ynor MATH",
 constitution_root,
 constitution_root / "MDL Ynor Canonique_",
 ROOT / "MDL_Ynor_Framework",
 ]

 for bucket in buckets:
 if not bucket.exists():
 continue
 for path in sorted(bucket.glob("*.pdf")):
 if path in seen:
 continue
 seen.add(path)
 found.append(path)

 filtered: list[Path] = []
 for path in found:
 probe = str(path)
 if "FRACTAL_CHIASTE" in probe or "FRACTAL_CHIASME_MDL_YNOR" in probe:
 continue
 if path.name == "YNOR_FULL_CORPUS_FORMAL_SPEC_V2.3.pdf":
 filtered.append(path)
 continue
 if path.parent.name in {"MDL Ynor MATH", "MDL Ynor Canonique_"}:
 filtered.append(path)
 continue
 if path.parent == constitution_root:
 filtered.append(path)
 return filtered


def normalize(text: str) -> str:
 return " ".join((text or "").split())


def extract_pdf_text(path: Path, max_pages: int = 2) -> tuple[int, str]:
 reader = PdfReader(str(path))
 chunks = []
 for page in reader.pages[:max_pages]:
 try:
 chunks.append(page.extract_text() or "")
 except Exception:
 chunks.append("")
 return len(reader.pages), normalize(" ".join(chunks))


def infer_center(name: str, text: str) -> str:
 probe = f"{name.lower()} {text.lower()}"
 if "axiomatique" in probe:
 return "Le centre chiastique est l'axiome minimal, c'est-a-dire le point ou la formalisation commence avant toute expansion."
 if "théorèmes" in probe or "marge dissipative" in probe:
 return "Le centre chiastique est la marge dissipative comme articulation entre preuve, stabilité et gouvernement du systeme."
 if "théorie structurelle" in probe or "constitution structurelle" in probe:
 return "Le centre chiastique est la structure elle-meme : faire tenir ensemble forme, borne et dissipation."
 if "intégrale du noyau" in probe or "noyau" in probe:
 return "Le centre chiastique est le noyau integral, c'est-a-dire la region ou tout le corpus se condense et se replie."
 if "traité" in probe:
 return "Le centre chiastique est la dynamique : convertir le mouvement en stabilite lisible."
 if "canonique" in probe:
 return "Le centre chiastique est l'unification canonique du corpus."
 if "formal spec" in probe or "corpus" in probe:
 return "Le centre chiastique est la specification integrale du corpus."
 return "Le centre chiastique est la transformation d'un PDF source en preuve fractale transmissible."


def classify_family(path: Path) -> str:
 probe = str(path).lower()
 if "mdl ynor math" in probe:
 return "mathematique"
 if "constitution" in probe:
 return "constitutionnel"
 if "formal_spec" in probe or "corpus" in probe:
 return "corpus_formel"
 return "source_primaire"


def build_markdown(rel_path: str, title: str, family: str, pages: int, excerpt: str, center: str) -> str:
 excerpt = excerpt[:1800] if excerpt else "[EXTRACTION_TEXTE_LIMITEE]"
 return "\n".join(
 [
 f"# {title} - VERSION PDF FRACTALE ET CHIASTIQUE",
 "",
 f"Source : `{rel_path.replace(chr(92), '/')}`",
 f"Famille : `{family}`",
 f"Pages : `{pages}`",
 "",
 "## A. Ouverture",
 "Le PDF est implante comme forme source dans la fractale.",
 "",
 "## B. Expansion",
 "Le document est lu comme un noeud de theorie, de constitution ou de noyau formel.",
 "",
 "## C. Matiere",
 "Extrait textuel interpretable :",
 "```text",
 excerpt,
 "```",
 "",
 "## X. Centre",
 center,
 "",
 "## C'. Retour",
 "Le retour du centre transforme le PDF en document transmissible, indexable et rejouable dans l'architecture chiastique.",
 "",
 "## B'. Miroir",
 "Le miroir fait correspondre pagination, densite conceptuelle et fonction structurale.",
 "",
 "## A'. Cloture",
 "La cloture scelle la source PDF comme arche de preuve dans le corpus fractal.",
 ]
 )


def wrap_lines(text: str, width: float, font_name: str, font_size: int) -> list[str]:
 words = text.split()
 if not words:
 return [""]
 lines: list[str] = []
 current = words[0]
 for word in words[1:]:
 candidate = current + " " + word
 if stringWidth(candidate, font_name, font_size) <= width:
 current = candidate
 else:
 lines.append(current)
 current = word
 lines.append(current)
 return lines


def build_pdf(output_path: Path, title: str, rel_path: str, family: str, pages: int, excerpt: str, center: str) -> None:
 output_path.parent.mkdir(parents=True, exist_ok=True)
 c = canvas.Canvas(str(output_path), pagesize=A4)
 width, height = A4
 margin_x = 2.1 * cm
 y = height - 2.3 * cm

 def draw_block(block_title: str, body: str) -> None:
 nonlocal y
 if y < 4 * cm:
 c.showPage()
 y = height - 2.3 * cm
 c.setFont("Helvetica-Bold", 14)
 c.drawString(margin_x, y, block_title)
 y -= 0.7 * cm
 c.setFont("Helvetica", 10)
 for line in wrap_lines(body, width - 2 * margin_x, "Helvetica", 10):
 if y < 2.2 * cm:
 c.showPage()
 y = height - 2.3 * cm
 c.setFont("Helvetica", 10)
 c.drawString(margin_x, y, line)
 y -= 0.45 * cm
 y -= 0.2 * cm

 c.setTitle(title)
 c.setFont("Helvetica-Bold", 17)
 c.drawString(margin_x, y, title[:85])
 y -= 0.8 * cm
 c.setFont("Helvetica", 11)
 c.drawString(margin_x, y, "Compagnon PDF fractal et chiastique")
 y -= 0.7 * cm
 c.setFont("Helvetica-Oblique", 9)
 c.drawString(margin_x, y, rel_path.replace("\\", "/")[:110])
 y -= 0.9 * cm

 draw_block("A. Ouverture", f"Famille: {family}. Pages source: {pages}.")
 draw_block("B. Expansion", "Le document est replie en sept moments chiastiques pour renforcer sa lisibilite structurale.")
 draw_block("C. Matiere", excerpt[:1100] if excerpt else "Extraction textuelle limitee.")
 draw_block("X. Centre", center)
 draw_block("C'. Retour", "Le retour convertit la source en objet partageable et archivable.")
 draw_block("B'. Miroir", "Le miroir relie le document original, sa version textuelle et sa version PDF compagnon.")
 draw_block("A'. Cloture", "Cette cloture confirme l'implantation du PDF dans la fractale.")
 c.save()


def main() -> None:
 targets = resolve_targets()
 manifest_items = []
 for source in targets:
 rel_path = str(source.relative_to(ROOT))
 title = source.stem
 family = classify_family(source)
 try:
 pages, text = extract_pdf_text(source)
 except Exception as exc:
 pages, text = 0, f"[EXTRACTION_FAILED] {exc}"
 excerpt = text[:2200] if text else "[EXTRACTION_TEXTE_LIMITEE]"
 center = infer_center(source.name, excerpt)

 target_dir = OUT_ROOT / source.parent.relative_to(ROOT)
 target_dir.mkdir(parents=True, exist_ok=True)
 md_out = target_dir / f"{source.stem}.fractale.md"
 pdf_out = target_dir / f"{source.stem}.fractale_compagnon.pdf"

 md_out.write_text(
 build_markdown(rel_path, title, family, pages, excerpt, center),
 encoding="utf-8",
 )
 build_pdf(pdf_out, title, rel_path, family, pages, excerpt, center)

 manifest_items.append(
 {
 "source": rel_path.replace("\\", "/"),
 "family": family,
 "pages": pages,
 "markdown_rewrite": str(md_out.relative_to(ROOT)).replace("\\", "/"),
 "companion_pdf": str(pdf_out.relative_to(ROOT)).replace("\\", "/"),
 }
 )

 manifest = {
 "stage": "step_5_constitution_pdf_augmented",
 "total_documents": len(manifest_items),
 "output_root": str(OUT_ROOT.relative_to(ROOT)).replace("\\", "/"),
 "items": manifest_items,
 }
 (UNIVERSE / "manifest_step5_constitution_pdf_augmented.json").write_text(
 json.dumps(manifest, ensure_ascii=False, indent=2),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
