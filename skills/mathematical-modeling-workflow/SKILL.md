---
name: mathematical-modeling-workflow
description: Organize and execute a Chinese mathematical-modeling project from material inventory and data audit through model selection, validation, paper writing, figures, tables, and final handoff. Use for CUMCM-style contest work or comparable data-driven modeling reports; do not use it as authority to invent data, install packages, publish materials, or overwrite original files.
---

# Mathematical Modeling Workflow

Use this repository-scoped skill to turn a problem statement and its attachments into an auditable modeling result and a concise Chinese paper. The user's latest request and the actual problem statement override repository defaults.

## Start Here

1. Read the repository [workflow overview](../../docs/工作流总览.md) and the project-level `AGENTS.md`.
2. Inventory all supplied materials before drafting. Separate verified records, calculations, inference, unresolved questions, and planned work.
3. Create a project skeleton with `../../scripts/new_project.py` when the user requests a new project directory. Never overwrite a non-empty target without explicit approval.
4. For each problem, follow: question target -> preprocessing -> exploratory analysis -> model choice -> solution -> validation -> direct conclusion.
5. End every substantive change with the checks in [validation and handoff](../../docs/验证与交付规范.md).

## Route By Task

- For variable relationships, model comparison, fitting, optimization, uncertainty, or near-perfect fit, read [modeling and statistics](../../docs/建模与统计规范.md).
- For abstracts, assumptions, question sections, page budgets, emphasis, or Overleaf wording, read [paper writing](../../docs/论文写作规范.md).
- For Excel outputs, tables, charts, captions, resolution, or visual consistency, read [figures and tables](../../docs/图表与表格规范.md).
- Before committing or publishing repository content, read [publication boundary](../../docs/发布边界.md).

## Non-Negotiable Checks

- Do not invent preprocessing, variables, sample sizes, experimental results, validation, deployment, or publication.
- Preserve originals and write generated artifacts to a separate project output area.
- Use professional statistical conclusions. State direction and strength only when supported; describe non-monotonic structure separately.
- Prefer the simplest model that satisfies predictive, statistical, and domain requirements. Investigate any fit metric near its theoretical maximum.
- Use the configured Python interpreter only after confirming it exists. Do not install packages from the network unless the user separately authorizes it.
- Keep Chinese spreadsheet filenames and headers, four-decimal computational precision by default, paper figures at no less than 300 dpi, and restrained emphasis in prose.
- A final PDF is optional for intermediate work, but mandatory when validating a LaTeX paper's actual pagination and layout.

## Stopping Conditions

Stop and report the exact blocker when a required source cannot be read, a configured runtime is missing, a result cannot be reproduced, or publication would expose private competition material. Do not replace missing evidence with plausible prose.
