"""对外导出 CLI 解析接口。"""

from .parser import build_parser, parse_args

__all__ = ["build_parser", "parse_args"]
