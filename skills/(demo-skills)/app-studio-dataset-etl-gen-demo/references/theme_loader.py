"""
theme_loader.py — Compact theme selection index + pre-extracted loader.
"""

import json
import os
import random

_DIR = os.path.dirname(os.path.abspath(__file__))
_INDEX_PATH = os.path.join(_DIR, "theme_index.json")

THEMES = {
    "arctic-frost": {"mode": "Light", "font": "Sans", "mood": "Clinical calm, ultra high-key minimalism, medical-grade clarity"},
    "blueprint": {"mode": "Light", "font": "Condensed", "mood": "Grid-aligned engineering documentation"},
    "blush-rose": {"mode": "Light", "font": "Serif", "mood": "Soft luxury, spa calm, editorial beauty — dusty rose & warm gold"},
    "burgundy-editorial": {"mode": "Light", "font": "Serif", "mood": "Magazine editorial, cellar warmth, luxury print on cream stock"},
    "copper-patina": {"mode": "Light", "font": "Sans", "mood": "Museum catalog, crafted metal, calm precision — verdigris teal + copper"},
    "corporate-light": {"mode": "Light", "font": "Sans", "mood": "Professional, trustworthy, clean — cool blue-gray"},
    "data-ink": {"mode": "Light", "font": "Serif", "mood": "Tufte-like analytical clarity — neutral gray, alert red reserved"},
    "golden-hour": {"mode": "Light", "font": "Serif", "mood": "Warm editorial, regal complementary contrast — golden amber & dusky purple"},
    "midnight-navy": {"mode": "Light", "font": "Condensed", "mood": "Commanding, precise, institutional trust — steel blue & sky blue"},
    "moss-stone": {"mode": "Light", "font": "Slab", "mood": "Earthy organic calm, agriculture, stone-warm canvas"},
    "slate-granite": {"mode": "Light", "font": "Sans", "mood": "Technical clarity, infrastructure calm, understated precision — achromatic"},
    "terracotta-sand": {"mode": "Light", "font": "Sans", "mood": "Sun-baked clay, editorial warmth, Mediterranean calm"},
    "bc-forest-dark": {"mode": "Dark", "font": "Sans", "mood": "Organic, nocturnal, calm precision — luminous mint on deep forest"},
    "ch-charcoal-dark": {"mode": "Dark", "font": "Mixed", "mood": "Boutique hotel lounge, editorial data, confident warmth"},
    "charcoal-ember-dark": {"mode": "Dark", "font": "Sans", "mood": "Confident, technical, authoritative — warm orange on charcoal"},
    "electric-teal": {"mode": "Dark", "font": "Monospace", "mood": "Dev-tool precision, terminal calm, flat planes with grid discipline"},
    "emerald-dark": {"mode": "Dark", "font": "Sans", "mood": "Precision, technical, growth — green / emerald"},
    "indigo-velvet": {"mode": "Dark", "font": "Sans", "mood": "Luxurious VIP analytics, velvet depth, after-hours boardroom"},
    "neon-magenta-dark": {"mode": "Dark", "font": "Sans", "mood": "Bold, energetic, high-impact — hot pink / magenta"},
    "ocean-kelp": {"mode": "Dark", "font": "Mixed", "mood": "Deep marine calm, bioluminescent restraint — seaweed green & seafoam"},
    "terminal-sage": {"mode": "Dark", "font": "Monospace", "mood": "Flat console, DevOps monitoring — restrained sage / forest green"},
}

_cache = None


def _load_index():
    global _cache
    if _cache is None:
        with open(_INDEX_PATH, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def load_theme(name):
    """
    Returns: (color_map, font_map, nav_kwargs)
    """
    idx = _load_index()
    entry = idx[name]
    nav_raw = entry["nav"]
    nav_kwargs = {
        "nav_bg": nav_raw["nav_bg"],
        "active_bg": nav_raw["active_bg"],
        "hover_bg": nav_raw["hover_bg"],
        "title_font_color": nav_raw["nav_text"],
        "link_font_color": nav_raw["nav_text"],
    }
    return entry["color_map"], entry["font_map"], nav_kwargs


def pick_random(mode=None):
    candidates = [t for t, m in THEMES.items() if mode is None or m["mode"] == mode]
    return random.choice(candidates)
