# Provider Keys & "Acting on Behalf Of"

Use these patterns to integrate with third‑party providers safely:

- **OAuth BYOA:** User connects their account; we receive a scoped token (Slack, Google, Notion, GitHub Apps, Figma).
- **Manager/Subaccount:** Use official manager constructs to create/own subaccounts (Google Ads MCC, Meta Business Manager, Twilio subaccounts, SendGrid subusers, Stripe Connect).
- **Stripe Connect:** Create connected accounts programmatically; avoid handling raw card data.

When raw API keys are unavoidable:
- Store only in GitHub Secrets at the repo/org level.
- Scope tokens tightly; rotate regularly.
