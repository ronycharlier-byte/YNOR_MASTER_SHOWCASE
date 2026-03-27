from __future__ import annotations

import os
from datetime import datetime
from typing import Any
from urllib.parse import quote

import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go


DEFAULT_API_BASE = os.getenv("YNOR_API_BASE_URL", "http://localhost:8492").rstrip("/")


st.set_page_config(page_title="MDL Ynor Corpus Dashboard", layout="wide")


def _api_get(base_url: str, path: str, timeout: float = 10.0) -> Any:
    response = requests.get(f"{base_url}{path}", timeout=timeout)
    response.raise_for_status()
    return response.json()


def _api_text(base_url: str, path: str, timeout: float = 10.0) -> str:
    response = requests.get(f"{base_url}{path}", timeout=timeout)
    response.raise_for_status()
    return response.text


def _api_health(base_url: str) -> dict[str, Any]:
    try:
        payload = _api_get(base_url, "/api/corpus/status", timeout=5.0)
        if isinstance(payload, dict):
            return {"ok": True, "payload": payload}
        return {"ok": False, "error": "Unexpected payload"}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def _safe_df(items: list[dict[str, Any]]) -> pd.DataFrame:
    if not items:
        return pd.DataFrame(columns=["path", "kind", "size_bytes", "score"])
    return pd.DataFrame(items)


st.title("MDL Ynor Corpus Dashboard")
st.caption("Streamlit view connected to the unified corpus API.")

with st.sidebar:
    st.header("Connection")
    api_base = st.text_input("API base URL", value=DEFAULT_API_BASE)
    st.divider()
    st.subheader("Search")
    search_query = st.text_input("Corpus query", value="MASTER FINAL")
    search_limit = st.slider("Results", min_value=5, max_value=50, value=12)
    st.divider()
    st.subheader("Browse")
    node_choice = st.selectbox("Node", ["A", "B", "C", "X", "C'", "B'", "A'"], index=2)
    top_limit = st.slider("Files per page", min_value=10, max_value=200, value=20)
    file_query = st.text_input("File filter", value="")
    preview_limit = st.slider("Preview chars", min_value=200, max_value=5000, value=1200, step=100)


health = _api_health(api_base)
col1, col2, col3, col4 = st.columns(4)

if health["ok"]:
    payload = health["payload"]
    col1.metric("Status", payload.get("status", "ONLINE"))
    col2.metric("Files", payload.get("total_files", 0))
    col3.metric("Text files", payload.get("text_files", 0))
    col4.metric("Sensitive redacted", payload.get("sensitive_files_redacted", 0))
else:
    col1.metric("Status", "OFFLINE")
    col2.metric("Files", "0")
    col3.metric("Text files", "0")
    col4.metric("Sensitive redacted", "0")

if not health["ok"]:
    st.error(f"Cannot reach API at {api_base}: {health['error']}")
    st.stop()


summary = _api_get(api_base, "/api/corpus/summary")
nodes = _api_get(api_base, "/api/corpus/nodes")
entrypoints = _api_get(api_base, "/api/corpus/entrypoints")

summary_payload = summary.get("summary", {})
chiastic_axis = summary.get("chiastic_axis", [])

left, right = st.columns([1.1, 0.9])

with left:
    st.subheader("Corpus summary")
    st.write("Chiastic axis:", " -> ".join(chiastic_axis) if chiastic_axis else "n/a")
    st.json(
        {
            "root": summary_payload.get("root"),
            "total_files": summary_payload.get("total_files"),
            "text_files": summary_payload.get("text_files"),
            "binary_or_other_files": summary_payload.get("binary_or_other_files"),
            "sensitive_files_redacted": summary_payload.get("sensitive_files_redacted"),
        }
    )

with right:
    st.subheader("Node counts")
    node_df = pd.DataFrame(
        [{"node": k, "count": v} for k, v in nodes.get("top_level_counts", {}).items()]
    )
    if not node_df.empty:
        st.bar_chart(node_df.set_index("node"))
    else:
        st.info("No node data available.")


st.divider()

search_col, browse_col = st.columns([1, 1])

with search_col:
    st.subheader("Search results")
    if search_query:
        try:
            results = _api_get(
                api_base,
                f"/api/corpus/search?q={quote(search_query)}&limit={search_limit}",
            )
            result_df = _safe_df(results.get("results", []))
            st.dataframe(
                result_df[
                    [c for c in ["path", "kind", "size_bytes", "score", "sensitive"] if c in result_df.columns]
                ],
                use_container_width=True,
                hide_index=True,
            )
            if not result_df.empty and "preview" in result_df.columns:
                preview_choice = st.selectbox(
                    "Preview result",
                    options=result_df["path"].tolist(),
                    index=0,
                )
                selected = result_df[result_df["path"] == preview_choice].iloc[0].to_dict()
                st.code(selected.get("preview", "[no preview]"), language="text")
        except Exception as exc:
            st.error(f"Search failed: {exc}")
    else:
        st.info("Enter a search query in the sidebar.")

with browse_col:
    st.subheader(f"Node browser: {node_choice}")
    try:
        node_payload = _api_get(api_base, f"/api/corpus/node/{quote(node_choice)}")
        node_items = node_payload.get("items", [])
        node_df = _safe_df(node_items)
        st.write(f"Files in node: {node_payload.get('count', 0)}")
        if not node_df.empty:
            columns = [c for c in ["path", "kind", "size_bytes", "modified_ts", "sensitive"] if c in node_df.columns]
            st.dataframe(node_df[columns], use_container_width=True, hide_index=True)

            file_choice = st.selectbox(
                "Inspect file",
                options=node_df["path"].tolist(),
                index=0,
            )
            preview = _api_get(api_base, f"/api/corpus/preview/{quote(file_choice, safe='/')}")
            st.json(preview)
        else:
            st.info("No files in this node.")
    except Exception as exc:
        st.error(f"Node browsing failed: {exc}")


st.divider()

st.subheader("Entry points")
entry_items = entrypoints.get("items", [])
if entry_items:
    ep_df = pd.DataFrame(entry_items)
    st.dataframe(ep_df, use_container_width=True, hide_index=True)

st.subheader("Recent files")
try:
    files_payload = _api_get(api_base, f"/api/corpus/files?limit={top_limit}&offset=0")
    files_df = _safe_df(files_payload.get("items", []))
    if not files_df.empty:
        st.dataframe(
            files_df[[c for c in ["path", "kind", "size_bytes", "modified_ts", "sensitive"] if c in files_df.columns]],
            use_container_width=True,
            hide_index=True,
        )
except Exception as exc:
    st.warning(f"Unable to load file list: {exc}")


st.divider()
st.subheader("Quick visual")

manifest_count = len(summary.get("manifests", [])) if isinstance(summary, dict) else 0
chart_df = pd.DataFrame(
    [
        {"metric": "files", "value": summary_payload.get("total_files", 0)},
        {"metric": "text", "value": summary_payload.get("text_files", 0)},
        {"metric": "manifests", "value": manifest_count},
        {"metric": "entrypoints", "value": len(entry_items)},
    ]
)

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=chart_df["metric"],
        y=chart_df["value"],
        marker_color=["#7dd3fc", "#86efac", "#fbbf24", "#c084fc"],
    )
)
fig.update_layout(
    template="plotly_dark",
    height=320,
    margin=dict(l=20, r=20, t=20, b=20),
    yaxis_title="Count",
)
st.plotly_chart(fig, use_container_width=True)

st.caption(f"Last refreshed: {datetime.now().isoformat(timespec='seconds')}")

st.divider()
st.subheader("Visual explorer")

try:
    explorer_source = _api_get(api_base, f"/api/corpus/node/{quote(node_choice)}")
    explorer_items = explorer_source.get("items", [])
    explorer_df = _safe_df(explorer_items)

    if not explorer_df.empty and file_query.strip():
        mask = explorer_df["path"].str.contains(file_query.strip(), case=False, na=False)
        explorer_df = explorer_df[mask]

    if explorer_df.empty:
        st.info("No files match the current explorer filters.")
    else:
        explorer_df = explorer_df.sort_values(by=["path"])
        st.dataframe(
            explorer_df[[c for c in ["path", "kind", "size_bytes", "sensitive"] if c in explorer_df.columns]],
            use_container_width=True,
            hide_index=True,
        )

        selected_path = st.selectbox(
            "Open file",
            options=explorer_df["path"].tolist(),
            index=0,
            key="explorer_file_select",
        )

        selected_preview = _api_get(api_base, f"/api/corpus/preview/{quote(selected_path, safe='/')}")
        selected_file_url = f"{api_base}/api/corpus/file/{quote(selected_path, safe='/')}"

        detail_left, detail_right = st.columns([1.2, 0.8])
        with detail_left:
            st.json(selected_preview)
        with detail_right:
            st.link_button("Open file", selected_file_url)
            st.link_button("Download file", f"{selected_file_url}?download=true")
            st.code(selected_preview.get("preview", "[redacted or no preview]")[:preview_limit], language="text")
except Exception as exc:
    st.error(f"Explorer failed: {exc}")


st.divider()
st.subheader("Tree explorer")

def _folder_prefixes(path: str) -> list[str]:
    parts = [part for part in path.split("/") if part]
    prefixes = []
    for i in range(1, len(parts)):
        prefixes.append("/".join(parts[:i]))
    return prefixes

try:
    full_listing = _api_get(api_base, "/api/corpus/files?limit=2000&offset=0")
    full_items = full_listing.get("items", [])
    full_df = _safe_df(full_items)

    if not full_df.empty:
        tree_dirs = sorted({d for path in full_df["path"].tolist() for d in _folder_prefixes(path)})
        tree_dirs = ["[root]"] + tree_dirs
        selected_dir = st.selectbox("Directory", options=tree_dirs, index=0, key="tree_dir_select")

        if selected_dir == "[root]":
            scoped_df = full_df.copy()
        else:
            scoped_df = full_df[full_df["path"].str.startswith(selected_dir + "/", na=False)].copy()

        if file_query.strip():
            scoped_df = scoped_df[scoped_df["path"].str.contains(file_query.strip(), case=False, na=False)]

        scoped_df = scoped_df.sort_values(by=["path"])

        st.write(f"Files in scope: {len(scoped_df)}")
        st.dataframe(
            scoped_df[[c for c in ["path", "kind", "size_bytes", "modified_ts", "sensitive"] if c in scoped_df.columns]],
            use_container_width=True,
            hide_index=True,
        )

        if not scoped_df.empty:
            open_choice = st.selectbox(
                "Open scoped file",
                options=scoped_df["path"].tolist(),
                index=0,
                key="tree_file_select",
            )
            content_col, meta_col = st.columns([1.2, 0.8])
            with content_col:
                file_meta = _api_get(api_base, f"/api/corpus/preview/{quote(open_choice, safe='/')}")
                st.json(file_meta)
                if file_meta.get("kind") == "text" and not file_meta.get("sensitive"):
                    try:
                        full_text = _api_text(api_base, f"/api/corpus/file/{quote(open_choice, safe='/')}")
                        st.text_area("Full text", value=full_text[:preview_limit], height=320)
                    except Exception as exc:
                        st.warning(f"Could not load full text: {exc}")
            with meta_col:
                base_file_url = f"{api_base}/api/corpus/file/{quote(open_choice, safe='/')}"
                st.link_button("Open", base_file_url)
                st.link_button("Download", f"{base_file_url}?download=true")
                st.caption("The tree explorer exposes text files directly and keeps sensitive files redacted.")
    else:
        st.info("No corpus files available from the API.")
except Exception as exc:
    st.error(f"Tree explorer failed: {exc}")
