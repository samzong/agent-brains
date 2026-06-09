# Repository Guidelines

## Project Structure & Module Organization

This repository stores portable agent-brain definitions and supporting loader tooling.

- `agents/<agent-name>/` contains one agent brain. Each brain has `AGENTS.md`, `SOUL.md`, and `MEMORY.md`.
- `agents/<agent-name>/memories/` stores focused long-term memory files.
- `agents/<agent-name>/skills/<skill-name>/SKILL.md` stores brain-specific reusable methods.
- `agents/<agent-name>/workflows/<workflow-name>/WORKFLOW.md` stores brain-specific SOPs.
- `skills/agent-loader/` contains the shared loader skill and its helper script.
- `docs/AGENT_BRAIN_SPEC.md` defines the canonical brain format.
- `scripts/validate_brains.py` validates required files, frontmatter, names, and workflow statuses.

## Build, Test, and Development Commands

There is no application build step. This is a Markdown and Python validation repository.

- `git ls-files` lists tracked project files.
- `rg -n "<term>" . -g '!/.git/**' -g '!/.serena/**'` searches brain content.
- `uv run python scripts/validate_brains.py` runs the local validation gate.

Run validation before opening a PR or after changing any `agents/`, `skills/`, `workflows/`, or spec file.

## Coding Style & Naming Conventions

Use Markdown for brain content and Python only for repository tooling. Keep prose direct and durable; do not turn session notes into permanent rules.

Agent, skill, and workflow names must be lowercase kebab-case, matching their directory names, for example `dify-rag-pm` or `agent-loader`. Required frontmatter:

- Brain `AGENTS.md`: `name`, `description`
- `SKILL.md`: `name`, `description`
- `WORKFLOW.md`: `name`, `description`, `status`

Workflow `status` must be one of `draft`, `active`, `deprecated`, or `archived`.

## Testing Guidelines

The validation script is the test suite. It checks required structure, YAML frontmatter, directory/name consistency, skill layout, and workflow status values. Add new coverage to `scripts/validate_brains.py` when adding new repository-level format rules.

## Commit & Pull Request Guidelines

Existing history uses short imperative commits, often Conventional Commit style, such as `feat(agent-loader): add repo and user discovery` or `feat: add agent brain spec`.

PRs should describe the changed brain, skill, workflow, or spec area; include the validation result; and link related issues when available. For content changes, explain why the rule or memory belongs long-term instead of being session-specific.
