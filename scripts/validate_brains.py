from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
AGENTS_ROOT = ROOT / "agents"
VALID_WORKFLOW_STATUSES = {"draft", "active", "deprecated", "archived"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    data = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return None


def require(condition, message, errors):
    if not condition:
        errors.append(message)


def validate_frontmatter(path, required, errors):
    meta = parse_frontmatter(path)
    require(meta is not None, f"{path.relative_to(ROOT)} must start with YAML frontmatter", errors)
    if meta is None:
        return {}
    for key in required:
        require(meta.get(key), f"{path.relative_to(ROOT)} frontmatter missing `{key}`", errors)
    return meta


def validate_name(path, name, expected, errors):
    rel = path.relative_to(ROOT)
    require(NAME_RE.match(name or "") is not None, f"{rel} has invalid name `{name}`", errors)
    require(name == expected, f"{rel} name `{name}` must match directory `{expected}`", errors)


def validate_skill_dir(skills_dir, errors):
    if not skills_dir.exists():
        return

    for child in sorted(skills_dir.iterdir()):
        rel = child.relative_to(ROOT)
        if child.is_file():
            errors.append(f"{rel} is not allowed; use skills/<skill-name>/SKILL.md")
            continue
        if not child.is_dir():
            continue

        skill_md = child / "SKILL.md"
        require(skill_md.exists(), f"{rel}/ must contain SKILL.md", errors)
        if not skill_md.exists():
            continue

        meta = validate_frontmatter(skill_md, ("name", "description"), errors)
        if meta.get("name"):
            validate_name(skill_md, meta["name"], child.name, errors)


def validate_workflow_dir(workflows_dir, errors):
    if not workflows_dir.exists():
        return

    for child in sorted(workflows_dir.iterdir()):
        rel = child.relative_to(ROOT)
        if child.is_file():
            errors.append(f"{rel} is not allowed; use workflows/<workflow-name>/WORKFLOW.md")
            continue
        if not child.is_dir():
            continue

        workflow_md = child / "WORKFLOW.md"
        require(workflow_md.exists(), f"{rel}/ must contain WORKFLOW.md", errors)
        if not workflow_md.exists():
            continue

        meta = validate_frontmatter(workflow_md, ("name", "description", "status"), errors)
        if meta.get("name"):
            validate_name(workflow_md, meta["name"], child.name, errors)
        if meta.get("status"):
            require(
                meta["status"] in VALID_WORKFLOW_STATUSES,
                f"{workflow_md.relative_to(ROOT)} status `{meta['status']}` is invalid",
                errors,
            )


def brain_dirs():
    if not AGENTS_ROOT.exists():
        return
    for child in sorted(AGENTS_ROOT.iterdir()):
        if not child.is_dir():
            continue
        if (child / "AGENTS.md").exists():
            yield child


def validate_brain(brain_dir, errors):
    agents_md = brain_dir / "AGENTS.md"
    soul_md = brain_dir / "SOUL.md"
    memory_md = brain_dir / "MEMORY.md"

    require(soul_md.exists(), f"{brain_dir.name}/ must contain SOUL.md", errors)
    require(memory_md.exists(), f"{brain_dir.name}/ must contain MEMORY.md", errors)

    meta = validate_frontmatter(agents_md, ("name", "description"), errors)
    if meta.get("name"):
        validate_name(agents_md, meta["name"], brain_dir.name, errors)

    validate_skill_dir(brain_dir / "skills", errors)
    validate_workflow_dir(brain_dir / "workflows", errors)


def main():
    errors = []

    require((ROOT / "docs" / "AGENT_BRAIN_SPEC.md").exists(), "docs/AGENT_BRAIN_SPEC.md is required", errors)
    require(AGENTS_ROOT.exists(), "agents/ directory is required", errors)
    validate_skill_dir(ROOT / "skills", errors)

    brains = list(brain_dirs())
    require(brains, "at least one agent brain directory is required", errors)
    for brain_dir in brains:
        validate_brain(brain_dir, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(brains)} agent brains.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
