"""本地终端多轮对话（CLI）。"""

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from graph_agent import build_graph

from .content_manager import ContentManager
from .response_check import ResponseAction, detect_reply_command

_SYSTEM_PROMPT = "你是简洁助手，用中文回答。"


def run_local_demo() -> None:
    """本地多轮问答（不连接飞书）。

    用户输入或模型整段回复经去空白、小写后恰好为 exit 或 log 时，
    结束会话或打印当前对话 JSON 并写入 log/raw/。
    """
    app = build_graph()
    manager = ContentManager()
    messages: list[BaseMessage] = [SystemMessage(content=_SYSTEM_PROMPT)]
    manager.persist(messages)

    print(
        "多轮问答。输入 exit 结束；输入 log 打印当前全部对话 JSON（并写入 log/raw/）。"
    )
    try:
        while True:
            try:
                user_text = input("你: ").strip()
            except EOFError:
                break
            if not user_text:
                continue

            user_action = detect_reply_command(user_text)
            if user_action is ResponseAction.EXIT:
                break
            if user_action is ResponseAction.LOG:
                print(manager.dumps_session(messages))
                manager.persist(messages)
                continue

            messages.append(HumanMessage(content=user_text))
            try:
                result = app.invoke({"messages": messages})
            except Exception:
                manager.persist(messages)
                raise
            messages = list(result["messages"])

            last = messages[-1]
            if not isinstance(last, AIMessage):
                print(last)
                manager.persist(messages)
                continue

            assistant_text = (
                last.content if isinstance(last.content, str) else str(last.content)
            )
            print(f"助手: {assistant_text}")

            assistant_action = detect_reply_command(assistant_text)
            manager.persist(messages)
            if assistant_action is ResponseAction.EXIT:
                break
            if assistant_action is ResponseAction.LOG:
                print(manager.dumps_session(messages))
    finally:
        manager.persist(messages)
