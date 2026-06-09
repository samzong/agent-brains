from pathlib import Path
import argparse
import os
import subprocess
import sys


DEFAULT_ROOT = Path.home() / ".agents" / "agents"
AGENT_BRAINS_ROOT_ENV = "AGENT_BRAINS_ROOT"


def parse_frontmatter(path):
    with path.open(encoding="utf-8") as handle:
        first = handle.readline()
        if first.strip() != "---":
            return {}

        data = {}
        for line in handle:
            if line.strip() == "---":
                break
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def resolve_explicit_root(value):
    if value:
        return ("custom", Path(value).expanduser().resolve())
    env_root = os.environ.get(AGENT_BRAINS_ROOT_ENV)
    if env_root:
        return ("custom", Path(env_root).expanduser().resolve())
    return None


def repo_root(cwd):
    try:
        result = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    value = result.stdout.strip()
    if not value:
        return None
    return Path(value).resolve()


def repo_agent_roots(cwd):
    cwd = cwd.resolve()
    root = repo_root(cwd)
    if root is None:
        return [cwd / ".agents" / "agents"]

    roots = []
    current = cwd
    while True:
        roots.append(current / ".agents" / "agents")
        if current == root:
            break
        if root not in current.parents:
            break
        current = current.parent
    return roots


def discovery_roots(cwd=None):
    explicit = resolve_explicit_root(None)
    if explicit:
        return [explicit]

    roots = [("repo", root) for root in repo_agent_roots(cwd or Path.cwd())]
    roots.append(("user", DEFAULT_ROOT.expanduser()))
    return roots


def root_specs(root_arg):
    explicit = resolve_explicit_root(root_arg)
    if explicit:
        return [explicit]
    return discovery_roots()


def agent_rows(roots):
    rows = []
    seen = set()
    for scope, root in roots:
        if not root.exists():
            continue
        for agent_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            agents_md = agent_dir / "AGENTS.md"
            if not agents_md.exists():
                continue
            meta = parse_frontmatter(agents_md)
            name = meta.get("name") or agent_dir.name
            if name in seen:
                continue
            seen.add(name)
            description = meta.get("description") or "(missing description)"
            rows.append((name, description, scope, str(agent_dir.resolve())))
    return rows


def resolve_agent(roots, agent_name):
    for name, description, scope, path in agent_rows(roots):
        if name == agent_name:
            return (name, description, scope, Path(path))
    return None


def explicit_root_missing(explicit_root):
    if explicit_root and not explicit_root.exists():
        print(f"agents directory not found: {explicit_root}", file=sys.stderr)
        return True
    return False


def list_agents(roots, explicit_root=None):
    if explicit_root_missing(explicit_root):
        return 1

    rows = agent_rows(roots)

    if not rows:
        print("No agent brains found.")
        return 0

    for name, description, scope, path in rows:
        print(f"{name}\t{description}\t{scope}\t{path}")

    return 0


def print_agent_path(roots, agent_name, explicit_root=None):
    if explicit_root_missing(explicit_root):
        return 1

    record = resolve_agent(roots, agent_name)
    if record is None:
        print(f"agent not found: {agent_name}", file=sys.stderr)
        list_agents(roots)
        return 1

    name, description, scope, path = record
    print(f"{name}\t{description}\t{scope}\t{path}")
    return 0


def list_workflows(roots, agent_name, explicit_root=None):
    if explicit_root_missing(explicit_root):
        return 1

    record = resolve_agent(roots, agent_name)
    if record is None:
        print(f"agent not found: {agent_name}", file=sys.stderr)
        list_agents(roots)
        return 1

    agent_dir = record[3]

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
        rows.append((name, description, str(workflow_dir)))

    if not rows:
        print(f"No workflows found for agent: {agent_name}")
        return 0

    for name, description, path in rows:
        print(f"{name}\t{description}\t{path}")

    return 0


def main():
    parser = argparse.ArgumentParser(description="List personal agent brains and workflow summaries.")
    parser.add_argument("--root", help="Agent brains root directory. Overrides repo/user discovery.")
    parser.add_argument("--agent", help="Agent name for workflow listing.")
    parser.add_argument("--workflows", action="store_true", help="List workflow summaries for an agent.")
    args = parser.parse_args()

    roots = root_specs(args.root)
    explicit_root = roots[0][1] if args.root or os.environ.get(AGENT_BRAINS_ROOT_ENV) else None

    if args.workflows:
        if not args.agent:
            print("--workflows requires --agent", file=sys.stderr)
            return 2
        return list_workflows(roots, args.agent, explicit_root)

    if args.agent:
        return print_agent_path(roots, args.agent, explicit_root)

    return list_agents(roots, explicit_root)


if __name__ == "__main__":
    raise SystemExit(main())
