from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"

TARGETS = [
 ROOT / "_RELEASES",
 ROOT / "_SUBMISSIONS",
 ROOT / "MDL_Ynor_Framework" / "_01_THEORY_AND_PAPERS",
 ROOT / "MDL_Ynor_Framework" / "_05_MARKETING_AND_PITCH",
 ROOT / "MDL_Ynor_Framework" / "_07_ADMIN_LEGAL_GOVERNANCE",
]

NODE_BY_PREFIX = {
 "_RELEASES": "07_A_PRIME_ARCHIVES_ET_RELEASES",
 "_SUBMISSIONS": "06_B_PRIME_GOUVERNANCE_ET_DIFFUSION",
 "MDL_Ynor_Framework/_01_THEORY_AND_PAPERS": "02_B_THEORIE_ET_PREUVES",
 "MDL_Ynor_Framework/_05_MARKETING_AND_PITCH": "06_B_PRIME_GOUVERNANCE_ET_DIFFUSION",
 "MDL_Ynor_Framework/_07_ADMIN_LEGAL_GOVERNANCE": "06_B_PRIME_GOUVERNANCE_ET_DIFFUSION",
}


def read_text(path: Path) -> str:
 for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
 try:
 return path.read_text(encoding=encoding)
 except Exception:
 continue
 return path.read_text(errors="ignore")


def normalize_whitespace(text: str) -> str:
 text = text.replace("\r\n", "\n").replace("\r", "\n")
 text = re.sub(r"\n{3,}", "\n\n", text)
 return text.strip()


def first_heading_or_name(path: Path, text: str) -> str:
 for line in text.splitlines():
 stripped = line.strip()
 if stripped.startswith("#"):
 return stripped.lstrip("#").strip()
 if stripped:
 break
 return path.stem


def collect_bullets(text: str, limit: int = 6) -> list[str]:
 bullets = []
 for line in text.splitlines():
 stripped = line.strip()
 if stripped.startswith(("- ", "* ", "+ ")):
 bullets.append(stripped[2:].strip())
 elif re.match(r"^\d+\.\s+", stripped):
 bullets.append(re.sub(r"^\d+\.\s+", "", stripped))
 if len(bullets) >= limit:
 break
 return bullets


def collect_headings(text: str, limit: int = 6) -> list[str]:
 headings = []
 for line in text.splitlines():
 stripped = line.strip()
 if stripped.startswith("#"):
 headings.append(stripped.lstrip("#").strip())
 if len(headings) >= limit:
 break
 return headings


def first_paragraphs(text: str, limit: int = 2) -> list[str]:
 paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
 cleaned = []
 for paragraph in paragraphs:
 flat = " ".join(paragraph.split())
 if paragraph.startswith("#") or flat in {"---", "***"}:
 continue
 cleaned.append(flat)
 if len(cleaned) >= limit:
 break
 return cleaned


def infer_center(text: str, rel_path: str) -> str:
 lowered = text.lower()
 if "\\mu" in text or "mu =" in lowered or "marge dissipative" in lowered:
 return "La marge de viabilite constitue le centre de gravite du texte."
 if "proof" in lowered or "preuve" in lowered:
 return "Le centre chiastique est l'acte de preuve : faire converger hypothese, demonstration et validation."
 if "prompt" in lowered:
 return "Le centre chiastique est l'invocation : transformer une consigne en posture stable."
 if "submission" in lowered or "soumission" in lowered:
 return "Le centre chiastique est le passage du texte prive au texte publiquement evaluable."
 if "governance" in lowered or "gouvernance" in lowered or "legal" in lowered:
 return "Le centre chiastique est la membrane normative qui relie capacite et legitimite."
 if "marketing" in lowered or "pitch" in lowered or "sales" in lowered:
 return "Le centre chiastique est la conversion d'une these en desir de transmission."
 return f"Le centre chiastique du fichier {Path(rel_path).name} est son noyau d'intelligibilite interne."


def detect_sensitive_prompt(path: Path, text: str) -> bool:
 upper = path.name.upper()
 if "PROMPT" in upper:
 return True
 sensitive_markers = [
 "ROOT ACCESS GRANTED",
 "CLÉ ROOT",
 "CLE ROOT",
 "FOUNDER",
 "INITIALIZING SOVEREIGN",
 ]
 upper_text = text.upper()
 return any(marker in upper_text for marker in sensitive_markers)


def sanitize_excerpt(text: str) -> str:
 text = re.sub(r"`[^`]{20,}`", "`[SEGMENT REDACTED]`", text)
 text = re.sub(r"\([A-Z0-9]{8,}[^)]*\)", "([SEGMENT REDACTED])", text)
 return text


def classify_node(rel_path: str) -> str:
 rel_path_unix = rel_path.replace("\\", "/")
 for prefix, node in NODE_BY_PREFIX.items():
 if rel_path_unix.startswith(prefix):
 return node
 return "04_X_NOYAU_MEMOIRE"


def build_rewrite(path: Path, rel_path: str, text: str) -> str:
 title = first_heading_or_name(path, text)
 headings = collect_headings(text)
 bullets = collect_bullets(text)
 paragraphs = first_paragraphs(text)
 center = infer_center(text, rel_path)
 sensitive = detect_sensitive_prompt(path, text)

 opening = paragraphs[0] if paragraphs else f"{title} ouvre un segment important du corpus MDL Ynor."
 if sensitive:
 expansion_items = [
 "niveaux d'autorite",
 "posture d'identite",
 "invariants de stabilite",
 "protocoles defensifs",
 "signature de version",
 ]
 else:
 expansion_items = bullets or headings[1:] or ["Le texte se deploie en strates successives autour de sa these."]
 secondary = paragraphs[1] if len(paragraphs) > 1 else "Le mouvement du texte fait passer une intuition initiale vers une forme plus structurée."
 if sensitive:
 matter = "Le contenu source comporte des segments d'activation ou d'autorité. La version chiastique en conserve la structure sans recopier les marqueurs sensibles."
 else:
 matter = sanitize_excerpt(secondary)

 expansion_block = "\n".join(f"- {item}" for item in expansion_items[:6])
 headings_block = "\n".join(f"- {item}" for item in headings[:6]) if headings else "- Le fichier ne declare pas de titres explicites."

 return "\n".join(
 [
 f"# {title} - VERSION FRACTALE ET CHIASTIQUE",
 "",
 f"Source : `{rel_path.replace(chr(92), '/')}`",
 "",
 "## A. Ouverture",
 opening,
 "",
 "## B. Expansion",
 "Le texte se déplie selon les lignes suivantes :",
 expansion_block,
 "",
 "## C. Matiere",
 matter,
 "",
 "## X. Centre",
 center,
 "",
 "## C'. Retour",
 "Au retour du centre, le texte se relit comme un mécanisme de clarification, de stabilisation ou d'institution.",
 "",
 "## B'. Miroir",
 "Les titres ou repères structurants deviennent les miroirs de son organisation :",
 headings_block,
 "",
 "## A'. Cloture",
 "La clôture répond à l'ouverture : ce qui commençait comme énoncé devient ici arche, retour et scellement fractal.",
 "",
 "Forme chiastique :",
 "- A : ouverture",
 "- B : déploiement",
 "- C : matière",
 "- X : centre",
 "- C' : retour",
 "- B' : miroir",
 "- A' : clôture",
 ]
 )


def main() -> None:
 summary = []
 total = 0
 for target in TARGETS:
 if not target.exists():
 continue
 for path in target.rglob("*"):
 if not path.is_file():
 continue
 if path.suffix.lower() not in {".md", ".txt", ".tex"}:
 continue

 rel_path = str(path.relative_to(ROOT))
 node = classify_node(rel_path)
 out_root = UNIVERSE / node / "06_REECRITURE_CHIASTIQUE_BULK"
 out_file = out_root / path.relative_to(ROOT)
 out_file = out_file.with_name(out_file.name + ".fractale.md")
 out_file.parent.mkdir(parents=True, exist_ok=True)

 text = normalize_whitespace(read_text(path))
 rewrite = build_rewrite(path, rel_path, text)
 out_file.write_text(rewrite, encoding="utf-8")

 summary.append(
 {
 "source": rel_path.replace("\\", "/"),
 "node": node,
 "rewrite": str(out_file.relative_to(ROOT)).replace("\\", "/"),
 }
 )
 total += 1

 manifest = {
 "stage": "step_2_bulk_rewrite",
 "total_rewrites": total,
 "items": summary,
 }
 manifest_path = UNIVERSE / "manifest_step2_bulk_rewrite.json"
 manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
 main()
