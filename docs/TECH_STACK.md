# Tech Stack (L0 — Chief of Staff)

- **Runtime:** Python 3.11 on GitHub‑hosted Ubuntu runners
- **API (tests only):** FastAPI `/health`
- **CI/CD:** Reusable workflows:
  - `reusable-policy-gate.yml` to classify/guard PRs by P0/P1/P2 (checks out caller + L0)
  - `stage-gate-check.yml` to validate evidence vs. stage criteria (can infer `stage` from Issues)
  - `morning-brief.yml` (TZ aware, optional email; PR read perms)
  - `heartbeat.yml` (liveness)
  - `budget-guard.yml` (stub)
- **Security:** CodeQL, gitleaks (push + PR), Dependabot
- **Infra state:** Files + Issues (evidence bundles, briefs)
- **Secrets:** GitHub Secrets
- **Scale options:**
  - Add self‑hosted runners (autoscaling) and point heavy jobs there
  - Offload long tasks to serverless (Cloud Run/Lambda) via curl from Actions
- **Extension points:**
  - Add more evaluators under `cos/evaluators/`
  - Add new stage‑gates in `stage-gates/`
  - Tighten policies in `policy/policy.yaml`
