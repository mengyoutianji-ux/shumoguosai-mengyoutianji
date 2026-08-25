#!/usr/bin/env python3
"""Render the editable draw.io subset used by repository templates to PNG."""

from __future__ import annotations

import argparse
import html
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


RENDER_DPI = 200


def parse_style(raw: str | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in (raw or "").split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            result[key] = value
        elif item:
            result[item] = "1"
    return result


def plain_text(raw: str | None) -> str:
    value = re.sub(r"(?i)<br\s*/?>", "\n", raw or "")
    value = re.sub(r"<[^>]+>", "", value)
    return html.unescape(value)


def geometry(cell: ET.Element) -> tuple[float, float, float, float]:
    item = cell.find("mxGeometry")
    if item is None:
        return 0.0, 0.0, 0.0, 0.0
    return tuple(float(item.get(key, 0)) for key in ("x", "y", "width", "height"))


def boundary(box: tuple[float, float, float, float], toward: tuple[float, float]) -> tuple[float, float]:
    x, y, width, height = box
    center_x, center_y = x + width / 2, y + height / 2
    delta_x, delta_y = toward[0] - center_x, toward[1] - center_y
    if not delta_x and not delta_y:
        return center_x, center_y
    scales: list[float] = []
    if abs(delta_x) > 1e-9:
        scales.append((width / 2) / abs(delta_x))
    if abs(delta_y) > 1e-9:
        scales.append((height / 2) / abs(delta_y))
    scale = min(scales)
    return center_x + delta_x * scale, center_y + delta_y * scale


def font_properties() -> font_manager.FontProperties:
    font_path = Path(r"C:\Windows\Fonts\msyh.ttc")
    if font_path.is_file():
        return font_manager.FontProperties(fname=font_path)
    return font_manager.FontProperties(family="sans-serif")


def draw_vertex(axis, cell: ET.Element, font: font_manager.FontProperties) -> None:
    x, y, width, height = geometry(cell)
    style = parse_style(cell.get("style"))
    text_only = "text" in style
    if not text_only:
        fill = style.get("fillColor", "#FFFFFF")
        edge = style.get("strokeColor", "#CBD5E1")
        line_width = float(style.get("strokeWidth", 1.0))
        if style.get("rounded") == "1":
            patch = FancyBboxPatch(
                (x, y), width, height,
                boxstyle="round,pad=0,rounding_size=6",
                facecolor="none" if fill == "none" else fill,
                edgecolor=edge,
                linewidth=line_width,
            )
        else:
            patch = Rectangle(
                (x, y), width, height,
                facecolor="none" if fill == "none" else fill,
                edgecolor=edge,
                linewidth=line_width,
            )
        axis.add_patch(patch)

    label = plain_text(cell.get("value"))
    if not label:
        return
    align = style.get("align", "center")
    vertical = style.get("verticalAlign", "middle")
    text_x = x + 16 if align == "left" else x + width / 2
    horizontal_alignment = "left" if align == "left" else "center"
    if vertical == "top":
        text_y, vertical_alignment = y + 16, "top"
    elif vertical == "bottom":
        text_y, vertical_alignment = y + height - 14, "bottom"
    else:
        text_y, vertical_alignment = y + height / 2, "center"
    axis.text(
        text_x,
        text_y,
        label,
        ha=horizontal_alignment,
        va=vertical_alignment,
        fontsize=float(style.get("fontSize", 16)) * 72 / RENDER_DPI,
        fontweight="bold" if style.get("fontStyle") == "1" else "normal",
        color=style.get("fontColor", "#334155"),
        fontproperties=font,
        linespacing=1.25,
    )


def draw_edge(axis, cell: ET.Element, cells: dict[str, ET.Element], font: font_manager.FontProperties) -> None:
    source = cells.get(cell.get("source", ""))
    target = cells.get(cell.get("target", ""))
    if source is None or target is None:
        return
    source_box, target_box = geometry(source), geometry(target)
    source_center = (source_box[0] + source_box[2] / 2, source_box[1] + source_box[3] / 2)
    target_center = (target_box[0] + target_box[2] / 2, target_box[1] + target_box[3] / 2)
    start = boundary(source_box, target_center)
    end = boundary(target_box, source_center)
    geometry_node = cell.find("mxGeometry")
    points: list[tuple[float, float]] = []
    if geometry_node is not None:
        array = geometry_node.find("Array")
        if array is not None:
            points = [(float(point.get("x", 0)), float(point.get("y", 0))) for point in array.findall("mxPoint")]
    path = [start, *points, end]
    style = parse_style(cell.get("style"))
    color = style.get("strokeColor", "#374151")
    line_width = float(style.get("strokeWidth", 2.0))
    line_style = (0, (7, 5)) if style.get("dashed") == "1" else "solid"
    for index in range(len(path) - 2):
        axis.plot(
            [path[index][0], path[index + 1][0]],
            [path[index][1], path[index + 1][1]],
            color=color,
            linewidth=line_width,
            linestyle=line_style,
        )
    arrow = FancyArrowPatch(
        path[-2],
        path[-1],
        arrowstyle="-|>",
        mutation_scale=16,
        color=color,
        linewidth=line_width,
        linestyle=line_style,
        shrinkA=0,
        shrinkB=0,
    )
    axis.add_patch(arrow)
    label = plain_text(cell.get("value"))
    if label:
        middle = path[len(path) // 2]
        axis.text(
            middle[0],
            middle[1] + 24,
            label,
            ha="center",
            va="top",
            fontsize=float(style.get("fontSize", 14)) * 72 / RENDER_DPI,
            color=style.get("fontColor", color),
            fontproperties=font,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 2},
        )


def render(source: Path, output: Path) -> None:
    root = ET.parse(source).getroot()
    model = root.find(".//mxGraphModel")
    if model is None:
        raise ValueError("draw.io file does not contain mxGraphModel")
    width = int(float(model.get("pageWidth", 1400)))
    height = int(float(model.get("pageHeight", 800)))
    cells = {cell.get("id"): cell for cell in model.findall("./root/mxCell") if cell.get("id")}
    vertices = [cell for cell in cells.values() if cell.get("vertex") == "1"]
    edges = [cell for cell in cells.values() if cell.get("edge") == "1"]
    backgrounds = [cell for cell in vertices if cell.get("id", "").startswith(("band-", "p"))]
    foreground = [cell for cell in vertices if cell not in backgrounds]

    dpi = RENDER_DPI
    figure, axis = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    figure.patch.set_facecolor("white")
    axis.set_xlim(0, width)
    axis.set_ylim(height, 0)
    axis.set_aspect("equal")
    axis.axis("off")
    figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
    font = font_properties()

    for cell in backgrounds:
        draw_vertex(axis, cell, font)
    for cell in edges:
        draw_edge(axis, cell, cells, font)
    for cell in foreground:
        draw_vertex(axis, cell, font)

    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=dpi, facecolor="white", transparent=False)
    plt.close(figure)


def main() -> int:
    parser = argparse.ArgumentParser(description="将仓库 draw.io 模板渲染为 PNG 预览。")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    render(args.source.resolve(), args.output.resolve())
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
