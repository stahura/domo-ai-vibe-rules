"""
card_templates.py — Reusable card body builders for App Studio native cards.

Placement: advanced-app-studio/references/card_templates.py

These functions return dicts ready for:
    json.dump(card_body, open('card.json', 'w'))
    community-domo-cli --output json -y cards create --body-file card.json --page-id $PAGE_ID

CRITICAL REMINDERS:
    - badge_line is BROKEN — use badge_two_trendline
    - badge_area is INVALID — use badge_vert_area_overlay
    - Aggregation "AVERAGE" is invalid — use "AVG"
    - All chart types need badge_ prefix
"""

_EMPTY_FORMULAS = {"dsUpdated": [], "dsDeleted": [], "card": []}
_EMPTY_ANNOTATIONS = {"new": [], "modified": [], "deleted": []}
_EMPTY_COND_FORMATS = {"card": [], "datasource": []}
_EMPTY_SEGMENTS = {"active": [], "create": [], "update": [], "delete": []}
_ABBREVIATED_FORMAT = {"type": "abbreviated", "format": "#A"}


def _base_definition(title, subscriptions, chart_type, overrides=None):
    """Internal helper for full card definition wrapper."""
    return {
        "definition": {
            "subscriptions": subscriptions,
            "formulas": _EMPTY_FORMULAS,
            "annotations": _EMPTY_ANNOTATIONS,
            "conditionalFormats": _EMPTY_COND_FORMATS,
            "controls": [],
            "segments": _EMPTY_SEGMENTS,
            "charts": {
                "main": {"component": "main", "chartType": chart_type, "overrides": overrides or {}, "goal": None}
            },
            "dynamicTitle": {"text": [{"text": title, "type": "TEXT"}]},
            "dynamicDescription": {"text": [], "displayOnCardDetails": True},
            "chartVersion": "12",
            "inputTable": False,
            "noDateRange": False,
            "title": title,
            "description": "",
        },
        "variables": True,
        "columns": False,
    }


def _date_range_filter(date_column):
    """YEAR-based PoP date range filter. Use YEAR, never MONTH."""
    return {
        "column": {"column": date_column, "exprType": "COLUMN"},
        "dateTimeRange": {"dateTimeRangeType": "INTERVAL_OFFSET", "interval": "YEAR", "offset": 0, "count": 0},
        "periods": {"type": "COMBINED", "combined": [{"interval": "YEAR", "type": "OVER", "count": 1}], "count": 0},
    }


def hero_card(title, value_column, aggregation, date_column, dataset_id, fmt=None):
    """Period-over-period hero metric card (`badge_pop_multi_value`)."""
    if fmt is None:
        fmt = _ABBREVIATED_FORMAT

    subs = {
        "big_number": {
            "name": "big_number",
            "columns": [{"column": value_column, "aggregation": aggregation, "alias": title, "format": fmt}],
            "filters": [],
        },
        "main": {
            "name": "main",
            "columns": [
                {"column": date_column, "aggregation": "MAX", "mapping": "ITEM"},
                {"column": value_column, "mapping": "VALUE", "aggregation": aggregation, "alias": title},
            ],
            "filters": [],
            "orderBy": [],
            "groupBy": [],
            "dateRangeFilter": _date_range_filter(date_column),
            "fiscal": False,
            "projection": False,
            "distinct": False,
        },
        "time_period": {
            "name": "time_period",
            "columns": [{"column": date_column, "aggregation": "MAX"}],
            "filters": [],
            "orderBy": [],
            "groupBy": [],
            "fiscal": False,
            "projection": False,
            "distinct": False,
        },
    }

    body = _base_definition(
        title,
        subs,
        "badge_pop_multi_value",
        {"gauge_layout": "Center Vertical", "comp_val_displayed": "Percent Change", "addl_text": "Prior Year", "title_text": title},
    )
    body["dataProvider"] = {"dataSourceId": dataset_id}
    return body


def filter_card(title, column, dataset_id, multi_select=True):
    """Dropdown filter card (`badge_dropdown_selector`)."""
    subs = {
        "big_number": {
            "name": "big_number",
            "columns": [{"column": column, "aggregation": "COUNT", "alias": column, "format": _ABBREVIATED_FORMAT}],
            "filters": [],
        },
        "main": {
            "name": "main",
            "columns": [{"column": column, "mapping": "ITEM"}],
            "filters": [],
            "orderBy": [],
            "groupBy": [{"column": column}],
            "fiscal": False,
            "projection": False,
            "distinct": False,
        },
    }
    body = _base_definition(
        title,
        subs,
        "badge_dropdown_selector",
        {"allow_multi_select": "true" if multi_select else "false", "dropdown_label_text": title, "dropdown_label_pos": "Top"},
    )
    body["dataProvider"] = {"dataSourceId": dataset_id}
    return body


def date_filter_card(title, date_column, dataset_id):
    """Date range selector card (`badge_date_selector`)."""
    subs = {
        "big_number": {
            "name": "big_number",
            "columns": [{"column": date_column, "aggregation": "MAX", "alias": date_column, "format": _ABBREVIATED_FORMAT}],
            "filters": [],
        },
        "main": {
            "name": "main",
            "columns": [{"column": date_column, "mapping": "ITEM"}],
            "filters": [],
            "orderBy": [],
            "groupBy": [],
            "fiscal": False,
            "projection": False,
            "distinct": False,
        },
    }
    body = _base_definition(title, subs, "badge_date_selector", {})
    body["dataProvider"] = {"dataSourceId": dataset_id}
    return body


def chart_card(title, chart_type, item_column, value_column, value_agg, dataset_id, series_column=None, value_alias=None):
    """Generic chart card body builder for `badge_*` chart types."""
    if value_alias is None:
        value_alias = title

    columns = [
        {"column": item_column, "mapping": "ITEM"},
        {"column": value_column, "mapping": "VALUE", "aggregation": value_agg, "alias": value_alias},
    ]
    if series_column:
        columns.append({"column": series_column, "mapping": "SERIES"})

    subs = {
        "main": {
            "name": "main",
            "columns": columns,
            "filters": [],
            "orderBy": [],
            "groupBy": [],
            "fiscal": False,
            "projection": False,
            "distinct": False,
        }
    }

    body = _base_definition(title, subs, chart_type)
    body["dataProvider"] = {"dataSourceId": dataset_id}
    return body


def time_series_chart(
    title, chart_type, date_column, value_column, value_agg, dataset_id, series_column=None, value_alias=None
):
    """Time-series variant of `chart_card` with date `ITEM` column aggregation `MAX`."""
    if value_alias is None:
        value_alias = title

    columns = [
        {"column": date_column, "mapping": "ITEM", "aggregation": "MAX"},
        {"column": value_column, "mapping": "VALUE", "aggregation": value_agg, "alias": value_alias},
    ]
    if series_column:
        columns.append({"column": series_column, "mapping": "SERIES"})

    subs = {
        "main": {
            "name": "main",
            "columns": columns,
            "filters": [],
            "orderBy": [],
            "groupBy": [],
            "fiscal": False,
            "projection": False,
            "distinct": False,
        }
    }

    body = _base_definition(title, subs, chart_type)
    body["dataProvider"] = {"dataSourceId": dataset_id}
    return body
