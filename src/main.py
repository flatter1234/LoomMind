"""最小 LangGraph Agent：单节点调用聊天模型。"""

from __future__ import annotations

import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def build_graph():
    model = ChatOpenAI(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
    )

    def agent(state: AgentState) -> dict:
        reply: AIMessage = model.invoke(state["messages"])
        return {"messages": [reply]}

    g = StateGraph(AgentState)
    g.add_node("agent", agent)
    g.add_edge(START, "agent")
    g.add_edge("agent", END)
    return g.compile()


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("请在 .env 中设置 OPENAI_API_KEY")

    app = build_graph()
    result = app.invoke(
        {
            "messages": [
                SystemMessage(content="你是简洁助手，用中文回答。"),
                HumanMessage(content="用一句话说明 LangGraph 适合做什么。"),
            ]
        }
    )
    last = result["messages"][-1]
    if isinstance(last, AIMessage):
        print(last.content)
    else:
        print(last)


if __name__ == "__main__":
    main()
