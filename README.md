# agent-brains

Portable **domain agent brains** for coding agents (Codex, Claude Code, Cursor, and others that read markdown context).

An agent brain is a structured, long-lived knowledge pack for a recurring domain: identity, style, memory, skills, and workflows. Load one by name when a task matches that domain.

## Layout

Each brain lives in its own directory:

```text
agent-name/
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

See [AGENT_PACK_DESIGN.md](./AGENT_PACK_DESIGN.md) for the full spec (Chinese, normative for this repo).

## Install

### As a submodule in `~/.agents` (recommended)

```bash
cd ~/.agents
git submodule add https://github.com/samzong/agent-brains.git agents
git submodule update --init --recursive
```

Brains are loaded from `~/.agents/agents/`.

### Standalone clone

```bash
git clone https://github.com/samzong/agent-brains.git ~/.agents/agents
```

## Included brains

| Name | Purpose |
|------|---------|
| `agent-creator` | Create, audit, and evolve agent brains |
| `dify-rag-pm` | Dify RAG product design |
| `dify-prototype-builder` | Source-faithful Dify prototypes |

## Loader

Listing and loading brains is handled by the `agent-loader` skill in [samzong/.agents](https://github.com/samzong/.agents) (`skills/agent-loader/`). It reads `AGENTS.md`, `SOUL.md`, and `MEMORY.md` first; skills, workflows, and sub-memories are loaded on demand.

## Related projects

- [agentskills.io](https://agentskills.io) — portable skill format (`SKILL.md`)
- [OpenClaw workspace](https://docs.openclaw.ai/concepts/agent) — runtime-injected workspace files (similar file semantics, different loading model)

**Not** [agentspack](https://github.com/farfarawaylabs/agentspack) — that project generates multi-IDE config from templates. agent-brains is a catalog of domain brains, not a sync tool.

## License

MIT
