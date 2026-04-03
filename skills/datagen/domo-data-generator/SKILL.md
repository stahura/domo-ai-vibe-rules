---
name: domo-data-generator
description: "**Generating sample data for Domo** -- invoke when a user needs to create realistic sample datasets and upload them to a Domo instance. Primary signals: requests for sample data, demo data, test data, fake data for Domo; mentions of Salesforce, Google Analytics, QuickBooks, NetSuite, Google Ads, Facebook Ads, or HubSpot sample data; questions about the datagen CLI or domo_data_generator. Covers: generating datasets, uploading to Domo, creating datasets in Domo, rolling dates, entity pools, connector icons, catalog management, and adding new dataset definitions. Skip for: real connector setup, production data pipelines, data transformations (Magic ETL), or Domo App Platform."
---

# Domo Sample Data Generator

Generate realistic, cross-referenced sample data for Domo using the `domo_data_generator` CLI.

**Repository:** <https://github.com/brrink/domo_data_generator>

---

## Overview

The generator creates sample data mirroring major business platforms with consistent cross-source entity integrity, then uploads it to Domo. It includes:

- 10 pre-built datasets across 4 source categories (Salesforce, Google Analytics, Financial, Marketing)
- YAML-driven catalog for easy dataset additions
- Shared entity pool (companies, people, products, sales reps, campaigns)
- Date rolling to keep data looking current
- Direct Domo integration (create datasets, upload, set connector icons)
- Cron-friendly for scheduled automation

---

## Setup

```bash
# Clone the repository
git clone https://github.com/brrink/domo_data_generator.git
cd domo_data_generator

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Domo credentials
```

### Required Environment Variables

| Variable | Purpose |
|----------|---------|
| `DOMO_CLIENT_ID` | OAuth client identifier |
| `DOMO_CLIENT_SECRET` | OAuth client secret |
| `DOMO_DEVELOPER_TOKEN` | Internal API auth token |
| `DOMO_API_HOST` | API endpoint hostname |
| `DOMO_INSTANCE` | Domo instance name |
| `DOMO_SET_CONNECTOR_TYPE` | Enable connector icon customization (optional, default: false) |

---

## CLI Reference

Entry point: `python -m datagen [OPTIONS] COMMAND [ARGS]`

Global option: `--verbose / -v` enables verbose logging.

### Core Commands

#### `generate` -- Generate sample data

```bash
python -m datagen generate --all                    # Generate all datasets
python -m datagen generate salesforce_opportunities  # Generate one dataset
python -m datagen generate --all --seed 42          # Reproducible generation
python -m datagen generate --all --dry-run          # Preview without writing
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
python -m datagen upload --all
python -m datagen upload salesforce_opportunities
```

| Option | Description |
|--------|-------------|
| `name` | Dataset name, optional |
| `--all` | Upload all datasets |
| `--catalog-dir PATH` | Catalog directory override |
| `--data-dir PATH` | Data directory override |

#### `create-dataset` -- Create dataset(s) in Domo from catalog

```bash
python -m datagen create-dataset --all --skip-existing
python -m datagen create-dataset salesforce_opportunities
```

| Option | Description |
|--------|-------------|
| `name` | Dataset name, optional |
| `--all` | Create all datasets |
| `--skip-existing` | Skip datasets that already have a `domo_id` |
| `--catalog-dir PATH` | Catalog directory override |

#### `roll-dates` -- Shift rolling date columns to stay current

```bash
python -m datagen roll-dates
python -m datagen roll-dates --anchor-date 2026-04-01
```

| Option | Description |
|--------|-------------|
| `--anchor-date TEXT` | Target date (YYYY-MM-DD), defaults to today |
| `--catalog-dir PATH` | Catalog directory override |
| `--data-dir PATH` | Data directory override |

### Informational Commands

#### `list` -- List catalog dataset definitions

```bash
python -m datagen list
python -m datagen list --verbose   # Show column details
```

#### `status` -- Display generation status for all datasets

```bash
python -m datagen status
```

### Connector Icon Commands

#### `discover-types` -- Search Domo connector/provider types

```bash
python -m datagen discover-types salesforce
```

#### `set-type` -- Set connector icon on a Domo dataset

```bash
python -m datagen set-type salesforce_opportunities
python -m datagen set-type salesforce_opportunities --provider-key custom_key
```

#### `set-type-all` -- Set connector icon on all datasets with a `domo_id`

```bash
python -m datagen set-type-all
```

### Entity Pool Commands

#### `pool regenerate` -- Regenerate the shared entity pool

```bash
python -m datagen pool regenerate
python -m datagen pool regenerate --seed 99
python -m datagen pool regenerate --company-count 500 --person-count 1000
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
python -m datagen pool show
```

---

## Common Workflows

### Full setup for a new Domo instance

```bash
python -m datagen pool regenerate
python -m datagen generate --all
python -m datagen create-dataset --all
python -m datagen upload --all
python -m datagen set-type-all
```

### Daily refresh via cron

```bash
# Crontab entry: roll dates and re-upload daily at 6 AM
0 6 * * * cd /path/to/domo_data_generator && .venv/bin/python -m datagen roll-dates && .venv/bin/python -m datagen upload --all
```

### Generate a single dataset end-to-end

```bash
python -m datagen generate salesforce_opportunities
python -m datagen create-dataset salesforce_opportunities
python -m datagen upload salesforce_opportunities
python -m datagen set-type salesforce_opportunities
```

---

## Included Datasets

| Category | Dataset Name |
|----------|-------------|
| Salesforce | `salesforce_accounts`, `salesforce_contacts`, `salesforce_opportunities` |
| Google Analytics | `ga_sessions`, `ga_pageviews` |
| Financial | `financial_gl_entries`, `financial_invoices` |
| Marketing | `marketing_google_ads`, `marketing_facebook_ads`, `marketing_hubspot_contacts` |

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
meta:
  name: my_custom_dataset
  source_type: custom
  description: "Description of the dataset"
  row_count: 1000
  tags:
    - custom
    - demo

columns:
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

1. **Always generate before uploading** -- Run `generate` (or `generate --all`) before `upload` to ensure data files exist.
2. **Create datasets before first upload** -- Run `create-dataset` before `upload` for new datasets. The `domo_id` is stored in the catalog YAML.
3. **Use `--skip-existing`** -- When running `create-dataset --all`, use `--skip-existing` to avoid duplicating datasets that already have a `domo_id`.
4. **Entity pool consistency** -- Regenerating the pool (`pool regenerate`) invalidates all previously generated data. Re-generate all datasets afterward.
5. **Date rolling** -- Use `roll-dates` before upload to keep date columns current. Only columns with `rolling: true` are affected.
6. **Environment variables** -- Ensure `.env` is configured before any Domo operations (`upload`, `create-dataset`, `set-type`).
7. **Reproducibility** -- Use `--seed` for reproducible data generation across runs.

---

## Checklist

- [ ] Repository cloned and dependencies installed
- [ ] `.env` configured with valid Domo credentials
- [ ] Entity pool generated (`pool regenerate`)
- [ ] Datasets generated (`generate --all`)
- [ ] Datasets created in Domo (`create-dataset --all --skip-existing`)
- [ ] Data uploaded (`upload --all`)
- [ ] Connector icons set (`set-type-all`) if desired
- [ ] Cron configured for daily date rolling and upload if needed
