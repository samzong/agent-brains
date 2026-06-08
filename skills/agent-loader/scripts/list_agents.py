from pathlib import Path
import argparse
import os
import sys


DEFAULT_ROOT = Path.home() / ".agents" / "agents"


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    data = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def resolve_root(value):
    if value:
        return Path(value).expanduser()
    env_root = os.environ.get("AGENT_BRAINS_ROOT")
    if env_root:
        return Path(env_root).expanduser()
    return DEFAULT_ROOT


def list_agents(root):
    if not root.exists():
        print(f"agents directory not found: {root}", file=sys.stderr)
        return 1

    rows = []
    for agent_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        agents_md = agent_dir / "AGENTS.md"
        if not agents_md.exists():
            continue
        meta = parse_frontmatter(agents_md)
        name = meta.get("name") or agent_dir.name
        description = meta.get("description") or "(missing description)"
        rows.append((name, description, str(agent_dir)))

    if not rows:
        print("No agent brains found.")
        return 0

    for name, description, path in rows:
        print(f"{name}\t{description}\t{path}")

    return 0


def list_workflows(root, agent_name):
    agent_dir = root / agent_name
    if not agent_dir.exists():
        print(f"agent not found: {agent_name}", file=sys.stderr)
        return list_agents(root)

    workflows_dir = agent_dir / "workflows"
    if not workflows_dir.exists():
        print(f"No workflows directory for agent: {agent_name}")
        return 0

    rows = []
    for workflow_dir in sorted(p for p in workflows_dir.iterdir() if p.is_dir()):
        workflow_md = workflow_dir / "WORKFLOW.md"
        if not workflow_md.exists():
            continue
        meta = parse_frontmatter(workflow_md)
        name = meta.get("name") or workflow_dir.name
        description = meta.get("description") or "(missing description)"
        status = meta.get("status") or "(missing status)"
        rows.append((name, description, status, str(workflow_dir)))

    if not rows:
        print(f"No workflows found for agent: {agent_name}")
        return 0

    for name, description, status, path in rows:
        print(f"{name}\t{status}\t{description}\t{path}")

    return 0


def main():
    parser = argparse.ArgumentParser(description="List personal agent brains and workflow summaries.")
    parser.add_argument("--root", help="Agent brains root directory. Defaults to ~/.agents/agents.")
    parser.add_argument("--agent", help="Agent name for workflow listing.")
    parser.add_argument("--workflows", action="store_true", help="List workflow summaries for an agent.")
    args = parser.parse_args()

    root = resolve_root(args.root)

    if args.workflows:
        if not args.agent:
            print("--workflows requires --agent", file=sys.stderr)
            return 2
        return list_workflows(root, args.agent)

    return list_agents(root)


if __name__ == "__main__":
    raise SystemExit(main())
