"""
layout_assembler.py — Composable App Studio page layout builder.

Placement: advanced-app-studio/references/layout_assembler.py

This is NOT a hardcoded layout. It provides reusable building blocks while handling:
    - content key tracking (cardId -> contentKey)
    - template-only entry preservation
    - standard + compact dual templates
    - final safety checks before layout-set
"""

STYLE_PRESETS = {
    "hero": {
        "hideTitle": True,
        "hideSummary": True,
        "hideDescription": True,
        "hideFooter": True,
        "hideBorder": False,
        "acceptFilters": True,
        "acceptDateFilter": True,
        "style": {"sourceId": "ca1", "textColor": None},
    },
    "filter": {
        "hideTitle": True,
        "hideDescription": True,
        "hideSummary": True,
        "hideFooter": True,
        "hideTimeframe": True,
        "hideMargins": True,
        "fitToFrame": True,
        "hideBorder": True,
        "acceptFilters": True,
        "acceptDateFilter": True,
        "style": None,
    },
    "chart": {
        "hideTitle": True,
        "hideDescription": True,
        "hideFooter": True,
        "fitToFrame": True,
        "acceptFilters": True,
        "acceptDateFilter": True,
        "style": {"sourceId": "ca1", "textColor": None},
    },
}


class LayoutBuilder:
    """Composable layout builder for App Studio `layout-set` payloads."""

    def __init__(self, layout):
        self.layout = layout
        self.card_to_key = {
            c["cardId"]: c["contentKey"]
            for c in layout["content"]
            if c.get("type") == "CARD" and c.get("cardId")
        }
        content_keys = {c["contentKey"] for c in layout["content"]}
        template_keys = {e["contentKey"] for e in layout["standard"]["template"]}
        self._all_known_keys = content_keys | template_keys
        self._next_key = max(self._all_known_keys) + 1 if self._all_known_keys else 1
        self._std = []
        self._cmp = []
        self._y = 0
        self._cy = 0

    def _alloc_key(self):
        k = self._next_key
        self._next_key += 1
        self._all_known_keys.add(k)
        return k

    def _entry(self, type_, key, x, y, w, h, canvas=True):
        return {
            "type": type_,
            "contentKey": key,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "virtualAppendix": not canvas,
            "virtual": not canvas,
            "children": None,
        }

    def style_cards(self, card_ids, preset_name, custom_style=None):
        style = {**STYLE_PRESETS.get(preset_name, {})}
        if custom_style:
            style.update(custom_style)
        card_set = set(card_ids)
        for c in self.layout["content"]:
            if c.get("cardId") in card_set:
                c.update(style)

    def add_row(self, card_ids, height, compact_height=None, widths=None):
        if compact_height is None:
            compact_height = max(height // 2, 6)
        n = len(card_ids)
        if n == 0:
            return
        if widths is None:
            w_each = 60 // n
            widths_list = [w_each] * n
        elif isinstance(widths, int):
            widths_list = [widths] * n
        else:
            widths_list = list(widths)

        x = 0
        for i, cid in enumerate(card_ids):
            key = self.card_to_key.get(cid)
            if key is None:
                continue
            w = widths_list[i] if i < len(widths_list) else widths_list[-1]
            self._std.append(self._entry("CARD", key, x, self._y, w, height))
            self._cmp.append(self._entry("CARD", key, 0, self._cy, 12, compact_height))
            x += w
            self._cy += compact_height
        self._y += height

    def add_header(self, text, height=4, compact_height=3):
        key = self._alloc_key()
        self.layout["content"].append({"contentKey": key, "text": text, "type": "HEADER"})
        self._std.append(self._entry("HEADER", key, 0, self._y, 60, height))
        self._cmp.append(self._entry("HEADER", key, 0, self._cy, 12, compact_height))
        self._y += height
        self._cy += compact_height

    def add_spacer(self, height=3, compact_height=2):
        key = self._alloc_key()
        self._std.append(self._entry("SPACER", key, 0, self._y, 60, height))
        self._cmp.append(self._entry("SPACER", key, 0, self._cy, 12, compact_height))
        self._y += height
        self._cy += compact_height

    def add_separator(self, height=2, compact_height=1):
        key = self._alloc_key()
        self._std.append(self._entry("SEPARATOR", key, 0, self._y, 60, height))
        self._cmp.append(self._entry("SEPARATOR", key, 0, self._cy, 12, compact_height))
        self._y += height
        self._cy += compact_height

    def finalize(self):
        placed_std = {e["contentKey"] for e in self._std}
        placed_cmp = {e["contentKey"] for e in self._cmp}

        for entry in self.layout["standard"]["template"]:
            k = entry["contentKey"]
            if k not in placed_std:
                self._std.append(
                    {
                        "type": entry["type"],
                        "contentKey": k,
                        "x": entry.get("x", 0),
                        "y": entry.get("y", 0),
                        "width": entry.get("width", 60),
                        "height": entry.get("height", 2),
                        "virtualAppendix": True,
                        "virtual": True,
                        "children": None,
                    }
                )
        for entry in self.layout["compact"]["template"]:
            k = entry["contentKey"]
            if k not in placed_cmp:
                self._cmp.append(
                    {
                        "type": entry["type"],
                        "contentKey": k,
                        "x": entry.get("x", 0),
                        "y": entry.get("y", 0),
                        "width": entry.get("width", 12),
                        "height": entry.get("height", 2),
                        "virtualAppendix": True,
                        "virtual": True,
                        "children": None,
                    }
                )

        all_content_keys = {c["contentKey"] for c in self.layout["content"]}
        std_keys = {e["contentKey"] for e in self._std}
        cmp_keys = {e["contentKey"] for e in self._cmp}

        for k in all_content_keys - std_keys:
            self._std.append(self._entry("CARD", k, 0, 999, 15, 10, canvas=False))
        for k in all_content_keys - cmp_keys:
            self._cmp.append(self._entry("CARD", k, 0, 999, 12, 6, canvas=False))

        self.layout["standard"]["template"] = self._std
        self.layout["compact"]["template"] = self._cmp
        return self.layout


def assemble_demo_page(layout, hero_ids, filter_ids, chart_ids, primary_title="Primary Visualization", detail_title="Detail Analysis"):
    """Shortcut for the common demo layout pattern."""
    builder = LayoutBuilder(layout)
    builder.style_cards(filter_ids, "filter")
    builder.style_cards(hero_ids, "hero")
    builder.style_cards(chart_ids, "chart")
    builder.add_row(filter_ids, height=6)
    builder.add_row(hero_ids, height=14)
    builder.add_header(primary_title)
    if chart_ids:
        builder.add_row([chart_ids[0]], height=30)
    builder.add_header(detail_title)
    if len(chart_ids) > 1:
        builder.add_row(chart_ids[1:], height=22)
    return builder.finalize()
