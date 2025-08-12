"""
Policy Gate evaluator (L0).
- Reads policy/policy.yaml
- Inspects changed files in the PR (in the TARGET_REPO_PATH working tree)
- Ensures 'change.yaml' exists and declared level matches inferred level
- Optionally enforces tests on P1+ changes that touch code (see policy.rules.require_tests_on_p1)
- Writes 'policy_level' to GITHUB_OUTPUT so the caller can label or automerge
"""
import os, sys, subprocess, json
from pathlib import Path
import yaml, fnmatch

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "policy" / "policy.yaml"
TARGET_REPO = Path(os.getenv("TARGET_REPO_PATH", "."))

def load_policy():
    with open(POLICY_PATH, "r") as f:
        return yaml.safe_load(f)

def get_default_branch():
    return os.getenv("DEFAULT_BRANCH") or "main"

def get_changed_files():
    base = os.getenv("GITHUB_BASE_SHA") or os.getenv("PR_BASE_SHA")
    head = os.getenv("GITHUB_SHA") or os.getenv("PR_HEAD_SHA")
    git_cmd = ["git", "-C", str(TARGET_REPO)]
    if base and head:
        out = subprocess.check_output(git_cmd + ["diff", "--name-only", f"{base}...{head}"], text=True)
        return [l.strip() for l in out.splitlines() if l.strip()]
    default_branch = get_default_branch()
    out = subprocess.check_output(git_cmd + ["diff", "--name-only", f"origin/{default_branch}..."], text=True)
    return [l.strip() for l in out.splitlines() if l.strip()]

def infer_level(changed, policy):
    for level in ("P2","P1","P0"):  # prioritize most restrictive
        patterns = policy["classification"].get(level, [])
        for f in changed:
            if any(fnmatch.fnmatch(f, pat) for pat in patterns):
                return level
    return "P1"

def read_declared_level():
    for p in [TARGET_REPO / "change.yaml", TARGET_REPO / ".github" / "change.yaml"]:
        if p.exists():
            with open(p) as f:
                y = yaml.safe_load(f) or {}
                return y.get("level"), y
    return None, {}

def write_output(level: str):
    out = os.getenv("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as fh:
            fh.write(f"policy_level={level}\n")

def requires_tests(changed, policy):
    # Heuristic: if P1-classified "code-ish" paths changed (excluding tests/**), require tests/** change on P1+
    codeish = [ "app/**", "ring1/agents/**", "ring1/tools/**" ]
    touches_code = any(any(fnmatch.fnmatch(f, pat) for pat in codeish) for f in changed)
    has_tests = any(
        f.startswith("tests/") or "/tests/" in f or f.endswith("_test.py") or Path(f).name.startswith("test_")
        for f in changed
    )
    return touches_code and not has_tests

def main():
    policy = load_policy()
    changed = get_changed_files()
    inferred = infer_level(changed, policy)
    declared, manifest = read_declared_level()

    summary = {
        "changed_files": changed,
        "inferred_level": inferred,
        "declared_level": declared,
        "policy_rules": policy["rules"],
    }
    print("::group::Policy Gate Summary")
    print(json.dumps(summary, indent=2))
    print("::endgroup::")

    if policy["rules"].get("require_change_manifest", True) and not declared:
        print("::error::Missing change.yaml manifest.")
        write_output(inferred)
        sys.exit(2)

    allowed = policy["rules"].get("allowed_change_levels", [])
    if declared not in allowed:
        print(f"::error::Declared level {declared} not allowed.")
        write_output(declared or inferred)
        sys.exit(3)

    order = {"P0":0,"P1":1,"P2":2}
    if order[declared] < order[inferred]:
        print(f"::error::Declared level {declared} lower than inferred {inferred}.")
        write_output(inferred)
        sys.exit(4)

    if policy["rules"].get("require_tests_on_p1", False) and declared in ("P1","P2"):
        if requires_tests(changed, policy):
            print("::error::P1+ code change without corresponding tests/** updates.")
            write_output(declared)
            sys.exit(5)

    write_output(declared or inferred)
    print("Policy gate passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
