"""
theme_transform.py — Convert DESIGN.md theme JSON to App Studio API format.

Placement: domo-app-theme/references/theme_transform.py

Usage by agent:
    import theme_transform
    theme_transform.apply_theme(app, design_colors, design_fonts)

The DESIGN.md files use an "importable" format (index-based).
The App Studio API uses an id-based format with value wrappers.
This script bridges the gap.
"""


def apply_colors(theme, color_map):
    """
    Apply hex colors to an existing theme's color array.

    Args:
        theme: The theme dict from app-studio get response
        color_map: Dict of {"c1": "#F0F4F8", "c2": "#FFFFFF", ...}
                   Keys are slot IDs (c1-c59). Never include c60.

    Modifies theme in-place. Safe to call multiple times.
    """
    for color in theme.get("colors", []):
        cid = color["id"]
        if cid in color_map and cid != "c60":
            color["value"] = {"value": color_map[cid], "type": "RGB_HEX"}


def apply_fonts(theme, font_map):
    """
    Apply font settings to an existing theme's font array.

    Args:
        theme: The theme dict from app-studio get response
        font_map: Dict of {"f1": {"family": "Condensed", "weight": 600, "size": 22}, ...}
                  'style' is always "Regular" (API format). Size is an integer (not "22px").

    Modifies theme in-place.
    """
    for font in theme.get("fonts", []):
        fid = font["id"]
        if fid in font_map:
            update = font_map[fid].copy()
            update.setdefault("style", "Regular")
            font.update(update)


def apply_card_styles(theme, border_radius=0, border_width=0):
    """
    Apply card style overrides. Safe subset that won't cause 400.

    NOTE: dropShadow changes are fragile. Valid values: null, "FLOATING", "STANDARD".
          The string "NONE" causes 400. Omit to keep existing value.
    NOTE: fontColor, accentColor, backgroundColor changes sometimes cause 400
          when combined with other changes. Apply in a separate PUT if needed.
    """
    for card in theme.get("cards", []):
        card["borderRadius"] = border_radius
        card["borderWidth"] = border_width


def apply_nav_chrome(
    theme, nav_bg="c4", active_bg="c5", hover_bg="c32", title_font_color="c2", link_font_color="c2"
):
    """
    Apply navigation chrome colors. Use color slot IDs (e.g., "c4").

    For dark nav backgrounds, title/link font colors should be "c2" (white),
    NEVER "c58" (dark text) or "c60" (automatic — unreliable on dark).
    """
    for nav in theme.get("navigation", []):
        nav["background"] = {"value": nav_bg, "type": "COLOR_REFERENCE"}
        nav["activeBackground"] = {"value": active_bg, "type": "COLOR_REFERENCE"}
        nav["hoverBackground"] = {"value": hover_bg, "type": "COLOR_REFERENCE"}
        nav["titleFontColor"] = {"value": title_font_color, "type": "COLOR_REFERENCE"}
        nav["linkFontColor"] = {"value": link_font_color, "type": "COLOR_REFERENCE"}
        nav["showShadow"] = False


def apply_zero_border_radius(theme):
    """Set borderRadius to 0 on all theme components that support it."""
    for section in ["buttons", "forms", "notebooks", "components", "pills"]:
        for item in theme.get(section, []):
            if "borderRadius" in item:
                item["borderRadius"] = 0


def apply_full_theme(
    app, color_map, font_map, theme_name=None, nav_bg="c4", active_bg="c5", hover_bg="c32", nav_text="c2"
):
    """
    Full theme application in the correct order.

    IMPORTANT: Due to API quirks, the caller should apply this in
    SEPARATE update calls:
      1. Colors (apply_colors)
      2. Fonts (apply_fonts)
      3. Card/nav/component styles (apply_card_styles, apply_nav_chrome, apply_zero_border_radius)

    This function modifies the app dict in-place for a SINGLE update.
    If it 400s, split into separate calls.
    """
    theme = app["theme"]
    if theme_name:
        theme["name"] = theme_name
    apply_colors(theme, color_map)
    apply_fonts(theme, font_map)
    apply_card_styles(theme)
    apply_nav_chrome(theme, nav_bg, active_bg, hover_bg, nav_text, nav_text)
    apply_zero_border_radius(theme)


def design_colors_to_map(design_colors):
    """
    Convert DESIGN.md Section 8 color array to a color_map dict.

    Input format (from DESIGN.md):
        [{"index": 1, "value": "#F0F4F8", "tag": "PRIMARY"}, ...]

    Output format (for apply_colors):
        {"c1": "#F0F4F8", "c2": "#FFFFFF", ...}
    """
    return {f"c{c['index']}": c["value"] for c in design_colors if "index" in c}


def design_fonts_to_map(design_fonts):
    """
    Convert DESIGN.md Section 8 font array to a font_map dict.

    Input format (from DESIGN.md):
        [{"index": 1, "family": "Condensed", "weight": "SemiBold", "size": "22px"}, ...]

    Output format (for apply_fonts):
        {"f1": {"family": "Condensed", "weight": 600, "size": 22}, ...}
    """
    weight_map = {"Light": 300, "Regular": 400, "Medium": 500, "SemiBold": 600, "Bold": 700}
    result = {}
    for f in design_fonts:
        fid = f"f{f['index']}"
        size = f.get("size", "13px")
        if isinstance(size, str):
            size = int(size.replace("px", ""))
        weight = f.get("weight", "Regular")
        if isinstance(weight, str):
            weight = weight_map.get(weight, 400)
        result[fid] = {
            "family": f.get("family", "Sans"),
            "style": "Regular",
            "weight": weight,
            "size": size,
        }
    return result
