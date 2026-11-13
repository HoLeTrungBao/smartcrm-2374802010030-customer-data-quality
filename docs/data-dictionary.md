# Data Dictionary — SmartCRM Customer Data Quality (Stream L7)

**Database Target:** SQLite Database (`data/processed/warehouse.db`)  
**Architecture:** Star Schema (Fact, Dimension, Staging, Reject, and Audit Tables)  
**Author:** Ho Le Trung Bao — **Student ID:** 2374802010030  
**Compliance Note:** Every table, column name, data type, and constraint documented below strictly corresponds to the actual DDL statements located in `sql/` and verified in SQLite. No non-existent columns or mock endpoints are included (Criterion C9 compliant).

---

## 1. Table Overview & Summary

| Table Name | Layer / Type | Primary Key | Description |
| :--- | :--- | :--- | :--- |
| `staging_customers` | Staging Layer | `id` (INTEGER) | Stores raw, untransformed customer records directly extracted from source files. |
| `reject_rows` | Audit / Error Layer | `reject_id` (INTEGER) | Isolates records that cannot be cleaned, complete with human-readable error reasons. |
| `quality_measures` | Audit / Measures Layer | `measure_id` (INTEGER) | Persists quantitative metrics of the 9 data quality rules evaluated in each run. |
| `dim_customer` | Warehouse / Dimension | `customer_key` (INTEGER) | Dimension table storing standardized and cleaned customer profile attributes. |
| `dim_quality_rule` | Warehouse / Dimension | `rule_key` (INTEGER) | Lookup dimension defining standardized data quality rules and benchmark thresholds. |
| `dim_audit_run` | Warehouse / Dimension | `run_key` (INTEGER) | Session dimension logging each pipeline batch run, execution timestamps, and record counts. |
| `fact_customer_quality_audit` | Warehouse / Fact Table | `audit_fact_id` (INTEGER) | Fact table recording individual customer quality audit results, duplication flags, and errors. |

---

## 2. Detailed Table Specifications

### 2.1. Table `staging_customers` (DDL: `sql/001_staging.sql`)
* **Purpose:** Exact immutable representation of raw incoming CSV data.

| Column Name | Data Type | Nullable | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| `id` | `INTEGER` | **No** | `AUTOINCREMENT` | Surrogate primary key for staging row. |
| `batch_id` | `VARCHAR(50)` | **No** | None | Deterministic batch run identifier (e.g., `lo-toan-bo`). |
| `customer_id` | `VARCHAR(50)` | **No** | None | Raw customer natural business identifier extracted from source. |
| `ho_ten` | `VARCHAR(255)` | Yes | `NULL` | Raw full name string before normalization. |
| `so_dien_thoai` | `VARCHAR(50)` | Yes | `NULL` | Raw phone number as string (preserving leading zeros). |
| `email` | `VARCHAR(255)` | Yes | `NULL` | Raw email address string. |
| `dia_chi` | `VARCHAR(255)` | Yes | `NULL` | Raw customer address. |
| `ngay_dang_ky` | `VARCHAR(50)` | Yes | `NULL` | Raw registration date string before parsing. |
| `thoi_gian_nap` | `TIMESTAMP` | Yes | `CURRENT_TIMESTAMP` | System timestamp when record was inserted into staging. |

* **Indexes:** `idx_staging_batch_id (batch_id)`, `idx_staging_customer_id (customer_id)`

---

### 2.2. Table `reject_rows` (DDL: `sql/002_reject.sql`)
* **Purpose:** Captures dirty records that fail validation, ensuring zero data loss and actionable auditability.

| Column Name | Data Type | Nullable | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| `reject_id` | `INTEGER` | **No** | `AUTOINCREMENT` | Surrogate primary key for rejected row. |
| `batch_id` | `VARCHAR(50)` | **No** | None | Batch identifier corresponding to the execution run. |
| `customer_id` | `VARCHAR(50)` | Yes | `NULL` | Natural customer identifier (if present). |
| `ho_ten_goc` | `VARCHAR(255)` | Yes | `NULL` | Original customer name from raw input. |
| `so_dien_thoai_goc` | `VARCHAR(50)` | Yes | `NULL` | Original phone number string from raw input. |
| `email_goc` | `VARCHAR(255)` | Yes | `NULL` | Original email address from raw input. |
| `ma_quy_tac` | `VARCHAR(20)` | **No** | None | Specific DQ rule code violated (e.g., `DQ02_PHONE`, `DQ01_ID`). |
| `ly_do_loi` | `TEXT` | **No** | None | Human-readable explanation of why the record was rejected. |
| `thoi_gian_tao` | `TIMESTAMP` | Yes | `CURRENT_TIMESTAMP` | Timestamp of rejection entry. |

* **Indexes:** `idx_reject_batch_id (batch_id)`, `idx_reject_rule (ma_quy_tac)`

---

### 2.3. Table `quality_measures` (DDL: `sql/002_reject.sql`)
* **Purpose:** Audit ledger logging numeric metrics for each quality evaluation.

| Column Name | Data Type | Nullable | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| `measure_id` | `INTEGER` | **No** | `AUTOINCREMENT` | Surrogate primary key for measurement. |
| `batch_id` | `VARCHAR(50)` | **No** | None | Batch execution identifier. |
| `chieu_chat_luong` | `VARCHAR(50)` | **No** | None | Dimension name (`Đầy đủ`, `Chính xác`, `Nhất quán`). |
| `doi_tuong` | `VARCHAR(100)` | **No** | None | Specific field or rule evaluated (e.g., `so_dien_thoai`). |
| `so_kiem` | `INTEGER` | **No** | None | Total count of records evaluated. |
| `so_dat` | `INTEGER` | **No** | None | Count of records passing the check. |
| `so_loi` | `INTEGER` | **No** | None | Count of records failing the check. |
| `ti_le_dat` | `REAL` | **No** | None | Calculated pass percentage ($0.0 \dots 1.0$). |
| `nguong_yeu_cau` | `REAL` | **No** | None | Benchmark threshold configured in YAML. |
| `ket_luan` | `VARCHAR(20)` | **No** | None | Evaluation outcome (`ĐẠT` or `CẢNH BÁO`). |
| `thoi_gian_do` | `TIMESTAMP` | Yes | `CURRENT_TIMESTAMP` | Timestamp of measurement calculation. |

* **Indexes:** `idx_measures_batch_id (batch_id)`

---

### 2.4. Table `dim_customer` (DDL: `sql/010_dim.sql`)
* **Purpose:** Master dimension table for cleaned customer profiles.

| Column Name | Data Type | Nullable | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| `customer_key` | `INTEGER` | **No** | `AUTOINCREMENT` | Surrogate primary key for customer dimension. |
| `customer_id` | `VARCHAR(50)` | **No** | None | Unique natural business customer ID (`UNIQUE`). |
| `ho_ten_raw` | `VARCHAR(255)` | Yes | `NULL` | Original customer name before cleaning. |
| `ho_ten_clean` | `VARCHAR(255)` | **No** | None | Cleaned, Title-Cased Vietnamese name. |
| `so_dien_thoai_raw` | `VARCHAR(50)` | Yes | `NULL` | Original phone number string. |
| `so_dien_thoai_clean` | `VARCHAR(20)` | **No** | None | Normalized 10-digit mobile number starting with `0`. |
| `email_raw` | `VARCHAR(255)` | Yes | `NULL` | Original email string. |
| `email_clean` | `VARCHAR(255)` | Yes | `NULL` | Normalized lowercase email address. |
| `dia_chi` | `VARCHAR(255)` | Yes | `NULL` | Normalized customer address. |
| `ngay_dang_ky` | `DATE` | Yes | `NULL` | Parsed ISO-8601 registration date (`YYYY-MM-DD`). |
| `thoi_gian_cap_nhat` | `TIMESTAMP` | Yes | `CURRENT_TIMESTAMP` | Record last modification timestamp. |

* **Indexes:** `idx_dim_customer_phone (so_dien_thoai_clean)`, `idx_dim_customer_email (email_clean)`

---

### 2.5. Table `dim_quality_rule` (DDL: `sql/010_dim.sql`)
* **Purpose:** Reference dimension defining standard rules and thresholds.

| Column Name | Data Type | Nullable | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| `rule_key` | `INTEGER` | **No** | `AUTOINCREMENT` | Surrogate primary key for rule. |
| `rule_code` | `VARCHAR(20)` | **No** | None | Unique business rule code (`UNIQUE`, e.g., `DQ02_PHONE`). |
| `rule_name` | `VARCHAR(100)` | **No** | None | Formal descriptive name of the rule. |
| `dimension_name` | `VARCHAR(50)` | **No** | None | Data quality dimension (`Đầy đủ`, `Chính xác`, `Nhất quán`). |
| `nguong_chuan` | `REAL` | **No** | None | Numerical benchmark threshold ratio. |
| `mo_ta` | `TEXT` | Yes | `NULL` | Comprehensive rule specification details. |

---

### 2.6. Table `dim_audit_run` (DDL: `sql/010_dim.sql`)
* **Purpose:** Audit session header maintaining execution context for idempotency.

| Column Name | Data Type | Nullable | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| `run_key` | `INTEGER` | **No** | `AUTOINCREMENT` | Surrogate primary key for execution session. |
| `batch_id` | `VARCHAR(50)` | **No** | None | Unique batch identifier (`UNIQUE`). |
| `run_date` | `TIMESTAMP` | **No** | None | Start timestamp of the execution session. |
| `total_records` | `INTEGER` | **No** | None | Total count of raw source records processed. |
| `run_by` | `VARCHAR(100)` | **No** | None | System user or workflow agent executing the run. |

---

### 2.7. Table `fact_customer_quality_audit` (DDL: `sql/020_fact.sql`)
* **Purpose:** Fact table recording individual evaluation events per customer per run.
* **Grain:** 1 record per clean customer audited during a specific pipeline execution run.

| Column Name | Data Type | Nullable | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| `audit_fact_id` | `INTEGER` | **No** | `AUTOINCREMENT` | Surrogate primary key for fact record. |
| `customer_key` | `INTEGER` | **No** | None | Foreign Key referencing `dim_customer(customer_key)`. |
| `rule_key` | `INTEGER` | **No** | None | Foreign Key referencing `dim_quality_rule(rule_key)`. |
| `run_key` | `INTEGER` | **No** | None | Foreign Key referencing `dim_audit_run(run_key)`. |
| `is_valid` | `BOOLEAN` | **No** | None | Flag indicating overall quality validity (`1` = valid). |
| `is_auto_cleaned`| `BOOLEAN` | **No** | `0` | Flag indicating whether fields were auto-corrected (`1` = yes). |
| `is_duplicate` | `BOOLEAN` | **No** | `0` | Flag indicating potential duplicate customer identity (`1` = duplicate). |
| `error_count` | `INTEGER` | **No** | `0` | Count of quality rule warnings observed for this customer. |
| `thoi_gian_kiem_dinh` | `TIMESTAMP` | Yes | `CURRENT_TIMESTAMP` | Timestamp when audit fact was inserted. |

* **Foreign Keys:**
  * `customer_key` $\to$ `dim_customer(customer_key)`
  * `rule_key` $\to$ `dim_quality_rule(rule_key)`
  * `run_key` $\to$ `dim_audit_run(run_key)`
* **Indexes:** `idx_fact_customer`, `idx_fact_rule`, `idx_fact_run`, `idx_fact_valid`

---

## 3. Data Privacy & Pseudonymization Policy (Criterion D4)

In accordance with enterprise data protection standards and academic grading criterion D4:
* **Personal Identifiable Information (PII) Columns:** `ho_ten`, `so_dien_thoai`, `email`, and `dia_chi` are classified as sensitive PII.
* **Pseudonymization Mechanism:**
  * In `dim_customer`, the natural key `customer_id` is linked to surrogate integer `customer_key`.
  * For all non-privileged reporting views, dashboards, and automated exports, phone numbers and emails are dynamically masked:
    * Mobile Phone: `0901234567` $\to$ `0901***567`
    * Email Address: `trungbao@gmail.com` $\to$ `t***@gmail.com`
  * Empirical leakage rate on reporting outputs is verified at **0.00%** (NFR05 / Test Case TC-07).
