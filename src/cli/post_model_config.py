"""选模型后：根据 `.env` 文件内容决定还需配置项（供 TUI 列表 / 输入框）。"""

from pathlib import Path

from api.provider import LLMProvider

from .env_file import parse_dotenv


def dotenv_path_for_session() -> Path:
    """与 `src/cli/app.py` 同级：项目根 `.env`。"""
    return Path(__file__).resolve().parents[2] / ".env"


def _file_nonempty(path: Path, key: str) -> bool:
    vals = parse_dotenv(path) if path.is_file() else {}
    return bool(str(vals.get(key, "")).strip())


def collect_post_model_config_items(session) -> list[dict]:
    """返回 `{"id","label","hint"}` 列表；仅当 `.env` 中对应项为空时列入。"""
    path = dotenv_path_for_session()
    p = session.llm.effective_provider()
    out: list[dict] = []
    if p is LLMProvider.OPENROUTER:
        if not _file_nonempty(path, "OPENROUTER_API_KEY"):
            out.append(
                {
                    "id": "OPENROUTER_API_KEY",
                    "label": "OpenRouter API 密钥",
                    "hint": "在 openrouter.ai 获取密钥；将写入项目根 .env",
                }
            )
    elif p is LLMProvider.OLLAMA:
        if not _file_nonempty(path, "OLLAMA_BASE_URL"):
            out.append(
                {
                    "id": "OLLAMA_BASE_URL",
                    "label": "Ollama Base URL",
                    "hint": "例 http://127.0.0.1:11434 ；可带或不带 /v1",
                }
            )
        if not _file_nonempty(path, "OLLAMA_API_KEY"):
            out.append(
                {
                    "id": "OLLAMA_API_KEY",
                    "label": "Ollama API Key（占位）",
                    "hint": "本地一般填 ollama；将写入 .env",
                }
            )
    return out
