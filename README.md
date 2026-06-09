# agent-brains

Portable **domain agent brains** for coding agents (Codex, Claude Code, Cursor, and others that read markdown context).

An agent brain is a long-lived context pack for a recurring domain. It keeps identity, judgment criteria, style, durable memory, domain methods, and stable SOPs in one loadable structure so the agent does not start from a blank context every session.

See [docs/AGENT_BRAIN_SPEC.md](./docs/AGENT_BRAIN_SPEC.md) for the full specification.

**Skill vs workflow vs brain** (see spec for detail):

- `skill` — reusable method or tool capability (**how**)
- `workflow` — end-to-end SOP for stable business behavior (**what process**)
- `agent brain` — identity, memory, and domain judgment (**who**, on **what history and standards**)

## Create brains

| Name | Purpose |
|------|---------|
| `agent-creator` | Create, audit, and evolve agent brains |

## Bundled skills

| Name | Purpose |
|------|---------|
| `agent-loader` | List and load repo-scoped and user-scoped agent brains |

Built-in loader: [`skills/agent-loader/`](./skills/agent-loader/). Copy or symlink it into your agent client's global skills directory to use it outside this repo.

Discovery checks repo-local `.agents/agents` directories from the current working directory up to the repository root, then `$HOME/.agents/agents`. It reads only `AGENTS.md` frontmatter and reports `name`, `description`, `scope`, and `path`. On load, `agent-loader` resolves the agent path, then reads `AGENTS.md`, `SOUL.md`, and `MEMORY.md` first. `memories/`, `skills/`, and `workflows/` are lazy-loaded only when the task needs them or core files point to them.

## Optional local routing

For Codex users, [`codex-agents-local`](https://github.com/samzong/codex-agents-local) can add a private `AGENTS.local.md` prompt that nudges Codex to choose an agent brain only when useful:

```md
When a task is domain-specific or recurring enough to benefit from a personal agent brain, proactively use `agent-loader` to list/resolve candidates, load the single best-matching agent core before working, ask only if the match is ambiguous, and keep skills/workflows/memories lazy-loaded.
```

## Brain structure

Each brain lives under `agents/`:

```text
agents/
└── agent-name/
    ├── AGENTS.md
    ├── SOUL.md
    ├── MEMORY.md
    ├── memories/
    ├── skills/
    │   └── SKILL_NAME/
    │       └── SKILL.md
    └── workflows/
        └── WORKFLOW_NAME/
            └── WORKFLOW.md
```

- `AGENTS.md` — identity, responsibilities, rules, boundaries (`name`, `description` frontmatter required)
- `SOUL.md` — style, judgment, taste, and tone
- `MEMORY.md` — durable main memory
- `memories/` — optional focused sub-memories (by date or topic)
- `skills/<skill-name>/SKILL.md` — optional reusable methods and tools
- `workflows/<workflow-name>/WORKFLOW.md` — optional end-to-end SOPs

Keep brains narrow. ***A useful brain knows one domain well instead of trying to manage every task.***

## Related projects

- [AGENTS.md](https://agents.md) — open format for agent-facing project instructions
- [OpenClaw workspace](https://docs.openclaw.ai/concepts/agent) — runtime-injected workspace files (similar file semantics, different loading model)

## License

MIT
