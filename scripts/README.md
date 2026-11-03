# Automation Scripts & Asset Generators

This directory contains the automation tooling used to generate and maintain the hand-crafted SVG assets for Ishan Vaidya's GitHub profile.

## Scripts Overview

### 1. `generate_stats.py`
Queries the GitHub GraphQL API to compile authenticated real-time metrics:
- Past year commit volume
- Pull request activity
- Owned repositories
- Current contribution streak (computed from the contribution calendar)
- Byte-weighted language distribution

Falls back to unauthenticated REST telemetry and, as a last resort, to a
verified static snapshot — the numbers are never inflated.

Generates two production SVGs:
- `assets/stats-card-dark.svg`
- `assets/stats-card-light.svg`

**Local Execution:**
```bash
# Using personal access token (full GraphQL telemetry):
export GITHUB_TOKEN="ghp_your_token_here"
python scripts/generate_stats.py

# Without token (computed from the public REST API):
python scripts/generate_stats.py
```

### 2. `build_assets.py`
The master design compiler that builds all 44 vector assets (hero terminal, avatar ring, section headers, flagship LivePass card with live feed simulation, compact project cards, tech stack matrix, and the contact-channel connect banner) with dark and light variants.

**Local Execution:**
```bash
python scripts/build_assets.py
```

### 3. `verify_render.py`
Quality gate verification harness that uses headless Chromium to render every asset at 830px (desktop) and 390px (mobile), verifying visual bounds and animation execution.

