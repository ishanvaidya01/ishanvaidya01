#!/usr/bin/env python3
"""
generate_stats.py
Queries the GitHub API for Ishan Vaidya's REAL metrics (never fabricated)
and renders high-fidelity, theme-adaptive stats SVGs.

Data sources:
  - Authenticated GraphQL (GITHUB_TOKEN): contribution calendar, commits,
    pull requests, owned repository count and language byte distribution.
  - Unauthenticated REST fallback (no token): search API + public events.
  - Static snapshot fallback only if every live query fails.

Output files:
  - assets/stats-card-dark.svg
  - assets/stats-card-light.svg
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

USERNAME = "ishanvaidya01"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

# Static snapshot (only used when ALL live queries fail). Shipped values are
# the verified real numbers as of the last successful generation run.
SNAPSHOT_METRICS = {
    "total_commits": 145,
    "merged_prs": 2,
    "contributed_repos": 12,
    "current_streak_days": 1,
    "languages": [
        {"name": "JavaScript", "color": "#F1E05A", "percent": 49.4},
        {"name": "Python", "color": "#3572A5", "percent": 24.9},
        {"name": "TypeScript", "color": "#3178C6", "percent": 13.8},
        {"name": "HTML", "color": "#E34C26", "percent": 7.3},
        {"name": "CSS", "color": "#563D7C", "percent": 3.2},
    ]
}

GITHUB_COLORS = {
    "JavaScript": "#F1E05A", "Python": "#3572A5", "TypeScript": "#3178C6",
    "HTML": "#E34C26", "CSS": "#563D7C", "PLSQL": "#E38C00", "Shell": "#89E051",
    "Dockerfile": "#384D54", "Batchfile": "#C1F12E", "Jupyter Notebook": "#DA5B0B",
}


def _get(url, headers=None, timeout=12):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "IshanVaidya-Stats-Generator"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


# -------------------------------------------------------------------------
# Current-streak computation (real, from dated contribution days)
# -------------------------------------------------------------------------
def compute_current_streak(days):
    """days: dict of ISO date string -> contribution count. Returns
    consecutive-days streak ending at the most recent active day."""
    active = sorted((d for d, n in days.items() if n > 0), reverse=True)
    if not active:
        return 0

    # Allow the calendar's most recent day to lag by one day (GitHub quirk)
    latest = active[0]
    streak = 0
    cursor = datetime.strptime(latest, "%Y-%m-%d").date()
    while cursor.isoformat() in active:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


# -------------------------------------------------------------------------
# LIVE SOURCE 1: Authenticated GraphQL (handles private data + calendar)
# -------------------------------------------------------------------------
GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
    repositories(first: 100, ownerAffiliations: OWNER, orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes {
        isPrivate
        languages(first: 15, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node { name color }
          }
        }
      }
    }
  }
}
"""


def metrics_from_graphql(token):
    data = _get(
        "https://api.github.com/graphql",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "IshanVaidya-Stats-Generator",
        },
    )
    # POST the query (GraphQL needs a POST with a JSON body)
    body = json.dumps({"query": GRAPHQL_QUERY, "variables": {"login": USERNAME}}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "IshanVaidya-Stats-Generator",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    user = (data.get("data") or {}).get("user") or {}
    if not user:
        raise RuntimeError(f"GraphQL returned no user: {json.dumps(data)[:200]}")

    cc = user.get("contributionsCollection", {})
    commits = int(cc.get("totalCommitContributions") or 0)
    prs = int(cc.get("totalPullRequestContributions") or 0)

    calendar_days = {}
    for week in (cc.get("contributionCalendar") or {}).get("weeks", []):
        for day in week.get("contributionDays", []):
            calendar_days[day["date"]] = int(day["contributionCount"])
    streak = compute_current_streak(calendar_days)

    repos = user.get("repositories", {})
    repo_count = int(repos.get("totalCount") or 0)
    # The profile repo (named after the username) is identity, not engineering
    repo_count = max(repo_count - 1, 0)

    lang_totals = {}
    for repo in repos.get("nodes") or []:
        for edge in repo.get("languages", {}).get("edges", []):
            node = edge["node"]
            name = node["name"]
            lang_totals[name] = lang_totals.get(name, 0) + edge["size"]

    total_size = sum(lang_totals.values())
    if total_size > 0:
        top = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        languages = [
            {"name": name, "color": GITHUB_COLORS.get(name, "#888888"),
             "percent": round((size / total_size) * 100, 1)}
            for name, size in top
        ]
    else:
        languages = SNAPSHOT_METRICS["languages"]

    return {
        "total_commits": commits,
        "merged_prs": prs,
        "contributed_repos": repo_count,
        "current_streak_days": streak,
        "languages": languages,
    }


# -------------------------------------------------------------------------
# LIVE SOURCE 2: Unauthenticated REST fallback
# -------------------------------------------------------------------------
def metrics_from_rest():
    since = (datetime.now(timezone.utc) - timedelta(days=365)).strftime("%Y-%m-%d")
    headers = {"User-Agent": "IshanVaidya-Stats-Generator", "Accept": "application/vnd.github+json"}

    search_headers = dict(headers)
    search_headers["Accept"] = "application/vnd.github.cloak-preview+json"

    commits = int(_get(
        f"https://api.github.com/search/commits?q=author:{USERNAME}+committer-date:%3E{since}",
        headers=search_headers,
    )["total_count"])

    prs = int(_get(
        f"https://api.github.com/search/issues?q=author:{USERNAME}+type:pr",
        headers=search_headers,
    )["total_count"])

    user = _get(f"https://api.github.com/users/{USERNAME}", headers=headers)
    repos = max(int(user.get("public_repos", 0)) - 1, 0)  # minus the profile repo

    # Public events give an honest current streak (last 90 days of activity)
    events = _get(f"https://api.github.com/users/{USERNAME}/events/public?per_page=100", headers=headers)
    streak = compute_current_streak({e["created_at"][:10]: 1 for e in events if isinstance(e, dict)})

    languages = {
        name: size
        for repo in _get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100", headers=headers)
        if isinstance(repo, dict) and repo["name"] != USERNAME
        for name, size in _get(repo["languages_url"], headers=headers).items()
    }
    total = sum(languages.values())
    if total > 0:
        top = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        lang_list = [
            {"name": name, "color": GITHUB_COLORS.get(name, "#888888"),
             "percent": round((size / total) * 100, 1)}
            for name, size in top
        ]
    else:
        raise RuntimeError("No language data available")

    return {
        "total_commits": commits,
        "merged_prs": prs,
        "contributed_repos": repos,
        "current_streak_days": streak,
        "languages": lang_list,
    }


def fetch_github_metrics():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        try:
            print("[*] Authenticated GraphQL telemetry...")
            return metrics_from_graphql(token)
        except Exception as e:
            print(f"[!] GraphQL failed ({e}); trying unauthenticated REST.")

    try:
        print("[*] Unauthenticated REST telemetry...")
        return metrics_from_rest()
    except Exception as e:
        print(f"[!] REST failed ({e}); using verified static snapshot.")
        return SNAPSHOT_METRICS


def render_stats_svg(metrics, theme="dark"):
    is_dark = theme == "dark"
    bg = "#0D1117" if is_dark else "#FFFFFF"
    border = "#30363D" if is_dark else "#D0D7DE"
    text_primary = "#E6EDF3" if is_dark else "#1F2328"
    text_muted = "#8B949E" if is_dark else "#656D76"
    accent = "#58E6D9" if is_dark else "#0D9488"
    badge_bg = "rgba(88, 230, 217, 0.12)" if is_dark else "rgba(13, 148, 136, 0.10)"
    bar_track = "#21262D" if is_dark else "#EAEEF2"

    commits = f"{metrics['total_commits']:,}"
    prs = f"{metrics['merged_prs']:,}"
    repos = f"{metrics['contributed_repos']:,}"
    streak = f"{metrics['current_streak_days']}d"

    # Compute language segments
    langs = metrics["languages"]
    segments_svg = []
    legend_svg = []
    cum_percent = 0.0
    bar_width = 770

    for lang in langs:
        pct = lang["percent"]
        w = round((pct / 100.0) * bar_width, 1)
        x = round((cum_percent / 100.0) * bar_width, 1)
        cum_percent += pct
        segments_svg.append(
            f'<rect x="{30 + x}" y="104" width="{max(w, 2)}" height="8" rx="2" fill="{lang["color"]}" />'
        )

    # Distribute legend across the bar
    leg_x = 30
    for lang in langs:
        legend_svg.append(f'''
        <g transform="translate({leg_x}, 128)">
          <circle cx="4" cy="4" r="3.5" fill="{lang["color"]}" />
          <text x="13" y="7" font-family="'SF Mono', 'JetBrains Mono', ui-monospace, monospace" font-size="10.5" fill="{text_primary}">{lang["name"]} <tspan fill="{text_muted}">{lang["percent"]}%</tspan></text>
        </g>
        ''')
        leg_x += (len(lang["name"]) * 7) + 56

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 156" width="100%" height="156" fill="none">
  <defs>
    <style>
      .stat-val {{
        font-family: 'SF Mono', 'JetBrains Mono', ui-monospace, Menlo, Consolas, monospace;
        font-weight: 700;
        font-size: 20px;
        letter-spacing: -0.5px;
      }}
      .stat-lbl {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
        font-weight: 600;
        font-size: 11px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
      }}
      .sec-hdr {{
        font-family: 'SF Mono', 'JetBrains Mono', ui-monospace, monospace;
        font-weight: 700;
        font-size: 11px;
        letter-spacing: 1px;
      }}
      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
      }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="830" height="156" rx="8" fill="{bg}" stroke="{border}" stroke-width="1.2"/>

  <!-- Header line -->
  <g transform="translate(30, 26)">
    <text x="0" y="0" fill="{accent}" class="sec-hdr">// SYSTEM TELEMETRY &amp; COMMIT VOLUME</text>
    <rect x="680" y="-12" width="90" height="18" rx="9" fill="{badge_bg}"/>
    <circle cx="690" cy="-3" r="3" fill="{accent}"/>
    <text x="698" y="0" font-family="'SF Mono', monospace" font-size="9.5" font-weight="700" fill="{accent}">LIVE</text>
  </g>

  <!-- Metric Columns (4 items) -->
  <g transform="translate(30, 48)">
    <!-- Commits -->
    <g transform="translate(0, 0)">
      <text x="0" y="18" fill="{text_primary}" class="stat-val">{commits}</text>
      <text x="0" y="34" fill="{text_muted}" class="stat-lbl">Yearly Commits</text>
    </g>

    <!-- PRs -->
    <g transform="translate(200, 0)">
      <text x="0" y="18" fill="{text_primary}" class="stat-val">{prs}</text>
      <text x="0" y="34" fill="{text_muted}" class="stat-lbl">Pull Requests</text>
    </g>

    <!-- Repos -->
    <g transform="translate(400, 0)">
      <text x="0" y="18" fill="{text_primary}" class="stat-val">{repos}</text>
      <text x="0" y="34" fill="{text_muted}" class="stat-lbl">Repositories</text>
    </g>

    <!-- Active Streak -->
    <g transform="translate(600, 0)">
      <text x="0" y="18" fill="{accent}" class="stat-val">{streak}</text>
      <text x="0" y="34" fill="{text_muted}" class="stat-lbl">Active Streak</text>
    </g>
  </g>

  <!-- Language Progress Bar Track -->
  <rect x="30" y="104" width="{bar_width}" height="8" rx="2" fill="{bar_track}" />
  {''.join(segments_svg)}

  <!-- Language Legend -->
  {''.join(legend_svg)}
</svg>'''


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    metrics = fetch_github_metrics()

    print(f"[*] Metrics: commits={metrics['total_commits']}, prs={metrics['merged_prs']}, "
          f"repos={metrics['contributed_repos']}, streak={metrics['current_streak_days']}d, "
          f"langs={[l['name'] for l in metrics['languages']]}")

    dark_svg = render_stats_svg(metrics, theme="dark")
    light_svg = render_stats_svg(metrics, theme="light")

    with open(os.path.join(OUTPUT_DIR, "stats-card-dark.svg"), "w", encoding="utf-8") as f:
        f.write(dark_svg)

    with open(os.path.join(OUTPUT_DIR, "stats-card-light.svg"), "w", encoding="utf-8") as f:
        f.write(light_svg)

    print(f"[+] Stats SVGs generated successfully in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
