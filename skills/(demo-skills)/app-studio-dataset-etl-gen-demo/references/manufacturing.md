# Manufacturing Demo Pack

## Industry Context
Industrial manufacturing operations — production lines, quality control, supply chain, and materials management.

---

## Star Schema

### Fact Tables

**work_orders** (~1500 rows)
| Column | Type | Description |
|---|---|---|
| work_order_id | INT | PK |
| product_id | INT | FK → products |
| plant_id | INT | FK → plants |
| order_date | DATE | Rolling, last 18 months |
| completion_date | DATE | order_date + 1–14 days |
| order_quantity | INT | 50–5000 |
| completed_quantity | INT | ≤ order_quantity |
| cycle_time_hours | DECIMAL | 2–48 |
| status | STRING | Open, In Progress, Completed, On Hold |
| priority | STRING | Low, Medium, High, Critical |

**quality_inspections** (~2000 rows)
| Column | Type | Description |
|---|---|---|
| inspection_id | INT | PK |
| work_order_id | INT | FK → work_orders |
| product_id | INT | FK → products |
| plant_id | INT | FK → plants |
| inspection_date | DATE | Rolling, last 18 months |
| result | STRING | Pass, Fail, Conditional |
| defect_count | INT | 0–15 |
| scrap_quantity | INT | 0–50 |
| inspector_name | STRING | From entity pool |
| defect_type | STRING | Dimensional, Surface, Structural, Assembly, Cosmetic |

**material_consumption** (~1800 rows)
| Column | Type | Description |
|---|---|---|
| consumption_id | INT | PK |
| material_id | INT | FK → materials |
| supplier_id | INT | FK → suppliers |
| plant_id | INT | FK → plants |
| consumption_date | DATE | Rolling, last 18 months |
| quantity_used | DECIMAL | 10–500 |
| unit_cost | DECIMAL | 1.50–250.00 |
| waste_quantity | DECIMAL | 0–25 |
| purchase_order_ref | STRING | PO-XXXXX format |

### Dimension Tables

**products** (~40 rows)
| Column | Type |
|---|---|
| product_id | INT (PK) |
| product_name | STRING |
| product_category | STRING (Assemblies, Components, Sub-assemblies, Raw Parts) |
| product_line | STRING (Industrial, Commercial, Consumer, Specialty) |
| unit_weight_kg | DECIMAL |

**plants** (~8 rows)
| Column | Type |
|---|---|
| plant_id | INT (PK) |
| plant_name | STRING (e.g., "Plant A - Detroit", "Plant B - Austin") |
| region | STRING (Midwest, South, West, Northeast) |
| capacity_units_day | INT |
| shift_count | INT (1, 2, 3) |

**suppliers** (~25 rows)
| Column | Type |
|---|---|
| supplier_id | INT (PK) |
| supplier_name | STRING |
| supplier_tier | STRING (Tier 1, Tier 2, Tier 3) |
| country | STRING |
| lead_time_days | INT |

**materials** (~30 rows)
| Column | Type |
|---|---|
| material_id | INT (PK) |
| material_name | STRING |
| material_type | STRING (Steel, Aluminum, Polymer, Electronic, Rubber) |
| unit_of_measure | STRING (kg, units, liters, meters) |
| reorder_point | INT |

---

## ETL Outputs

### Output 1: Production Performance
**Joins**: work_orders ← products, plants
**Key columns**: order_date, product_name, product_category, plant_name, region, order_quantity, completed_quantity, cycle_time_hours, status, priority

### Output 2: Quality Metrics
**Joins**: quality_inspections ← products, plants (via work_order_id if needed, or directly)
**Key columns**: inspection_date, product_name, product_category, plant_name, result, defect_count, scrap_quantity, defect_type

### Output 3: Supply Chain Analytics
**Joins**: material_consumption ← materials, suppliers, plants
**Key columns**: consumption_date, material_name, material_type, supplier_name, supplier_tier, plant_name, quantity_used, unit_cost, waste_quantity

---

## App Studio Pages

| Page | Icon | Focus | Primary Dataset |
|---|---|---|---|
| Overview | `analytics` | High-level KPIs across all operations | Production Performance |
| Production | `gauge` | Output, cycle time, efficiency by plant/product | Production Performance |
| Quality | `certified` | Defect rates, inspection results, scrap | Quality Metrics |
| Supply Chain | `globe` | Material costs, supplier performance, waste | Supply Chain Analytics |

---

## Hero Metrics (per page)

**Overview**: Total Output (sum completed_quantity), Avg Cycle Time, Defect Rate (%), On-Time Completion %
**Production**: Orders Completed, Avg Cycle Time, Capacity Utilization %, Open Orders
**Quality**: Inspection Pass Rate %, Total Defects, Scrap Quantity, Inspections Completed
**Supply Chain**: Total Material Cost, Avg Lead Time, Waste Rate %, Active Suppliers

---

## Chart Assignments

| Page | Template | Chart Type | X-Axis | Y-Axis |
|---|---|---|---|---|
| Overview | A (area/line) | Time series trend | order_date (monthly) | completed_quantity |
| Production | B (bar) | By plant or product | plant_name or product_category | order_quantity |
| Quality | C (multi-line) | Defect + scrap trends | inspection_date (monthly) | defect_count, scrap_quantity |
| Supply Chain | B (bar, horizontal) | By supplier | supplier_name | total cost (quantity_used × unit_cost) |

---

## Theme

Use a dark industrial palette from `~/.agents/skills/domo-app-theme/references/themes/`. Recommended: charcoal or shades family. Font: sans-serif (Open Sans or similar).
