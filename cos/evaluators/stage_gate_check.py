"""
Stage Gate Check (L0).
- Loads gate spec from L0/stage-gates/{stage}.yaml
- Checks artifacts and simple numeric thresholds in venture repo
- Writes a short summary; exits nonzero on failure
"""
import os, sys, json
from pathlib import Path
import yaml

L0_PATH = Path(os.getenv("L0_PATH", "l0"))
VENTURE_PATH = Path(os.getenv("VENTURE_PATH", "venture"))
STAGE = os.getenv("STAGE", "").strip()

def fail(msg):
    print(f"::error::{msg}")
    sys.exit(1)

def load_gate(stage):
    p = L0_PATH / "stage-gates" / f"{stage}.yaml"
    if not p.exists():
        fail(f"Stage file not found: {p}")
    return yaml.safe_load(p.read_text())

def check_artifacts(artifacts):
    missing = []
    for a in artifacts or []:
        if not (VENTURE_PATH / "evidence" / a).exists():
            missing.append(a)
    return missing

def read_json(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return None

def main():
    if not STAGE:
        fail("STAGE input is required.")
    gate = load_gate(STAGE)

    missing = check_artifacts(gate.get("artifacts", []))
    if missing:
        fail(f"Missing required artifacts under evidence/: {missing}")

    # VAL thresholds
    if STAGE == "VAL":
        lm = read_json(VENTURE_PATH / "evidence" / "landing-metrics.json") or {}
        ok = (lm.get("waitlist_signups", 0) >= 100) or (lm.get("qualified_leads", 0) >= 10) or (lm.get("paid_pilots", 0) >= 3)
        if not ok:
            fail("VAL thresholds not met (need waitlist>=100 OR leads>=10 OR paid_pilots>=3).")

    # BUILD thresholds
    if STAGE == "BUILD":
        e2e = read_json(VENTURE_PATH / "evidence" / "e2e-report.json") or {}
        act = read_json(VENTURE_PATH / "evidence" / "activation-metrics.json") or {}
        if (e2e.get("pass_rate", 0) < 0.9) or (act.get("activation_rate", 0) < 0.2):
            fail("BUILD thresholds not met (e2e pass_rate>=0.9 AND activation_rate>=0.2).")

    # LAUNCH thresholds
    if STAGE == "LAUNCH":
        uptime = (read_json(VENTURE_PATH / "evidence" / "uptime-report.json") or {}).get("uptime", 0.0)
        cac = (read_json(VENTURE_PATH / "evidence" / "cac-microtest.json") or {}).get("cac", 1e9)
        if uptime < 0.995 or cac > 10.0:
            fail("LAUNCH thresholds not met (uptime>=0.995 AND CAC<=10.0).")

    # GROW thresholds
    if STAGE == "GROW":
        cohort = read_json(VENTURE_PATH / "evidence" / "cohort-report.json") or {}
        unit = read_json(VENTURE_PATH / "evidence" / "unit-econ.json") or {}
        if (cohort.get("retention_dN", 0.0) < 0.3) or (unit.get("payback_months", 1e9) > 6):
            fail("GROW thresholds not met (retention_dN>=0.3 AND payback_months<=6).")

    print(f"Stage Gate Check passed for {STAGE}.")
    sys.exit(0)

if __name__ == "__main__":
    main()
