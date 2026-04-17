"""LoomMind 入口：默认连接飞书长连接；--demo 为本地问答。"""

from dotenv import load_dotenv

from parser import parse_args


def main() -> None:
    load_dotenv()
    args = parse_args()
    if args.demo:
        from graph_agent import run_local_demo

        run_local_demo()
        return

    from feishu_app import run_feishu_long_connection

    run_feishu_long_connection()


if __name__ == "__main__":
    main()
