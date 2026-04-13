# Retail & E-Commerce Demo Pack

## Industry Context
Omnichannel retail — in-store and online transactions, customer behavior, inventory management, and product performance.

---

## Star Schema

### Fact Tables

**transactions** (~2000 rows)
| Column | Type | Description |
|---|---|---|
| transaction_id | INT | PK |
| customer_id | INT | FK → customers |
| product_id | INT | FK → products |
| store_id | INT | FK → stores |
| transaction_date | DATE | Rolling, last 18 months |
| quantity | INT | 1–20 |
| unit_price | DECIMAL | 5.99–499.99 |
| discount_pct | DECIMAL | 0–0.35 |
| channel | STRING | In-Store, Online, Mobile App |
| payment_method | STRING | Credit, Debit, Digital Wallet, Cash |

**web_sessions** (~2500 rows)
| Column | Type | Description |
|---|---|---|
| session_id | INT | PK |
| customer_id | INT | FK → customers |
| product_id | INT | FK → products (viewed product, nullable) |
| session_date | DATE | Rolling, last 18 months |
| page_views | INT | 1–45 |
| session_duration_sec | INT | 10–1800 |
| device_type | STRING | Desktop, Mobile, Tablet |
| traffic_source | STRING | Organic, Paid Search, Social, Email, Direct |
| converted | BOOLEAN | ~12% true |
| cart_abandonment | BOOLEAN | ~25% true |

**inventory_movements** (~1800 rows)
| Column | Type | Description |
|---|---|---|
| movement_id | INT | PK |
| product_id | INT | FK → products |
| store_id | INT | FK → stores |
| movement_date | DATE | Rolling, last 18 months |
| movement_type | STRING | Receipt, Sale, Transfer, Return, Shrinkage |
| quantity | INT | -50 to 500 (negative for outbound) |
| on_hand_after | INT | 0–2000 |
| days_of_supply | INT | 0–120 |

### Dimension Tables

**products** (~80 rows)
| Column | Type |
|---|---|
| product_id | INT (PK) |
| product_name | STRING |
| category | STRING (Electronics, Apparel, Home & Garden, Sports, Beauty) |
| subcategory | STRING |
| brand | STRING |
| cost | DECIMAL |

**customers** (~400 rows)
| Column | Type |
|---|---|
| customer_id | INT (PK) |
| customer_segment | STRING (VIP, Regular, New, Lapsed) |
| age_group | STRING (18-24, 25-34, 35-44, 45-54, 55+) |
| region | STRING |
| loyalty_tier | STRING (Bronze, Silver, Gold, Platinum) |
| signup_date | DATE |

**stores** (~15 rows)
| Column | Type |
|---|---|
| store_id | INT (PK) |
| store_name | STRING |
| store_type | STRING (Flagship, Standard, Outlet, Online-Only) |
| city | STRING |
| state | STRING |
| region | STRING (Northeast, Southeast, Midwest, West) |
| sqft | INT |

**categories** (~20 rows)
| Column | Type |
|---|---|
| category_id | INT (PK) |
| category_name | STRING |
| department | STRING (Hardlines, Softlines, Consumables) |
| margin_target_pct | DECIMAL |
| seasonal | BOOLEAN |

---

## ETL Outputs

### Output 1: Sales Performance
**Joins**: transactions ← products, customers, stores
**Key columns**: transaction_date, product_name, category, brand, customer_segment, loyalty_tier, store_name, region, quantity, unit_price, discount_pct, channel

### Output 2: Customer Analytics
**Joins**: web_sessions ← customers, products
**Key columns**: session_date, customer_segment, age_group, loyalty_tier, page_views, session_duration_sec, device_type, traffic_source, converted, cart_abandonment, product_name, category

### Output 3: Inventory Health
**Joins**: inventory_movements ← products, stores
**Key columns**: movement_date, product_name, category, brand, store_name, store_type, region, movement_type, quantity, on_hand_after, days_of_supply

---

## App Studio Pages

| Page | Icon | Focus | Primary Dataset |
|---|---|---|---|
| Overview | `analytics` | Revenue, traffic, inventory KPIs | Sales Performance |
| Sales | `shopping_cart` | Revenue trends, channel mix, discounting | Sales Performance |
| Customers | `people` | Conversion, engagement, segmentation | Customer Analytics |
| Inventory | `cube-filled` | Stock levels, days of supply, shrinkage | Inventory Health |

---

## Hero Metrics (per page)

**Overview**: Total Revenue, Conversion Rate %, Avg Order Value, Active Customers
**Sales**: Gross Revenue, Units Sold, Avg Discount %, Online vs In-Store Split
**Customers**: Unique Sessions, Conversion Rate %, Cart Abandonment %, Avg Session Duration
**Inventory**: Total Units On-Hand, Avg Days of Supply, Shrinkage Rate %, Stockout Count

---

## Chart Assignments

| Page | Template | Chart Type | X-Axis | Y-Axis |
|---|---|---|---|---|
| Overview | A (area/line) | Revenue trend | transaction_date (monthly) | revenue (quantity × unit_price) |
| Sales | C (multi-line) | Revenue by channel | transaction_date (monthly) | revenue per channel |
| Customers | B (bar) | By segment or traffic source | customer_segment or traffic_source | session count or conversion rate |
| Inventory | B (bar, horizontal) | By category or store | category or store_name | on_hand_after or days_of_supply |

---

## Theme

Use a vibrant modern palette from `~/.agents/skills/domo-app-theme/references/themes/`. Recommended: punk or a bright accent family. Font: sans-serif.
