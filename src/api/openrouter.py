# https://openrouter.ai/docs

import os

from langchain_openai import ChatOpenAI

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = "deepseek/deepseek-chat"
# OPENROUTER_MODEL = "deepseek/deepseek-chat-v3.1"
# OPENROUTER_MODEL = "qwen/qwen3-30b-a3b"


def create_openrouter_chat_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=OPENROUTER_MODEL,
        openai_api_key=os.environ.get("OPENROUTER_API_KEY", "").strip(),
        openai_api_base=OPENROUTER_BASE_URL,
        temperature=0,
    )
