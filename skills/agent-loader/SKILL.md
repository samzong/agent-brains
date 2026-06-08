---
name: agent-loader
description: Load or list personal agent brains from ~/.agents/agents. Use when the user asks to load an agent by name, list available agents, inspect agent descriptions or workflows, or start a session or task with a personal agent brain.
---

# Agent Loader

Use this skill to list and load personal agent brains from:

```text
~/.agents/agents
```

Recommended setup: clone this repository to `~/.agents/agent-brains`, then symlink `~/.agents/agents` to `~/.agents/agent-brains/agents`.

The directory can be overridden with `AGENT_BRAINS_ROOT` or the script's `--root` option.

## Modes

### List Agents

Use when the user asks what agents exist, asks for agent names, or is unsure which agent to load.

Run the bundled script:

```bash
uv run python skills/agent-loader/scripts/list_agents.py
```

Report each agent's `name` and `description` from its `AGENTS.md` frontmatter. If an agent has no description, say so directly.

### List Workflows

Use when the user asks what workflows an agent has, or when loading an agent and a lightweight workflow summary is useful.

Run:

```bash
uv run python skills/agent-loader/scripts/list_agents.py --agent <name> --workflows
```

Report each workflow's `name`, `description`, and `status` from its `WORKFLOW.md` frontmatter. Do not read workflow bodies just to list workflows.

### Load An Agent

Use when the user names an agent or asks to start working as an agent.

For agent `<name>`, read in this order:

1. `~/.agents/agents/<name>/AGENTS.md`
2. `~/.agents/agents/<name>/SOUL.md`
3. `~/.agents/agents/<name>/MEMORY.md`

Then acknowledge the active agent and summarize:

- identity
- main responsibilities
- key operating rules
- available skills
- available workflows

Do not read every file under `memories/` by default. Read a memory file only when `AGENTS.md`, `MEMORY.md`, or the user's task points to it.

Do not read every `skills/*/SKILL.md` by default. Read a skill only when the task matches that skill or the agent's `AGENTS.md` tells you to use it for the current task.

Do not read every `workflows/*/WORKFLOW.md` by default. Use the workflow frontmatter list first; read a workflow body only when the current task matches it or the user asks for it.

## Validation

If the agent directory does not exist, list available agents instead of guessing.

If `AGENTS.md`, `SOUL.md`, or `MEMORY.md` is missing, report the missing file and load only the existing files.

If `AGENTS.md` lacks frontmatter with `name` and `description`, report that the agent brain needs metadata cleanup.

If `skills/` contains files directly under it instead of `skills/SKILL_NAME/SKILL.md`, report that the agent brain violates the current skill layout.

If `workflows/` contains files directly under it instead of `workflows/WORKFLOW_NAME/WORKFLOW.md`, report that the agent brain violates the current workflow layout.

If a `WORKFLOW.md` lacks frontmatter with `name`, `description`, and `status`, report that the workflow needs metadata cleanup.

## Boundaries

This skill loads agent context. It does not create, update, or audit agent brains unless the user explicitly asks for that work.

For creating, updating, or auditing agent brains, load `agent-creator`.
