from __future__ import annotations

import html
import json
import mimetypes
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse, Response

from corpus_index import REPO_ROOT, load_corpus_index


SOURCE_ROOT = REPO_ROOT / "03_C_MOTEURS_ET_DEPLOIEMENT" / "01_SOURCE_IMPLANTEE" / "MDL_Ynor_Framework"
if SOURCE_ROOT.exists() and str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

try:
    from _04_DEPLOYMENT_AND_API.ynor_api_server import app as legacy_app  # type: ignore
except Exception:
    legacy_app = FastAPI(title="MDL Ynor Corpus API", version="1.0.0")


app = legacy_app

NODE_PREFIXES = {
    "A": "01_A_",
    "B": "02_B_",
    "C": "03_C_",
    "X": "04_X_",
    "C'": "05_C_PRIME_",
    "B'": "06_B_PRIME_",
    "A'": "07_A_PRIME_",
}


def _index():
    return load_corpus_index()


def _resolve_relative_path(rel_path: str) -> Path:
    candidate = (REPO_ROOT / rel_path).resolve()
    try:
        candidate.relative_to(REPO_ROOT.resolve())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Path traversal blocked.") from exc
    if not candidate.exists() or not candidate.is_file():
        raise HTTPException(status_code=404, detail="File not found.")
    return candidate


def _html_layout(title: str, body: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #09090b;
      --panel: #121216;
      --panel-2: #17171d;
      --line: #262633;
      --text: #f8fafc;
      --muted: #a1a1aa;
      --accent: #7dd3fc;
      --accent-2: #86efac;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(125, 211, 252, 0.12), transparent 24%),
        radial-gradient(circle at top right, rgba(134, 239, 172, 0.10), transparent 20%),
        var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      min-height: 100vh;
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    .wrap {{ max-width: 1280px; margin: 0 auto; padding: 28px; }}
    .hero {{
      padding: 28px;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: linear-gradient(180deg, rgba(18,18,22,.96), rgba(10,10,12,.96));
      box-shadow: 0 18px 60px rgba(0,0,0,.35);
      margin-bottom: 22px;
    }}
    .eyebrow {{
      text-transform: uppercase;
      letter-spacing: .24em;
      color: var(--accent-2);
      font-size: 12px;
      margin-bottom: 10px;
    }}
    h1 {{ margin: 0 0 8px; font-size: clamp(30px, 4vw, 54px); line-height: 1.03; }}
    .sub {{ color: var(--muted); max-width: 920px; line-height: 1.65; }}
    .grid {{
      display: grid;
      gap: 18px;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    }}
    .panel {{
      border: 1px solid var(--line);
      border-radius: 20px;
      background: rgba(18,18,22,.92);
      padding: 18px;
    }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 12px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(255,255,255,.02);
      color: var(--text);
      font-size: 13px;
    }}
    .label {{
      color: var(--muted);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: .12em;
      margin-bottom: 8px;
    }}
    input {{
      width: 100%;
      padding: 12px 14px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: var(--panel-2);
      color: var(--text);
      outline: none;
    }}
    button {{
      padding: 12px 16px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: linear-gradient(180deg, rgba(125,211,252,.18), rgba(125,211,252,.08));
      color: var(--text);
      cursor: pointer;
      font-weight: 700;
    }}
    .section-title {{ margin: 0 0 12px; font-size: 20px; }}
    .list {{ display: flex; flex-direction: column; gap: 10px; }}
    .item {{
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: rgba(255,255,255,.02);
    }}
    .path {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 13px;
      color: var(--accent);
      word-break: break-all;
    }}
    .meta {{ color: var(--muted); font-size: 12px; margin-top: 4px; }}
    .preview {{
      margin-top: 10px;
      white-space: pre-wrap;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 12px;
      color: #d4d4d8;
      max-height: 220px;
      overflow: auto;
    }}
    .row {{ display: flex; gap: 12px; flex-wrap: wrap; }}
    .row > * {{ flex: 1 1 240px; }}
    .small {{ font-size: 12px; color: var(--muted); }}
    .two-col {{ display: grid; grid-template-columns: 1.2fr .8fr; gap: 18px; }}
    .footer {{ margin-top: 20px; color: var(--muted); font-size: 12px; }}
    @media (max-width: 900px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    {body}
  </div>
</body>
</html>
"""


def _render_entry_card(entry: Any) -> str:
    preview = html.escape((entry.preview or "")[:520]) if entry.preview else ""
    link = f"/api/corpus/file/{quote(entry.path, safe='/')}"
    return f"""
      <div class="item">
        <div class="path"><a href="{html.escape(link)}">{html.escape(entry.path)}</a></div>
        <div class="meta">type={entry.kind} | size={entry.size_bytes} bytes | sha256={entry.sha256[:12]}...</div>
        {f'<div class="preview">{preview}</div>' if preview else ''}
      </div>
    """


def _matches_node(entry: Any, node: str) -> bool:
    normalized = node.strip().upper()
    top_level = str(entry.top_level).upper()
    if normalized in NODE_PREFIXES:
        return top_level.startswith(NODE_PREFIXES[normalized])
    if normalized in {"APRIME", "A_PRIME"}:
        return top_level.startswith(NODE_PREFIXES["A'"])
    if normalized in {"BPRIME", "B_PRIME"}:
        return top_level.startswith(NODE_PREFIXES["B'"])
    if normalized in {"CPRIME", "C_PRIME"}:
        return top_level.startswith(NODE_PREFIXES["C'"])
    return top_level == normalized


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def corpus_home() -> str:
    idx = _index()
    summary = idx.summary
    entrypoints = [
        "00_HOMEPAGE/HOMEPAGE_DU_CORPUS.md",
        "00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md",
        "00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md",
        "00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md",
        "03_C_MOTEURS_ET_DEPLOIEMENT/README.md",
        "05_C_PRIME_VALIDATION_ET_TESTS/README.md",
        "00_SUBMISSION_PACK/RESUME_DE_SOUMISSION.md",
        "00_MASTER_FINAL/MASTER_FINAL.md",
    ]

    entrypoint_html = "".join(
        f'<div class="item"><div class="path">{html.escape(item)}</div></div>' for item in entrypoints
    )
    recent_html = "".join(_render_entry_card(entry) for entry in idx.entries[:8])
    extension_html = "".join(
        f'<span class="chip">{html.escape(ext or "[none]")} <strong>{count}</strong></span>'
        for ext, count in list(summary["extension_counts"].items())[:14]
    )

    body = f"""
    <section class="hero">
      <div class="eyebrow">MDL Ynor Corpus API</div>
      <h1>Application API du corpus fractal et chiastique</h1>
      <p class="sub">
        This application indexes the corpus, exposes non-sensitive files, supports search,
        and provides a unified access point for the documentation runtime.
      </p>
      <div class="chips" style="margin-top:14px;">
        <span class="chip">Total files: <strong>{summary["total_files"]}</strong></span>
        <span class="chip">Text files: <strong>{summary["text_files"]}</strong></span>
        <span class="chip">Sensitive redacted: <strong>{summary["sensitive_files_redacted"]}</strong></span>
        <span class="chip">Root: <strong>{html.escape(summary["root"])}</strong></span>
      </div>
    </section>

    <div class="grid">
      <div class="panel">
        <div class="label">Corpus search</div>
        <div class="row">
          <input id="query" type="text" placeholder="Search a file, keyword, or title..." />
          <button onclick="runSearch()">Search</button>
        </div>
        <div class="small" style="margin-top:8px;">Search covers paths, file names, and indexed text previews.</div>
        <div id="results" class="list" style="margin-top:16px;"></div>
      </div>

      <div class="panel">
        <div class="label">Entrypoints</div>
        <div class="list">{entrypoint_html}</div>
      </div>
    </div>

    <div class="two-col" style="margin-top:18px;">
      <div class="panel">
        <h2 class="section-title">Recent corpus files</h2>
        <div class="list">{recent_html}</div>
      </div>
      <div class="panel">
        <h2 class="section-title">Statistics</h2>
        <div class="chips">{extension_html}</div>
        <h3 class="section-title" style="margin-top:18px;">Chiastic axis</h3>
        <div class="item">
          <div class="path">A -> B -> C -> X -> C' -> B' -> A'</div>
          <div class="meta">Foundation | Theory | Engines | Memory | Validation | Governance | Archives</div>
        </div>
        <div class="footer">
          Existing API: <a href="/status">/status</a> |
          <a href="/docs">/docs</a> |
          <a href="/dashboard">/dashboard</a>
        </div>
      </div>
    </div>

    <script>
      async function runSearch() {{
        const query = document.getElementById('query').value.trim();
        const results = document.getElementById('results');
        results.innerHTML = '<div class="item">Searching...</div>';
        if (!query) {{
          results.innerHTML = '<div class="item">Enter a keyword to search.</div>';
          return;
        }}
        const response = await fetch(`/api/corpus/search?q=${{encodeURIComponent(query)}}&limit=12`);
        const payload = await response.json();
        if (!payload.results || !payload.results.length) {{
          results.innerHTML = '<div class="item">No results.</div>';
          return;
        }}
        results.innerHTML = payload.results.map(renderResult).join('');
      }}

      function renderResult(item) {{
        const preview = item.preview ? `<div class="preview">${{escapeHtml(item.preview)}}</div>` : '';
        return `
          <div class="item">
            <div class="path"><a href="/api/corpus/file/${{encodeURIComponent(item.path)}}">${{escapeHtml(item.path)}}</a></div>
            <div class="meta">type=${{item.kind}} | size=${{item.size_bytes}} bytes | score=${{item.score}}</div>
            ${preview}
          </div>
        `;
      }}

      function escapeHtml(value) {{
        return String(value)
          .replaceAll('&', '&amp;')
          .replaceAll('<', '&lt;')
          .replaceAll('>', '&gt;')
          .replaceAll('"', '&quot;')
          .replaceAll("'", '&#39;');
      }}
    </script>
    """
    return _html_layout("MDL Ynor Corpus API", body)


@app.get("/corpus", response_class=HTMLResponse, include_in_schema=False)
async def corpus_alias() -> str:
    return await corpus_home()


@app.get("/api/corpus/status")
async def corpus_status() -> dict[str, Any]:
    idx = _index()
    summary = idx.summary
    return {
        "status": "ONLINE",
        "corpus_root": summary["root"],
        "total_files": summary["total_files"],
        "text_files": summary["text_files"],
        "sensitive_files_redacted": summary["sensitive_files_redacted"],
    }


@app.get("/api/corpus/summary")
async def corpus_summary() -> dict[str, Any]:
    idx = _index()
    return {
        "summary": idx.summary,
        "chiastic_axis": ["A", "B", "C", "X", "C'", "B'", "A'"],
        "manifests": idx.manifests(),
        "primary_entrypoints": [
            "00_HOMEPAGE/HOMEPAGE_DU_CORPUS.md",
            "00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md",
            "00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md",
            "00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md",
            "00_MASTER_FINAL/MASTER_FINAL.md",
        ],
    }


@app.get("/api/corpus/files")
async def corpus_files(
    limit: int = Query(200, ge=1, le=2000),
    offset: int = Query(0, ge=0),
) -> dict[str, Any]:
    idx = _index()
    entries = idx.entries[offset : offset + limit]
    return {
        "total": len(idx.entries),
        "offset": offset,
        "limit": limit,
        "items": [entry.to_dict() for entry in entries],
    }


@app.get("/api/corpus/search")
async def corpus_search(q: str = Query(..., min_length=1), limit: int = Query(25, ge=1, le=100)) -> dict[str, Any]:
    idx = _index()
    return {"query": q, "limit": limit, "results": idx.search(q, limit=limit)}


@app.get("/api/corpus/node/{node}")
async def corpus_node(node: str) -> dict[str, Any]:
    idx = _index()
    matches = [entry.to_dict() for entry in idx.entries if _matches_node(entry, node) or entry.top_level == node]
    return {"node": node, "count": len(matches), "items": matches}


@app.get("/api/corpus/nodes")
async def corpus_nodes() -> dict[str, Any]:
    idx = _index()
    return {
        "top_level_counts": idx.top_level_counts,
        "chiastic_aliases": NODE_PREFIXES,
    }


@app.get("/api/corpus/manifests")
async def corpus_manifests() -> dict[str, Any]:
    return {"items": _index().manifests()}


@app.get("/api/corpus/entrypoints")
async def corpus_entrypoints() -> dict[str, Any]:
    return {
        "items": [
            {"name": "homepage", "path": "00_HOMEPAGE/HOMEPAGE_DU_CORPUS.md"},
            {"name": "public_brief", "path": "00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md"},
            {"name": "executive_digest", "path": "00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md"},
            {"name": "canonical_portal", "path": "00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md"},
            {"name": "submission_summary", "path": "00_SUBMISSION_PACK/RESUME_DE_SOUMISSION.md"},
            {"name": "master_final", "path": "00_MASTER_FINAL/MASTER_FINAL.md"},
            {"name": "deployment_readme", "path": "03_C_MOTEURS_ET_DEPLOIEMENT/README.md"},
            {"name": "validation_readme", "path": "05_C_PRIME_VALIDATION_ET_TESTS/README.md"},
        ]
    }


@app.get("/api/corpus/preview/{rel_path:path}")
async def corpus_preview(rel_path: str) -> dict[str, Any]:
    path = _resolve_relative_path(rel_path)
    idx = _index()
    entry = idx.by_path.get(path.relative_to(REPO_ROOT).as_posix())
    if not entry:
        raise HTTPException(status_code=404, detail="File not indexed.")
    payload = entry.to_dict()
    if entry.sensitive:
        payload["preview"] = "[redacted]"
    return payload


@app.get("/api/corpus/file/{rel_path:path}")
async def corpus_file(rel_path: str, download: bool = Query(False)) -> Response:
    path = _resolve_relative_path(rel_path)
    idx = _index()
    entry = idx.by_path.get(path.relative_to(REPO_ROOT).as_posix())
    if entry and entry.sensitive:
        raise HTTPException(
            status_code=403,
            detail="This file is sensitive and is only exposed as redacted metadata.",
        )

    mime_type, _ = mimetypes.guess_type(path.name)
    if download:
        return FileResponse(path, filename=path.name, media_type=mime_type or "application/octet-stream")

    textual_suffixes = {
        ".md",
        ".json",
        ".txt",
        ".py",
        ".tex",
        ".yaml",
        ".yml",
        ".toml",
        ".cfg",
        ".html",
        ".htm",
        ".ps1",
        ".bat",
        ".sh",
    }

    if (mime_type and mime_type.startswith("text/")) or path.suffix.lower() in textual_suffixes:
        text = path.read_text(encoding="utf-8", errors="replace")
        media = mime_type or "text/plain; charset=utf-8"
        if path.suffix.lower() == ".json":
            try:
                return JSONResponse(json.loads(text))
            except Exception:
                pass
        return PlainTextResponse(text, media_type=media)

    return FileResponse(path, filename=path.name, media_type=mime_type or "application/octet-stream")


if __name__ == "__main__":
    import uvicorn  # type: ignore

    port = int(os.environ.get("PORT", 8492))
    uvicorn.run(app, host="0.0.0.0", port=port)
