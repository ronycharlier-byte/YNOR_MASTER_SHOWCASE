from __future__ import annotations

import html
import json
import mimetypes
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote

from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.encoders import jsonable_encoder
import requests

from corpus_index import REPO_ROOT, load_corpus_index

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    OpenAI = None


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


def _confidence_label(score: float) -> str:
    if score >= 0.82:
        return "High"
    if score >= 0.62:
        return "Medium"
    return "Low"


def _format_money(price: str) -> str:
    return price.replace("EUR", "€").replace(" / ", "/").replace("month", "month")


def _ynor_logo_svg(with_background: bool = False) -> str:
    background = ""
    if with_background:
        background = """
  <rect width="64" height="64" rx="16" fill="#07111f"/>
"""
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" role="img" aria-label="Ynor logo">
  <defs>
    <linearGradient id="ynorGlow" x1="10%" y1="10%" x2="90%" y2="90%">
      <stop offset="0%" stop-color="#c6ecff"/>
      <stop offset="48%" stop-color="#8fd6ff"/>
      <stop offset="100%" stop-color="#4fb8ff"/>
    </linearGradient>
    <linearGradient id="ynorCore" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#eefcff"/>
      <stop offset="100%" stop-color="#76caff"/>
    </linearGradient>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="1.4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
{background}
  <g filter="url(#softGlow)" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 32l20-16 20 16-20 16-20-16Z" stroke="url(#ynorGlow)" stroke-width="1.5" opacity=".92"/>
    <path d="M32 9l15 7v32l-15 7-15-7V16l15-7Z" stroke="url(#ynorGlow)" stroke-width="1.2" opacity=".72"/>
    <path d="M21 17h22M20 25h24M18 39h28M20 47h24" stroke="url(#ynorGlow)" stroke-width="1.35" opacity=".7"/>
    <path d="M28 13c-4.5 5.4-5.8 11.1-5.8 19.2S23.4 48 28 53.5" stroke="url(#ynorGlow)" stroke-width="2.2" opacity=".95"/>
    <path d="M36 13c4.5 5.4 5.8 11.1 5.8 19.2S40.6 48 36 53.5" stroke="url(#ynorGlow)" stroke-width="2.2" opacity=".95"/>
    <path d="M30 15c1.7 2.2 3 4.5 3 7.2s-1.3 5-3 7.2M34 15c-1.7 2.2-3 4.5-3 7.2s1.3 5 3 7.2M30 34c1.7 2.2 3 4.5 3 7.2s-1.3 5-3 7.2M34 34c-1.7 2.2-3 4.5-3 7.2s1.3 5 3 7.2" stroke="url(#ynorCore)" stroke-width="1.7" opacity=".9"/>
    <circle cx="20" cy="20" r="1.2" fill="#c6ecff"/>
    <circle cx="44" cy="20" r="1.2" fill="#c6ecff"/>
    <circle cx="18" cy="44" r="1.2" fill="#c6ecff"/>
    <circle cx="46" cy="44" r="1.2" fill="#c6ecff"/>
    <circle cx="32" cy="11" r="1.1" fill="#eefcff"/>
    <circle cx="32" cy="53" r="1.1" fill="#eefcff"/>
  </g>
</svg>
""".strip()


def _site_shell(title: str, body: str, active: str = "home") -> str:
    nav_items = [
        ("home", "Home", "/"),
        ("chat", "Ask Ynor", "/chat"),
        ("pricing", "Pricing", "/pricing"),
        ("account", "Account", "/account"),
    ]
    nav_html = "".join(
        f'<a class="nav-link{" active" if key == active else ""}" href="{href}">{label}</a>'
        for key, label, href in nav_items
    )
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#07111f" />
  <title>{html.escape(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Cormorant+Garamond:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #07111f;
      --bg-2: #0a1729;
      --panel: rgba(10, 22, 39, 0.84);
      --panel-strong: rgba(8, 18, 33, 0.96);
      --panel-soft: rgba(255,255,255,0.03);
      --line: rgba(123, 183, 255, 0.16);
      --line-strong: rgba(123, 183, 255, 0.28);
      --text: #f4f7fb;
      --muted: #9fb2cc;
      --muted-2: #7890af;
      --accent: #8fd6ff;
      --accent-2: #6eb6ff;
      --accent-3: #c6ecff;
      --shadow: 0 30px 90px rgba(0,0,0,.45);
      --radius-xl: 28px;
      --radius-lg: 22px;
      --radius-md: 16px;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 10% 10%, rgba(110, 182, 255, 0.16), transparent 22%),
        radial-gradient(circle at 90% 8%, rgba(143, 214, 255, 0.12), transparent 18%),
        radial-gradient(circle at 50% 90%, rgba(64, 120, 191, 0.12), transparent 25%),
        linear-gradient(180deg, #050b14 0%, #07111f 46%, #08101c 100%);
      background-attachment: fixed;
    }}
    body::before {{
      content: "";
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,0.022) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.022) 1px, transparent 1px);
      background-size: 44px 44px;
      mask-image: linear-gradient(180deg, rgba(0,0,0,.2), rgba(0,0,0,0));
      pointer-events: none;
      opacity: .48;
    }}
    a {{ color: inherit; text-decoration: none; }}
    a:hover {{ color: var(--accent); }}
    .shell {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 26px 22px 38px;
      position: relative;
      z-index: 1;
    }}
    .topbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      padding: 16px 18px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(7, 17, 31, 0.76);
      backdrop-filter: blur(18px);
      box-shadow: 0 12px 40px rgba(0,0,0,.22);
      position: sticky;
      top: 18px;
      z-index: 5;
    }}
    .brand {{
      display: inline-flex;
      align-items: center;
      gap: 12px;
      font-weight: 700;
      letter-spacing: .04em;
    }}
    .brand-mark {{
      width: 38px;
      height: 38px;
      border-radius: 12px;
      display: grid;
      place-items: center;
      background:
        radial-gradient(circle at 35% 30%, rgba(198,236,255,.36), rgba(198,236,255,0) 42%),
        linear-gradient(180deg, rgba(143,214,255,.24), rgba(143,214,255,.06));
      border: 1px solid rgba(143,214,255,.24);
      box-shadow: inset 0 1px 0 rgba(255,255,255,.08), 0 0 0 1px rgba(255,255,255,.02);
      color: var(--accent-3);
      font-size: 17px;
      overflow: hidden;
    }}
    .brand-mark img {{
      width: 100%;
      height: 100%;
      display: block;
      object-fit: contain;
      padding: 4px;
      filter: drop-shadow(0 0 8px rgba(143,214,255,.28));
    }}
    .brand-name {{ font-size: 18px; }}
    .nav {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: center;
    }}
    .nav-link {{
      padding: 10px 14px;
      border-radius: 999px;
      color: var(--muted);
      border: 1px solid transparent;
      font-weight: 600;
      font-size: 14px;
      transition: 180ms ease;
    }}
    .nav-link:hover, .nav-link.active {{
      color: var(--text);
      background: rgba(255,255,255,.03);
      border-color: var(--line);
    }}
    .cta-pill {{
      padding: 10px 14px;
      border-radius: 999px;
      border: 1px solid rgba(143,214,255,.22);
      background: linear-gradient(180deg, rgba(143,214,255,.14), rgba(143,214,255,.06));
      color: var(--text);
      font-size: 14px;
      font-weight: 700;
      white-space: nowrap;
    }}
    .hero-grid {{
      display: grid;
      grid-template-columns: 1.05fr .95fr;
      gap: 22px;
      margin-top: 22px;
    }}
    .hero, .panel {{
      border: 1px solid var(--line);
      border-radius: var(--radius-xl);
      background: linear-gradient(180deg, rgba(9, 20, 37, .92), rgba(6, 13, 24, .92));
      box-shadow: var(--shadow);
      backdrop-filter: blur(16px);
    }}
    .hero {{
      padding: 34px;
      overflow: hidden;
      position: relative;
    }}
    .hero::after {{
      content: "";
      position: absolute;
      inset: auto -14% -20% auto;
      width: 300px;
      height: 300px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(143,214,255,.18), rgba(143,214,255,0) 68%);
      filter: blur(16px);
      pointer-events: none;
    }}
    .eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      text-transform: uppercase;
      letter-spacing: .26em;
      color: var(--accent);
      font-size: 11px;
      font-weight: 700;
      margin-bottom: 14px;
    }}
    .eyebrow::before {{
      content: "";
      width: 16px;
      height: 1px;
      background: currentColor;
      opacity: .9;
    }}
    .title {{
      margin: 0;
      font-family: "Cormorant Garamond", ui-serif, Georgia, serif;
      font-size: clamp(54px, 6vw, 92px);
      line-height: .92;
      letter-spacing: -.03em;
      font-weight: 600;
      max-width: 10ch;
    }}
    .lead {{
      margin: 16px 0 0;
      font-size: clamp(16px, 1.5vw, 19px);
      line-height: 1.75;
      color: var(--muted);
      max-width: 56ch;
    }}
    .hero-actions {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 26px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      min-height: 46px;
      padding: 0 18px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.02);
      color: var(--text);
      font-weight: 700;
      box-shadow: inset 0 1px 0 rgba(255,255,255,.05);
    }}
    .btn.primary {{
      color: #05101d;
      background: linear-gradient(180deg, var(--accent-3), var(--accent));
      border-color: rgba(198,236,255,.6);
      box-shadow: 0 18px 40px rgba(111, 181, 255, .16);
    }}
    .btn.secondary:hover {{ border-color: var(--line-strong); }}
    .micro {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 18px;
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 13px;
      border-radius: 999px;
      background: rgba(255,255,255,.03);
      border: 1px solid var(--line);
      color: var(--text);
      font-size: 13px;
    }}
    .chip strong {{ color: var(--accent-3); }}
    .surface {{
      border: 1px solid var(--line);
      border-radius: var(--radius-lg);
      background: linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,.015));
    }}
    .stack {{
      display: grid;
      gap: 16px;
    }}
    .feature-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin-top: 18px;
    }}
    .feature {{
      padding: 18px;
    }}
    .feature h3, .section h2, .panel h2 {{
      margin: 0;
      font-size: 20px;
      line-height: 1.15;
    }}
    .feature p, .section p, .panel p {{
      margin: 8px 0 0;
      color: var(--muted);
      line-height: 1.72;
      font-size: 14px;
    }}
    .icon {{
      width: 38px;
      height: 38px;
      border-radius: 12px;
      display: grid;
      place-items: center;
      background: rgba(143,214,255,.08);
      border: 1px solid rgba(143,214,255,.16);
      color: var(--accent-3);
      margin-bottom: 14px;
      font-size: 16px;
    }}
    .section {{
      margin-top: 22px;
      padding: 24px;
    }}
    .section-head {{
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: 18px;
      margin-bottom: 16px;
    }}
    .kicker {{
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: .24em;
      font-size: 11px;
      font-weight: 700;
      margin-bottom: 8px;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }}
    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }}
    .grid-4 {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }}
    .card {{
      padding: 18px;
      border-radius: var(--radius-lg);
      border: 1px solid var(--line);
      background: rgba(255,255,255,.02);
    }}
    .card.featured {{
      background: linear-gradient(180deg, rgba(143,214,255,.10), rgba(255,255,255,.03));
      border-color: rgba(143,214,255,.28);
      box-shadow: 0 18px 45px rgba(111, 181, 255, .12);
    }}
    .card .price {{
      font-size: 32px;
      font-weight: 800;
      letter-spacing: -.04em;
      margin: 4px 0 10px;
    }}
    .card .muted {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.7;
    }}
    .card ul {{
      margin: 14px 0 0;
      padding: 0;
      list-style: none;
      display: grid;
      gap: 10px;
      color: var(--text);
      font-size: 14px;
    }}
    .card li::before {{
      content: "•";
      color: var(--accent);
      margin-right: 8px;
    }}
    .prompt-bar {{
      display: flex;
      gap: 12px;
      padding: 14px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.02);
    }}
    .prompt-bar input, .prompt-bar textarea {{
      flex: 1;
      border: 0;
      background: transparent;
      color: var(--text);
      font: inherit;
      outline: none;
      padding: 0 4px;
      resize: none;
      min-height: 22px;
    }}
    .prompt-bar button {{
      border: 0;
      color: #05101d;
      background: linear-gradient(180deg, var(--accent-3), var(--accent));
      padding: 12px 18px;
      border-radius: 999px;
      font-weight: 800;
      cursor: pointer;
    }}
    .chat-panel {{
      min-height: 620px;
      display: grid;
      grid-template-rows: auto 1fr auto;
      overflow: hidden;
    }}
    .chat-stream {{
      padding: 20px;
      display: grid;
      gap: 14px;
      align-content: start;
      max-height: 760px;
      overflow: auto;
    }}
    .bubble {{
      max-width: 92%;
      padding: 16px 18px;
      border-radius: 22px;
      border: 1px solid var(--line);
      line-height: 1.72;
      white-space: pre-wrap;
      background: rgba(255,255,255,.025);
    }}
    .bubble.user {{
      margin-left: auto;
      background: linear-gradient(180deg, rgba(111, 181, 255,.18), rgba(111, 181, 255,.08));
      border-color: rgba(143,214,255,.26);
    }}
    .bubble.assistant {{
      background: rgba(9, 20, 37, .9);
    }}
    .bubble .sources {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
    }}
    .source-chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 10px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.03);
      font-size: 12px;
      color: var(--muted);
    }}
    .source-chip strong {{ color: var(--text); }}
    .assistant-meta {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }}
    .toggle {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      color: var(--muted);
    }}
    .toggle input {{
      width: 18px;
      height: 18px;
      accent-color: var(--accent);
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.03);
      color: var(--muted);
      font-size: 12px;
    }}
    .badge.high {{ color: #b7f6d4; border-color: rgba(183,246,212,.18); }}
    .badge.medium {{ color: #e2e5ff; }}
    .badge.low {{ color: #ffd8d8; }}
    .footer {{
      margin-top: 18px;
      color: var(--muted-2);
      font-size: 12px;
      line-height: 1.7;
    }}
    .mono {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      word-break: break-word;
    }}
    .muted {{ color: var(--muted); }}
    .small {{ font-size: 13px; color: var(--muted); line-height: 1.7; }}
    .mt-8 {{ margin-top: 8px; }}
    .mt-12 {{ margin-top: 12px; }}
    .mt-16 {{ margin-top: 16px; }}
    .mt-20 {{ margin-top: 20px; }}
    .mt-24 {{ margin-top: 24px; }}
    .mb-0 {{ margin-bottom: 0; }}
    .section-links {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}
    @media (max-width: 1180px) {{
      .hero-grid, .grid-4, .grid-3, .grid-2, .feature-grid {{ grid-template-columns: 1fr; }}
      .topbar {{ border-radius: 24px; flex-wrap: wrap; }}
      .nav {{ justify-content: flex-start; }}
    }}
    @media (max-width: 700px) {{
      .shell {{ padding: 14px 12px 28px; }}
      .hero, .section, .panel {{ border-radius: 22px; }}
      .hero {{ padding: 24px; }}
      .title {{ max-width: 8ch; }}
      .chat-panel {{ min-height: 520px; }}
      .bubble {{ max-width: 100%; }}
      .topbar {{
        position: static;
        padding: 14px 16px;
        gap: 12px;
      }}
      .nav-link, .cta-pill {{ font-size: 13px; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <header class="topbar">
      <a href="/" class="brand" aria-label="Ynor home">
        <span class="brand-mark"><img src="/ynor-logo.svg" alt="" aria-hidden="true" /></span>
        <span class="brand-name">Ynor</span>
      </a>
      <nav class="nav" aria-label="Primary">
        {nav_html}
      </nav>
      <a class="cta-pill" href="/chat">Start your session</a>
    </header>
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


def _duckduckgo_search(query: str, limit: int = 5) -> list[dict[str, str]]:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"}
    candidates: list[dict[str, str]] = []

    try:
      from bs4 import BeautifulSoup  # type: ignore
    except Exception:
        BeautifulSoup = None  # type: ignore

    try:
        response = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        if BeautifulSoup is not None:
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
    score = 0.56
    score += min(corpus_hits, 6) * 0.055
    score += min(web_hits, 5) * 0.03
    if used_model:
        score += 0.08
    if brief_mode:
        score += 0.02
    return max(0.15, min(score, 0.97))


def _render_context_block(label: str, items: list[dict[str, str]]) -> str:
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
    model_name = os.getenv("YNOR_MODEL", "gpt-5.2")
    api_key = os.getenv("OPENAI_API_KEY")
    if OpenAI is not None and api_key:
        try:
            client = OpenAI(api_key=api_key)
            system = (
                "You are Ynor, a premium AI assistant. "
                "Answer using the supplied corpus context and web context. "
                "Prefer the corpus for foundational claims and the web for current context. "
                "Use concise executive phrasing by default. "
                "If Brief Mode is enabled, keep the answer especially compact, decision-oriented, and structured. "
                "Cite sources inline with [1], [2], etc. when useful. "
                "Never invent sources. "
                "If the evidence is weak, say so clearly. "
                "Return plain text with short sections and bullets when helpful."
            )
            user_prompt = f"""
Question:
{query}

{_render_context_block('Corpus context', corpus_sources)}

{_render_context_block('Web context', web_sources)}
""".strip()
            if brief_mode:
                user_prompt += "\n\nBrief Mode: On. Deliver a concise executive summary with strict source confidence."
            completion = client.chat.completions.create(
                model=model_name,
                temperature=0.2,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_prompt},
                ],
            )
            content = completion.choices[0].message.content or ""
            return content.strip(), True
        except Exception as exc:
            fallback_notice = f"Ynor assistant fallback engaged due to model error: {exc}"
            if brief_mode:
                fallback_notice = "Brief Mode fallback engaged."
            return fallback_notice, False

    combined = []
    if corpus_sources:
        combined.append("Corpus grounding:")
        for i, item in enumerate(corpus_sources[:3], start=1):
            combined.append(f"{i}. {item['title']} — {item['snippet'][:220]}")
    if web_sources:
        combined.append("Internet context:")
        for i, item in enumerate(web_sources[:3], start=1):
            combined.append(f"{i}. {item['title']} — {item['snippet'][:220]}")
    if brief_mode:
        answer = (
            "Executive summary:\n"
            f"{query}\n\n"
            + "\n".join(combined[:8])
            + "\n\nRecommended next step: use the strongest corpus reference first, then validate against live web context if the question is time-sensitive."
        )
    else:
        answer = (
            f"Question: {query}\n\n"
            + "\n".join(combined or ["No context found."])
            + "\n\nYnor synthesis: the assistant should blend corpus evidence with live web context, prioritizing direct evidence and clear source references."
        )
    return answer, False


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def corpus_home() -> str:
    idx = _index()
    summary = idx.summary
    total_files = summary["total_files"]
    text_files = summary["text_files"]
    redacted = summary["sensitive_files_redacted"]
    root_path = html.escape(summary["root"])
    recent_cards = "".join(_render_entry_card(entry) for entry in idx.entries[:6])
    entrypoints = [
        ("Ask Ynor", "/chat"),
        ("Pricing", "/pricing"),
        ("Account", "/account"),
        ("Onboarding", "/onboarding"),
    ]
    entrypoint_html = "".join(
        f'<a class="btn secondary" href="{href}">{label}</a>' for label, href in entrypoints
    )
    body = f"""
    <section class="hero-grid">
      <div class="hero">
        <div class="eyebrow">Ynor / premium intelligence platform</div>
        <h1 class="title">Precision begins here.</h1>
        <p class="lead">
          Ynor turns the MDL Ynor corpus and live internet knowledge into a premium conversational
          intelligence experience. Ask naturally, receive precise answers, and keep the interface calm,
          fast, and editorial.
        </p>
        <div class="hero-actions">
          <a class="btn primary" href="/chat">Start your session</a>
          <a class="btn secondary" href="/pricing">View plans</a>
        </div>
        <div class="micro">
          <span class="chip">Live internet layer</span>
          <span class="chip">Corpus grounding</span>
          <span class="chip">Brief Mode ready</span>
          <span class="chip">PWA installable</span>
        </div>
      </div>
      <div class="panel chat-panel">
        <div class="section-head" style="padding:24px 24px 0;">
          <div>
            <div class="kicker">Live assistant preview</div>
            <h2>Ask. Understand. Act.</h2>
          </div>
          <span class="badge high">0.91 • High</span>
        </div>
        <div class="chat-stream">
          <div class="bubble user">How does Ynor blend corpus knowledge with live internet context?</div>
          <div class="bubble assistant">
Ynor combines corpus grounding with live web retrieval behind the scenes, then answers with source-aware reasoning.

<div class="sources">
  <span class="source-chip"><strong>[1]</strong> Corpus evidence</span>
  <span class="source-chip"><strong>[2]</strong> Live web context</span>
</div>
          </div>
          <div class="bubble assistant">Brief Mode is available for executive summaries with stricter confidence scoring.</div>
        </div>
        <div style="padding: 0 20px 20px;">
          <div class="prompt-bar">
            <input value="Ask a question about the MDL Ynor corpus..." aria-label="Prompt preview" />
            <button onclick="location.href='/chat'">Open chat</button>
          </div>
        </div>
      </div>
    </section>

    <section class="section surface">
      <div class="section-head">
        <div>
          <div class="kicker">Why Ynor</div>
          <h2>Built to feel faster, calmer, and sharper than standard AI products.</h2>
        </div>
        <div class="section-links">
          {entrypoint_html}
        </div>
      </div>
      <div class="feature-grid">
        <div class="card feature">
          <div class="icon">✦</div>
          <h3>Premium chat-first experience</h3>
          <p>The assistant is the product. The corpus and internet support it behind the scenes.</p>
        </div>
        <div class="card feature">
          <div class="icon">⟡</div>
          <h3>Source-aware intelligence</h3>
          <p>Responses stay grounded in corpus evidence, with live web context when relevance matters.</p>
        </div>
        <div class="card feature">
          <div class="icon">◌</div>
          <h3>Blue nuit editorial design</h3>
          <p>Midnight-blue atmosphere, luxury typography, and a calm premium tone throughout.</p>
        </div>
      </div>
    </section>

    <section class="section surface">
      <div class="section-head">
        <div>
          <div class="kicker">Corpus status</div>
          <h2>Live confidence signals from the indexed corpus.</h2>
        </div>
        <a class="btn secondary" href="/api/corpus/status">API status</a>
      </div>
      <div class="grid-4">
        <div class="card"><div class="kicker">Corpus</div><div class="price">{total_files}</div><div class="muted">Indexed files</div></div>
        <div class="card"><div class="kicker">Text</div><div class="price">{text_files}</div><div class="muted">Readable files</div></div>
        <div class="card"><div class="kicker">Redacted</div><div class="price">{redacted}</div><div class="muted">Sensitive files masked</div></div>
        <div class="card"><div class="kicker">Root</div><div class="price" style="font-size:18px; line-height:1.3;">YNOR</div><div class="muted mono">{root_path}</div></div>
      </div>
    </section>

    <section class="section surface">
      <div class="section-head">
        <div>
          <div class="kicker">Pricing preview</div>
          <h2>Four premium tiers designed to scale from entry to flagship.</h2>
        </div>
        <a class="btn secondary" href="/pricing">See all plans</a>
      </div>
      <div class="grid-4">
        <div class="card">
          <div class="kicker">Essential</div>
          <div class="price">€9<span style="font-size:16px; color:var(--muted);">/month</span></div>
          <div class="muted">A refined entry point into the Ynor experience.</div>
        </div>
        <div class="card">
          <div class="kicker">Plus</div>
          <div class="price">€29<span style="font-size:16px; color:var(--muted);">/month</span></div>
          <div class="muted">For regular users who want more depth and continuity.</div>
        </div>
        <div class="card">
          <div class="kicker">Pro</div>
          <div class="price">€79<span style="font-size:16px; color:var(--muted);">/month</span></div>
          <div class="muted">For advanced users who require stronger reasoning.</div>
        </div>
        <div class="card">
          <div class="kicker">Elite</div>
          <div class="price">€199<span style="font-size:16px; color:var(--muted);">/month</span></div>
          <div class="muted">Flagship access with maximum continuity and trust.</div>
        </div>
      </div>
    </section>

    <section class="section surface">
      <div class="section-head">
        <div>
          <div class="kicker">Recent corpus files</div>
          <h2>A curated view of the corpus surface.</h2>
        </div>
        <a class="btn secondary" href="/api/corpus/files">Browse API</a>
      </div>
      <div class="grid-2">
        <div class="stack">{recent_cards}</div>
        <div class="card">
          <div class="kicker">Chiastic axis</div>
          <h3 class="mb-0">A → B → C → X → C' → B' → A'</h3>
          <p>Foundation, theory, engines, memory, validation, governance, archives.</p>
          <div class="footer">
            API surfaces:
            <a href="/api/corpus/summary"> summary</a>,
            <a href="/api/corpus/search?q=Ynor"> search</a>,
            <a href="/api/corpus/entrypoints"> entrypoints</a>,
            <a href="/docs"> docs</a>
          </div>
        </div>
      </div>
    </section>
    """
    return _site_shell("Ynor | Premium Intelligence", body, active="home")


@app.get("/corpus", response_class=HTMLResponse, include_in_schema=False)
async def corpus_alias() -> str:
    return await corpus_home()


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Response:
    return Response(content=_ynor_logo_svg(with_background=True), media_type="image/svg+xml")


@app.get("/ynor-logo.svg", include_in_schema=False)
async def ynor_logo() -> Response:
    return Response(content=_ynor_logo_svg(with_background=False), media_type="image/svg+xml")


def _pricing_cards() -> str:
    tiers = [
        ("Essential", "€9/month", "A refined entry point into the Ynor experience.", ["Limited monthly questions", "Standard AI responses", "Basic corpus grounding", "Basic chat history"], False),
        ("Plus", "€29/month", "For regular users who want more depth and continuity.", ["More monthly questions", "Improved response quality", "Longer chat history", "Better context handling", "Faster answers"], False),
        ("Pro", "€79/month", "For advanced users who require stronger reasoning and deeper intelligence.", ["Advanced AI responses", "Deeper context retrieval", "Priority access", "Source references when relevant", "Priority support"], False),
        ("Elite", "€199/month", "The flagship experience for maximum continuity and trust.", ["Full access", "Highest question limits", "Best reasoning and response quality", "Maximum context depth", "Concierge-level support"], True),
    ]
    cards = []
    for title, price, desc, features, featured in tiers:
        card_class = "card" + (" featured" if featured else "")
        cards.append(
            f"""
            <div class="{card_class}">
              <div class="kicker">{html.escape(title)}</div>
              <div class="price">{html.escape(price)}</div>
              <div class="muted">{html.escape(desc)}</div>
              <ul>{''.join(f'<li>{html.escape(item)}</li>' for item in features)}</ul>
            </div>
            """
        )
    return "".join(cards)


@app.get("/chat", response_class=HTMLResponse, include_in_schema=False)
async def chat_page() -> str:
    body = """
    <section class="hero-grid">
      <div class="panel chat-panel" style="grid-column: 1 / -1;">
        <div class="section-head" style="padding:24px 24px 0;">
          <div>
            <div class="kicker">Ask Ynor</div>
            <h2>Chat with a premium intelligence assistant.</h2>
            <p>Hybrid answers combine the MDL Ynor corpus with live internet context, then stream back with source-aware citations.</p>
          </div>
          <div class="section-links">
            <span class="badge high" id="confidenceBadge">0.84 • High</span>
            <label class="toggle"><input id="briefMode" type="checkbox" /> Brief Mode</label>
          </div>
        </div>
        <div class="chat-stream" id="chatStream" aria-live="polite"></div>
        <div style="padding: 0 20px 20px;">
          <div class="prompt-bar">
            <textarea id="chatInput" rows="1" placeholder="Ask a question about the MDL Ynor corpus or current internet context..."></textarea>
            <button id="sendBtn" onclick="sendMessage()">Send</button>
          </div>
          <div class="micro mt-12">
            <button class="chip" type="button" onclick="setPrompt('Summarize the MDL Ynor corpus in executive language.')">Summarize</button>
            <button class="chip" type="button" onclick="setPrompt('What are the strongest premium features of Ynor?')">Explain</button>
            <button class="chip" type="button" onclick="setPrompt('Compare the subscription tiers and recommend one.')">Compare</button>
            <button class="chip" type="button" onclick="setPrompt('Find source material related to the latest question.')">Find sources</button>
          </div>
        </div>
      </div>
    </section>

    <section class="section surface">
      <div class="section-head">
        <div>
          <div class="kicker">Assistant rules</div>
          <h2>Brief Mode is optional. Confidence is explicit.</h2>
        </div>
        <a class="btn secondary" href="/pricing">View plans</a>
      </div>
      <div class="grid-3">
        <div class="card">
          <div class="kicker">Brief Mode</div>
          <div class="muted">Returns concise executive summaries with stricter confidence scoring. Best for decision-making.</div>
        </div>
        <div class="card">
          <div class="kicker">Sources</div>
          <div class="muted">Corpus references and web context appear as chips below the answer when relevant.</div>
        </div>
        <div class="card">
          <div class="kicker">Memory</div>
          <div class="muted">History is saved locally for this phase and can later be upgraded to persistent account memory.</div>
        </div>
      </div>
    </section>

    <script>
      const storageKey = "ynor_chat_history";
      const briefKey = "ynor_brief_mode";
      const chatStream = document.getElementById("chatStream");
      const chatInput = document.getElementById("chatInput");
      const sendBtn = document.getElementById("sendBtn");
      const briefMode = document.getElementById("briefMode");
      const confidenceBadge = document.getElementById("confidenceBadge");
      let messages = JSON.parse(localStorage.getItem(storageKey) || "[]");
      briefMode.checked = localStorage.getItem(briefKey) === "true";

      function escapeHtml(value) {
        return String(value)
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;")
          .replaceAll('"', "&quot;")
          .replaceAll("'", "&#39;");
      }

      function renderMessages() {
        chatStream.innerHTML = "";
        if (!messages.length) {
          chatStream.innerHTML = `
            <div class="bubble assistant">
              Your private intelligence workspace is ready.<br><br>
              Ask a question, and Ynor will combine corpus grounding with live web context.
            </div>
          `;
          return;
        }
        chatStream.innerHTML = messages.map(renderMessage).join("");
        chatStream.scrollTop = chatStream.scrollHeight;
      }

      function renderMessage(message) {
        const role = message.role === "user" ? "user" : "assistant";
        const sources = (message.sources || []).map((source, index) => `
          <a class="source-chip" href="${escapeHtml(source.url || "#")}" target="_blank" rel="noreferrer">
            <strong>[${index + 1}]</strong> ${escapeHtml(source.title || "Source")}
          </a>
        `).join("");
        const meta = message.confidence_label ? `
          <div class="assistant-meta">
            <span class="badge ${message.confidence_label.toLowerCase()}">${escapeHtml(message.confidence_score)} • ${escapeHtml(message.confidence_label)}</span>
          </div>
        ` : "";
        const sourceBlock = sources ? `<div class="sources">${sources}</div>` : "";
        return `
          <div class="bubble ${role}">
            ${escapeHtml(message.content)}
            ${meta}
            ${sourceBlock}
          </div>
        `;
      }

      function persist() {
        localStorage.setItem(storageKey, JSON.stringify(messages));
      }

      function setPrompt(text) {
        chatInput.value = text;
        chatInput.focus();
      }

      briefMode.addEventListener("change", () => {
        localStorage.setItem(briefKey, String(briefMode.checked));
      });

      chatInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
          event.preventDefault();
          sendMessage();
        }
      });

      async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        messages.push({ role: "user", content: text });
        messages.push({ role: "assistant", content: "Thinking across corpus and live web context..." });
        persist();
        renderMessages();
        chatInput.value = "";
        sendBtn.disabled = true;

        try {
          const response = await fetch("/api/assistant/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              messages: messages.filter((item) => item.content !== "Thinking across corpus and live web context..."),
              brief_mode: briefMode.checked,
            }),
          });
          const payload = await response.json();
          messages.pop();
          messages.push({
            role: "assistant",
            content: payload.answer || "No answer returned.",
            sources: payload.sources || [],
            confidence_score: payload.confidence_score,
            confidence_label: payload.confidence_label,
          });
          confidenceBadge.textContent = `${payload.confidence_score || "0.00"} • ${payload.confidence_label || "Low"}`;
          confidenceBadge.className = `badge ${(payload.confidence_label || "low").toLowerCase()}`;
        } catch (error) {
          messages.pop();
          messages.push({
            role: "assistant",
            content: `The assistant is temporarily unavailable. ${String(error)}`,
            sources: [],
            confidence_score: "0.00",
            confidence_label: "Low",
          });
        } finally {
          persist();
          renderMessages();
          sendBtn.disabled = false;
        }
      }

      window.setPrompt = setPrompt;
      window.sendMessage = sendMessage;
      renderMessages();
    </script>
    """
    return _site_shell("Ynor | Ask", body, active="chat")


@app.get("/pricing", response_class=HTMLResponse, include_in_schema=False)
async def pricing_page() -> str:
    body = f"""
    <section class="hero">
      <div class="eyebrow">Subscription plans</div>
      <h1 class="title" style="max-width: 12ch;">Select your tier of intelligence.</h1>
      <p class="lead">From Essential to Elite, each tier is designed to scale access, depth, continuity, and trust.</p>
      <div class="hero-actions">
        <a class="btn primary" href="/chat">Start your session</a>
        <a class="btn secondary" href="/">Back home</a>
      </div>
    </section>
    <section class="section surface">
      <div class="grid-4">
        {_pricing_cards()}
      </div>
    </section>
    <section class="section surface">
      <div class="section-head">
        <div>
          <div class="kicker">Why upgrade</div>
          <h2>Higher tiers unlock stronger reasoning, deeper context, and more continuity.</h2>
        </div>
      </div>
      <div class="grid-3">
        <div class="card"><div class="kicker">Speed</div><div class="muted">Shorter paths to answers, less friction, faster decision support.</div></div>
        <div class="card"><div class="kicker">Depth</div><div class="muted">Deeper corpus retrieval, broader context, and richer explanation quality.</div></div>
        <div class="card"><div class="kicker">Trust</div><div class="muted">Confidence scoring, source chips, and citation-aware answers.</div></div>
      </div>
    </section>
    """
    return _site_shell("Ynor | Pricing", body, active="pricing")


@app.get("/account", response_class=HTMLResponse, include_in_schema=False)
async def account_page() -> str:
    body = """
    <section class="hero-grid">
      <div class="hero">
        <div class="eyebrow">Account</div>
        <h1 class="title" style="max-width: 10ch;">Your private workspace.</h1>
        <p class="lead">Plan status, chat history, and usage controls are staged for this phase, ready for persistence and billing upgrades.</p>
        <div class="hero-actions">
          <a class="btn primary" href="/pricing">Upgrade plan</a>
          <a class="btn secondary" href="/chat">Open chat</a>
        </div>
      </div>
      <div class="panel">
        <div class="section-head" style="padding:24px 24px 0;">
          <div>
            <div class="kicker">Current plan</div>
            <h2>Elite</h2>
            <p>Mocked billing flow for this phase.</p>
          </div>
          <span class="badge high">Active</span>
        </div>
        <div class="grid-2" style="padding:20px;">
          <div class="card"><div class="kicker">Usage</div><div class="price">128</div><div class="muted">Questions this month</div></div>
          <div class="card"><div class="kicker">History</div><div class="price">Local</div><div class="muted">Saved on device until persistent auth lands</div></div>
        </div>
      </div>
    </section>
    <section class="section surface">
      <div class="section-head">
        <div>
          <div class="kicker">Account roadmap</div>
          <h2>Billing is mocked for now, with Stripe and persistent memory ready for the next phase.</h2>
        </div>
      </div>
      <div class="grid-3">
        <div class="card"><div class="kicker">Phase 1</div><div class="muted">Premium UI, chat-first assistant, local history, staged billing.</div></div>
        <div class="card"><div class="kicker">Phase 2</div><div class="muted">Stripe checkout, webhooks, and subscription management.</div></div>
        <div class="card"><div class="kicker">Phase 3</div><div class="muted">Persistent memory, team accounts, and advanced plan analytics.</div></div>
      </div>
    </section>
    """
    return _site_shell("Ynor | Account", body, active="account")


@app.get("/onboarding", response_class=HTMLResponse, include_in_schema=False)
async def onboarding_page() -> str:
    body = """
    <section class="hero-grid">
      <div class="hero">
        <div class="eyebrow">Onboarding</div>
        <h1 class="title" style="max-width: 12ch;">Start in one screen.</h1>
        <p class="lead">Ask a question, get a premium answer grounded in corpus knowledge and live web context, then keep going with confidence.</p>
        <div class="hero-actions">
          <a class="btn primary" href="/chat">Continue</a>
          <a class="btn secondary" href="/">Skip to home</a>
        </div>
      </div>
      <div class="panel">
        <div class="section-head" style="padding:24px 24px 0;">
          <div>
            <div class="kicker">How to use Ynor</div>
            <h2>Ask naturally. Read clearly. Act decisively.</h2>
          </div>
        </div>
        <div class="chat-stream" style="padding-top:12px;">
          <div class="bubble user">What makes Ynor different?</div>
          <div class="bubble assistant">Ynor blends live internet context with your MDL corpus and returns concise, source-aware answers in a premium interface.</div>
        </div>
      </div>
    </section>
    <section class="section surface">
      <div class="grid-3">
        <div class="card"><div class="kicker">1</div><div class="muted">Choose a question or quick action.</div></div>
        <div class="card"><div class="kicker">2</div><div class="muted">Allow the assistant to blend corpus and live web context.</div></div>
        <div class="card"><div class="kicker">3</div><div class="muted">Use the answer with citations, confidence, and next steps.</div></div>
      </div>
    </section>
    """
    return _site_shell("Ynor | Onboarding", body, active="home")


@app.post("/api/assistant/chat")
async def assistant_chat(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    messages = payload.get("messages") or []
    brief_mode = bool(payload.get("brief_mode", False))
    user_messages = [message for message in messages if isinstance(message, dict) and message.get("role") == "user" and message.get("content")]
    query = str(user_messages[-1]["content"]).strip() if user_messages else ""
    if not query:
        raise HTTPException(status_code=400, detail="A user message is required.")

    idx = _index()
    corpus_results = idx.search(query, limit=6)
    preferred_paths = [
        "00_HOMEPAGE/HOMEPAGE_DU_CORPUS.md",
        "00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md",
        "00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md",
        "00_MASTER_FINAL/MASTER_FINAL.md",
        "00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md",
    ]
    if not corpus_results:
        tokens = [token for token in re.findall(r"[A-Za-z0-9']+", query) if len(token) > 2]
        for token in tokens:
            corpus_results = idx.search(token, limit=6)
            if corpus_results:
                break
    generic_query = "ynor" in query.lower() and len(query.split()) <= 4
    if not corpus_results:
        corpus_results = idx.search("Ynor", limit=6) or idx.search("MDL", limit=6)
    if generic_query:
        corpus_results = []
        for anchor in preferred_paths[:4]:
            entry = idx.by_path.get(anchor)
            if entry:
                corpus_results.append(entry.to_dict())

    def _rank(item: dict[str, Any]) -> tuple[int, int, str]:
        path = str(item.get("path", ""))
        anchor_rank = len(preferred_paths) + 1
        for idx_priority, anchor in enumerate(preferred_paths):
            if path.endswith(anchor):
                anchor_rank = idx_priority
                break
        return (anchor_rank, -int(item.get("score", 0)), path)

    corpus_results = sorted(corpus_results, key=_rank)
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
    if brief_mode and len(answer) > 1200:
        answer = answer[:1200].rstrip() + "..."
    return {
        "query": query,
        "brief_mode": brief_mode,
        "answer": answer,
        "sources": corpus_sources[:3] + web_sources[:3],
        "confidence_score": f"{confidence_score:.2f}",
        "confidence_label": confidence_label,
        "used_model": used_model,
    }


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
