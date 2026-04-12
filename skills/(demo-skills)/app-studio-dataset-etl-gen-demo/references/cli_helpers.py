"""
cli_helpers.py — Thin wrappers around community-domo-cli for batch operations.

v2 changes:
  - create_view() returns pageId directly (nested response handled)
  - get_owner_id() convenience helper
  - update_view() and rename_view()
  - delete_app() for cleanup
  - better CLI error output
"""

import json
import os
import subprocess
import sys


def _run(args):
    """Run a CLI command, return parsed JSON."""
    env = {
        **os.environ,
        "DOMO_INSTANCE": os.environ.get("DOMO_INSTANCE", "modocorp"),
        "DOMO_AUTH_MODE": os.environ.get("DOMO_AUTH_MODE", "ryuu-session"),
    }
    result = subprocess.run(
        ["community-domo-cli", "--output", "json"] + args,
        capture_output=True,
        text=True,
        env=env,
    )
    if result.returncode != 0 and result.stderr.strip():
        print(f"  CLI ERROR: {' '.join(args[:3])}: {result.stderr.strip()}", file=sys.stderr)
    if result.stdout.strip():
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            print(f"  CLI JSON ERROR: {result.stdout[:200]}", file=sys.stderr)
            return {"ok": False, "raw": result.stdout}
    return {"ok": True}


def _run_write(args):
    """Run a mutating CLI command (adds -y)."""
    return _run(["-y"] + args)


def _write_body(prefix, body):
    f = f"/tmp/{prefix}.json"
    with open(f, "w", encoding="utf-8") as fp:
        json.dump(body, fp)
    return f


def create_app(title, description=""):
    body = json.dumps({"title": title, "description": description})
    return _run_write(["app-studio", "create", "--body", body])


def get_app(app_id):
    """
    Get full app state.
    Owner ID path is app["owners"][0]["id"] (top-level), not views[].
    """
    return _run(["app-studio", "get", str(app_id)])


def update_app(app_id, app_body):
    f = _write_body(f"app_update_{app_id}", app_body)
    return _run_write(["app-studio", "update", str(app_id), "--body-file", f])


def delete_app(app_id):
    return _run_write(["app-studio", "delete", str(app_id)])


def get_owner_id(app_id):
    app = get_app(app_id)
    return app["owners"][0]["id"]


def create_view(app_id, title, owner_id):
    """
    Create a new view.
    Returns pageId as int.
    """
    body = {
        "owners": [{"id": owner_id, "type": "USER", "displayName": None}],
        "type": "dataappview",
        "title": title,
        "pageName": title,
        "locked": False,
        "mobileEnabled": True,
        "sharedViewPage": True,
        "virtualPage": False,
    }
    f = _write_body(f"view_{title.replace(' ', '_')}", body)
    resp = _run_write(["app-studio", "create-view", str(app_id), "--body-file", f])
    return resp.get("view", {}).get("pageId", resp.get("pageId"))


def update_view(app_id, view_id, updates):
    f = _write_body(f"view_update_{view_id}", updates)
    return _run_write(["app-studio", "update-view", str(app_id), str(view_id), "--body-file", f])


def rename_view(app_id, view_id, title):
    return update_view(app_id, view_id, {"title": title, "pageName": title})


def create_card(card_body, page_id):
    title = card_body.get("definition", {}).get("title", "card")
    safe_title = title.replace(" ", "_").replace("/", "_")
    f = _write_body(f"card_{page_id}_{safe_title}", card_body)
    return _run_write(["cards", "create", "--body-file", f, "--page-id", str(page_id)])


def create_cards_batch(card_bodies, page_id):
    ids = []
    for body in card_bodies:
        resp = create_card(body, page_id)
        card_id = resp.get("id")
        title = body.get("definition", {}).get("title", "?")
        print(f"  Created '{title}' -> id={card_id}")
        ids.append(card_id)
    return ids


def get_layout(app_id, page_id):
    return _run(["app-studio", "layout-get", str(app_id), str(page_id)])


def set_layout(app_id, page_id, layout):
    f = _write_body(f"layout_{page_id}", layout)
    return _run_write(["app-studio", "layout-set", str(app_id), str(page_id), "--body-file", f])


def reorder_pages(page_ids):
    """
    Reorder pages in nav. This does not set icons.
    """
    order_str = ",".join(str(p) for p in page_ids)
    body = json.dumps({"pageOrderMap": {"0": order_str}})
    return _run_write(["pages", "nav-reorder", "--body", body])


def get_schema(dataset_id):
    resp = _run(["datasets", "schema", dataset_id])
    return resp.get("tables", [{}])[0].get("columns", [])


def get_column_names(dataset_id):
    return [c["name"] for c in get_schema(dataset_id)]


def query_sql(dataset_id, sql):
    body = json.dumps({"sql": sql})
    return _run(["datasets", "sql", dataset_id, "--body", body])


def upload_file(file_path):
    return _run_write(["files", "upload", "--file-path", file_path])
