from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from .openrouter import create_openrouter_chat_model


def create_chat_model() -> ChatOpenAI:
    return create_openrouter_chat_model()


def invoke(messages: list[BaseMessage]) -> BaseMessage:
    return create_chat_model().invoke(messages)
