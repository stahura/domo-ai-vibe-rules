# Logistics & Transportation Demo Pack

## Industry Context
Freight and logistics operations — shipment tracking, fleet management, warehouse throughput, and carrier performance.

---

## Star Schema

### Fact Tables

**shipments** (~1800 rows)
| Column | Type | Description |
|---|---|---|
| shipment_id | INT | PK |
| carrier_id | INT | FK → carriers |
| route_id | INT | FK → routes |
| warehouse_id | INT | FK → warehouses |
| ship_date | DATE | Rolling, last 18 months |
| delivery_date | DATE | ship_date + 1–14 days |
| weight_kg | DECIMAL | 5–15000 |
| freight_cost | DECIMAL | 25–12000 |
| on_time_flag | BOOLEAN | ~82% true |
| damage_flag | BOOLEAN | ~3% true |
| shipment_mode | STRING | FTL, LTL, Parcel, Intermodal, Air |
| priority | STRING | Standard, Expedited, Next-Day |

**fleet_events** (~2000 rows)
| Column | Type | Description |
|---|---|---|
| event_id | INT | PK |
| vehicle_id | INT | FK → vehicles |
| carrier_id | INT | FK → carriers |
| event_date | DATE | Rolling, last 18 months |
| event_type | STRING | Departure, Arrival, Maintenance, Fuel Stop, Inspection, Breakdown |
| mileage | DECIMAL | 0–800 |
| fuel_gallons | DECIMAL | 0–150 |
| idle_hours | DECIMAL | 0–6 |
| location_city | STRING | From entity pool |

**warehouse_operations** (~1500 rows)
| Column | Type | Description |
|---|---|---|
| operation_id | INT | PK |
| warehouse_id | INT | FK → warehouses |
| operation_date | DATE | Rolling, last 18 months |
| operation_type | STRING | Inbound, Outbound, Pick, Pack, Putaway, Cycle Count |
| units_processed | INT | 10–5000 |
| labor_hours | DECIMAL | 0.5–24 |
| error_count | INT | 0–10 |
| dock_utilization_pct | DECIMAL | 0.2–1.0 |

### Dimension Tables

**carriers** (~20 rows)
| Column | Type |
|---|---|
| carrier_id | INT (PK) |
| carrier_name | STRING |
| carrier_type | STRING (Asset-Based, Brokerage, 3PL, Parcel) |
| dot_rating | STRING (Satisfactory, Conditional, Unsatisfactory) |
| contract_type | STRING (Dedicated, Spot, Contract) |

**routes** (~30 rows)
| Column | Type |
|---|---|
| route_id | INT (PK) |
| origin_city | STRING |
| origin_state | STRING |
| destination_city | STRING |
| destination_state | STRING |
| distance_miles | INT |
| lane_type | STRING (Primary, Secondary, Backhaul) |

**warehouses** (~10 rows)
| Column | Type |
|---|---|
| warehouse_id | INT (PK) |
| warehouse_name | STRING |
| city | STRING |
| state | STRING |
| region | STRING (East, Central, West, South) |
| sqft | INT |
| max_capacity_units | INT |

**vehicles** (~50 rows)
| Column | Type |
|---|---|
| vehicle_id | INT (PK) |
| vehicle_type | STRING (Dry Van, Reefer, Flatbed, Box Truck, Sprinter) |
| model_year | INT |
| carrier_id | INT (FK → carriers) |
| status | STRING (Active, Maintenance, Retired) |

---

## ETL Outputs

### Output 1: Shipping Performance
**Joins**: shipments ← carriers, routes, warehouses
**Key columns**: ship_date, delivery_date, carrier_name, carrier_type, origin_city, destination_city, distance_miles, weight_kg, freight_cost, on_time_flag, damage_flag, shipment_mode, warehouse_name

### Output 2: Fleet Analytics
**Joins**: fleet_events ← vehicles, carriers
**Key columns**: event_date, event_type, vehicle_type, carrier_name, mileage, fuel_gallons, idle_hours, location_city, model_year, status

### Output 3: Warehouse Operations
**Joins**: warehouse_operations ← warehouses
**Key columns**: operation_date, operation_type, units_processed, labor_hours, error_count, dock_utilization_pct, warehouse_name, city, region, sqft

---

## App Studio Pages

| Page | Icon | Focus | Primary Dataset |
|---|---|---|---|
| Overview | `analytics` | Network-wide KPIs | Shipping Performance |
| Shipping | `local_shipping` | On-time delivery, cost per mile, carrier performance | Shipping Performance |
| Fleet | `gauge` | Utilization, fuel efficiency, maintenance | Fleet Analytics |
| Warehouse | `warehouse` | Throughput, labor productivity, accuracy | Warehouse Operations |

---

## Hero Metrics (per page)

**Overview**: Total Shipments, On-Time Rate %, Avg Freight Cost, Fleet Utilization %
**Shipping**: Shipments Delivered, On-Time %, Avg Cost/Mile, Damage Rate %
**Fleet**: Active Vehicles, Avg Miles/Day, Fuel Efficiency (MPG), Idle Hours %
**Warehouse**: Units Processed, Pick Accuracy %, Labor Hours, Dock Utilization %

---

## Chart Assignments

| Page | Template | Chart Type | X-Axis | Y-Axis |
|---|---|---|---|---|
| Overview | A (area/line) | Shipment volume trend | ship_date (monthly) | shipment count |
| Shipping | B (bar) | By carrier or mode | carrier_name or shipment_mode | freight_cost or on_time % |
| Fleet | C (multi-line) | Mileage + fuel trends | event_date (monthly) | total mileage, total fuel |
| Warehouse | B (bar, horizontal) | By warehouse | warehouse_name | units_processed or labor_hours |

---

## Theme

Use a bold dark palette from `~/.agents/skills/domo-app-theme/references/themes/`. Recommended: shades or charcoal family. Font: sans-serif.
