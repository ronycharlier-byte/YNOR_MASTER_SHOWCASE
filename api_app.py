import html
import json
import mimetypes
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==============================================================================
# YNOR MASTER ENGINE - V7.0 (LE CONSEIL DU LOGOS)
# STATUT : GOUVERNANCE MULTI-MODALE SOUVERAINE (PoC V7)
# ==============================================================================
YNOR_VERSION = "V7.0 MASTER COUNCIL"
YNOR_ENGINE_KEYS = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "NOT_SET"),
    "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY", "NOT_SET"),
    "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", "NOT_SET")
}
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from fastapi import Body, FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from corpus_index import REPO_ROOT, load_corpus_index

app = FastAPI(
    title="Ynor API Engine",
    description="The premium intelligence engine for the MDL Ynor Universel corpus.",
    version="2.3.4",
)

# Configuration & Mappings
NODE_PREFIXES = {
    "A": "01_A_",
    "B": "02_B_",
    "C": "03_C_",
    "X": "04_X_",
    "C'": "05_C_PRIME_",
    "B'": "06_B_PRIME_",
    "A'": "07_A_PRIME_",
}

# Static Assets & Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def _index():
    """Loads the latest corpus index."""
    return load_corpus_index()


def _resolve_relative_path(rel_path: str) -> Path:
    """Safe resolution of relative paths within the repo root."""
    try:
        path = (REPO_ROOT / rel_path).resolve()
        if not str(path).startswith(str(REPO_ROOT)):
            raise HTTPException(status_code=403, detail="Path outside of repository root.")
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found.")
        return path
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid path.")


def _matches_node(entry: Any, node: str) -> bool:
    """Checks if an entry belongs to a specific chiastic node."""
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


def _duckduckgo_search(query: str, limit: int = 5) -> list[dict[str, str]]:
    """Performs a live web search using DuckDuckGo."""
    import requests
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"}
    candidates: list[dict[str, str]] = []

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        BeautifulSoup = None

    # Try HTML interface first for snippets
    try:
        response = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        if BeautifulSoup:
            soup = BeautifulSoup(response.text, "html.parser")
            for card in soup.select(".result")[:limit]:
                link = card.select_one(".result__title a")
                snippet = card.select_one(".result__snippet")
                if not link:
                    continue
                title = link.get_text(" ", strip=True)
                url = link.get("href") or ""
                text = snippet.get_text(" ", strip=True) if snippet else ""
                candidates.append({"title": title, "url": url, "snippet": text, "source": "web"})
        if candidates:
            return candidates[:limit]
    except Exception:
        pass

    # Fallback to simple API
    try:
        response = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"},
            headers=headers,
            timeout=8,
        )
        response.raise_for_status()
        payload = response.json()
        abstract = payload.get("AbstractText")
        abstract_url = payload.get("AbstractURL")
        heading = payload.get("Heading")
        if abstract and abstract_url:
            candidates.append({
                "title": heading or query,
                "url": abstract_url,
                "snippet": abstract,
                "source": "web",
            })
    except Exception:
        pass

    return candidates[:limit]


def _format_corpus_context(entries: list[Any], limit: int = 6) -> list[dict[str, str]]:
    """Formats corpus entries for LLM context."""
    items: list[dict[str, str]] = []
    for entry in entries[:limit]:
        title = entry.path.split("/")[-1]
        items.append(
            {
                "title": title,
                "url": f"/api/corpus/file/{quote(entry.path, safe='/')}",
                "snippet": (entry.preview or "").strip(),
                "source": "corpus",
            }
        )
    return items


def _confidence_score(corpus_hits: int, web_hits: int, used_model: bool, brief_mode: bool) -> float:
    """Calculates a confidence score between 0.0 and 1.0."""
    score = 0.56
    score += min(corpus_hits, 6) * 0.055
    score += min(web_hits, 5) * 0.03
    if used_model:
        score += 0.08
    if brief_mode:
        score += 0.02
    return max(0.15, min(score, 0.97))


def _confidence_label(score: float) -> str:
    """Tags a score with a human-readable label."""
    if score >= 0.85: return "High"
    if score >= 0.60: return "Medium"
    return "Low"


def _render_context_block(label: str, items: list[dict[str, str]]) -> str:
    """Prepares a text block of sources for the LLM."""
    lines = [f"{label}:"]
    for idx, item in enumerate(items, start=1):
        snippet = (item.get("snippet") or "").replace("\n", " ").strip()
        if len(snippet) > 360:
            snippet = snippet[:357].rstrip() + "..."
        lines.append(f"[{idx}] {item.get('title', 'untitled')} | {item.get('url', '')} | {snippet}")
    return "\n".join(lines)


def _synthesize_reply(
    query: str,
    corpus_sources: list[dict[str, str]],
    web_sources: list[dict[str, str]],
    brief_mode: bool,
) -> tuple[str, bool]:
    """Uses LLM to synthesize a grounded answer."""
    model_name = os.getenv("YNOR_MODEL", "gpt-4-turbo-preview")
    api_key = os.getenv("OPENAI_API_KEY")
    if OpenAI is not None and api_key:
        try:
            client = OpenAI(api_key=api_key)
            system = (
                "You are Ynor, a premium AI assistant for the MDL Ynor framework. "
                "Answer using the supplied corpus context and web context. "
                "Prefer the corpus for foundational architectural claims and the web for current context. "
                "Use concise executive phrasing. If Brief Mode is enabled, keep the answer especially compact. "
                "Cite sources inline with [1], [2], etc. "
                "Never invent sources."
            )
            user_prompt = f"""
Question: {query}

{_render_context_block('Corpus context', corpus_sources)}
{_render_context_block('Web context', web_sources)}
""".strip()
            if brief_mode:
                user_prompt += "\n\nBrief Mode: On. Deliver a concise executive summary."
            
            # DYNAMIC TOKEN DEBRIDAGE (MDL YNOR V7.1)
            is_bm = "benchmark" in query.lower() or "frontiermath" in query.lower()
            max_t = 8192 if is_bm else 4096
            
            completion = client.chat.completions.create(
                model=model_name,
                temperature=0.2,
                max_tokens=max_t,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return completion.choices[0].message.content.strip(), True
        except Exception:
            pass

    # Simple fallback synthesis
    combined = []
    if corpus_sources:
        combined.append("Based on the indexed corpus:")
        for i, item in enumerate(corpus_sources[:3], start=1):
            combined.append(f"[{i}] {item['title']}: {item['snippet'][:180]}...")
    if web_sources:
        combined.append("\nLive web context:")
        for i, item in enumerate(web_sources[:2], start=1):
            combined.append(f"[{i+3}] {item['title']}: {item['snippet'][:180]}...")
    
    return "\n".join(combined) if combined else "The assistant is unable to retrieve context at this time.", False


# --- HTML ENDPOINTS (Server-Side Templating) ---

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def corpus_home(request: Request):
    idx = _index()
    summary = idx.summary
    canonical = idx.canonical_summary
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "active_page": "home",
            "total_files": summary["total_files"],
            "text_files": summary["text_files"],
            "redacted": summary["sensitive_files_redacted"],
            "duplicate_hash_groups": summary["duplicate_hash_groups"],
            "duplicate_hash_entries": summary["duplicate_hash_entries"],
            "duplicate_hash_share_percent": summary["duplicate_hash_share_percent"],
            "derived_entries": summary["derived_entries"],
            "versioned_entries": summary["versioned_entries"],
            "canonical_total_files": canonical["total_files"],
            "canonical_duplicate_entries": canonical["duplicate_hash_entries"],
            "canonical_duplicate_groups": canonical["duplicate_hash_groups"],
            "canonical_duplicate_share_percent": canonical["duplicate_hash_share_percent"],
            "root_path": summary["root"],
            "recent_cards": idx.canonical_entries[:6],
        },
    )


@app.get("/chat", response_class=HTMLResponse, include_in_schema=False)
async def chat_page(request: Request):
    return templates.TemplateResponse(
        "chat.html", {"request": request, "active_page": "chat"}
    )


@app.get("/pricing", response_class=HTMLResponse, include_in_schema=False)
async def pricing_page(request: Request):
    tiers = [
        {
            "title": "Essential",
            "price": "€9/month",
            "desc": "A refined entry point into the Ynor experience.",
            "features": ["Limited monthly questions", "Standard AI responses", "Basic corpus grounding", "Basic chat history"],
            "featured": False,
        },
        {
            "title": "Plus",
            "price": "€29/month",
            "desc": "For regular users who want more depth and continuity.",
            "features": ["More monthly questions", "Improved response quality", "Longer chat history", "Better context handling", "Faster answers"],
            "featured": False,
        },
        {
            "title": "Pro",
            "price": "€79/month",
            "desc": "For advanced users who require stronger reasoning and deeper intelligence.",
            "features": ["Advanced AI responses", "Deeper context retrieval", "Priority access", "Source references", "Priority support"],
            "featured": False,
        },
        {
            "title": "Elite",
            "price": "€199/month",
            "desc": "The flagship experience for maximum continuity and trust.",
            "features": ["Full access", "Highest question limits", "Best reasoning", "Maximum context depth", "Concierge-level support"],
            "featured": True,
        },
    ]
    return templates.TemplateResponse(
        "pricing.html", {"request": request, "active_page": "pricing", "tiers": tiers}
    )


@app.get("/account", response_class=HTMLResponse, include_in_schema=False)
async def account_page(request: Request):
    return templates.TemplateResponse(
        "account.html", {"request": request, "active_page": "account"}
    )


@app.get("/onboarding", response_class=HTMLResponse, include_in_schema=False)
async def onboarding_page(request: Request):
    return templates.TemplateResponse(
        "onboarding.html", {"request": request, "active_page": "onboarding"}
    )


# --- API ENDPOINTS ---

@app.post("/api/assistant/chat")
async def assistant_chat(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    messages = payload.get("messages") or []
    brief_mode = bool(payload.get("brief_mode", False))
    user_messages = [m for m in messages if isinstance(m, dict) and m.get("role") == "user" and m.get("content")]
    query = str(user_messages[-1]["content"]).strip() if user_messages else ""
    if not query:
        raise HTTPException(status_code=400, detail="A user message is required.")

    idx = _index()
    corpus_results = idx.search(query, limit=6)
    
    # Generic brand reinforcement if no results
    if not corpus_results:
        corpus_results = idx.search("Ynor", limit=6) or idx.search("MDL", limit=6)

    corpus_sources = [
        {
            "title": item.get("name") or item.get("path", "").split("/")[-1],
            "url": f"/api/corpus/file/{quote(item['path'], safe='/')}",
            "snippet": item.get("preview") or "",
            "source": "corpus",
        }
        for item in corpus_results
    ]
    web_sources = _duckduckgo_search(query, limit=5)
    answer, used_model = _synthesize_reply(query, corpus_sources, web_sources, brief_mode=brief_mode)
    confidence_score = _confidence_score(len(corpus_sources), len(web_sources), used_model, brief_mode)
    confidence_label = _confidence_label(confidence_score)

    return {
        "query": query,
        "brief_mode": brief_mode,
        "answer": answer,
        "sources": corpus_sources[:3] + web_sources[:3],
        "confidence_score": f"{confidence_score:.2f}",
        "confidence_label": confidence_label,
        "used_model": used_model,
    }


@app.get("/api/corpus/summary")
async def corpus_summary() -> dict[str, Any]:
    idx = _index()
    return {
        "summary": idx.summary,
        "canonical_summary": idx.canonical_summary,
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


@app.get("/api/corpus/node/{node}")
async def corpus_node(node: str, scope: str = Query("canonical")) -> dict[str, Any]:
    idx = _index()
    source_entries = idx.canonical_entries if scope.strip().lower() in {"canonical", "clean", "primary"} else idx.entries
    matches = [entry.to_dict() for entry in source_entries if _matches_node(entry, node) or entry.top_level == node]
    return {"node": node, "scope": scope, "count": len(matches), "items": matches}


@app.get("/api/corpus/nodes")
async def corpus_nodes(scope: str = Query("canonical")) -> dict[str, Any]:
    idx = _index()
    entries = idx.canonical_entries if scope.strip().lower() in {"canonical", "clean", "primary"} else idx.entries
    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry.top_level] = counts.get(entry.top_level, 0) + 1
    return {
        "scope": scope,
        "top_level_counts": dict(sorted(counts.items(), key=lambda item: (-item[1], item[0]))),
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


@app.get("/api/corpus/status")
async def corpus_status() -> dict[str, Any]:
    idx = _index()
    summary = idx.summary
    canonical = idx.canonical_summary
    return {
        "status": "ONLINE",
        "corpus_root": summary["root"],
        "total_files": summary["total_files"],
        "text_files": summary["text_files"],
        "sensitive_files_redacted": summary["sensitive_files_redacted"],
        "duplicate_hash_groups": summary["duplicate_hash_groups"],
        "duplicate_hash_entries": summary["duplicate_hash_entries"],
        "duplicate_hash_share_percent": summary["duplicate_hash_share_percent"],
        "derived_entries": summary["derived_entries"],
        "versioned_entries": summary["versioned_entries"],
        "canonical_total_files": canonical["total_files"],
        "canonical_duplicate_groups": canonical["duplicate_hash_groups"],
        "canonical_duplicate_entries": canonical["duplicate_hash_entries"],
        "canonical_duplicate_share_percent": canonical["duplicate_hash_share_percent"],
    }


@app.get("/api/corpus/files")
async def corpus_files(
    limit: int = Query(200, ge=1, le=2000),
    offset: int = Query(0, ge=0),
    scope: str = Query("canonical"),
) -> dict[str, Any]:
    idx = _index()
    entries_source = idx.canonical_entries if scope.strip().lower() in {"canonical", "clean", "primary"} else idx.entries
    entries = entries_source[offset : offset + limit]
    return {
        "scope": scope,
        "total": len(entries_source),
        "offset": offset,
        "limit": limit,
        "items": [entry.to_dict() for entry in entries],
    }


@app.get("/api/corpus/duplicates")
async def corpus_duplicates(
    scope: str = Query("raw"),
    limit: int = Query(100, ge=1, le=1000),
) -> dict[str, Any]:
    idx = _index()
    clusters = idx.duplicate_clusters(scope=scope)
    return {
        "scope": scope,
        "total_clusters": len(clusters),
        "limit": limit,
        "items": clusters[:limit],
    }


@app.get("/api/corpus/archive")
async def corpus_archive() -> dict[str, Any]:
    idx = _index()
    return {
        "summary": idx.archive_summary,
        "canonical_summary": idx.canonical_summary,
        "raw_summary": idx.summary,
    }


@app.get("/api/corpus/search")
async def corpus_search(
    q: str = Query(..., min_length=1),
    limit: int = Query(25, ge=1, le=100),
    scope: str = Query("canonical"),
) -> dict[str, Any]:
    idx = _index()
    return {"query": q, "limit": limit, "scope": scope, "results": idx.search(q, limit=limit, scope=scope)}


@app.get("/api/corpus/file/{rel_path:path}")
async def corpus_file(rel_path: str, download: bool = Query(False)) -> Response:
    path = _resolve_relative_path(rel_path)
    idx = _index()
    entry = idx.by_path.get(path.relative_to(REPO_ROOT).as_posix())
    if entry and entry.sensitive:
        raise HTTPException(status_code=403, detail="Redacted file.")

    mime_type, _ = mimetypes.guess_type(path.name)
    if download:
        return FileResponse(path, filename=path.name, media_type=mime_type or "application/octet-stream")

    textual_suffixes = {".md", ".json", ".txt", ".py", ".tex", ".yaml", ".yml", ".toml", ".cfg", ".html", ".htm"}
    if (mime_type and mime_type.startswith("text/")) or path.suffix.lower() in textual_suffixes:
        text = path.read_text(encoding="utf-8", errors="replace")
        media = mime_type or "text/plain; charset=utf-8"
        if path.suffix.lower() == ".json":
            try: return JSONResponse(json.loads(text))
            except Exception: pass
        return PlainTextResponse(text, media_type=media)

    return FileResponse(path, media_type=mime_type or "application/octet-stream")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse("static/img/logo.svg")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8492))
    uvicorn.run(app, host="0.0.0.0", port=port)
