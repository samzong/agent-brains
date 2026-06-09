---
name: agent-loader
description: Load or list repo-scoped and user-scoped agent brains. Use when the user asks to load an agent by name, list available agents, inspect agent descriptions or workflows, or start a session or task with a personal agent brain.
---

# Agent Loader

Use this skill to list and load agent brains from two scopes:

```text
REPO: $CWD/.agents/agents up to $REPO_ROOT/.agents/agents
USER: $HOME/.agents/agents
```

Repo scope is searched from the current working directory upward to the repository root. User scope is searched after repo scope. If the same agent name exists in multiple places, the first discovered agent wins.

For a global setup, clone this repository to `~/.agents/agent-brains`, then symlink `~/.agents/agents` to `~/.agents/agent-brains/agents`.

The discovery roots can be overridden with `AGENT_BRAINS_ROOT` or the script's `--root` option. Overrides use `custom` scope.

## Modes

### List Agents

Use when the user asks what agents exist, asks for agent names, or is unsure which agent to load.

Run the bundled script:

```bash
uv run python skills/agent-loader/scripts/list_agents.py
```

Report each agent's `name`, `description`, `scope`, and `path`. Discovery only reads `AGENTS.md` frontmatter; it does not read the body or any other core file. If an agent has no description, say so directly.

### List Workflows

Use when the user asks what workflows an agent has, or when loading an agent and a lightweight workflow summary is useful.

Run:

```bash
uv run python skills/agent-loader/scripts/list_agents.py --agent <name> --workflows
```

The script resolves `<name>` through the same repo/user discovery order, then reads only each workflow's `WORKFLOW.md` frontmatter. Report each workflow's `name`, `description`, `status`, and `path`. Do not read workflow bodies just to list workflows.

### Load An Agent

Use when the user names an agent or asks to start working as an agent.

First resolve the agent path:

```bash
uv run python skills/agent-loader/scripts/list_agents.py --agent <name>
```

The script prints:

```text
name<TAB>description<TAB>scope<TAB>path
```

For the resolved `path`, read in this order:

1. `path/AGENTS.md`
2. `path/SOUL.md`
3. `path/MEMORY.md`

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

If the agent cannot be resolved, list available agents instead of guessing.

If `AGENTS.md`, `SOUL.md`, or `MEMORY.md` is missing, report the missing file and load only the existing files.

If `AGENTS.md` lacks frontmatter with `name` and `description`, report that the agent brain needs metadata cleanup.

If `skills/` contains files directly under it instead of `skills/SKILL_NAME/SKILL.md`, report that the agent brain violates the current skill layout.

If `workflows/` contains files directly under it instead of `workflows/WORKFLOW_NAME/WORKFLOW.md`, report that the agent brain violates the current workflow layout.

If a `WORKFLOW.md` lacks frontmatter with `name`, `description`, and `status`, report that the workflow needs metadata cleanup.

## Boundaries

This skill loads agent context. It does not create, update, or audit agent brains unless the user explicitly asks for that work.

For creating, updating, or auditing agent brains, load `agent-creator`.
