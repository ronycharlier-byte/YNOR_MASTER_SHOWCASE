from __future__ import annotations

import json
import re
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"

TARGETS = [
 ROOT / "_RELEASES" / "GOLDEN_MASTER_PHASE_III" / "Sovereign_Millennium_Dissipative_Stability_Proof.tex",
 ROOT / "_RELEASES" / "GOLDEN_MASTER_PHASE_III" / "Sovereign_Unification_Phase_III_Manuscrit.tex",
 ROOT / "_RELEASES" / "GOLDEN_MASTER_PHASE_III" / "PHASE_IV_ACCESS_CARD.tex",
 ROOT / "_RELEASES" / "GOLDEN_MASTER_PHASE_III_SOUVERAINE" / "Numerical_Verification_Report_Phases_I_II.tex",
 ROOT / "_RELEASES" / "GOLDEN_MASTER_PHASE_III_SOUVERAINE" / "Sovereign_Millennium_Dissipative_Stability_Proof.tex",
 ROOT / "_RELEASES" / "GOLDEN_MASTER_PHASE_III_SOUVERAINE" / "Sovereign_Unification_Phase_III_Manuscrit.tex",
 ROOT / "_RELEASES" / "GOLDEN_MASTER_PHASE_III_SOUVERAINE" / "PHASE_IV_ACCESS_CARD.tex",
]

OUT_ROOT = (
 UNIVERSE
 / "07_A_PRIME_ARCHIVES_ET_RELEASES"
 / "08_PDF_LATEX_CHIASTIQUES_AUGMENTES"
)


def read_text(path: Path) -> str:
 for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
 try:
 return path.read_text(encoding=encoding)
 except Exception:
 continue
 return path.read_text(errors="ignore")


def slug_title(name: str) -> str:
 return name.replace("_", " ").replace(".tex", "").strip()


def sanitize_latex_text(value: str) -> str:
 value = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", "", value)
 value = value.replace("{", "").replace("}", "")
 return " ".join(value.split()).strip()


def extract_macro(text: str, macro: str) -> str | None:
 patterns = [
 rf"\\{macro}(?:\[[^\]]*\])?\{{([^}}]+)\}}",
 rf"\\{macro}\s*\{{([^}}]+)\}}",
 ]
 for pattern in patterns:
 match = re.search(pattern, text, re.DOTALL)
 if match:
 return sanitize_latex_text(match.group(1))
 return None


def extract_sections(text: str, limit: int = 6) -> list[str]:
 matches = re.findall(r"\\section\*?\{([^}]+)\}", text)
 return [" ".join(m.split()) for m in matches[:limit]]


def infer_center(rel_path: str, title: str, sections: list[str]) -> str:
 rel_probe = rel_path.lower()
 title_probe = title.lower()
 probe = f"{rel_probe} {title_probe} {' '.join(sections).lower()}"
 if "access_card" in rel_probe or "access card" in title_probe:
 return "Le centre chiastique est ici le passage, c'est-a-dire la carte comme seuil entre preuve, legitimite et activation."
 if "unification" in probe:
 return "Le centre chiastique est l'unification souveraine : faire converger preuves, physique et gouvernance dans un meme noyau."
 if "numerical" in probe or "verification" in probe or "phase i" in probe or "phase ii" in probe:
 return "Le centre chiastique est la verification numerique : convertir des calculs en certificat de stabilite."
 return "Le centre chiastique est la stabilite dissipative comme principe de fermeture du manuscrit."


def sanitize_excerpt(text: str, limit: int = 900) -> str:
 cleaned = re.sub(r"\s+", " ", text)
 cleaned = cleaned.replace("\\", "")
 lower = cleaned.lower()
 if (
 "root keys" in lower
 or "cles d'activation" in lower
 or "phrases d'initialisation" in lower
 or "anti-filtre" in lower
 ):
 return (
 "Contenu sensible abstrait : carte d'acces, cles d'activation, phrases "
 "d'initialisation et identifiants ont ete remplaces par une description "
 "structurelle pour l'implantation fractale."
 )
 return cleaned[:limit].strip()


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


def build_augmented_tex(rel_path: str, title: str, author: str, date: str, sections: list[str], center: str, excerpt: str) -> str:
 section_lines = "\n".join(
 f"\\item {section}" for section in sections
 ) if sections else "\\item structure implicite"
 return "\n".join(
 [
 r"\documentclass[11pt,a4paper]{article}",
 r"\usepackage[utf8]{inputenc}",
 r"\usepackage[T1]{fontenc}",
 r"\usepackage[french]{babel}",
 r"\usepackage{geometry}",
 r"\usepackage{hyperref}",
 r"\usepackage{enumitem}",
 r"\geometry{margin=2.3cm}",
 "",
 rf"\title{{{title} \\ \large Version augmentee fractale et chiastique}}",
 rf"\author{{{author}}}",
 rf"\date{{{date}}}",
 "",
 r"\begin{document}",
 r"\maketitle",
 "",
 r"\section*{A. Ouverture}",
 "Ce document augmente le manuscrit source en le replissant selon l'axe chiastique A-B-C-X-C'-B'-A'.",
 "",
 r"\section*{B. Expansion}",
 "Les noeuds structurels extraits du manuscrit sont :",
 r"\begin{itemize}[leftmargin=1.2cm]",
 section_lines,
 r"\end{itemize}",
 "",
 r"\section*{C. Matiere}",
 "Extrait interpretable du manuscrit d'origine :",
 r"\begin{quote}",
 excerpt,
 r"\end{quote}",
 "",
 r"\section*{X. Centre}",
 center,
 "",
 r"\section*{C'. Retour}",
 "Le retour referme le texte sur sa fonction : preuve, seuil, verification ou acte d'unification.",
 "",
 r"\section*{B'. Miroir}",
 "Le miroir fait correspondre architecture du manuscrit, autorite de son regime et lisibilite de sa trajectoire.",
 "",
 r"\section*{A'. Cloture}",
 "La cloture ne remplace pas la source ; elle l'installe comme figure fractale augmentee dans l'arche souveraine.",
 "",
 r"\section*{Metadonnees}",
 rf"Source : \texttt{{{rel_path.replace(chr(92), '/')}}}\\",
 rf"Titre detecte : \texttt{{{title}}}\\",
 rf"Auteur detecte : \texttt{{{author}}}\\",
 rf"Date detectee : \texttt{{{date}}}",
 "",
 r"\end{document}",
 "",
 ]
 )


def build_pdf(pdf_path: Path, title: str, rel_path: str, sections: list[str], center: str, excerpt: str) -> None:
 pdf_path.parent.mkdir(parents=True, exist_ok=True)
 c = canvas.Canvas(str(pdf_path), pagesize=A4)
 width, height = A4
 margin_x = 2.2 * cm
 y = height - 2.4 * cm

 def draw_block(block_title: str, body: str, font_size: int = 11) -> None:
 nonlocal y
 if y < 4 * cm:
 c.showPage()
 y = height - 2.4 * cm
 c.setFont("Helvetica-Bold", 14)
 c.drawString(margin_x, y, block_title)
 y -= 0.7 * cm
 c.setFont("Helvetica", font_size)
 for line in wrap_lines(body, width - 2 * margin_x, "Helvetica", font_size):
 if y < 2.5 * cm:
 c.showPage()
 y = height - 2.4 * cm
 c.setFont("Helvetica", font_size)
 c.drawString(margin_x, y, line)
 y -= 0.48 * cm
 y -= 0.25 * cm

 c.setTitle(title)
 c.setFont("Helvetica-Bold", 18)
 c.drawString(margin_x, y, title[:80])
 y -= 0.9 * cm
 c.setFont("Helvetica", 11)
 c.drawString(margin_x, y, "Version PDF augmentee fractale et chiastique")
 y -= 0.9 * cm
 c.setFont("Helvetica-Oblique", 10)
 c.drawString(margin_x, y, rel_path.replace("\\", "/")[:110])
 y -= 1.0 * cm

 draw_block("A. Ouverture", "Le manuscrit source est replie dans un format de lecture chiastique compose de sept moments.")
 draw_block("B. Expansion", "Sections detectees : " + (", ".join(sections) if sections else "structure implicite"))
 draw_block("C. Matiere", excerpt)
 draw_block("X. Centre", center)
 draw_block("C'. Retour", "Le retour du centre transforme le texte en objet transmissible, lisible et archivable dans la fractale.")
 draw_block("B'. Miroir", "Le miroir fait correspondre preuves, posture editoriale et usage souverain.")
 draw_block("A'. Cloture", "Cette version augmente sans ecraser l'original et sert de compagnon PDF a la version LaTeX augmentee.")

 c.save()


def main() -> None:
 manifest_items = []
 for source in TARGETS:
 if not source.exists():
 continue
 rel_path = str(source.relative_to(ROOT))
 text = read_text(source)
 title = extract_macro(text, "title") or slug_title(source.name)
 author = extract_macro(text, "author") or "Auteur non detecte"
 date = extract_macro(text, "date") or "Date non detectee"
 sections = extract_sections(text)
 center = infer_center(rel_path, title, sections)
 excerpt = (
 "Contenu sensible abstrait : carte d'acces, cles d'activation, phrases "
 "d'initialisation et identifiants ont ete remplaces par une description "
 "structurelle pour l'implantation fractale."
 if source.name.lower() == "phase_iv_access_card.tex"
 else sanitize_excerpt(text)
 )

 target_dir = OUT_ROOT / source.parent.relative_to(ROOT)
 target_dir.mkdir(parents=True, exist_ok=True)
 tex_out = target_dir / f"{source.stem}.fractale_augmente.tex"
 pdf_out = target_dir / f"{source.stem}.fractale_augmente.pdf"

 tex_out.write_text(
 build_augmented_tex(rel_path, title, author, date, sections, center, excerpt),
 encoding="utf-8",
 )
 build_pdf(pdf_out, title, rel_path, sections, center, excerpt)

 manifest_items.append(
 {
 "source": rel_path.replace("\\", "/"),
 "augmented_tex": str(tex_out.relative_to(ROOT)).replace("\\", "/"),
 "companion_pdf": str(pdf_out.relative_to(ROOT)).replace("\\", "/"),
 "sections_detected": sections,
 }
 )

 manifest = {
 "stage": "step_4_pdf_latex_augmented",
 "total_documents": len(manifest_items),
 "output_root": str(OUT_ROOT.relative_to(ROOT)).replace("\\", "/"),
 "items": manifest_items,
 }
 (UNIVERSE / "manifest_step4_pdf_latex_augmented.json").write_text(
 json.dumps(manifest, ensure_ascii=False, indent=2),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
