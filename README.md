# 数学建模工作流

这是一个面向 CUMCM 类竞赛及其他数据驱动型数学建模任务的轻量工作流仓库。它将材料核验、数据预处理、模型建立、统计结论、模型验证、论文写作、图表制作和最终交付组织为一套可检查、可复用、可持续改进的流程。

仓库只保存规则、模板、检查工具和 Codex 技能，不保存赛题原始附件、未公开论文、个人信息、音视频或实验数据。

## 快速使用

1. 阅读 [工作流总览](docs/工作流总览.md) 与 [AGENTS.md](AGENTS.md)。
2. 运行环境检查：

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts\check_environment.ps1
   ```

3. 创建一个新的项目骨架：

   ```powershell
   & "D:\我的资料\大一\python\.venv\Scripts\python.exe" .\scripts\new_project.py "E:\2026数模模拟\第四次"
   ```

   如果首选 Python 路径不存在，先修复或明确替换 `config/workflow.yml` 中的配置，不要联网安装新环境。

4. 按顺序填写 `材料清单.csv`、`数据预处理记录.md`、`问题建模记录.md` 和 `结果核验表.csv`。
5. 完成后运行仓库自检：

   ```powershell
   py .\scripts\validate_repository.py
   ```

## 仓库结构

```text
.
|-- AGENTS.md                         Codex 项目级约束
|-- config/workflow.yml               可调整的工作流参数
|-- docs/                              分主题规范
|-- templates/                         新项目模板
|-- scripts/                           环境检查、建项目与仓库校验
|-- skills/mathematical-modeling-workflow/
|                                      可调用的 Codex 技能
`-- .github/                           自动校验与改进模板
```

## 改进原则

工作流可以持续完善，但每条新增规则应说明它解决的真实问题、适用范围和验证方式。不要因为一次特殊错误就增加普遍性的强制约束；稳定规则写入 `docs/`，可调参数写入 `config/workflow.yml`，具体项目事实留在项目目录中。

## 当前状态

版本：`0.1.0`。当前建立了完整主流程、项目模板、仓库校验和 Codex 技能入口；尚未关联远程 GitHub 仓库。
