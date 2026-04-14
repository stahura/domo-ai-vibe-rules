---
name: domo-data-generator
description: "**Generating sample data for Domo** -- invoke when a user needs to create realistic sample datasets and upload them to a Domo instance. Primary signals: requests for sample data, demo data, test data, fake data for Domo; mentions of Salesforce, Google Analytics, QuickBooks, NetSuite, Google Ads, Facebook Ads, HubSpot, Marketo, or Health Portal sample data; questions about the datagen CLI or domo_data_generator. Covers: generating datasets, uploading to Domo, creating datasets in Domo, rolling dates, entity pools, connector icons, catalog management, and adding new dataset definitions. Skip for: real connector setup, production data pipelines, data transformations (Magic ETL), or Domo App Platform."
---

# Domo Sample Data Generator

Generate realistic, cross-referenced sample data for Domo using the `datagen` CLI.

**Repository:** <https://github.com/brrink/domo_data_generator>

---

## Overview

The generator creates sample data mirroring major business platforms with consistent cross-source entity integrity, then uploads it to Domo. It includes:

- 18 pre-built datasets across 6 source categories (Salesforce, Google Analytics, Financial, Marketing, Health, AdPoint)
- YAML-driven catalog for easy dataset additions
- Shared entity pool (companies, people, products, sales reps, campaigns)
- Date rolling to keep data looking current
- Direct Domo integration (create datasets, upload, set connector icons)
- Structured JSON output by default (AI-agent-friendly)
- pipx installable -- runs from any directory

---

## Setup

```bash
# Install globally with pipx (recommended)
pipx install git+https://github.com/brrink/domo_data_generator.git

# Initialize a working directory
mkdir my-domo-data && cd my-domo-data
datagen init

# Edit .env with your Domo credentials
```

### Required Environment Variables

Edit the `.env` file created by `datagen init`:

| Variable | Purpose | Required for |
|----------|---------|-------------|
| `DOMO_INSTANCE` | Domo instance name (e.g. `mycompany`) | All Domo operations |
| `DOMO_DEVELOPER_TOKEN` | Access token from Domo Admin | Connector icons, provider discovery |
| `DOMO_CLIENT_ID` | OAuth client ID | Dataset creation, data upload |
| `DOMO_CLIENT_SECRET` | OAuth client secret | Dataset creation, data upload |

To create OAuth client credentials: **Domo > Admin > Authentication > Client credentials** -- create a client with `data` and `dashboard` scopes.

To create a developer token: **Domo > Admin > Authentication > Access tokens**.

Offline commands (`generate`, `list`, `status`, `pool`, `roll-dates`, `init`) require no credentials.

> **Auth boundary:** This tool authenticates directly with the Domo API using OAuth client credentials (`DOMO_CLIENT_ID` / `DOMO_CLIENT_SECRET`) or a developer token. It does **not** use `community-domo-cli` or ryuu-session auth. If `domo login` has been run, datagen can fall back to the ryuu session, but OAuth credentials are the primary and recommended auth method.

> **Multi-instance usage:** Credentials in `.env` are tied to a single Domo instance. If targeting a different instance, you must update `DOMO_INSTANCE`, `DOMO_CLIENT_ID`, and `DOMO_CLIENT_SECRET` in `.env` for the target instance before running any Domo commands. Verify credentials are correct before starting a long workflow.

---

## CLI Reference

Entry point: `datagen [OPTIONS] COMMAND [ARGS]`

### Global Options

| Option | Description |
|--------|-------------|
| `--verbose / -v` | Enable verbose logging |
| `--output / -o TEXT` | Output format: `json` (default), `table`, `yaml` |
| `--yes / -y` | Skip confirmation prompts |

All commands emit structured JSON by default for easy machine parsing.

### Init Command

#### `init` -- Initialize a working directory

```bash
datagen init                  # Initialize current directory
datagen init /path/to/dir     # Initialize a specific directory
```

Copies bundled catalog YAML files to `./catalog/`, creates `.env` template, and creates `./data/` directory. Run this once before using the CLI in a new directory.

### Core Commands

#### `generate` -- Generate sample data

```bash
datagen generate --all                    # Generate all datasets
datagen generate salesforce_opportunities  # Generate one dataset
datagen generate --all --seed 42          # Reproducible generation
datagen generate --all --dry-run          # Preview without writing
```

| Option | Description |
|--------|-------------|
| `name` | Dataset name (YAML filename stem), optional |
| `--all` | Generate all datasets |
| `--seed INTEGER` | Random seed for reproducibility |
| `--catalog-dir PATH` | Catalog directory override |
| `--data-dir PATH` | Data directory override |
| `--dry-run` | Preview without writing files |

#### `upload` -- Upload data to Domo (full replace)

```bash
datagen upload --all
datagen upload salesforce_opportunities
```

Requires `DOMO_CLIENT_ID` and `DOMO_CLIENT_SECRET`.

| Option | Description |
|--------|-------------|
| `name` | Dataset name, optional |
| `--all` | Upload all datasets |
| `--catalog-dir PATH` | Catalog directory override |
| `--data-dir PATH` | Data directory override |

#### `create-dataset` -- Create dataset(s) in Domo from catalog

```bash
datagen create-dataset --all --skip-existing
datagen create-dataset salesforce_opportunities
```

Requires `DOMO_CLIENT_ID` and `DOMO_CLIENT_SECRET`. The `domo_id` is persisted locally (in the catalog YAML if writable, otherwise in `data/domo_ids.json`).

| Option | Description |
|--------|-------------|
| `name` | Dataset name, optional |
| `--all` | Create all datasets |
| `--skip-existing` | Skip datasets that already have a `domo_id` |
| `--catalog-dir PATH` | Catalog directory override |

#### `roll-dates` -- Shift rolling date columns to stay current

```bash
datagen roll-dates
datagen roll-dates --anchor-date 2026-04-01
```

| Option | Description |
|--------|-------------|
| `--anchor-date TEXT` | Target date (YYYY-MM-DD), defaults to today |
| `--catalog-dir PATH` | Catalog directory override |
| `--data-dir PATH` | Data directory override |

### Informational Commands

#### `list` -- List catalog dataset definitions

```bash
datagen list                    # JSON output (default)
datagen --output table list     # Rich table for humans
datagen list --verbose          # Include column/schema details
```

#### `status` -- Display generation status for all datasets

```bash
datagen status
```

### Connector Icon Commands

Require `DOMO_DEVELOPER_TOKEN` and `DOMO_INSTANCE`.

#### `discover-types` -- Search Domo connector/provider types

```bash
datagen discover-types salesforce
```

#### `set-type` -- Set connector icon on a Domo dataset

```bash
datagen set-type salesforce_opportunities
datagen set-type salesforce_opportunities --provider-key custom_key
```

#### `set-type-all` -- Set connector icon on all datasets with a `domo_id`

```bash
datagen set-type-all
```

### Entity Pool Commands

#### `pool regenerate` -- Regenerate the shared entity pool

```bash
datagen pool regenerate
datagen pool regenerate --seed 99
datagen pool regenerate --company-count 500 --person-count 1000
```

| Option | Default |
|--------|---------|
| `--seed INTEGER` | 42 |
| `--company-count INTEGER` | 200 |
| `--person-count INTEGER` | 500 |
| `--product-count INTEGER` | 50 |
| `--sales-rep-count INTEGER` | 20 |
| `--campaign-count INTEGER` | 30 |

#### `pool show` -- Display entity pool summary

```bash
datagen pool show
```

---

## Common Workflows

### Full setup for a new Domo instance

```bash
datagen init
# Edit .env with credentials
datagen pool regenerate
datagen generate --all
datagen create-dataset --all
datagen upload --all
datagen set-type-all
```

### Daily refresh via cron

```bash
# Crontab entry: roll dates and re-upload daily at 6 AM
0 6 * * * cd /path/to/project && datagen roll-dates && datagen upload --all
```

### Generate a single dataset end-to-end

```bash
datagen generate salesforce_opportunities
datagen create-dataset salesforce_opportunities
datagen upload salesforce_opportunities
datagen set-type salesforce_opportunities
```

---

## Included Datasets

| Category | Dataset Name | Key | Rows |
|----------|-------------|-----|------|
| Salesforce | Salesforce - Accounts | `salesforce_accounts` | 500 |
| Salesforce | Salesforce - Contacts | `salesforce_contacts` | 1,500 |
| Salesforce | Salesforce - Opportunities | `salesforce_opportunities` | 2,500 |
| Google Analytics | Google Analytics - Sessions | `ga_sessions` | 5,000 |
| Google Analytics | Google Analytics - Page Views | `ga_pageviews` | 10,000 |
| Financial | QuickBooks - Invoices | `financial_invoices` | 3,000 |
| Financial | NetSuite - General Ledger | `financial_gl_entries` | 5,000 |
| Marketing | Google Ads - Campaign Performance | `marketing_google_ads` | 3,000 |
| Marketing | Facebook Ads - Campaign Performance | `marketing_facebook_ads` | 2,500 |
| Marketing | HubSpot - Contacts | `marketing_hubspot_contacts` | 2,000 |
| Marketing | Marketing - Market Leads | `marketing_market_leads` | 2,500 |
| Marketing | Marketo - Leads | `marketing_marketo_leads` | 3,000 |
| Health | Health Portal - Demographics | `health_demographics` | 15 |
| Health | Health Portal - Lab Results | `health_lab_results` | 1,470 |
| Health | Health Portal - Vitals | `health_vitals` | 5,250 |
| AdPoint | AdPoint - Orders | `adpoint_orders` | 150 |
| AdPoint | AdPoint - Line Items | `adpoint_line_items` | 500 |
| AdPoint | AdPoint - Flights | `adpoint_flights` | 2,000 |

---

## Entity Pool

The shared entity pool provides consistent cross-dataset references. Entities are generated once and reused across all datasets.

| Entity Type | Default Count | Key Fields |
|-------------|---------------|------------|
| company | 200 | id, account_id, name, domain, industry, size, city, state, annual_revenue, employee_count |
| person | 500 | id, contact_id, first_name, last_name, full_name, email, company_id, company_name, title, phone |
| product | 50 | id, name, category, unit_price, sku |
| sales_rep | 20 | id, rep_id, first_name, last_name, full_name, email, region |
| campaign | 30 | id, name, channel, budget, status |

---

## Adding New Dataset Definitions

Dataset definitions live in the `catalog/` directory as YAML files. Each YAML file defines metadata, columns, and generator configurations.

### YAML Structure

```yaml
dataset:
  name: My Custom Dataset
  domo_id: null
  source_type: custom
  description: "Description of the dataset"
  row_count: 1000
  tags:
    - custom
    - demo

schema:
  - name: id
    type: STRING
    generator: uuid4

  - name: company_name
    type: STRING
    generator: entity_ref
    entity: company
    field: name

  - name: amount
    type: DOUBLE
    generator: random_decimal
    min: 100.0
    max: 10000.0
    precision: 2

  - name: tier
    type: STRING
    generator: weighted_choice
    choices:
      "Tier 1": 0.40
      "Tier 2": 0.35
      "Tier 3": 0.25

  - name: created_date
    type: DATE
    generator: date_range
    start_days_ago: 365
    end_days_ahead: 0
    rolling: true
```

### Available Column Types

`STRING`, `LONG`, `DOUBLE`, `DECIMAL`, `DATETIME`, `DATE`

### Available Generators

**Generic:** `uuid4`, `random_choice`, `weighted_choice`, `random_int`, `random_decimal`, `date_range`, `entity_ref`, `compound`, `sequence`, `constant`, `derived_from_date`, `stage_derived`, `faker`

**Salesforce:** `sf_id`, `sf_opportunity_name`, `sf_case_subject`, `sf_lead_rating`

**Google Analytics:** `ga_session_id`, `ga_page_path`, `ga_source`, `ga_medium`, `ga_campaign`, `ga_browser`, `ga_device_category`, `ga_country`, `ga_bounce_rate`, `ga_session_duration`, `ga_pageviews`, `ga_landing_page`

**Financial:** `gl_account_code`, `gl_account_name`, `invoice_number`, `payment_terms`, `payment_method`, `invoice_status`, `journal_type`, `department`, `fiscal_period`, `debit_credit`

**Marketing/Ads:** `ad_platform`, `campaign_objective`, `ad_format`, `ad_headline`, `ad_keyword`, `targeting_type`, `impressions`, `clicks_from_impressions`, `ctr`, `cost_per_click`, `ad_spend`, `conversions_from_clicks`, `hubspot_lifecycle`, `hubspot_lead_status`, `ad_group_id`

**Health:** `health_lab_init`, `health_lab_field`, `health_vital_init`, `health_vital_field`, `health_demographics`

### Generator Column Options

| Option | Used With | Description |
|--------|-----------|-------------|
| `entity` | `entity_ref` | Entity pool type to reference |
| `field` | `entity_ref` | Field to pull from the entity |
| `choices` | `random_choice`, `weighted_choice` | List of possible values |
| `min` / `max` | `random_int`, `random_decimal` | Value range |
| `precision` | `random_decimal` | Decimal places |
| `template` | `compound` | String template with `{field}` placeholders |
| `refs` | `compound` | Column references for template substitution |
| `start_days_ago` / `end_days_ahead` | `date_range` | Date range relative to today |
| `rolling` | `date_range` | Enable date rolling for freshness |
| `mapping` | `stage_derived` | Map source values to derived values |
| `source_column` | `stage_derived`, `derived_from_date` | Column to derive from |
| `format` | `derived_from_date` | Date format string |
| `faker_method` | `faker` | Faker library method name |
| `faker_args` | `faker` | Arguments for the Faker method |

---

## Rules

1. **Run `datagen init` first** -- Initialize a working directory before using any other commands. This copies the catalog and creates `.env`.
2. **Always run `pool regenerate` then `generate` before uploading** -- Run `pool regenerate` (if no pool exists yet) then `generate` before `upload`. Some generators depend on the entity pool even if your schema has no explicit `entity_ref` columns.
3. **Create datasets before first upload** -- Run `create-dataset` before `upload` for new datasets. The `domo_id` is persisted locally.
4. **Use `--skip-existing`** -- When running `create-dataset --all`, use `--skip-existing` to avoid duplicating datasets that already have a `domo_id`.
5. **Entity pool consistency** -- Regenerating the pool (`pool regenerate`) invalidates all previously generated data. Re-generate all datasets afterward.
6. **Date rolling** -- Use `roll-dates` before upload to keep date columns current. Only columns with `rolling: true` are affected.
7. **Credentials** -- `DOMO_CLIENT_ID` and `DOMO_CLIENT_SECRET` are required for `upload` and `create-dataset`. `DOMO_DEVELOPER_TOKEN` is required for `set-type` and `discover-types`. Offline commands need no credentials.
8. **Reproducibility** -- Use `--seed` for reproducible data generation across runs.
9. **Output format** -- Default output is JSON. Use `--output table` for human-readable Rich tables.
10. **Dataset provisioning boundary** -- Use `datagen create-dataset` and `datagen upload` for dataset creation and CSV upload. The `community-domo-cli` does **not** support dataset creation or CSV upload. Do not attempt `community-domo-cli datasets upload-csv` or similar -- it does not exist.

---

## Checklist

- [ ] CLI installed (`pipx install git+https://github.com/brrink/domo_data_generator.git`)
- [ ] Working directory initialized (`datagen init`)
- [ ] `.env` configured with Domo credentials
- [ ] Entity pool generated (`datagen pool regenerate`)
- [ ] Datasets generated (`datagen generate --all`)
- [ ] Datasets created in Domo (`datagen create-dataset --all --skip-existing`)
- [ ] Data uploaded (`datagen upload --all`)
- [ ] Connector icons set (`datagen set-type-all`) if desired
- [ ] Cron configured for daily date rolling and upload if needed
