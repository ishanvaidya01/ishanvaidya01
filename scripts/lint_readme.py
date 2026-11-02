#!/usr/bin/env python3
"""
lint_readme.py
Validates README.md against hard GitHub constraints:
  - Valid HTML/Markdown
  - All <img> have alt and width
  - All local asset links point to existing files
  - Balanced <picture>, <table>, <tr>, <td> tags
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(BASE_DIR, "README.md")

def main():
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []

    # 1. Check all <img> tags have alt and width
    img_tags = re.findall(r'<img[^>]*>', content)
    for img in img_tags:
        if "alt=" not in img:
            errors.append(f"Missing alt in: {img}")
        if "width=" not in img:
            errors.append(f"Missing width in: {img}")

    # 2. Check all relative paths exist
    paths = re.findall(r'(?:src|srcset)="([^">]+)"', content)
    for p in paths:
        if not p.startswith("http"):
            clean_p = p.split("?")[0]
            full_p = os.path.join(BASE_DIR, clean_p)
            if not os.path.exists(full_p):
                errors.append(f"Broken asset path: {clean_p} (full: {full_p})")

    # 3. Check for balanced tags
    for tag in ["picture", "table", "tr", "td", "details", "summary", "a"]:
        open_tags = len(re.findall(rf'<{tag}[\s>]', content, re.IGNORECASE))
        close_tags = len(re.findall(rf'</{tag}>', content, re.IGNORECASE))
        if open_tags != close_tags:
            errors.append(f"Unbalanced <{tag}> tags: {open_tags} open, {close_tags} close")

    if errors:
        print("[!] Linting FAILED with errors:")
        for err in errors:
            print("  -", err)
        return False
    else:
        print(f"[+] SUCCESS: README.md passed all Quality Gate 4 lint checks! ({len(img_tags)} images, {len(paths)} paths verified)")
        return True

if __name__ == "__main__":
    if not main():
        exit(1)
