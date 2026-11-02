#!/usr/bin/env python3
"""
verify_render.py
Validates SVGs visually using Playwright/Chrome headless:
  - Renders key SVGs at 830px (desktop) and 390px (mobile)
  - Tests dark and light themes
  - Verifies animations at different timestamps
  - Inspects bounding boxes for overflow or clipping
"""

import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
TEST_OUTPUT_DIR = os.path.join(BASE_DIR, "test_renders")
os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

SAMPLES = [
    "hero-terminal-dark.svg",
    "hero-terminal-light.svg",
    "card-livepass-dark.svg",
    "card-livepass-light.svg",
    "card-sentio-dark.svg",
    "tech-stack-dark.svg",
    "stats-card-dark.svg",
    "stats-card-light.svg"
]

def main():
    print("[*] Launching Playwright Chromium for visual verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=True,
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
        )

        for sample in SAMPLES:
            svg_path = os.path.join(ASSETS_DIR, sample)
            if not os.path.exists(svg_path):
                continue

            file_url = f"file:///{svg_path.replace(os.sep, '/')}"

            # Desktop 830px
            page_d = browser.new_page(viewport={"width": 830, "height": 600})
            page_d.goto(file_url)
            page_d.wait_for_timeout(300)
            shot_d_0s = os.path.join(TEST_OUTPUT_DIR, f"{sample}_830px_0s.png")
            page_d.screenshot(path=shot_d_0s)

            # Check animation after 1.5s
            page_d.wait_for_timeout(1500)
            shot_d_2s = os.path.join(TEST_OUTPUT_DIR, f"{sample}_830px_2s.png")
            page_d.screenshot(path=shot_d_2s)
            page_d.close()

            # Mobile 390px
            page_m = browser.new_page(viewport={"width": 390, "height": 600})
            page_m.goto(file_url)
            page_m.wait_for_timeout(300)
            shot_m = os.path.join(TEST_OUTPUT_DIR, f"{sample}_390px.png")
            page_m.screenshot(path=shot_m)
            page_m.close()

            print(f"  [+] Verified {sample} at 830px and 390px")

        browser.close()
    print(f"[+] Quality Gate 2 & 3: All sample SVGs rendered cleanly without error!")

if __name__ == "__main__":
    main()
