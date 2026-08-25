---
name: mathematical-modeling-workflow
description: Organize and execute a Chinese mathematical-modeling project from complete material reading and ambiguity resolution through proof-oriented modeling, computation, diverse evidence-led visualization, paper writing, validation, and final handoff. Use for CUMCM-style contest work or comparable modeling reports; do not use it to invent facts, install packages, publish materials, or overwrite originals.
---

# Mathematical Modeling Workflow

Use this repository-scoped skill to turn a problem statement and its attachments into an auditable model, reproducible result, and concise Chinese paper. The repository root `AGENTS.md` is the mandatory entrypoint.

## Start Here

1. Read [`AGENTS.md`](../../AGENTS.md), [rule versions and conflict handling](../../docs/规则版本与冲突处理.md), and the [workflow overview](../../docs/工作流总览.md).
2. Inventory and read every supplied source before modeling, especially the problem statement and formal attachments. Record unreadable materials, duplicate versions, and ambiguities that can change the model.
3. Create a project skeleton with `../../scripts/new_project.py` only when a new project directory is needed. Never overwrite a non-empty target without explicit approval.
4. For each question, complete: target and interpretation -> input audit -> model choice -> formula explanation -> key proof -> computation -> result -> validation -> direct conclusion.
5. End every substantive change with the checks in [validation and handoff](../../docs/验证与交付规范.md).

## Route By Task

- For material inventory, ambiguity handling, model comparison, fitting, optimization, uncertainty, or near-perfect fit, read [modeling and statistics](../../docs/建模与统计规范.md).
- For formulas, mathematical criteria, necessary or sufficient conditions, geometric arguments, or user-selected interpretations, also read [model expression and key proofs](../../docs/建模表达与关键证明规范.md).
- For abstracts, assumptions, question sections, page budgets, emphasis, conclusions, tables in LaTeX, or Overleaf wording, read [paper writing](../../docs/论文写作规范.md).
- For figure selection, tables, captions, resolution, or visual consistency, read [figures and tables](../../docs/图表与表格规范.md) and use the [chart selection catalog](../../docs/图表选择目录.md) only as a decision aid.
- For whole-question flowcharts, two- or three-dimensional model schematics, and editable draw.io sources, read [flowcharts and model schematics](../../docs/流程图与建模示意图规范.md).
- For time-dependent models, animations, parameter scans, or representative `2 x 2` frames, read [animations and representative frames](../../docs/动态图与典型时刻图规范.md).
- When using award-winning papers as style evidence, read [excellent-paper reference use](../../docs/优秀论文参考使用规范.md). Do not copy their text, figures, or unpublished files into a public repository.
- Before committing or publishing repository content, read [publication boundary](../../docs/发布边界.md).

## Non-Negotiable Checks

- Do not invent preprocessing, variables, sample sizes, experimental results, proofs, validation, deployment, or publication.
- Preserve originals and write generated artifacts to a separate project output area.
- Keep problem facts out of model assumptions. Define or replace specialist terms that a non-specialist reader cannot understand.
- Explain what each substantive formula models and prove every condition on which the final conclusion depends. A diagram supports the argument but does not replace it.
- Record random seeds for reproduction but omit their values from the paper and figures.
- Use the configured Python interpreter only after confirming it exists. Do not call system Python or install packages from the network unless the user separately authorizes it.
- Keep Chinese spreadsheet filenames and headers, four-decimal computational precision by default, paper figures at no less than 300 dpi, and table text at `\zihao{-5}` in the LaTeX paper.
- Follow the current per-question page ranges and abstract line budgets in `config/workflow.yml`; verify them against the rendered PDF rather than the source editor.
- A final PDF is optional for intermediate work but mandatory when validating a LaTeX paper's pagination and layout.

## Stopping Conditions

Stop and report the exact blocker when a required source cannot be read, a user choice would change the mathematical interpretation, a configured runtime is missing, a key proof cannot be established, a result cannot be reproduced, or publication would expose private or unlicensed material. Do not replace missing evidence with plausible prose.
