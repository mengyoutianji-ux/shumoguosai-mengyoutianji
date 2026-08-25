#!/usr/bin/env python3
"""Create a non-destructive Chinese mathematical-modeling project skeleton."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


DIRECTORIES = (
    "00_项目管理",
    "01_题目与附件",
    "02_数据与预处理",
    "03_模型与代码",
    "04_结果表",
    "05_图表",
    "06_论文",
    "07_验证",
    "08_交付",
)

TEMPLATE_TARGETS = {
    "项目README模板.md": "README.md",
    "材料清单.csv": "00_项目管理/材料清单.csv",
    "未解决问题.md": "00_项目管理/未解决问题.md",
    "数据预处理记录.md": "02_数据与预处理/数据预处理记录.md",
    "问题建模记录.md": "03_模型与代码/问题建模记录.md",
    "关键证明记录.md": "03_模型与代码/关键证明记录.md",
    "结果核验表.csv": "07_验证/结果核验表.csv",
    "最终检查清单.md": "07_验证/最终检查清单.md",
    "图表规划表.csv": "05_图表/图表规划表.csv",
    "页面预算表.csv": "06_论文/页面预算表.csv",
    "参考论文写作特征记录.md": "00_项目管理/参考论文写作特征记录.md",
}

ASSET_TARGETS = {
    "建模论证闭环.drawio": "05_图表/可编辑模板/建模论证闭环.drawio",
    "建模论证闭环.svg": "05_图表/可编辑模板/建模论证闭环.svg",
    "建模论证闭环.png": "05_图表/可编辑模板/建模论证闭环.png",
    "典型时刻四联图.drawio": "05_图表/可编辑模板/典型时刻四联图.drawio",
    "典型时刻四联图.svg": "05_图表/可编辑模板/典型时刻四联图.svg",
    "典型时刻四联图.png": "05_图表/可编辑模板/典型时刻四联图.png",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="创建数学建模项目目录；默认拒绝覆盖非空目录。"
    )
    parser.add_argument("target", type=Path, help="新项目的绝对或相对路径")
    return parser.parse_args()


def ensure_safe_target(target: Path) -> None:
    if target.exists() and not target.is_dir():
        raise ValueError(f"目标存在但不是目录：{target}")
    if target.exists() and any(target.iterdir()):
        raise ValueError(f"目标目录非空，已停止以避免覆盖：{target}")


def create_project(target: Path) -> None:
    repository_root = Path(__file__).resolve().parents[1]
    templates = repository_root / "templates"
    assets = repository_root / "assets" / "可编辑图示"
    missing = [name for name in TEMPLATE_TARGETS if not (templates / name).is_file()]
    missing.extend(name for name in ASSET_TARGETS if not (assets / name).is_file())
    if missing:
        raise FileNotFoundError("缺少模板：" + "、".join(missing))

    ensure_safe_target(target)
    target.mkdir(parents=True, exist_ok=True)
    for directory in DIRECTORIES:
        (target / directory).mkdir()

    for source_name, relative_target in TEMPLATE_TARGETS.items():
        source = templates / source_name
        destination = target / relative_target
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    for source_name, relative_target in ASSET_TARGETS.items():
        source = assets / source_name
        destination = target / relative_target
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    readme = target / "README.md"
    content = readme.read_text(encoding="utf-8")
    readme.write_text(content.replace("{{PROJECT_NAME}}", target.name), encoding="utf-8")


def main() -> int:
    args = parse_args()
    target = args.target.expanduser().resolve()
    try:
        create_project(target)
    except (OSError, ValueError) as exc:
        print(f"创建失败：{exc}", file=sys.stderr)
        return 1
    print(f"已创建项目骨架：{target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
