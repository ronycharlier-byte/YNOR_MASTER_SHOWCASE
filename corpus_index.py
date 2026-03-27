from __future__ import annotations

import hashlib
import json
import mimetypes
import os
from dataclasses import dataclass, asdict
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parent

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
    def summary(self) -> dict[str, Any]:
        total_size = sum(entry.size_bytes for entry in self.entries)
        text_entries = sum(1 for entry in self.entries if entry.kind == "text")
        sensitive_entries = sum(1 for entry in self.entries if entry.sensitive)
        return {
            "root": str(self.root),
            "total_files": len(self.entries),
            "total_size_bytes": total_size,
            "text_files": text_entries,
            "binary_or_other_files": len(self.entries) - text_entries,
            "sensitive_files_redacted": sensitive_entries,
            "top_level_counts": self.top_level_counts,
            "extension_counts": self.extension_counts,
        }

    def search(self, query: str, limit: int = 25) -> list[dict[str, Any]]:
        normalized = query.strip().lower()
        if not normalized:
            return []

        scored: list[tuple[int, CorpusEntry, str]] = []
        for entry in self.entries:
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

    def by_top_level(self, top_level: str) -> list[dict[str, Any]]:
        return [entry.to_dict() for entry in self.entries if entry.top_level == top_level]

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

