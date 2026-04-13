# Healthcare Demo Pack

## Industry Context
Hospital/health system operations — patient encounters, clinical outcomes, lab diagnostics, and revenue cycle management.

---

## Star Schema

### Fact Tables

**patient_encounters** (~1500 rows)
| Column | Type | Description |
|---|---|---|
| encounter_id | INT | PK |
| patient_id | INT | FK → patients |
| provider_id | INT | FK → providers |
| department_id | INT | FK → departments |
| encounter_date | DATE | Rolling, last 18 months |
| discharge_date | DATE | encounter_date + 0–14 days |
| encounter_type | STRING | Inpatient, Outpatient, Emergency, Telehealth |
| length_of_stay_days | INT | 0–21 |
| readmission_flag | BOOLEAN | ~8% true |
| satisfaction_score | DECIMAL | 1.0–5.0 |

**lab_results** (~2000 rows)
| Column | Type | Description |
|---|---|---|
| lab_id | INT | PK |
| encounter_id | INT | FK → patient_encounters |
| patient_id | INT | FK → patients |
| department_id | INT | FK → departments |
| order_date | DATE | Rolling, last 18 months |
| result_date | DATE | order_date + 0–3 days |
| test_category | STRING | Hematology, Chemistry, Microbiology, Pathology, Radiology |
| result_status | STRING | Normal, Abnormal, Critical |
| turnaround_hours | DECIMAL | 0.5–72 |

**billing_claims** (~1800 rows)
| Column | Type | Description |
|---|---|---|
| claim_id | INT | PK |
| encounter_id | INT | FK → patient_encounters |
| patient_id | INT | FK → patients |
| diagnosis_id | INT | FK → diagnosis_codes |
| claim_date | DATE | Rolling, last 18 months |
| billed_amount | DECIMAL | 150–85000 |
| allowed_amount | DECIMAL | ≤ billed_amount |
| paid_amount | DECIMAL | ≤ allowed_amount |
| payer_type | STRING | Medicare, Medicaid, Commercial, Self-Pay |
| claim_status | STRING | Paid, Denied, Pending, Appealed |

### Dimension Tables

**patients** (~500 rows)
| Column | Type |
|---|---|
| patient_id | INT (PK) |
| age_group | STRING (0-17, 18-34, 35-49, 50-64, 65+) |
| gender | STRING |
| zip_code | STRING |
| insurance_type | STRING (Medicare, Medicaid, Commercial, Self-Pay) |

**providers** (~60 rows)
| Column | Type |
|---|---|
| provider_id | INT (PK) |
| provider_name | STRING |
| specialty | STRING (Cardiology, Orthopedics, Internal Medicine, Surgery, Pediatrics, Emergency Medicine) |
| credential | STRING (MD, DO, NP, PA) |

**departments** (~12 rows)
| Column | Type |
|---|---|
| department_id | INT (PK) |
| department_name | STRING (Emergency, ICU, Medical/Surgical, Outpatient Clinic, Radiology, Lab, Cardiology, Orthopedics) |
| floor | INT |
| bed_count | INT |

**diagnosis_codes** (~50 rows)
| Column | Type |
|---|---|
| diagnosis_id | INT (PK) |
| icd_code | STRING (e.g., I25.10, M54.5) |
| description | STRING |
| category | STRING (Cardiovascular, Musculoskeletal, Respiratory, Endocrine, Neurological) |
| severity | STRING (Minor, Moderate, Major, Critical) |

---

## ETL Outputs

### Output 1: Patient Care Analytics
**Joins**: patient_encounters ← patients, providers, departments
**Key columns**: encounter_date, encounter_type, length_of_stay_days, readmission_flag, satisfaction_score, age_group, provider_name, specialty, department_name

### Output 2: Clinical Outcomes
**Joins**: lab_results ← patients, departments
**Key columns**: order_date, result_date, test_category, result_status, turnaround_hours, age_group, department_name

### Output 3: Revenue Cycle
**Joins**: billing_claims ← patients, diagnosis_codes
**Key columns**: claim_date, billed_amount, allowed_amount, paid_amount, payer_type, claim_status, age_group, icd_code, description, category, severity

---

## App Studio Pages

| Page | Icon | Focus | Primary Dataset |
|---|---|---|---|
| Overview | `analytics` | System-wide KPIs | Patient Care Analytics |
| Patient Care | `heart` | Encounters, LOS, readmissions, satisfaction | Patient Care Analytics |
| Clinical Quality | `certified` | Lab turnaround, result distribution, test volume | Clinical Outcomes |
| Financial Performance | `money-universal` | Revenue, denials, payer mix, collections | Revenue Cycle |

---

## Hero Metrics (per page)

**Overview**: Total Encounters, Avg LOS, Readmission Rate %, Avg Satisfaction Score
**Patient Care**: Inpatient Count, Avg LOS, Readmission Rate %, Discharge Volume
**Clinical Quality**: Lab Orders Completed, Avg Turnaround Hours, Critical Result %, Normal Result %
**Financial Performance**: Total Billed, Total Collected, Denial Rate %, Net Collection Rate %

---

## Chart Assignments

| Page | Template | Chart Type | X-Axis | Y-Axis |
|---|---|---|---|---|
| Overview | A (area/line) | Encounter volume trend | encounter_date (monthly) | encounter count |
| Patient Care | C (multi-line) | LOS + readmission trends | encounter_date (monthly) | avg LOS, readmission count |
| Clinical Quality | B (bar) | By test category or department | test_category | count or avg turnaround |
| Financial Performance | B (bar, horizontal) | By payer type | payer_type | paid_amount |

---

## Theme

Use a clean blue/teal palette from `~/.agents/skills/domo-app-theme/references/themes/`. Recommended: corporate or green family. Font: sans-serif.
