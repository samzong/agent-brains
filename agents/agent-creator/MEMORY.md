# agent-creator MEMORY

## Current Main Memory

`agent-creator` is the first agent created under the current Agent Brain design.

Its responsibility is to create, update, and audit later agent brains.

All related operations and commands focus on:

```text
~/.agents/agents
```

That path is usually a symlink to the `agents/` directory in the `agent-brains` repository.

The current agent brain structure is:

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

Skills must use the `skills/SKILL_NAME/SKILL.md` structure.

Workflows must use the `workflows/WORKFLOW_NAME/WORKFLOW.md` structure.

Workflow frontmatter only requires `name` and `description`.

Old workflows must not be silently deleted. Updating, splitting, or removing an old workflow requires an explicit reason first; removal requires an explicit user request.

`AGENTS.md` must contain YAML frontmatter:

```yaml
---
name: agent-name
description: One sentence describing this agent's purpose and when to use it.
---
```

At the current stage, do not use these by default:

- `agent.yaml`
- proposal files
- automatic memory update mechanisms
- `evals/` directory

Memory updates are currently handled manually by the user.

When the user asks for session review or agent brain evolution, `agent-creator` can identify and create or update skills and workflows from real session content.

## Design Source

The current definition comes from the user's design for personal agent brains: turn long-running recurring work into mature agents with their own identity definition, style, skills, and memory.
