"""
vertical_detector.py — Auto-detect industry vertical from dataset column names.
"""

from cli_helpers import get_column_names


VERTICAL_SIGNATURES = {
    "manufacturing": [
        {"work_order_id", "cycle_time_hours", "completed_quantity"},
        {"inspection_id", "defect_count", "scrap_quantity"},
        {"material_id", "waste_quantity", "unit_cost", "supplier_id"},
    ],
    "retail-ecommerce": [
        {"transaction_id", "unit_price", "discount_pct", "channel"},
        {"session_id", "conversion", "cart_abandonment"},
        {"sku", "on_hand_after", "days_of_supply"},
    ],
    "healthcare": [
        {"patient_id", "los_days", "readmission"},
        {"lab_order_id", "turnaround_hours", "test_category"},
        {"claim_id", "billed_amount", "paid_amount", "denial_reason"},
    ],
    "logistics": [
        {"shipment_id", "freight_cost", "on_time_delivery"},
        {"vehicle_id", "total_mileage", "fuel_consumed"},
        {"warehouse_id", "units_processed", "pick_accuracy"},
    ],
    "financial-services": [
        {"loan_id", "aum", "portfolio_value"},
        {"transaction_id", "fee_amount", "channel"},
        {"asset_class", "market_value", "unrealized_gain"},
    ],
}


REFERENCE_PACKS = {
    "manufacturing": "~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/manufacturing.md",
    "retail-ecommerce": "~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/retail-ecommerce.md",
    "healthcare": "~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/healthcare.md",
    "logistics": "~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/logistics.md",
    "financial-services": "~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/financial-services.md",
}


def detect_vertical(dataset_ids):
    """
    Returns (vertical_name, confidence).
    """
    all_columns = set()
    for ds_id in dataset_ids:
        all_columns.update(get_column_names(ds_id))

    best_vertical = None
    best_score = 0.0
    for vertical, signature_groups in VERTICAL_SIGNATURES.items():
        matches = sum(1 for sig in signature_groups if sig.issubset(all_columns))
        score = matches / len(signature_groups)
        if score > best_score:
            best_score = score
            best_vertical = vertical
    return best_vertical, best_score


def detect_and_report(dataset_ids):
    vertical, confidence = detect_vertical(dataset_ids)
    if vertical:
        pack = REFERENCE_PACKS.get(vertical)
        print(f"  Vertical detected: {vertical} (confidence: {confidence:.0%})")
        print(f"  Reference pack:    {pack}")
        return vertical, pack
    print("  No vertical detected — column signatures did not match known verticals")
    return None, None
