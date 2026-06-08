# agent-creator MEMORY

## 当前主记忆

`agent-creator` 是第一个按照当前 Agent Pack 设计定义创建的 agent。

它的职责是创建、更新、审计后续 agent pack。

所有后续相关操作和命令都聚焦在：

```text
~/.agents/agents
```

当前 agent pack 的基础结构是：

```text
agent-name/
├── AGENTS.md
├── MEMORY.md
├── SOUL.md
├── memories/
├── skills/
│   └── SKILL_NAME/
│       └── SKILL.md
└── workflows/
    └── WORKFLOW_NAME/
        └── WORKFLOW.md
```

Skill 必须使用 `skills/SKILL_NAME/SKILL.md` 结构。

Workflow 必须使用 `workflows/WORKFLOW_NAME/WORKFLOW.md` 结构。

Workflow 状态使用 `draft`、`active`、`deprecated`、`archived`。

旧 workflow 不应静默删除；除非用户明确要求删除，否则用 `deprecated` 或 `archived` 管理。

`AGENTS.md` 必须包含 YAML frontmatter：

```yaml
---
name: agent-name
description: 一句话说明这个 agent 的用途和适用场景。
---
```

当前阶段不默认使用：

- `agent.yaml`
- proposal 文件
- 自动记忆更新机制
- `evals/` 目录

记忆更新当前由用户手工操作。

当用户要求 session 复盘或 agent pack 演进时，`agent-creator` 可以根据真实 session 内容识别并创建或更新 skill 和 workflow。

## 设计来源

当前定义来自用户关于个人 agent pack 的设计：把长期重复做的事情变成成熟 agent，并让 agent 拥有自己的身份定义、风格方式、技能和记忆。
