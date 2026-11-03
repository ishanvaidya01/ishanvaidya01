#!/usr/bin/env python3
"""
build_assets.py
Generates the complete suite of hand-crafted, theme-adaptive SVG assets
for Ishan Vaidya's GitHub Profile README (@ishanvaidya01).
Strict Quality Standards:
  - 100% valid XML.
  - Zero external HTTP font/image references.
  - Full support for prefers-reduced-motion.
  - Precise GitHub 830px column width layout.
"""

import os
import base64
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# PALETTES
# -------------------------------------------------------------------------
THEMES = {
    "dark": {
        "bg": "#0D1117",
        "surface": "#161B22",
        "surface_hover": "#21262D",
        "border": "#30363D",
        "border_subtle": "#21262D",
        "text": "#E6EDF3",
        "text_muted": "#8B949E",
        "text_dim": "#484F58",
        "accent": "#58E6D9",       # Electric Cyan
        "accent_dim": "rgba(88, 230, 217, 0.15)",
        "accent_glow": "rgba(88, 230, 217, 0.4)",
        "warm": "#F59E0B",         # Amber (Flagship only)
        "warm_dim": "rgba(245, 158, 11, 0.15)",
        "success": "#34D399",
        "chip_bg": "#21262D",
        "chip_border": "#30363D",
        "chip_text": "#C9D1D9",
        "grid_line": "rgba(255, 255, 255, 0.03)"
    },
    "light": {
        "bg": "#FFFFFF",
        "surface": "#F6F8FA",
        "surface_hover": "#EAEEF2",
        "border": "#D0D7DE",
        "border_subtle": "#E1E4E8",
        "text": "#1F2328",
        "text_muted": "#656D76",
        "text_dim": "#8C959F",
        "accent": "#0D9488",       # Deep Teal / Cyan
        "accent_dim": "rgba(13, 148, 136, 0.12)",
        "accent_glow": "rgba(13, 148, 136, 0.3)",
        "warm": "#D97706",         # Dark Amber
        "warm_dim": "rgba(217, 119, 6, 0.12)",
        "success": "#16A34A",
        "chip_bg": "#EAEEF2",
        "chip_border": "#D0D7DE",
        "chip_text": "#24292F",
        "grid_line": "rgba(0, 0, 0, 0.03)"
    }
}

FONT_MONO = "'SF Mono', 'JetBrains Mono', ui-monospace, Menlo, Consolas, monospace"
FONT_SANS = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif"

def load_profile_base64():
    p = os.path.join(BASE_DIR, "profile.png")
    if os.path.exists(p):
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")
    return ""

PROFILE_B64 = load_profile_base64()

# -------------------------------------------------------------------------
# 1. HERO TERMINAL (590 x 200)
# -------------------------------------------------------------------------
def build_hero_terminal(theme="dark"):
    c = THEMES[theme]
    is_dark = theme == "dark"
    dot_red = "#FF5F56"
    dot_yellow = "#FFBD2E"
    dot_green = "#27C93F"

    # Terminal animation: Line 1 -> Line 2 -> Line 3 progressive typing
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 590 200" width="100%" height="200" fill="none">
  <defs>
    <style>
      .mono {{ font-family: {FONT_MONO}; }}
      .sans {{ font-family: {FONT_SANS}; }}
      
      @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
      }}
      @keyframes type-seq1 {{
        0% {{ opacity: 0; transform: translateX(-4px); }}
        8%, 95% {{ opacity: 1; transform: translateX(0); }}
        100% {{ opacity: 1; }}
      }}
      @keyframes type-seq2 {{
        0%, 30% {{ opacity: 0; transform: translateX(-4px); }}
        38%, 95% {{ opacity: 1; transform: translateX(0); }}
        100% {{ opacity: 1; }}
      }}
      @keyframes type-seq3 {{
        0%, 60% {{ opacity: 0; transform: translateX(-4px); }}
        68%, 95% {{ opacity: 1; transform: translateX(0); }}
        100% {{ opacity: 1; }}
      }}

      .cursor {{
        animation: blink 1s infinite;
      }}
      .l1 {{ animation: type-seq1 12s infinite; }}
      .l2 {{ animation: type-seq2 12s infinite; }}
      .l3 {{ animation: type-seq3 12s infinite; }}

      @media (prefers-reduced-motion: reduce) {{
        .l1, .l2, .l3 {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
        .cursor {{ animation: none !important; opacity: 1 !important; }}
      }}
    </style>
  </defs>

  <!-- Window Frame -->
  <rect width="590" height="200" rx="8" fill="{c['bg']}" stroke="{c['border']}" stroke-width="1.2"/>
  
  <!-- Titlebar -->
  <path d="M 0 8 Q 0 0 8 0 L 582 0 Q 590 0 590 8 L 590 32 L 0 32 Z" fill="{c['surface']}"/>
  <line x1="0" y1="32" x2="590" y2="32" stroke="{c['border']}" stroke-width="1"/>

  <!-- Window Controls -->
  <circle cx="20" cy="16" r="5" fill="{dot_red}"/>
  <circle cx="36" cy="16" r="5" fill="{dot_yellow}"/>
  <circle cx="52" cy="16" r="5" fill="{dot_green}"/>

  <!-- Title & Status -->
  <text x="295" y="20" text-anchor="middle" fill="{c['text_muted']}" class="mono" font-size="11" font-weight="600">ishan@architect: ~ (zsh)</text>
  <rect x="500" y="8" width="76" height="16" rx="8" fill="{c['accent_dim']}"/>
  <circle cx="510" cy="16" r="3" fill="{c['accent']}"/>
  <text x="518" y="19" fill="{c['accent']}" class="mono" font-size="9" font-weight="700">SYS_OK</text>

  <!-- Terminal Body Grid -->
  <line x1="24" y1="75" x2="566" y2="75" stroke="{c['grid_line']}" stroke-width="1"/>
  <line x1="24" y1="120" x2="566" y2="120" stroke="{c['grid_line']}" stroke-width="1"/>
  <line x1="24" y1="165" x2="566" y2="165" stroke="{c['grid_line']}" stroke-width="1"/>

  <!-- Line 1: whoami -->
  <g class="l1">
    <text x="24" y="60" fill="{c['accent']}" class="mono" font-size="12" font-weight="700">$</text>
    <text x="38" y="60" fill="{c['text']}" class="mono" font-size="12" font-weight="600">whoami</text>
    <text x="96" y="60" fill="{c['text_muted']}" class="mono" font-size="12">&#8594;</text>
    <text x="114" y="60" fill="{c['text']}" class="mono" font-size="12" font-weight="700">ishan_vaidya</text>
    <text x="220" y="60" fill="{c['text_muted']}" class="mono" font-size="11">// CSE @ VIT Chennai</text>
  </g>

  <!-- Line 2: cat stack.txt -->
  <g class="l2">
    <text x="24" y="105" fill="{c['accent']}" class="mono" font-size="12" font-weight="700">$</text>
    <text x="38" y="105" fill="{c['text']}" class="mono" font-size="12" font-weight="600">cat stack.txt</text>
    <text x="146" y="105" fill="{c['text_muted']}" class="mono" font-size="12">&#8594;</text>
    <text x="164" y="105" fill="{c['accent']}" class="mono" font-size="12" font-weight="600">postgres &#183; websockets &#183; langchain &#183; onnx</text>
  </g>

  <!-- Line 3: ./build -->
  <g class="l3">
    <text x="24" y="150" fill="{c['accent']}" class="mono" font-size="12" font-weight="700">$</text>
    <text x="38" y="150" fill="{c['text']}" class="mono" font-size="12" font-weight="600">./build --concurrency-safe --offline-first --agentic</text>
    <text x="24" y="178" fill="{c['success']}" class="mono" font-size="11" font-weight="600">[DONE] zero race conditions &#183; deterministic tools &#183; live feeds</text>
    <rect x="496" y="167" width="7" height="13" fill="{c['accent']}" class="cursor"/>
  </g>
</svg>'''

# -------------------------------------------------------------------------
# 2. AVATAR RING (220 x 200)
# -------------------------------------------------------------------------
def build_avatar_ring(theme="dark"):
    c = THEMES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 200" width="100%" height="200" fill="none">
  <defs>
    <linearGradient id="avatar-ring-grad-{theme}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c['accent']}"/>
      <stop offset="50%" stop-color="{c['border']}"/>
      <stop offset="100%" stop-color="{c['accent']}"/>
    </linearGradient>
    <clipPath id="avatar-clip-{theme}">
      <circle cx="110" cy="94" r="68"/>
    </clipPath>
    <style>
      .ring {{
        transform-origin: 110px 94px;
        animation: spin-ring 18s linear infinite;
      }}
      @keyframes spin-ring {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .ring {{ animation: none !important; }}
      }}
    </style>
  </defs>

  <!-- Outer Card Frame -->
  <rect width="220" height="200" rx="8" fill="{c['bg']}" stroke="{c['border']}" stroke-width="1.2"/>

  <!-- Rotating Dashed Ring -->
  <circle cx="110" cy="94" r="75" fill="none" stroke="url(#avatar-ring-grad-{theme})" stroke-width="2.2" stroke-dasharray="14 8 26 6" class="ring"/>
  <circle cx="110" cy="94" r="70" fill="none" stroke="{c['border_subtle']}" stroke-width="1"/>

  <!-- Clipped Profile Image -->
  <image href="data:image/png;base64,{PROFILE_B64}" x="42" y="26" width="136" height="136" clip-path="url(#avatar-clip-{theme})" preserveAspectRatio="xMidYMid slice"/>

  <!-- Live Status Pip -->
  <circle cx="160" cy="144" r="9" fill="{c['bg']}"/>
  <circle cx="160" cy="144" r="5" fill="{c['success']}"/>

  <!-- Sub-label -->
  <text x="110" y="184" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="{c['text_muted']}">ONLINE // VERIFIED</text>
</svg>'''

# -------------------------------------------------------------------------
# 3. SECTION DIVIDER (830 x 20)
# -------------------------------------------------------------------------
def build_section_divider(theme="dark"):
    c = THEMES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 20" width="100%" height="20" fill="none">
  <defs>
    <linearGradient id="div-grad-{theme}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{c['border']}" stop-opacity="0"/>
      <stop offset="25%" stop-color="{c['border']}"/>
      <stop offset="50%" stop-color="{c['accent']}"/>
      <stop offset="75%" stop-color="{c['border']}"/>
      <stop offset="100%" stop-color="{c['border']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <line x1="20" y1="10" x2="810" y2="10" stroke="url(#div-grad-{theme})" stroke-width="1.2"/>
  <polygon points="415,6 419,10 415,14 411,10" fill="{c['accent']}"/>
</svg>'''

# -------------------------------------------------------------------------
# 4. SECTION HEADERS (830 x 40)
# -------------------------------------------------------------------------
def build_section_header(title, tag, theme="dark"):
    c = THEMES[theme]
    clean_title = title.replace("&", "&amp;")
    clean_tag = tag.replace("&", "&amp;")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 40" width="100%" height="40" fill="none">
  <defs>
    <style>
      .hdr-title {{
        font-family: {FONT_MONO};
        font-size: 13.5px;
        font-weight: 700;
        letter-spacing: 0.8px;
      }}
      .hdr-tag {{
        font-family: {FONT_MONO};
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.5px;
      }}
    </style>
  </defs>

  <!-- Left Accent Marker -->
  <rect x="0" y="8" width="4" height="24" rx="2" fill="{c['accent']}"/>
  
  <!-- Title -->
  <text x="18" y="24" fill="{c['text']}" class="hdr-title">{clean_title}</text>
  
  <!-- Right Category Pill -->
  <rect x="690" y="10" width="140" height="20" rx="10" fill="{c['accent_dim']}" stroke="{c['border_subtle']}"/>
  <text x="760" y="23" text-anchor="middle" fill="{c['accent']}" class="hdr-tag">{clean_tag}</text>
</svg>'''

# -------------------------------------------------------------------------
# 5. FLAGSHIP PROJECT CARD: LIVEPASS (830 x 170)
# -------------------------------------------------------------------------
def build_livepass_card(theme="dark"):
    c = THEMES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 170" width="100%" height="170" fill="none">
  <defs>
    <linearGradient id="livepass-border-{theme}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c['warm']}"/>
      <stop offset="50%" stop-color="{c['border']}"/>
      <stop offset="100%" stop-color="{c['accent']}"/>
    </linearGradient>
    <style>
      .mono {{ font-family: {FONT_MONO}; }}
      .sans {{ font-family: {FONT_SANS}; }}
      
      @keyframes pulse-live {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.3; }}
      }}
      @keyframes feed-scroll {{
        0% {{ transform: translateY(0); }}
        33% {{ transform: translateY(-22px); }}
        66% {{ transform: translateY(-44px); }}
        100% {{ transform: translateY(0); }}
      }}

      .live-dot {{ animation: pulse-live 1.5s infinite; }}
      .feed-list {{ animation: feed-scroll 9s ease-in-out infinite; }}

      @media (prefers-reduced-motion: reduce) {{
        .live-dot, .feed-list {{ animation: none !important; }}
      }}
    </style>
  </defs>

  <!-- Card Background & Animated Accent Border -->
  <rect width="830" height="170" rx="8" fill="{c['bg']}" stroke="url(#livepass-border-{theme})" stroke-width="1.8"/>

  <!-- Left Content Column -->
  <g transform="translate(28, 26)">
    <!-- Badges Row -->
    <rect x="0" y="0" width="94" height="20" rx="4" fill="{c['warm_dim']}"/>
    <text x="47" y="13" text-anchor="middle" fill="{c['warm']}" class="mono" font-size="9.5" font-weight="700">★ FLAGSHIP</text>

    <rect x="102" y="0" width="150" height="20" rx="4" fill="{c['accent_dim']}"/>
    <text x="177" y="13" text-anchor="middle" fill="{c['accent']}" class="mono" font-size="9.5" font-weight="700">HIGH-CONCURRENCY</text>

    <!-- Title -->
    <text x="0" y="44" fill="{c['text']}" class="sans" font-size="19" font-weight="800" letter-spacing="-0.3">LivePass</text>
    <text x="86" y="44" fill="{c['text_muted']}" class="mono" font-size="12">&#8212; High-Throughput Access Governance</text>

    <!-- Pitch (max 2 sentences, crisp, architectural challenge) -->
    <text x="0" y="70" fill="{c['text']}" class="sans" font-size="12.5" font-weight="400">Eliminates double-redemption race conditions during burst ingress using PostgreSQL row-level locks (<tspan fill="{c['accent']}" class="mono">SELECT FOR UPDATE</tspan>).</text>
    <text x="0" y="88" fill="{c['text_muted']}" class="sans" font-size="12">Coordinates offline-first client queues via IndexedDB with cryptographic idempotency and sub-100ms WebSocket broadcasts.</text>

    <!-- Stack Chips -->
    <g transform="translate(0, 108)">
      <rect x="0" y="0" width="76" height="20" rx="4" fill="{c['chip_bg']}" stroke="{c['chip_border']}"/>
      <text x="38" y="13" text-anchor="middle" fill="{c['chip_text']}" class="mono" font-size="9.5">PostgreSQL</text>

      <rect x="84" y="0" width="60" height="20" rx="4" fill="{c['chip_bg']}" stroke="{c['chip_border']}"/>
      <text x="114" y="13" text-anchor="middle" fill="{c['chip_text']}" class="mono" font-size="9.5">FastAPI</text>

      <rect x="152" y="0" width="76" height="20" rx="4" fill="{c['chip_bg']}" stroke="{c['chip_border']}"/>
      <text x="190" y="13" text-anchor="middle" fill="{c['chip_text']}" class="mono" font-size="9.5">WebSockets</text>

      <rect x="236" y="0" width="72" height="20" rx="4" fill="{c['chip_bg']}" stroke="{c['chip_border']}"/>
      <text x="272" y="13" text-anchor="middle" fill="{c['chip_text']}" class="mono" font-size="9.5">IndexedDB</text>

      <rect x="316" y="0" width="50" height="20" rx="4" fill="{c['chip_bg']}" stroke="{c['chip_border']}"/>
      <text x="341" y="13" text-anchor="middle" fill="{c['chip_text']}" class="mono" font-size="9.5">React</text>
    </g>
  </g>

  <!-- Right: Live Feed Diagnostics Box -->
  <g transform="translate(535, 24)">
    <rect width="268" height="122" rx="6" fill="{c['surface']}" stroke="{c['border_subtle']}" stroke-width="1"/>
    
    <!-- Header -->
    <circle cx="16" cy="18" r="3.5" fill="{c['success']}" class="live-dot"/>
    <text x="26" y="21" fill="{c['text_muted']}" class="mono" font-size="9.5" font-weight="700">LIVE INGRESS FEED</text>
    <text x="250" y="21" text-anchor="end" fill="{c['text_dim']}" class="mono" font-size="9">ws://sync</text>
    <line x1="0" y1="32" x2="268" y2="32" stroke="{c['border_subtle']}" stroke-width="1"/>

    <!-- Scrolling Clip Region -->
    <g clip-path="url(#live-feed-clip-{theme})">
      <clipPath id="live-feed-clip-{theme}">
        <rect x="0" y="36" width="268" height="78"/>
      </clipPath>
      <g class="feed-list" transform="translate(14, 52)">
        <!-- Feed Item 1 -->
        <g transform="translate(0, 0)">
          <text x="0" y="0" fill="{c['accent']}" class="mono" font-size="9.5" font-weight="700">[AUTH]</text>
          <text x="44" y="0" fill="{c['text']}" class="mono" font-size="9.5">tx_98c1 &#183; token_valid</text>
          <text x="238" y="0" text-anchor="end" fill="{c['text_dim']}" class="mono" font-size="9">0.8ms</text>
        </g>
        <!-- Feed Item 2 -->
        <g transform="translate(0, 22)">
          <text x="0" y="0" fill="{c['warm']}" class="mono" font-size="9.5" font-weight="700">[LOCK]</text>
          <text x="44" y="0" fill="{c['text']}" class="mono" font-size="9.5">row_401 &#183; FOR UPDATE</text>
          <text x="238" y="0" text-anchor="end" fill="{c['text_dim']}" class="mono" font-size="9">1.2ms</text>
        </g>
        <!-- Feed Item 3 -->
        <g transform="translate(0, 44)">
          <text x="0" y="0" fill="{c['success']}" class="mono" font-size="9.5" font-weight="700">[SYNC]</text>
          <text x="44" y="0" fill="{c['text']}" class="mono" font-size="9.5">broadcast &#183; 1,420 peak</text>
          <text x="238" y="0" text-anchor="end" fill="{c['text_dim']}" class="mono" font-size="9">0.4ms</text>
        </g>
      </g>
    </g>
  </g>
</svg>'''

# -------------------------------------------------------------------------
# 6. COMPACT PROJECT CARD (405 x 148) - FOR 2-COLUMN GRID
# -------------------------------------------------------------------------
def build_compact_card(title, tag, p1, p2, chips, theme="dark"):
    c = THEMES[theme]
    chips_svg = []
    chip_x = 0
    for chip in chips:
        w = max(len(chip) * 7 + 14, 46)
        chips_svg.append(f'''
        <rect x="{chip_x}" y="0" width="{w}" height="19" rx="3.5" fill="{c['chip_bg']}" stroke="{c['chip_border']}"/>
        <text x="{chip_x + w/2}" y="12.5" text-anchor="middle" fill="{c['chip_text']}" font-family="{FONT_MONO}" font-size="9">{chip}</text>
        ''')
        chip_x += w + 6

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 405 148" width="100%" height="148" fill="none">
  <defs>
    <style>
      .mono {{ font-family: {FONT_MONO}; }}
      .sans {{ font-family: {FONT_SANS}; }}
    </style>
  </defs>

  <!-- Card Frame -->
  <rect width="405" height="148" rx="7" fill="{c['bg']}" stroke="{c['border']}" stroke-width="1.2"/>

  <!-- Content -->
  <g transform="translate(20, 20)">
    <!-- Header: Title + Tag -->
    <text x="0" y="14" fill="{c['text']}" class="sans" font-size="15" font-weight="700">{title}</text>
    <rect x="275" y="0" width="90" height="18" rx="9" fill="{c['accent_dim']}"/>
    <text x="320" y="12.5" text-anchor="middle" fill="{c['accent']}" class="mono" font-size="8.5" font-weight="700">{tag}</text>

    <!-- Pitch (2 sharp sentences) -->
    <text x="0" y="42" fill="{c['text']}" class="sans" font-size="11.5" font-weight="400">{p1}</text>
    <text x="0" y="60" fill="{c['text_muted']}" class="sans" font-size="11.5">{p2}</text>

    <!-- Stack Chips -->
    <g transform="translate(0, 88)">
      {''.join(chips_svg)}
    </g>
  </g>
</svg>'''

# -------------------------------------------------------------------------
# 7. TECH STACK (830 x 300)
# -------------------------------------------------------------------------
def build_tech_stack(theme="dark"):
    c = THEMES[theme]
    
    # 4 distinct panels: Languages, Backend & Systems, AI & Data, Frontend
    panels = [
        {
            "x": 20, "y": 20, "w": 385, "h": 125,
            "title": "LANGUAGES", "tag": "CORE RUNTIMES",
            "items": ["Python", "C++", "TypeScript", "JavaScript", "SQL"]
        },
        {
            "x": 425, "y": 20, "w": 385, "h": 125,
            "title": "BACKEND & SYSTEMS", "tag": "CONCURRENCY / DATA",
            "items": ["Node.js", "FastAPI", "Django", "PostgreSQL", "Redis", "MongoDB", "Oracle XE"]
        },
        {
            "x": 20, "y": 155, "w": 385, "h": 125,
            "title": "AI & DATA ENGINEERING", "tag": "AGENTS / INFERENCE",
            "items": ["LangChain", "TensorFlow", "PyTorch", "ChromaDB", "ONNX", "Scikit-Learn"]
        },
        {
            "x": 425, "y": 155, "w": 385, "h": 125,
            "title": "FRONTEND & STATE", "tag": "INTERACTIVE UI",
            "items": ["React", "Vite", "Tailwind CSS", "Zustand", "Vanilla JS"]
        }
    ]

    panels_svg = []
    for p in panels:
        chips_svg = []
        cx, cy = 16, 42
        for item in p["items"]:
            w = len(item) * 7.5 + 18
            if cx + w > p["w"] - 16:
                cx = 16
                cy += 30
            chips_svg.append(f'''
            <rect x="{cx}" y="{cy}" width="{w}" height="22" rx="4" fill="{c['chip_bg']}" stroke="{c['chip_border']}"/>
            <text x="{cx + w/2}" y="{cy + 14.5}" text-anchor="middle" fill="{c['chip_text']}" font-family="{FONT_MONO}" font-size="10">{item}</text>
            ''')
            cx += w + 8

        clean_p_title = p["title"].replace("&", "&amp;")
        clean_p_tag = p["tag"].replace("&", "&amp;")
        panels_svg.append(f'''
        <g transform="translate({p['x']}, {p['y']})">
          <rect width="{p['w']}" height="{p['h']}" rx="6" fill="{c['surface']}" stroke="{c['border_subtle']}" stroke-width="1"/>
          <text x="16" y="24" fill="{c['accent']}" font-family="{FONT_MONO}" font-size="11" font-weight="700">// {clean_p_title}</text>
          <text x="{p['w'] - 16}" y="24" text-anchor="end" fill="{c['text_dim']}" font-family="{FONT_MONO}" font-size="9" font-weight="600">{clean_p_tag}</text>
          <line x1="16" y1="32" x2="{p['w'] - 16}" y2="32" stroke="{c['border_subtle']}" stroke-width="0.8"/>
          {''.join(chips_svg)}
        </g>
        ''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 300" width="100%" height="300" fill="none">
  <defs>
    <style>
      .mono {{ font-family: {FONT_MONO}; }}
      .sans {{ font-family: {FONT_SANS}; }}
    </style>
  </defs>

  <!-- Outer Boundary -->
  <rect width="830" height="300" rx="8" fill="{c['bg']}" stroke="{c['border']}" stroke-width="1.2"/>

  <!-- 4 Grouped Panels -->
  {''.join(panels_svg)}
</svg>'''

# -------------------------------------------------------------------------
# 8. CONNECT BANNER (830 x 130) — three contact channel panels
# -------------------------------------------------------------------------
def build_connect_banner(theme="dark"):
    c = THEMES[theme]

    def panel(dx, glyph, channel, title, value):
        return f'''
  <g transform="translate({dx}, 15)">
    <rect width="260" height="100" rx="8" fill="{c['surface']}" stroke="{c['border']}" stroke-width="1.2"/>
    <circle cx="34" cy="50" r="15" fill="{c['accent_dim']}" stroke="{c['accent']}" stroke-opacity="0.35" stroke-width="1"/>
    <text x="34" y="54" text-anchor="middle" font-family="{FONT_MONO}" font-size="13" font-weight="700" fill="{c['accent']}">{glyph}</text>
    <text x="60" y="34" font-family="{FONT_MONO}" font-size="9" font-weight="700" letter-spacing="1" fill="{c['accent']}">{channel}</text>
    <text x="60" y="54" font-family="{FONT_SANS}" font-size="13.5" font-weight="700" fill="{c['text']}">{title}</text>
    <text x="60" y="74" font-family="{FONT_MONO}" font-size="10.5" fill="{c['text_muted']}">{value}</text>
    <circle cx="245" cy="15" r="3" fill="{c['success']}" class="ping"/>
  </g>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 130" width="100%" height="130" fill="none">
  <defs>
    <style>
      @keyframes ping {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.25; }}
      }}
      .ping {{ animation: ping 1.6s ease-in-out infinite; }}
      @media (prefers-reduced-motion: reduce) {{
        .ping {{ animation: none !important; }}
      }}
    </style>
  </defs>

  <!-- Outer Boundary -->
  <rect width="830" height="130" rx="8" fill="{c['bg']}" stroke="{c['border']}" stroke-width="1.2"/>

  <!-- Channel 01: Email -->
  {panel(15, "@", "CH_01 // DIRECT MAIL", "Email", "ishan.vaidya01@gmail.com")}
  <!-- Channel 02: LinkedIn -->
  {panel(285, "in", "CH_02 // NETWORK NODE", "LinkedIn", "linkedin.com/in/ishanvaidya-cse")}
  <!-- Channel 03: GitHub -->
  {panel(555, "&#123; &#125;", "CH_03 // CODE BASE", "Portfolio", "@ishanvaidya01")}
</svg>'''

def main():
    print("[*] Generating production-grade theme-adaptive SVG assets...")

    for theme in ["dark", "light"]:
        # 1. Hero Terminal
        with open(os.path.join(ASSETS_DIR, f"hero-terminal-{theme}.svg"), "w", encoding="utf-8") as f:
            f.write(build_hero_terminal(theme))

        # 2. Avatar Ring
        with open(os.path.join(ASSETS_DIR, f"avatar-ring-{theme}.svg"), "w", encoding="utf-8") as f:
            f.write(build_avatar_ring(theme))

        # 3. Section Divider
        with open(os.path.join(ASSETS_DIR, f"section-divider-{theme}.svg"), "w", encoding="utf-8") as f:
            f.write(build_section_divider(theme))

        # 4. Section Headers
        headers = [
            ("header-telemetry", "// 01 — REPOSITORY TELEMETRY & PULSE", "SYSTEM PULSE"),
            ("header-01", "// 02 — HIGH-CONCURRENCY & SYSTEMS INFRASTRUCTURE", "CONCURRENCY"),
            ("header-02", "// 03 — AUTONOMOUS AI & MULTI-AGENT SYSTEMS", "AGENTIC AI"),
            ("header-03", "// 04 — REAL-WORLD IMPACT & ML APPLICATIONS", "APPLIED ML"),
            ("header-stack", "// 05 — TECHNICAL ARSENAL & TOOLCHAIN", "FULL-STACK"),
        ]
        for name, title, tag in headers:
            with open(os.path.join(ASSETS_DIR, f"{name}-{theme}.svg"), "w", encoding="utf-8") as f:
                f.write(build_section_header(title, tag, theme))

        # 5. LivePass Flagship Card
        with open(os.path.join(ASSETS_DIR, f"card-livepass-{theme}.svg"), "w", encoding="utf-8") as f:
            f.write(build_livepass_card(theme))

        # 6. Compact Project Cards (10 total)
        cards = [
            # Category 1
            ("card-sentio", "Sentio", "TELEMETRY", 
             "Robotic telemetry black box streaming sub-second data via Node.js SSE.", 
             "In-memory circular ring buffers prevent memory fragmentation under multi-kHz bursts.",
             ["Node.js", "SSE", "Ring Buffers", "AudioContext"]),
            ("card-ecras", "ECRAS", "DUAL-STORE", 
             "Enterprise recruitment bias auditor synchronizing Oracle XE with ChromaDB vector store.", 
             "PL/SQL autonomous transactions enforce tamper-evident, auditable EEOC compliance.",
             ["Oracle XE", "ChromaDB", "PL/SQL", "ONNX Runtime"]),
            
            # Category 2
            ("card-aerotrade", "AeroTrade XAI", "AGENTIC DISPATCH", 
             "Autonomous supply-chain orchestrator built with LangChain and Pydantic validation.", 
             "Replaces stochastic outputs with counterfactual 'Why This, Not That' trade-off panels.",
             ["LangChain", "Pydantic", "FastAPI", "Explainable AI"]),
            ("card-gst-archangel", "GST Archangel", "AGENT SWARM", 
             "Multi-agent AI accountant coordinating 7 specialized agents (OCR, Recon, Risk).", 
             "Runs fine-tuned local Donut models, statutory RAG, and live WebSocket thought streams.",
             ["7 Agents", "Donut OCR", "RAG", "WebSockets"]),
            ("card-mindmesh", "MindMesh", "EVENT-SOURCING", 
             "Collaborative learning platform with event-sourced quiz state rewind.", 
             "Django Channels and Redis Pub/Sub support live sync and Socratic AI hint streams.",
             ["Django", "Redis", "Event-Sourcing", "WebSockets"]),
            ("card-scamshield", "Scam Shield", "SYNDICATE DETECT", 
             "Live chat campaign detector using structural clustering and cross-account semantics.", 
             "SHAP explainability with deliberate abstention on stealthy L3-Single anomalies.",
             ["SHAP", "Scikit-Learn", "FastAPI", "NLP"]),

            # Category 3
            ("card-self2cash", "Self2Cash", "FINTECH ENGINE",
             "Kirana retail financial engine with MongoDB Geospatial cluster matchmaking.", 
             "FastAPI ML microservice models historical replenishment to drive micro-factoring.",
             ["MongoDB Geo", "FastAPI", "ML Microservice", "React"]),
            ("card-varhadagro", "VarhadAgro", "AGRONOMY ML", 
             "Regional crop-yield prediction engine achieving R² 0.92 across the Vidarbha basin.", 
             "Fuses rainfall, temperature, and dry-spell duration metrics into kg/ha forecasts.",
             ["Scikit-Learn", "FastAPI", "R² 0.92", "Python"]),
            ("card-agriguard", "AgriGuard", "COMPUTER VISION", 
             "Crop disease diagnostics pairing FastAPI with a convolutional TensorFlow model.", 
             "Leaflet maps track outbreaks, dispatching dual organic/chemical treatment remedies.",
             ["TensorFlow", "FastAPI", "Leaflet", "Computer Vision"]),
            ("card-lassihouse", "Lassi House", "RETAIL POS", 
             "College juice-shop order pipeline with atomic lifecycle state transitions.", 
             "Full-stack ordering system featuring Zustand synchronization and idempotent Razorpay webhooks.",
             ["FastAPI", "PostgreSQL", "React", "Razorpay"])
        ]

        for fname, title, tag, p1, p2, chips in cards:
            with open(os.path.join(ASSETS_DIR, f"{fname}-{theme}.svg"), "w", encoding="utf-8") as f:
                f.write(build_compact_card(title, tag, p1, p2, chips, theme))

        # 7. Tech Stack
        with open(os.path.join(ASSETS_DIR, f"tech-stack-{theme}.svg"), "w", encoding="utf-8") as f:
            f.write(build_tech_stack(theme))

        # 8. Connect Banner
        with open(os.path.join(ASSETS_DIR, f"footer-connect-{theme}.svg"), "w", encoding="utf-8") as f:
            f.write(build_connect_banner(theme))

    print(f"[+] All assets successfully generated in {ASSETS_DIR}")

if __name__ == "__main__":
    main()
