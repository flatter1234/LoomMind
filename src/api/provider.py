"""LLM 提供方：由环境变量解析，供 api 层统一分支。"""

import os
from enum import StrEnum


class LLMProvider(StrEnum):
    OPENROUTER = "openrouter"
    OLLAMA = "ollama"


_ENV_KEY = "LOOMMIND_LLM_PROVIDER"


def resolve_llm_provider() -> LLMProvider:
    """读取 `LOOMMIND_LLM_PROVIDER`。

    - 未设置、空串、`openrouter` → OpenRouter；
    - `ollama` → 本地 Ollama；
    - 其它未知值 → 回退为 OpenRouter（避免拼写错误导致进程无法启动）。
    """
    raw = os.environ.get(_ENV_KEY, "").strip().lower()
    if raw == LLMProvider.OLLAMA:
        return LLMProvider.OLLAMA
    if raw in ("", LLMProvider.OPENROUTER):
        return LLMProvider.OPENROUTER
    return LLMProvider.OPENROUTER
