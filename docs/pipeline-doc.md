# Pipeline Technical Documentation — SmartCRM Customer Data Quality (Stream L7)

**Course:** Graduation Internship / Capstone Project 1 (71ITGR40203) — Fall 2026  
**Specialization:** Data Analytics (DA) · **Business Stream:** L7 – Customer Data Quality  
**Author:** Ho Le Trung Bao — **Student ID:** 2374802010030  
**Target Database:** SQLite Star Schema (`data/processed/warehouse.db`)

---

## 1. High-Level Architecture Overview

The SmartCRM Data Quality Pipeline operates as a deterministic, batch-oriented ETL pipeline that ingests raw customer transaction records from Mekong Mobile, cleanses personal identifiers, quantitatively assesses multidimensional data quality, and branches records into a dimensional Star Schema data warehouse and an isolated audit reject table.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Raw Source: customers_raw.csv                   │
│                        (67,037 raw customer records)                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 1. EXTRACT (src/extract/read_sources.py)                               │
│    - Reads CSV with dtype=str to preserve leading zeros in phone codes │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. TRANSFORM (src/transform/clean_customers.py & rules.py)             │
│    - Pure functions: Title Case name, 10-digit phone, ISO-8601 date    │
│    - PII Pseudonymization & Masking (Criterion D4 compliant)           │
│    - Deterministic partitioning into Clean and Rejected datasets       │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
    (Clean Records) │                                │ (Dirty Records)
                    ▼                                ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────┐
│ 3. QUALITY (src/quality/checks.py)   │  │ 5a. REJECT ISOLATION         │
│    - Measures 3 Dimensions:          │  │     (src/load/load_staging)  │
│      * Completeness (3 checks)       │  │     - Quarantines 4,133      │
│      * Accuracy (4 checks)           │  │       records into           │
│      * Consistency / Uniqueness      │  │       reject_rows with       │
│    - Compares vs config.example.yaml │  │       human-readable reasons │
└───────────────────┬──────────────────┘  └──────────────┬───────────────┘
                    │                                    │
                    ▼                                    │
┌────────────────────────────────────────────────────────┴───────────────┐
│ 5b. LOAD (src/load/load_warehouse.py & load_staging.py)                │
│     - Idempotent upsert into dim_audit_run & dim_customer              │
│     - Records fact entries into fact_customer_quality_audit            │
│     - Persists quality metrics into quality_measures                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ SQLite Star Schema Warehouse (warehouse.db) + Dashboard & CLI Audits   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Source & Ingestion (`src/extract/read_sources.py`)

* **Source File:** `data/raw/customers_raw.csv` (Primary, 67,037 records) or `data/mau/customers_sample.csv` (Sample, 300 records).
* **Ingestion Strategy:**
  * Strict extraction with `dtype=str` and `keep_default_na=False`. This guarantees that Vietnamese mobile phone prefixes (`09x`, `08x`, `03x`, `07x`, `05x`) are never truncated by numerical auto-casting.
  * Resilient column mapping (`record_id` $\leftrightarrow$ `customer_id`, `ngay_tao` $\leftrightarrow$ `ngay_dang_ky`) to absorb heterogeneous naming conventions across retail stores.

---

## 3. Data Transformation & Cleansing Rules (`src/transform/rules.py`)

* **Customer Name:** Strips extraneous whitespaces; capitalizes initials into proper Vietnamese Title Case (`"  nguyễn  văn an "` $\to$ `"Nguyễn Văn An"`).
* **Phone Number:** Normalizes international codes (`+84` and `84`), strips dots/spaces/dashes, validates against the 10-digit mobile carrier prefix directory. Invalid formats return `None` and trigger rejection.
* **Registration Date:** Dynamically parses heterogeneous date formats (`YYYY-MM-DD`, `DD/MM/YYYY`, `DD-MM-YYYY`) into ISO-8601 `YYYY-MM-DD`.
* **PII Pseudonymization & Masking (Criterion D4):**
  * Phone numbers are masked for downstream reporting: `0901234567` $\to$ `0901***567`.
  * Email addresses are pseudonymized: `trungbao@gmail.com` $\to$ `t***@gmail.com`.
  * Evaluated leakage rate is strictly **$0.00\%$** (verified in test TC-07).

---

## 4. Multidimensional Quality Measurement (`src/quality/checks.py`)

The pipeline quantitatively calculates **9 distinct measures** across 3 data quality dimensions, comparing every result against benchmark thresholds configured in `configs/config.example.yaml`:

| Dimension | Measured Metric | Total Evaluated | Passed Records | Error Records | Pass Rate | Threshold | Evaluation |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | :---: |
| **Completeness** | `customer_id` Presence | 67,037 | 67,037 | 0 | 100.00% | $\ge 100.0\%$ | **PASS** |
| **Completeness** | `ho_ten` Presence | 67,037 | 67,037 | 0 | 100.00% | $\ge 98.0\%$ | **PASS** |
| **Completeness** | `so_dien_thoai` Presence | 67,037 | 62,904 | 4,133 | 93.83% | $\ge 90.0\%$ | **PASS** |
| **Accuracy** | Phone Formatting Validity | 67,037 | 62,904 | 4,133 | 93.83% | $\ge 90.0\%$ | **PASS** |
| **Accuracy** | Name Normalization Ratio | 67,037 | 67,037 | 0 | 100.00% | $\ge 95.0\%$ | **PASS** |
| **Accuracy** | Email Syntax Validity | 67,037 | 64,710 | 2,327 | 96.53% | $\ge 85.0\%$ | **PASS** |
| **Accuracy** | Registration Date Validity | 67,037 | 65,850 | 1,187 | 98.23% | $\ge 95.0\%$ | **PASS** |
| **Consistency** | Duplicate Customer Detection | 62,904 | 35,781 | 27,123 | 43.12% | $\le 70.0\%$ | **PASS** |
| **Consistency** | Carrier Area Code Uniformity | 67,037 | 62,904 | 4,133 | 93.83% | $\ge 90.0\%$ | **PASS** |

---

## 5. Storage Strategy & Reject Breakdown (`src/load/`)

### 5.1 Dimensional Star Schema
* **Clean Data Routing:** 62,904 cleaned records ($93.83\%$) are loaded into `dim_customer` and audited per rule in `fact_customer_quality_audit`.
* **Idempotency Guarantee:** Batch sessions are identified by deterministic keys (`batch_id = 'lo-toan-bo'`). Re-running updates `dim_audit_run` in-place, eliminating duplicate rows upon successive runs.

### 5.2 Breakdown of Discarded Rows (Matching Latest Audit Run Exactly)
* **Total Discarded Records:** Exactly **4,133 rows** ($6.17\%$ of input data).
* **Breakdown by Specific Rule Code:**
  * **`DQ02_PHONE`:** Exactly **4,133 rows** ($100.0\%$ of all rejections).
  * *Reason:* Phone numbers contained alphabetical characters, irregular length ($< 10$ or $> 11$ digits), or obsolete carrier prefixes that could not be deterministically standardized.
* **Auditability:** Every discarded row is preserved in `reject_rows` with raw values and the human-readable explanation: `"DQ02_PHONE: Số điện thoại không đúng định dạng 10 số di động VN"`.
* **Data Conservation Proof:**
  $$\text{Staging (67,037)} = \text{Fact/Dim (62,904)} + \text{Reject Rows (4,133)} \quad (\text{Net Loss} = 0)$$

---

## 6. Technical Limitations & Business Impact (Hạn chế kỹ thuật & Ảnh hưởng nghiệp vụ)

Documenting technical constraints alongside their direct business impact is essential for data governance and operational planning:

### Limitation 1: Batch-Oriented Offline Ingestion
* **Technical Constraint:** The current pipeline executes as an offline batch process triggered on demand or via schedule (hourly/daily), rather than an event-driven streaming pipeline (e.g., Kafka / Flink).
* **Business Impact:** Customer registrations or profile updates at Mekong Mobile retail kiosks have a synchronization latency of several hours before reaching the central analytics warehouse. Consequently, the automated CRM engine cannot send real-time personalized welcome offers or point-redemption vouchers immediately after a customer leaves the physical counter.

### Limitation 2: Exact-Match Duplicate Detection Algorithm
* **Technical Constraint:** Deduplication in `src/quality/checks.py` relies on exact string equality on phone number OR email address. It lacks fuzzy string distance matching (e.g., Levenshtein distance, Jaro-Winkler) for customer names and physical addresses.
* **Business Impact:** While 27,123 duplicate records ($43.1\%$) are accurately flagged via exact phone/email matching, customers who typo'd their email (e.g., `user@gmial.com` vs `user@gmail.com`) or registered with alternative phone numbers are treated as distinct individuals. This results in slight customer fragmentation and occasional duplicate promotional SMS broadcasts.

### Limitation 3: Manual Review Dependency for Rejected Records
* **Technical Constraint:** All 4,133 invalid records are quarantined in `reject_rows`. The pipeline does not feature automated external lookup (e.g., telco carrier verification API) to repair corrupt phone numbers automatically.
* **Business Impact:** These 4,133 customers ($6.17\%$ of total customer base) are temporarily excluded from loyalty tier calculations and marketing automation until a data steward manually inspects the reject table and updates customer profiles via tele-sales confirmation.
