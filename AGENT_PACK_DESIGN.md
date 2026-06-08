# Agent Pack 设计定义

## 范围

本文档定义个人 agent pack 的当前设计意图。

所有后续相关操作和命令都聚焦在：

```text
~/.agents/agents
```

## 意图

Agent pack 是一个面向长期领域任务的、结构化的、可持续积累的 agent 大脑。

它的目标是把个人长期重复做的事情沉淀成成熟的 agent。这个 agent 拥有自己的身份定义、风格方式、技能和记忆。以后当需要处理某个特定领域任务时，可以装载对应的 agent pack，作为这个 agent 的工作大脑。

示例：

```text
~/.agents/agents/dify-rag-pm
```

这个 agent 面向 Dify RAG 模块的产品设计工作。

## 当前目录结构

当前期望的结构是：

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

## 核心文件

### AGENTS.md

定义 agent 的身份、工作规则、职责和边界。

这是 agent 如何工作的主定义文件。

`AGENTS.md` 必须使用 YAML frontmatter，并至少包含：

```yaml
---
name: agent-name
description: 一句话说明这个 agent 的用途和适用场景。
---
```

`name` 用于索引和加载 agent。

`description` 用于在用户忘记 agent 名字时列出可用 agent。

### SOUL.md

定义 agent 的风格、气质、产品品味和思考方式。

这个文件描述的是严格规则之外，agent 应该如何呈现自己、如何判断问题、如何表达。

### MEMORY.md

定义 agent 的主记忆。

这个文件保存 agent 需要长期保留、跨任务持续可用的核心记忆。

### memories/

保存子记忆文件。

子记忆可以按日期整理，也可以按事项整理。

### skills/

保存 agent 的技能。

每个 skill 代表一个可重复使用的能力、流程或方法，用来帮助 agent 完成对应领域的工作。

每个 skill 必须使用独立目录，并且入口文件必须命名为 `SKILL.md`：

```text
skills/
└── SKILL_NAME/
    └── SKILL.md
```

不要把 skill 直接写成 `skills/SKILL_NAME.md`。

### workflows/

保存 agent 的流程。

Workflow 是端到端流程，用来把多个能力、判断点、产物和复盘规则串起来。

每个 workflow 必须使用独立目录，并且入口文件必须命名为 `WORKFLOW.md`：

```text
workflows/
└── WORKFLOW_NAME/
    └── WORKFLOW.md
```

不要把 workflow 直接写成 `workflows/WORKFLOW_NAME.md`。

`WORKFLOW.md` 必须使用 YAML frontmatter，并至少包含：

```yaml
---
name: workflow-name
description: 一句话说明这个 workflow 的用途和适用场景。
status: draft
---
```

`status` 可用值：

- `draft`
- `active`
- `deprecated`
- `archived`

旧 workflow 不应被静默删除。

当一个 workflow 不再适合当前 agent 时，优先标记为 `deprecated` 或移动到 `archived` 状态。真正删除 workflow 必须由用户明确要求。

## 加载入口

Agent pack 当前通过 Codex skill `agent-loader` 加载。

`agent-loader` 位于：

```text
~/.agents/skills/agent-loader
```

它不是一个 agent pack，而是 agent pack 体系的加载入口。

`agent-loader` 支持两类操作：

- 列出当前可用 agent
- 按名称加载指定 agent

列出 agent 时，`agent-loader` 读取每个 agent 的 `AGENTS.md` frontmatter，并展示：

- `name`
- `description`

加载 agent 时，`agent-loader` 按顺序读取：

1. `AGENTS.md`
2. `SOUL.md`
3. `MEMORY.md`

默认不要读取所有 `memories/` 文件。

默认不要读取所有 `skills/*/SKILL.md` 文件。

默认不要读取所有 `workflows/*/WORKFLOW.md` 文件。

只有当当前任务需要，或者 `AGENTS.md` / `MEMORY.md` 明确指向某个 memory、skill 或 workflow 时，才读取对应文件。

`agent-loader` 只负责加载上下文，不负责创建、更新或审计 agent pack。创建、更新和审计由 `agent-creator` 负责。

## 成长方式

Agent pack 应该具有成长性。

长期方向是：记忆可以通过定期整理，也就是 dreaming 过程，帮助更新：

- `AGENTS.md`
- `MEMORY.md`
- `SOUL.md`
- `skills/`
- `memories/`
- `workflows/`

当前阶段，记忆更新由用户手工操作。

当用户要求复盘真实 session 或演进 agent pack 时，`agent-creator` 可以根据 session 内容识别：

- 应该沉淀为 skill 的可复用能力
- 应该沉淀为 workflow 的端到端流程
- 应该更新的 agent 定义、主记忆、子记忆、技能或流程
- 应该标记为 `deprecated` 或 `archived` 的旧 workflow

这些演进必须基于真实 session 内容或用户明确描述，不能凭空发明。

## 当前非目标

当前设计暂时不需要：

- `agent.yaml`
- proposal 文件
- 自动更新记忆
- 定义 `evals/` 目录

`evals/` 的定位还没有想清楚，因此不纳入当前文件规范。

## 示例

```text
dify-rag-pm/
├── AGENTS.md
├── MEMORY.md
├── SOUL.md
├── memories
├── skills
│   └── dify-rag-pm
│       └── SKILL.md
└── workflows
    └── dataset-product-design
        └── WORKFLOW.md
```

`dify-rag-pm` 是一个面向 Dify RAG 产品管理和产品设计工作的领域大脑。它应该携带自己的 agent 定义、soul、记忆和技能，并且随着使用不断演进。
