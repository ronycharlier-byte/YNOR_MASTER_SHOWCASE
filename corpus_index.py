from __future__ import annotations

import hashlib
import json
import mimetypes
import os
from collections import Counter
from dataclasses import dataclass, asdict
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parent

YNOR_ENGINE_VERSION = "V6.1 MASTER LOGOS"
YNOR_STATUS = "SUPREME_RESISTANCE_ACTIVE"
YNOR_PROTOCOL = "RECURRENT_RESONANCE_v6.1"

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "dist",
    "build",
}

TEXT_EXTENSIONS = {
    ".md",
    ".json",
    ".txt",
    ".py",
    ".tex",
    ".html",
    ".htm",
    ".yml",
    ".yaml",
    ".toml",
    ".cfg",
    ".ini",
    ".bat",
    ".ps1",
    ".sh",
    ".csv",
    ".log",
    ".bib",
    ".ipynb",
}

SENSITIVE_NAME_MARKERS = {
    ".env",
    "secrets.local.json",
    "secrets.local.example.json",
    "obfuscation_mapping_private.json",
    "server_pids.json",
    "revocation_list.json",
    "usage_stats.json",
    "mu_audit_history.json",
    "shared_audits.json",
    "growth_events.json",
}

SENSITIVE_PATH_MARKERS = {
    "secrets",
    "private",
    "credential",
    "revocation",
    "usage_stats",
    "growth_events",
    "mu_audit_history",
    "shared_audits",
}

CANONICAL_TOP_LEVEL_PRIORITY = {
    "00_MASTER_FINAL": 0,
    "00_PUBLIC_BRIEF": 1,
    "00_HOMEPAGE": 2,
    "00_EXECUTIVE_DIGEST": 3,
    "00_EDITION_CANONIQUE_FINALE": 4,
    "00_SUBMISSION_PACK": 5,
    "04_X_NOYAU_MEMOIRE": 6,
    "02_B_THEORIE_ET_PREUVES": 7,
    "05_C_PRIME_VALIDATION_ET_TESTS": 8,
    "01_A_FONDATION": 9,
    "03_C_MOTEURS_ET_DEPLOIEMENT": 10,
    "06_B_PRIME_GOUVERNANCE_ET_DIFFUSION": 11,
    "07_A_PRIME_ARCHIVES_ET_RELEASES": 12,
}


def _sha256_for_path(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(chunk_size)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def _is_sensitive(path: Path) -> bool:
    lower_name = path.name.lower()
    lower_path = str(path).lower()
    return any(marker in lower_name for marker in SENSITIVE_NAME_MARKERS) or any(
        marker in lower_path for marker in SENSITIVE_PATH_MARKERS
    )


def _should_skip_dir(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def _is_textual(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    mime, _ = mimetypes.guess_type(path.name)
    return bool(mime and mime.startswith("text/"))


def _safe_read_text(path: Path, limit: int = 24_000) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    if len(text) > limit:
        return text[:limit] + "\n...[truncated]..."
    return text


def _relative_posix(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _is_derived_layer(path: str) -> bool:
    lower = path.lower()
    return any(
        marker in lower
        for marker in (
            "/02_miroir_textuel/",
            "/02_reflet/",
            "/06_reecriture_chiastique_bulk/",
            "/07_reecriture_json_chiastique/",
            "/09_pdf_constitution_math_augmente",
            "/_releases/",
            "/_release/",
            "/_archives/",
            "/_archive/",
            "/_exports/",
            "/_export/",
            "/_backup/",
            "/backup/",
            "/mirrors/",
            "/mirror/",
            "/miroir/",
            "miroir",
            "reflet",
            "/copies/",
            "/copy/",
            "/tmp_render/",
            "/_knowledge_final_export/",
            "/_00_dists_and_releases/",
            "/static_corpus/",
            "/_archives_logique_mdl/",
            "release_pipeline",
            "archive_",
            "release_",
            ".fractale.md",
            ".backup.md",
            ".md.md",
            ".pdf.md",
            ".tex.md",
            ".json.md",
            ".bin.md",
            ".aux",
            ".log",
            ".out",
        )
    )


def _is_versioned_name(name: str) -> bool:
    lower = name.lower()
    return any(
        marker in lower
        for marker in (
            "(1)",
            "v1",
            "v2",
            "v3",
            "v4",
            "v5",
            "v6",
            "v7",
            "v8",
            "v9",
            "final",
            "finale",
            "historique",
            "ultime",
            "complete",
            "consolidee",
        )
    )


def _is_canonical_path(path: str) -> bool:
    lower = path.lower()
    return not _is_derived_layer(lower) and not any(
        marker in lower
        for marker in (
            "/mirrors/",
            "/mirror/",
            "/miroir/",
            "/backup/",
            "/archives/",
            "/archive/",
            "/export/",
            "/exports/",
            "/copies/",
            "/copy/",
        )
    )


def _entry_preference(entry: "CorpusEntry") -> tuple[int, int, int, int, str]:
    top_level_rank = CANONICAL_TOP_LEVEL_PRIORITY.get(entry.top_level, 99)
    derived_rank = 1 if _is_derived_layer(entry.path) else 0
    versioned_rank = 1 if _is_versioned_name(entry.name) else 0
    canonical_rank = 0 if _is_canonical_path(entry.path) else 1
    path_rank = len(entry.path)
    return (derived_rank, versioned_rank, canonical_rank, top_level_rank, f"{path_rank:06d}:{entry.path}")


@dataclass(frozen=True)
class CorpusEntry:
    path: str
    name: str
    directory: str
    top_level: str
    extension: str
    kind: str
    size_bytes: int
    modified_ts: float
    sha256: str
    sensitive: bool
    preview: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.preview is None:
            payload.pop("preview", None)
        return payload


@dataclass
class CorpusIndex:
    root: Path
    entries: list[CorpusEntry]

    @property
    def _hash_counts(self) -> Counter[str]:
        return Counter(entry.sha256 for entry in self.entries)

    @property
    def by_path(self) -> dict[str, CorpusEntry]:
        return {entry.path: entry for entry in self.entries}

    @property
    def top_level_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for entry in self.entries:
            counts[entry.top_level] = counts.get(entry.top_level, 0) + 1
        return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))

    @property
    def extension_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for entry in self.entries:
            ext = entry.extension or "[none]"
            counts[ext] = counts.get(ext, 0) + 1
        return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))

    @property
    def duplicate_hash_groups(self) -> int:
        return sum(1 for count in self._hash_counts.values() if count > 1)

    @property
    def duplicate_hash_entries(self) -> int:
        return sum(count for count in self._hash_counts.values() if count > 1)

    @property
    def derived_entries(self) -> int:
        return sum(1 for entry in self.entries if _is_derived_layer(entry.path))

    @property
    def versioned_entries(self) -> int:
        return sum(1 for entry in self.entries if _is_versioned_name(entry.name))

    @property
    def canonical_entries(self) -> list[CorpusEntry]:
        grouped: dict[str, list[CorpusEntry]] = {}
        for entry in self.entries:
            if _is_derived_layer(entry.path) or _is_versioned_name(entry.name):
                continue
            grouped.setdefault(entry.sha256, []).append(entry)

        selected: list[CorpusEntry] = []
        seen_paths: set[str] = set()
        for group in grouped.values():
            representative = sorted(group, key=_entry_preference)[0]
            if representative.path not in seen_paths:
                selected.append(representative)
                seen_paths.add(representative.path)
        selected.sort(key=lambda entry: entry.path)
        return selected

    @property
    def canonical_duplicate_groups(self) -> int:
        hashes = {entry.sha256 for entry in self.canonical_entries}
        return len(self.canonical_entries) - len(hashes)

    @property
    def canonical_duplicate_entries(self) -> int:
        hashes = {entry.sha256 for entry in self.canonical_entries}
        return len(self.canonical_entries) - len(hashes)

    def _entries_for_scope(self, scope: str = "all") -> list[CorpusEntry]:
        normalized = scope.strip().lower()
        if normalized in {"canonical", "clean", "primary"}:
            return self.canonical_entries
        if normalized in {"raw", "all"}:
            return self.entries
        raise ValueError(f"Unsupported scope: {scope}")

    @property
    def summary(self) -> dict[str, Any]:
        total_size = sum(entry.size_bytes for entry in self.entries)
        text_entries = sum(1 for entry in self.entries if entry.kind == "text")
        sensitive_entries = sum(1 for entry in self.entries if entry.sensitive)
        duplicate_hash_entries = self.duplicate_hash_entries
        return {
            "root": str(self.root),
            "total_files": len(self.entries),
            "total_size_bytes": total_size,
            "text_files": text_entries,
            "binary_or_other_files": len(self.entries) - text_entries,
            "sensitive_files_redacted": sensitive_entries,
            "duplicate_hash_groups": self.duplicate_hash_groups,
            "duplicate_hash_entries": duplicate_hash_entries,
            "duplicate_hash_share_percent": round((duplicate_hash_entries / len(self.entries) * 100) if self.entries else 0.0, 1),
            "derived_entries": self.derived_entries,
            "versioned_entries": self.versioned_entries,
            "top_level_counts": self.top_level_counts,
            "extension_counts": self.extension_counts,
            "canonical_total_files": len(self.canonical_entries),
            "canonical_duplicate_groups": self.canonical_duplicate_groups,
            "canonical_duplicate_entries": self.canonical_duplicate_entries,
        }

    @property
    def canonical_summary(self) -> dict[str, Any]:
        entries = self.canonical_entries
        source_total = len(self.entries)
        total_size = sum(entry.size_bytes for entry in entries)
        text_entries = sum(1 for entry in entries if entry.kind == "text")
        sensitive_entries = sum(1 for entry in entries if entry.sensitive)
        collapsed_files = source_total - len(entries)
        return {
            "root": str(self.root),
            "source_total_files": source_total,
            "total_files": len(entries),
            "total_size_bytes": total_size,
            "text_files": text_entries,
            "binary_or_other_files": len(entries) - text_entries,
            "sensitive_files_redacted": sensitive_entries,
            "duplicate_hash_groups": self.canonical_duplicate_groups,
            "duplicate_hash_entries": self.canonical_duplicate_entries,
            "duplicate_hash_share_percent": round((collapsed_files / source_total * 100) if source_total else 0.0, 1),
            "collapsed_files": collapsed_files,
            "collapse_rate_percent": round((collapsed_files / source_total * 100) if source_total else 0.0, 1),
            "derived_entries": sum(1 for entry in self.entries if _is_derived_layer(entry.path)),
            "versioned_entries": sum(1 for entry in self.entries if _is_versioned_name(entry.name)),
            "top_level_counts": dict(
                sorted(
                    {
                        key: sum(1 for entry in entries if entry.top_level == key)
                        for key in CANONICAL_TOP_LEVEL_PRIORITY
                        if any(entry.top_level == key for entry in entries)
                    }.items(),
                    key=lambda item: (-item[1], item[0]),
                )
            ),
            "extension_counts": dict(
                sorted(
                    {
                        ext or "[none]": sum(1 for entry in entries if (entry.extension or "[none]") == (ext or "[none]"))
                        for ext in {entry.extension or "[none]" for entry in entries}
                    }.items(),
                    key=lambda item: (-item[1], item[0]),
                )
            ),
        }

    @property
    def archive_summary(self) -> dict[str, Any]:
        raw_clusters = self.duplicate_clusters(scope="raw")
        archive_candidates = [
            entry
            for entry in self.entries
            if _is_derived_layer(entry.path) or _is_versioned_name(entry.name) or not _is_canonical_path(entry.path)
        ]
        return {
            "source_total_files": len(self.entries),
            "archive_candidate_files": len(archive_candidates),
            "duplicate_clusters": len(raw_clusters),
            "duplicate_entries": sum(cluster["count"] for cluster in raw_clusters),
            "top_noise_clusters": raw_clusters[:20],
        }

    def search(self, query: str, limit: int = 25, scope: str = "canonical") -> list[dict[str, Any]]:
        normalized = query.strip().lower()
        if not normalized:
            return []

        scored: list[tuple[int, CorpusEntry, str]] = []
        for entry in self._entries_for_scope(scope):
            score = 0
            snippet = entry.preview or ""
            haystack = f"{entry.path}\n{entry.name}\n{snippet}".lower()
            if normalized in entry.path.lower():
                score += 4
            if normalized in entry.name.lower():
                score += 3
            if normalized in haystack:
                score += 2
            if score:
                idx = haystack.find(normalized)
                if idx >= 0 and snippet:
                    start = max(0, idx - 120)
                    end = min(len(snippet), idx + 260)
                    snippet = snippet[start:end]
                elif entry.preview:
                    snippet = entry.preview[:380]
                scored.append((score, entry, snippet))

        scored.sort(key=lambda item: (-item[0], item[1].path))
        results: list[dict[str, Any]] = []
        for score, entry, snippet in scored[:limit]:
            item = entry.to_dict()
            item["score"] = score
            if entry.sensitive:
                item["preview"] = "[redacted]"
            else:
                item["preview"] = snippet or entry.preview
            results.append(item)
        return results

    def by_top_level(self, top_level: str, scope: str = "all") -> list[dict[str, Any]]:
        return [entry.to_dict() for entry in self._entries_for_scope(scope) if entry.top_level == top_level]

    def duplicate_clusters(self, scope: str = "raw") -> list[dict[str, Any]]:
        entries = self._entries_for_scope(scope)
        grouped: dict[str, list[CorpusEntry]] = {}
        for entry in entries:
            grouped.setdefault(entry.sha256, []).append(entry)

        clusters: list[dict[str, Any]] = []
        for sha256, group in grouped.items():
            if len(group) < 2:
                continue
            ordered = sorted(group, key=_entry_preference)
            representative = ordered[0]
            clusters.append(
                {
                    "sha256": sha256,
                    "count": len(group),
                    "representative": representative.to_dict(),
                    "items": [entry.to_dict() for entry in ordered],
                }
            )
        clusters.sort(key=lambda item: (-item["count"], item["representative"]["path"]))
        return clusters

    def manifests(self) -> list[dict[str, Any]]:
        candidates = [
            "00_MASTER_FINAL/manifest_step14_master_final.json",
            "00_HOMEPAGE/manifest_step13_homepage.json",
            "00_PUBLIC_BRIEF/manifest_step11_public_brief.json",
            "00_EXECUTIVE_DIGEST/manifest_step10_executive_digest.json",
            "00_EDITION_CANONIQUE_FINALE/manifest_step9_canonical_edition.json",
            "00_SUBMISSION_PACK/manifest_step12_submission_pack.json",
            "manifest_step7_master_index.json",
            "manifest_step8_visual_navigation.json",
        ]
        out: list[dict[str, Any]] = []
        for rel in candidates:
            path = self.root / rel
            if not path.exists() or not path.is_file():
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                continue
            out.append(
                {
                    "path": rel,
                    "size_bytes": path.stat().st_size,
                    "modified_ts": path.stat().st_mtime,
                    "data": data,
                }
            )
        return out


def _build_entry(path: Path) -> CorpusEntry:
    stat = path.stat()
    rel = _relative_posix(path)
    top_level = path.relative_to(REPO_ROOT).parts[0] if path.relative_to(REPO_ROOT).parts else ""
    extension = path.suffix.lower()
    sensitive = _is_sensitive(path)
    is_text = _is_textual(path)
    preview = None
    if is_text and not sensitive:
        preview = _safe_read_text(path)
    elif sensitive and is_text:
        preview = "[redacted]"
    return CorpusEntry(
        path=rel,
        name=path.name,
        directory=path.parent.relative_to(REPO_ROOT).as_posix(),
        top_level=top_level,
        extension=extension,
        kind="text" if is_text else "binary",
        size_bytes=stat.st_size,
        modified_ts=stat.st_mtime,
        sha256=_sha256_for_path(path),
        sensitive=sensitive,
        preview=preview,
    )


def _iter_corpus_files(root: Path) -> Iterable[Path]:
    for current_root, dirs, files in os.walk(root):
        current_path = Path(current_root)
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        if _should_skip_dir(current_path):
            continue
        for file_name in files:
            path = current_path / file_name
            if _should_skip_dir(path):
                continue
            yield path


@lru_cache(maxsize=1)
def load_corpus_index() -> CorpusIndex:
    entries: list[CorpusEntry] = []
    for path in _iter_corpus_files(REPO_ROOT):
        try:
            entries.append(_build_entry(path))
        except Exception:
            continue

    entries.sort(key=lambda entry: entry.path)
    return CorpusIndex(root=REPO_ROOT, entries=entries)
