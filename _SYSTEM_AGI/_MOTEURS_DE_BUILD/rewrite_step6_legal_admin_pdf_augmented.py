from __future__ import annotations

import json
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"
SOURCE_ROOT = ROOT / "MDL Ynor Constitution" / "MDL — Argent & Juridique"
OUT_ROOT = (
 UNIVERSE
 / "06_B_PRIME_GOUVERNANCE_ET_DIFFUSION"
 / "07_PDF_JURIDIQUE_ADMIN_AUGMENTES"
)


def iter_targets() -> list[Path]:
 if not SOURCE_ROOT.exists():
 return []
 return sorted(SOURCE_ROOT.rglob("*.pdf"))


def normalize(text: str) -> str:
 return " ".join((text or "").split())


def classify_family(path: Path) -> str:
 probe = str(path).lower()
 name = path.name.lower()
 if "prospectus" in name:
 return "prospectus"
 if "foi" in name:
 return "foi_et_doctrine"
 if "constitution" in name:
 return "constitution_juridique"
 if "volume" in name:
 return "volume_monumental"
 if "depot" in name or "pack" in probe:
 return "depot_et_pack"
 return "juridique_admin"


def infer_center(path: Path, text: str) -> str:
 probe = f"{path.name.lower()} {text.lower()}"
 if "prospectus" in probe:
 return "Le centre chiastique est ici la projection publique : transformer doctrine et corpus en surface de presentation et de persuasion."
 if "foi" in probe:
 return "Le centre chiastique est ici l'engagement, c'est-a-dire la formalisation normative d'une adhesion structurale."
 if "constitution" in probe:
 return "Le centre chiastique est ici la norme souveraine : faire tenir legitimite, responsabilite et ordre documentaire."
 if "volume" in probe:
 return "Le centre chiastique est ici l'edition monumentale comme geste d'archivage et de souverainete."
 if "depot" in probe or "pack" in probe:
 return "Le centre chiastique est ici le depot : convertir accumulation, preuve et conservation en arche administrative."
 return "Le centre chiastique est ici la gouvernance documentaire du corpus."


def extract_text(path: Path, max_pages: int = 2) -> tuple[int, str]:
 reader = PdfReader(str(path))
 chunks = []
 for page in reader.pages[:max_pages]:
 try:
 chunks.append(page.extract_text() or "")
 except Exception:
 chunks.append("")
 return len(reader.pages), normalize(" ".join(chunks))


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


def build_markdown(rel_path: str, title: str, family: str, pages: int, excerpt: str, center: str) -> str:
 body = excerpt[:1800] if excerpt else "[EXTRACTION_TEXTE_LIMITEE]"
 return "\n".join(
 [
 f"# {title} - VERSION PDF JURIDIQUE/ADMIN FRACTALE ET CHIASTIQUE",
 "",
 f"Source : `{rel_path.replace(chr(92), '/')}`",
 f"Famille : `{family}`",
 f"Pages : `{pages}`",
 "",
 "## A. Ouverture",
 "Le PDF est projete dans la branche gouvernance et diffusion de la fractale.",
 "",
 "## B. Expansion",
 "Le document est lu comme un acte de depot, de norme, de prospectus ou d'edition monumentale.",
 "",
 "## C. Matiere",
 "Extrait textuel interpretable :",
 "```text",
 body,
 "```",
 "",
 "## X. Centre",
 center,
 "",
 "## C'. Retour",
 "Le retour referme le document sur sa fonction administrative, juridique ou de diffusion.",
 "",
 "## B'. Miroir",
 "Le miroir relie archive source, exposition textuelle et diffusion accompagnee.",
 "",
 "## A'. Cloture",
 "La cloture scelle le PDF comme noeud de gouvernance dans l'arche fractale.",
 ]
 )


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
 c.drawString(margin_x, y, "Compagnon PDF juridique/admin fractal et chiastique")
 y -= 0.7 * cm
 c.setFont("Helvetica-Oblique", 9)
 c.drawString(margin_x, y, rel_path.replace("\\", "/")[:110])
 y -= 0.9 * cm

 draw_block("A. Ouverture", f"Famille: {family}. Pages source: {pages}.")
 draw_block("B. Expansion", "Le document est replie en sept moments chiastiques pour renforcer sa lisibilite normative et documentaire.")
 draw_block("C. Matiere", excerpt[:1100] if excerpt else "Extraction textuelle limitee.")
 draw_block("X. Centre", center)
 draw_block("C'. Retour", "Le retour convertit la source en objet transmissible, gouvernable et archivable.")
 draw_block("B'. Miroir", "Le miroir relie document juridique, version textuelle et compagnon PDF.")
 draw_block("A'. Cloture", "Cette cloture confirme l'implantation du PDF dans la branche gouvernance/diffusion.")
 c.save()


def main() -> None:
 manifest_items = []
 for source in iter_targets():
 rel_path = str(source.relative_to(ROOT))
 title = source.stem
 family = classify_family(source)
 try:
 pages, text = extract_text(source)
 except Exception as exc:
 pages, text = 0, f"[EXTRACTION_FAILED] {exc}"
 excerpt = text[:2200] if text else "[EXTRACTION_TEXTE_LIMITEE]"
 center = infer_center(source, excerpt)

 target_dir = OUT_ROOT / source.parent.relative_to(ROOT)
 md_out = target_dir / f"{source.stem}.fractale.md"
 pdf_out = target_dir / f"{source.stem}.fractale_compagnon.pdf"
 target_dir.mkdir(parents=True, exist_ok=True)

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
 "stage": "step_6_legal_admin_pdf_augmented",
 "total_documents": len(manifest_items),
 "output_root": str(OUT_ROOT.relative_to(ROOT)).replace("\\", "/"),
 "items": manifest_items,
 }
 (UNIVERSE / "manifest_step6_legal_admin_pdf_augmented.json").write_text(
 json.dumps(manifest, ensure_ascii=False, indent=2),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
