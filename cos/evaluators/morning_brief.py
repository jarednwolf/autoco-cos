"""
Morning Brief (L0).
- Summarizes last 24h: merged PRs, open P2 PRs.
- Posts/updates an Issue titled "Morning Brief YYYY-MM-DD".
- Displays times in configured TIMEZONE.
"""
import os, datetime
from zoneinfo import ZoneInfo
from textwrap import dedent
from github import Github  # PyGithub

TOKEN = os.getenv("GITHUB_TOKEN")
REPO  = os.getenv("GITHUB_REPOSITORY")  # e.g., owner/autoco-cos
TZ    = os.getenv("TIMEZONE", "America/Chicago")

def main():
    if not TOKEN or not REPO:
        print("Missing GITHUB_TOKEN or GITHUB_REPOSITORY.")
        return
    gh = Github(TOKEN)
    repo = gh.get_repo(REPO)

    now_utc = datetime.datetime.utcnow()
    local_now = now_utc.replace(tzinfo=datetime.timezone.utc).astimezone(ZoneInfo(TZ))
    since = now_utc - datetime.timedelta(days=1)

    merged = []
    for p in repo.get_pulls(state="closed", sort="updated", direction="desc"):
        if p.merged and p.merged_at and p.merged_at >= since:
            merged.append(p)

    p2_open = []
    for p in repo.get_pulls(state="open", sort="created", direction="desc"):
        labels = [l.name for l in p.get_labels()]
        if "P2" in labels:
            p2_open.append(p)

    body = dedent(f"""
    ### Morning Brief — {local_now.date().isoformat()} ({TZ})

    **Local time:** {local_now.strftime('%Y-%m-%d %H:%M %Z')}
    **Merged in last 24h:** {len(merged)}
    **Open P2 approvals:** {len(p2_open)}

    **Merged PRs:**
    {''.join([f'- #{p.number} {p.title}\n' for p in merged]) or 'None'}

    **Open P2 PRs:**
    {''.join([f'- #{p.number} {p.title}\n' for p in p2_open]) or 'None'}
    """)

    title = f"Morning Brief {local_now.date().isoformat()}"
    existing = next((i for i in repo.get_issues(state="open") if i.title == title), None)
    if existing:
        existing.edit(body=body)
    else:
        repo.create_issue(title=title, body=body)

if __name__ == "__main__":
    main()
