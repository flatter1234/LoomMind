"""Ollama 本地模型（OpenAI 兼容 Chat API）。"""

# https://github.com/ollama/ollama/blob/main/docs/openai.md

import json
import os
import urllib.error
import urllib.request

from langchain_openai import ChatOpenAI

DEFAULT_OLLAMA_BASE = "http://127.0.0.1:11434"


def normalized_openai_api_base(*, base_url_override: str | None = None) -> str:
    """供 ChatOpenAI 使用的 base，形如 http://host:11434/v1。"""
    raw = (base_url_override or "").strip().rstrip("/")
    if not raw:
        raw = os.environ.get("OLLAMA_BASE_URL", "").strip().rstrip("/")
    if not raw:
        raw = f"{DEFAULT_OLLAMA_BASE}/v1"
    if not raw.lower().endswith("/v1"):
        raw = f"{raw}/v1"
    return raw


def _ollama_origin_for_tags(openai_api_base: str) -> str:
    b = openai_api_base.rstrip("/")
    if b.lower().endswith("/v1"):
        return b[:-3].rstrip("/")
    return b


def fetch_ollama_model_names(
    *, base_url_override: str | None = None, timeout: float = 3.0
) -> list[str]:
    origin = _ollama_origin_for_tags(
        normalized_openai_api_base(base_url_override=base_url_override)
    )
    url = f"{origin}/api/tags"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
    except (OSError, urllib.error.URLError, json.JSONDecodeError, ValueError):
        return []
    models = data.get("models") or []
    names: list[str] = []
    for m in models:
        n = m.get("name")
        if isinstance(n, str) and n.strip():
            names.append(n.strip())
    return names


def list_ollama_models(*, base_url_override: str | None = None) -> list[str]:
    names = fetch_ollama_model_names(base_url_override=base_url_override)
    extra = os.environ.get("OLLAMA_MODEL", "").strip()
    if extra and extra not in names:
        names.insert(0, extra)
    if not names:
        names = [extra or "llama3.2"]
    return names


def default_ollama_model(*, base_url_override: str | None = None) -> str:
    explicit = os.environ.get("OLLAMA_MODEL", "").strip()
    if explicit:
        return explicit
    found = fetch_ollama_model_names(base_url_override=base_url_override)
    if found:
        return found[0]
    return "llama3.2"


def create_ollama_chat_model(
    model: str | None = None,
    *,
    api_key: str | None = None,
    base_url_override: str | None = None,
) -> ChatOpenAI:
    resolved = (
        model or default_ollama_model(base_url_override=base_url_override)
    ).strip()
    if api_key is not None and api_key.strip():
        use_key = api_key.strip()
    else:
        use_key = os.environ.get("OLLAMA_API_KEY", "ollama").strip() or "ollama"
    return ChatOpenAI(
        model=resolved,
        openai_api_key=use_key,
        openai_api_base=normalized_openai_api_base(base_url_override=base_url_override),
        temperature=0,
    )
