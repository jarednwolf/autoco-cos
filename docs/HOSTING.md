# Hosting & Autonomy

This platform is **fully hosted** using GitHub Actions:
- No local machine or server required after the initial push.
- Schedules trigger cron jobs; PRs/issues trigger event‑driven jobs.
- Each venture (L2) carries its own CI, so the system scales horizontally.

## Scaling options
- **More parallelism (quick):** Increase concurrent jobs in GitHub Actions (Org settings).
- **Self‑hosted runners (later):** Add an autoscaling runner pool (e.g., DigitalOcean/AWS). Point workflows to those runners for heavy builds.
- **Serverless offload:** For long‑running tasks, invoke Cloud Run/Lambda from Actions and poll for completion.

## Observability
- Heartbeat workflow proves liveness.
- Morning Brief summarizes merges, pending approvals, and gate transitions (shown in configured local time).
- Evidence bundles live in repos for auditability.

## Security
- Secrets live in GitHub Secrets.
- Prefer OAuth or manager/subaccount patterns instead of raw keys.
- L1/L2 cannot edit L0 policy or secrets.
- CodeQL & gitleaks run by default (on **push** and **PR**); Dependabot updates Actions & Python deps.

## Reusable Workflows
- **Policy Gate** checks out the caller repo and this L0 repo, then evaluates changes in the caller (target) repo.
- **Stage Gate Check** can accept an explicit `stage` input or infer it from Issues (title/body) when triggered via issue flows.
