# Financial Services Demo Pack

## Industry Context
Wealth management and banking operations — client portfolios, transaction flows, loan origination, and compliance monitoring.

---

## Star Schema

### Fact Tables

**transactions** (~2000 rows)
| Column | Type | Description |
|---|---|---|
| transaction_id | INT | PK |
| account_id | INT | FK → accounts |
| product_id | INT | FK → products |
| branch_id | INT | FK → branches |
| transaction_date | DATE | Rolling, last 18 months |
| amount | DECIMAL | 10–500000 |
| transaction_type | STRING | Deposit, Withdrawal, Transfer, Fee, Interest, Payment |
| channel | STRING | Branch, Online, Mobile, ATM, Wire |
| currency | STRING | USD (95%), EUR, GBP |
| fraud_flag | BOOLEAN | ~1.5% true |

**loan_applications** (~1200 rows)
| Column | Type | Description |
|---|---|---|
| application_id | INT | PK |
| account_id | INT | FK → accounts |
| advisor_id | INT | FK → advisors |
| branch_id | INT | FK → branches |
| application_date | DATE | Rolling, last 18 months |
| loan_amount | DECIMAL | 5000–2000000 |
| interest_rate | DECIMAL | 3.5–18.0 |
| term_months | INT | 12, 24, 36, 60, 120, 180, 360 |
| loan_type | STRING | Mortgage, Auto, Personal, Business, HELOC |
| status | STRING | Approved, Declined, Pending, Withdrawn |
| credit_score | INT | 550–850 |
| debt_to_income | DECIMAL | 0.05–0.55 |

**portfolio_positions** (~1500 rows)
| Column | Type | Description |
|---|---|---|
| position_id | INT | PK |
| account_id | INT | FK → accounts |
| advisor_id | INT | FK → advisors |
| position_date | DATE | Rolling, last 18 months |
| asset_class | STRING | Equities, Fixed Income, Alternatives, Cash, Real Estate |
| market_value | DECIMAL | 1000–5000000 |
| cost_basis | DECIMAL | ≤ market_value ± 30% |
| unrealized_gain | DECIMAL | market_value - cost_basis |
| yield_pct | DECIMAL | 0–12 |
| risk_rating | STRING | Low, Moderate, Aggressive, Speculative |

### Dimension Tables

**accounts** (~300 rows)
| Column | Type |
|---|---|
| account_id | INT (PK) |
| account_type | STRING (Individual, Joint, Corporate, Trust, IRA, 401k) |
| client_segment | STRING (Mass Market, Affluent, High Net Worth, Ultra HNW) |
| relationship_start | DATE |
| region | STRING |
| aum_tier | STRING (<100K, 100K-500K, 500K-1M, 1M-5M, 5M+) |

**products** (~25 rows)
| Column | Type |
|---|---|
| product_id | INT (PK) |
| product_name | STRING |
| product_category | STRING (Checking, Savings, CD, Money Market, Brokerage, Advisory) |
| fee_schedule | STRING (Standard, Premium, Waived) |
| min_balance | DECIMAL |

**branches** (~20 rows)
| Column | Type |
|---|---|
| branch_id | INT (PK) |
| branch_name | STRING |
| city | STRING |
| state | STRING |
| region | STRING (Northeast, Southeast, Midwest, West, National) |
| branch_type | STRING (Full Service, Express, Private Banking, Digital Only) |

**advisors** (~40 rows)
| Column | Type |
|---|---|
| advisor_id | INT (PK) |
| advisor_name | STRING |
| title | STRING (Financial Advisor, VP, SVP, Managing Director) |
| certification | STRING (CFP, CFA, ChFC, Series 7) |
| team | STRING (Wealth Management, Retail Banking, Commercial, Private Client) |
| tenure_years | INT |

---

## ETL Outputs

### Output 1: Revenue Analytics
**Joins**: transactions ← accounts, products, branches
**Key columns**: transaction_date, transaction_type, amount, channel, account_type, client_segment, aum_tier, product_name, product_category, branch_name, region

### Output 2: Risk & Compliance
**Joins**: loan_applications ← accounts, advisors, branches
**Key columns**: application_date, loan_amount, interest_rate, term_months, loan_type, status, credit_score, debt_to_income, client_segment, advisor_name, certification, branch_name, region

### Output 3: Portfolio Performance
**Joins**: portfolio_positions ← accounts, advisors
**Key columns**: position_date, asset_class, market_value, cost_basis, unrealized_gain, yield_pct, risk_rating, account_type, client_segment, aum_tier, advisor_name, title, team

---

## App Studio Pages

| Page | Icon | Focus | Primary Dataset |
|---|---|---|---|
| Overview | `analytics` | Firm-wide KPIs | Revenue Analytics |
| Revenue | `money-universal` | Transaction volume, fee income, channel trends | Revenue Analytics |
| Risk | `exclamation-triangle` | Loan pipeline, credit quality, approval rates | Risk & Compliance |
| Portfolio | `chart-line` | AUM trends, allocation, performance, yield | Portfolio Performance |

---

## Hero Metrics (per page)

**Overview**: Total AUM, Net Revenue, Loan Volume, Active Accounts
**Revenue**: Total Transaction Volume, Fee Income, Avg Transaction Size, Digital Channel %
**Risk**: Applications Received, Approval Rate %, Avg Credit Score, Avg DTI Ratio
**Portfolio**: Total Market Value, Unrealized Gain, Avg Yield %, HNW Client Count

---

## Chart Assignments

| Page | Template | Chart Type | X-Axis | Y-Axis |
|---|---|---|---|---|
| Overview | A (area/line) | AUM or revenue trend | transaction_date (monthly) | total amount |
| Revenue | C (multi-line) | Revenue by channel | transaction_date (monthly) | amount per channel |
| Risk | B (bar) | By loan type or status | loan_type or status | loan_amount or count |
| Portfolio | B (bar, horizontal) | By asset class | asset_class | market_value |

---

## Theme

Use a sophisticated corporate palette from `~/.agents/skills/domo-app-theme/references/themes/`. Recommended: corporate or a navy/gold combination. Font: serif or refined sans-serif.
