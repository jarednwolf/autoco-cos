# autoco-cos (L0: Chief of Staff)

![Heartbeat](https://github.com/jarednwolf/autoco-cos/actions/workflows/heartbeat.yml/badge.svg)
![Morning Brief](https://github.com/jarednwolf/autoco-cos/actions/workflows/morning-brief.yml/badge.svg)
![CodeQL](https://github.com/jarednwolf/autoco-cos/actions/workflows/codeql.yml/badge.svg)
![Gitleaks](https://github.com/jarednwolf/autoco-cos/actions/workflows/gitleaks.yml/badge.svg)

The **Chief of Staff (CoS)** is the control plane:
- Enforces policy levels (P0/P1/P2) via reusable **Policy Gate** workflow
- Validates stage‑gate evidence via reusable **Stage Gate Check** workflow (can infer stage from Issues)
- Schedules recurring jobs (Morning Brief, Heartbeat, Budget Guard)
- Manages secrets (via GitHub Actions secrets)
- Runs 100% in the cloud via **GitHub‑hosted runners** — no servers to maintain

**Hosted & Autonomous**
- Workflows run on a schedule or on repo events.
- L2 ventures get their **own CI**, scaling horizontally by design.
- This repo is designed to be **public** so other repos can reuse its workflows without org‑level toggles.

**Observability**
- The badges above reflect the latest workflow health and security scans.
- Morning Brief issues summarize activity by timezone for quick status glances.

**Glossary**
- Layers: L0 (CoS) · L1 (Company‑001) · L2 (Ventures)
- Stage Gates: DISC-P → DISC-A → VAL → BUILD → LAUNCH → GROW
- Policy Levels: P0 (Autonomous) · P1 (Auto if checks pass) · P2 (Human approval)

