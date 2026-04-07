from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "FRACTAL_CHIASTE"

TARGETS = [
 ROOT / "MDL_Ynor_Framework" / "_05_DATA_AND_MEMORY",
 ROOT / "MDL_Ynor_Framework" / "_PREUVES_ET_RAPPORTS",
 ROOT / "MDL_Ynor_Framework" / "mdl_intelligence_report.json",
 ROOT / "_RELEASES" / "GOLDEN_MASTER_PHASE_III" / "Sovereign_Global_Knowledge.json",
 ROOT / "_RELEASES" / "GOLDEN_MASTER_PHASE_III_SOUVERAINE" / "Sovereign_Global_Knowledge.json",
]

NODE_BY_PREFIX = {
 "MDL_Ynor_Framework/_05_DATA_AND_MEMORY": "04_X_NOYAU_MEMOIRE",
 "MDL_Ynor_Framework/_PREUVES_ET_RAPPORTS": "02_B_THEORIE_ET_PREUVES",
 "MDL_Ynor_Framework/mdl_intelligence_report.json": "04_X_NOYAU_MEMOIRE",
 "_RELEASES/GOLDEN_MASTER_PHASE_III/": "07_A_PRIME_ARCHIVES_ET_RELEASES",
 "_RELEASES/GOLDEN_MASTER_PHASE_III_SOUVERAINE/": "07_A_PRIME_ARCHIVES_ET_RELEASES",
}

SENSITIVE_KEYS = {
 "api_key",
 "openai_api_key",
 "token",
 "secret",
 "password",
 "authorization",
 "admin_secret",
 "root_key",
 "gh_pat",
 "auth_key",
 "authorized_by",
}

SENSITIVE_WORDS = {
 "attack",
 "attaque",
 "exploit",
 "botnet",
 "payload",
 "root access",
 "authorized_by",
 "vulnerability",
 "offensive",
 "churn",
}

SENSITIVE_FILENAME_HINTS = {
 "prompt",
 "secret",
 "credential",
 "token",
 "key",
 "offensive",
 "attack",
 "exploit",
}


def classify_node(rel_path: str) -> str:
 rel = rel_path.replace("\\", "/")
 for prefix, node in NODE_BY_PREFIX.items():
 if rel.startswith(prefix):
 return node
 return "04_X_NOYAU_MEMOIRE"


def iter_json_files():
 for target in TARGETS:
 if not target.exists():
 continue
 if target.is_file():
 yield target
 else:
 for path in target.rglob("*.json"):
 if path.is_file():
 yield path


def redact_value(key: str, value):
 lowered = key.lower()
 if (
 lowered in SENSITIVE_KEYS
 or lowered.endswith("_key")
 or "token" in lowered
 or "secret" in lowered
 or "auth" in lowered
 ):
 return "[REDACTED]"
 if isinstance(value, str):
 probe = value.lower()
 if any(word in probe for word in SENSITIVE_WORDS):
 return "[SENSITIVE_CONTENT_ABSTRACTED]"
 return value


def sanitize(obj):
 if isinstance(obj, dict):
 return {k: sanitize(redact_value(k, v)) for k, v in obj.items()}
 if isinstance(obj, list):
 return [sanitize(v) for v in obj]
 return obj


def summarize_dict_keys(data: dict, limit: int = 10) -> list[str]:
 return list(data.keys())[:limit]


def sanitize_raw_excerpt(text: str, limit: int = 1200) -> str:
 excerpt = text[:limit]
 lines = []
 for line in excerpt.splitlines():
 masked = line
 lowered = masked.lower()
 if any(word in lowered for word in SENSITIVE_WORDS):
 masked = "[SENSITIVE_CONTENT_ABSTRACTED]"
 for token in (
 "api_key",
 "openai_api_key",
 "token",
 "secret",
 "password",
 "authorization",
 "gh_pat",
 "auth_key",
 "authorized_by",
 ):
 if token in lowered:
 masked = "[REDACTED_LINE]"
 break
 lines.append(masked)
 return "\n".join(lines).strip() or "[EMPTY]"


def infer_center(rel_path: str, data) -> str:
 rel = rel_path.lower()
 if "knowledge" in rel:
 return "Le centre chiastique est ici la condensation de connaissance : transformer des fragments disperses en noyau partageable."
 if "report" in rel or "snapshot" in rel or "validation" in rel:
 return "Le centre chiastique est l'acte d'audit : convertir des mesures en preuve de coherence ou d'ecart."
 if "prompt" in rel:
 return "Le centre chiastique est l'orientation du systeme : faire d'une configuration un regime de posture."
 if "memory" in rel:
 return "Le centre chiastique est la memoire structurale, c'est-a-dire le lieu ou les traces deviennent organisation."
 if "knowledge" in rel:
 return "Le centre chiastique est la condensation de connaissance : transformer des fragments disperses en noyau partageable."
 return "Le centre chiastique est la transformation de donnees brutes en structure interpretable."


def build_rewrite(rel_path: str, data) -> str:
 title = Path(rel_path).name
 kind = type(data).__name__
 size_hint = len(data) if isinstance(data, (list, dict)) else 1
 center = infer_center(rel_path, data)
 sanitized = sanitize(data)

 if isinstance(sanitized, dict):
 expansion_items = summarize_dict_keys(sanitized)
 material = json.dumps(
 {k: sanitized[k] for k in list(sanitized.keys())[:5]},
 ensure_ascii=False,
 indent=2,
 )
 elif isinstance(sanitized, list):
 expansion_items = [f"item_{i}" for i in range(min(len(sanitized), 6))]
 material = json.dumps(sanitized[:3], ensure_ascii=False, indent=2)
 else:
 expansion_items = ["scalar_value"]
 material = json.dumps(sanitized, ensure_ascii=False, indent=2)

 expansion_block = "\n".join(f"- {item}" for item in expansion_items) if expansion_items else "- structure implicite"

 return "\n".join(
 [
 f"# {title} - VERSION FRACTALE ET CHIASTIQUE",
 "",
 f"Source : `{rel_path.replace(chr(92), '/')}`",
 f"Type : `{kind}`",
 f"Amplitude structurelle : `{size_hint}`",
 "",
 "## A. Ouverture",
 "Le JSON s'ouvre comme une structure de traces, d'etats ou de connaissances formalisables.",
 "",
 "## B. Expansion",
 "Les premieres lignes de force sont :",
 expansion_block,
 "",
 "## C. Matiere",
 "Extrait interpretable et sanitise :",
 "```json",
 material,
 "```",
 "",
 "## X. Centre",
 center,
 "",
 "## C'. Retour",
 "Au retour du centre, la donnee n'est plus seulement archive ; elle devient lecture operationnelle, memoire ou preuve.",
 "",
 "## B'. Miroir",
 "Le miroir chiastique du JSON consiste a faire correspondre schema, trace et interpretation.",
 "",
 "## A'. Cloture",
 "La cloture replie la donnee sur son sens : ce qui etait tableau, liste ou objet devient noeud fractal dans une arche plus large.",
 "",
 "Forme chiastique :",
 "- A : ouverture de la structure",
 "- B : expansion des cles ou items",
 "- C : matiere sanitisee",
 "- X : centre interpretatif",
 "- C' : retour vers l'usage",
 "- B' : miroir de schema",
 "- A' : scellement fractal",
 ]
 )


def build_fallback_rewrite(rel_path: str, raw_text: str, parse_error: str) -> str:
 title = Path(rel_path).name
 excerpt = sanitize_raw_excerpt(raw_text)
 center = infer_center(rel_path, raw_text)
 path_probe = rel_path.lower()
 filename_markers = [
 marker for marker in sorted(SENSITIVE_FILENAME_HINTS) if marker in path_probe
 ]
 marker_block = "\n".join(f"- {marker}" for marker in filename_markers) if filename_markers else "- structure_nominale"

 return "\n".join(
 [
 f"# {title} - VERSION FRACTALE ET CHIASTIQUE",
 "",
 f"Source : `{rel_path.replace(chr(92), '/')}`",
 "Type : `invalid_json_fallback`",
 "",
 "## A. Ouverture",
 "Le document existe comme trace JSON attendue, mais sa syntaxe ne se laisse pas refermer en parse nominal.",
 "",
 "## B. Expansion",
 "Les indices de lecture provenant du nom et du chemin sont :",
 marker_block,
 "",
 "## C. Matiere",
 "Extrait brut sanitise :",
 "```text",
 excerpt,
 "```",
 "",
 "## X. Centre",
 center,
 "",
 "## C'. Retour",
 "Le retour chiastique traite ici l'echec syntaxique comme symptome structurel : une forme existe, mais sa fermeture reste incomplete.",
 "",
 "## B'. Miroir",
 "Le miroir confronte intention de schema et rupture de schema.",
 "",
 "## A'. Cloture",
 "La cloture ne corrige pas la source ; elle l'implante comme objet fractal incomplet mais interpretable.",
 "",
 "## Note Technique",
 f"Erreur de parse : `{parse_error}`",
 "",
 "Forme chiastique :",
 "- A : ouverture du fragment",
 "- B : expansion des indices nominaux",
 "- C : matiere brute sanitisee",
 "- X : centre interpretatif",
 "- C' : retour vers l'echec syntaxique comme signal",
 "- B' : miroir schema / rupture",
 "- A' : scellement fractal du fragment",
 ]
 )


def load_json_or_fallback(path: Path) -> tuple[Any, str | None]:
 errors = []
 text_candidates = []
 for encoding in ("utf-8", "utf-8-sig", "cp1252"):
 try:
 raw = path.read_text(encoding=encoding)
 text_candidates.append(raw)
 except Exception as exc:
 errors.append(f"{encoding}: {exc}")
 continue
 try:
 return json.loads(raw), None
 except Exception as exc:
 errors.append(f"{encoding}: {exc}")
 raw_fallback = text_candidates[0] if text_candidates else ""
 return raw_fallback, " | ".join(errors)


def main() -> None:
 items = []
 for path in iter_json_files():
 rel_path = str(path.relative_to(ROOT))
 node = classify_node(rel_path)
 out_root = UNIVERSE / node / "07_REECRITURE_JSON_CHIASTIQUE"
 out_file = out_root / path.relative_to(ROOT)
 out_file = out_file.with_name(out_file.name + ".fractale.md")
 out_file.parent.mkdir(parents=True, exist_ok=True)

 data, parse_error = load_json_or_fallback(path)
 if parse_error is None:
 rewrite = build_rewrite(rel_path, data)
 source_mode = "parsed_json"
 else:
 rewrite = build_fallback_rewrite(rel_path, data, parse_error)
 source_mode = "fallback_raw"
 out_file.write_text(rewrite, encoding="utf-8")
 items.append(
 {
 "source": rel_path.replace("\\", "/"),
 "node": node,
 "rewrite": str(out_file.relative_to(ROOT)).replace("\\", "/"),
 "mode": source_mode,
 }
 )

 manifest = {
 "stage": "step_3_json_rewrite",
 "total_rewrites": len(items),
 "items": items,
 }
 (UNIVERSE / "manifest_step3_json_rewrite.json").write_text(
 json.dumps(manifest, ensure_ascii=False, indent=2),
 encoding="utf-8",
 )


if __name__ == "__main__":
 main()
