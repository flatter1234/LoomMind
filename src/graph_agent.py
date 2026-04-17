"""LangGraph Agent：单节点调用聊天模型。"""

from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from api import create_chat_model


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def build_graph():
    model = create_chat_model()

    def agent(state: AgentState) -> dict:
        """根据当前状态中的消息列表调用模型，追加一条 AI 回复。"""
        reply: AIMessage = model.invoke(state["messages"])
        return {"messages": [reply]}

    g = StateGraph(AgentState)
    g.add_node("agent", agent)
    g.add_edge(START, "agent")
    g.add_edge("agent", END)
    return g.compile()


def run_local_demo() -> None:
    """本地打印一条问答（不连接飞书）。"""
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
