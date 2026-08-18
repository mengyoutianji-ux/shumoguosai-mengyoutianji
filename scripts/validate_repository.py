#!/usr/bin/env python3
"""Validate repository structure without third-party dependencies."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "mathematical-modeling-workflow"

REQUIRED_PATHS = (
    "README.md",
    "AGENTS.md",
    "config/workflow.yml",
    "docs/工作流总览.md",
    "docs/建模与统计规范.md",
    "docs/论文写作规范.md",
    "docs/图表与表格规范.md",
    "docs/验证与交付规范.md",
    "docs/发布边界.md",
    "templates/材料清单.csv",
    "templates/数据预处理记录.md",
    "templates/问题建模记录.md",
    "templates/结果核验表.csv",
    "templates/最终检查清单.md",
    "scripts/new_project.py",
    f"skills/{SKILL_NAME}/SKILL.md",
    f"skills/{SKILL_NAME}/agents/openai.yaml",
    ".github/workflows/validate-workflow.yml",
)

FORBIDDEN_SUFFIXES = {
    ".doc",
    ".docx",
    ".pdf",
    ".m4a",
    ".mp3",
    ".mp4",
    ".mov",
    ".psd",
    ".rar",
    ".7z",
    ".xls",
    ".xlsx",
    ".db",
    ".sqlite",
}

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fff]")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def validate_required_paths(errors: list[str]) -> None:
    for item in REQUIRED_PATHS:
        if not (ROOT / item).is_file():
            errors.append(f"缺少必需文件：{item}")


def validate_skill(errors: list[str]) -> None:
    skill = ROOT / "skills" / SKILL_NAME / "SKILL.md"
    if not skill.is_file():
        return
    text = skill.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.search(text)
    if not match:
        errors.append("SKILL.md 缺少有效 YAML frontmatter。")
        return
    frontmatter = match.group(1)
    if f"name: {SKILL_NAME}" not in frontmatter:
        errors.append("SKILL.md 的 name 与目录名不一致。")
    description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if not description or len(description.group(1).strip()) < 40:
        errors.append("SKILL.md 的 description 过短或缺失。")
    if "[TODO" in text or "Add the task-specific guidance" in text:
        errors.append("SKILL.md 仍含初始化占位符。")

    metadata = skill.parent / "agents" / "openai.yaml"
    if metadata.is_file():
        metadata_text = metadata.read_text(encoding="utf-8")
        if f"${SKILL_NAME}" not in metadata_text:
            errors.append("openai.yaml 的 default_prompt 未显式引用技能名。")


def validate_markdown_links(errors: list[str]) -> None:
    for markdown in ROOT.rglob("*.md"):
        if ".git" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (markdown.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"链接越出仓库：{relative(markdown)} -> {raw_target}")
                continue
            if not resolved.exists():
                errors.append(f"内部链接不存在：{relative(markdown)} -> {raw_target}")


def validate_csv_headers(errors: list[str]) -> None:
    for csv_path in (ROOT / "templates").glob("*.csv"):
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            row = next(csv.reader(handle), [])
        if not row:
            errors.append(f"CSV 模板没有表头：{relative(csv_path)}")
            continue
        non_chinese = [header for header in row if not CHINESE_PATTERN.search(header)]
        if non_chinese:
            errors.append(
                f"CSV 表头必须包含中文：{relative(csv_path)} -> {', '.join(non_chinese)}"
            )


def validate_config(errors: list[str]) -> None:
    config = ROOT / "config" / "workflow.yml"
    if not config.is_file():
        return
    text = config.read_text(encoding="utf-8")
    required_tokens = (
        "preferred_executable:",
        "allow_network_install: false",
        "minimum_raster_dpi: 300",
        "default_decimal_places: 4",
        "front_matter_max_pages: 4",
        "abstract_max_pages: 1",
        "inspect_near_perfect_fit: true",
    )
    for token in required_tokens:
        if token not in text:
            errors.append(f"配置缺少关键项：{token}")


def validate_repository_files(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"仓库包含默认禁止发布的文件类型：{relative(path)}")


def main() -> int:
    errors: list[str] = []
    validate_required_paths(errors)
    validate_skill(errors)
    validate_markdown_links(errors)
    validate_csv_headers(errors)
    validate_config(errors)
    validate_repository_files(errors)

    if errors:
        print("仓库校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    file_count = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    print(f"仓库校验通过：{file_count} 个文件。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
