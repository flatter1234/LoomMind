"""从 LOOMMIND_TOOLS 目录加载工具定义。"""

import json
import os
import shlex
import subprocess
from pathlib import Path

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

_VAR_SCRIPTS_PATH = "${scripts_path}"
_VAR_PARAMS = "${params}"


class _ToolInput(BaseModel):
    input: str = Field(description="传给工具的输入（JSON 字符串或纯文本）")


def _make_tool(data: dict, scripts_path: str) -> StructuredTool:
    cmd_template = data["cmd"]

    def run(input: str) -> str:
        cmd = cmd_template.replace(_VAR_SCRIPTS_PATH, scripts_path)

        # ${params} 出现时替换为 shell 转义后的参数，否则经 stdin 传入
        if _VAR_PARAMS in cmd:
            cmd = cmd.replace(_VAR_PARAMS, shlex.quote(input))
            stdin_data = None
        else:
            stdin_data = input

        result = subprocess.run(
            cmd,
            shell=True,
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return f"Error (exit {result.returncode}): {result.stderr.strip()}"
        return result.stdout.strip() or "(no output)"

    return StructuredTool.from_function(
        func=run,
        name=data["name"],
        description=data["description"],
        args_schema=_ToolInput,
    )


def load_tools() -> list[StructuredTool]:
    """读取 $LOOMMIND_TOOLS/loader/*.json，返回 LangChain StructuredTool 列表。

    若环境变量未设置或目录不存在，返回空列表。
    """
    base = os.environ.get("LOOMMIND_TOOLS", "").strip()
    if not base:
        return []

    loader_dir = Path(base) / "loader"
    if not loader_dir.is_dir():
        return []

    scripts_path = str(Path(base) / "scripts")

    tools = []
    for path in sorted(loader_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            tools.append(_make_tool(data, scripts_path))
        except (json.JSONDecodeError, KeyError):
            pass

    return tools
