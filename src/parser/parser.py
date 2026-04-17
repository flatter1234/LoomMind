"""CLI 参数解析。
uv run python src/main.py
uv run python src/main.py --demo
uv run python src/main.py --help
"""

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="LoomMind：LangGraph + 飞书（用户身份发消息）"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="仅在本地打印一条示例问答，不连接飞书",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)
