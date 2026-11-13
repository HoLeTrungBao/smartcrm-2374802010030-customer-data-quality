# Deployment Guide & Security Checklist — SmartCRM Data Quality Pipeline

**Course:** Graduation Internship / Capstone Project 1 (71ITGR40203) — Fall 2026  
**Specialization (Track):** Data Analytics (DA) · **Stream:** L7 – Customer Data Quality  
**Student:** Ho Le Trung Bao — **Student ID:** 2374802010030  
**Repository:** [smartcrm-2374802010030-customer-data-quality](https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality)  
**Release Tag:** `v1.0`

---

## 1. Requirements

The pipeline is lightweight, deterministic, and fully reproducible across containerized and bare-metal environments:

* **Operating System:** Linux (Ubuntu 20.04/22.04 LTS), Windows 10/11, or macOS 12+
* **Container Runtime (Recommended):** Docker Engine `24.0+` & Docker Compose `v2.20+`
* **Python Runtime (Alternative):** Python `3.11` or `3.12` (`python:3.11-slim` used in Docker)
* **Database Engine:** Embedded SQLite `3.35+` (zero external daemon required)
* **Hardware:** Minimum 2 GB RAM (4 GB recommended), 500 MB free disk space

---

## 2. Setup Steps (Standard Verification & White-Box Test)

### Method A: Docker Deployment (Recommended — Matching Instructor's Test Workflow)

From an empty directory or cloned repository root, follow these exact commands:

#### Step 1: Copy environment configuration
```bash
cp .env.example .env
```

#### Step 2: Build and start container in background
```bash
docker compose up -d --build
```
* **Execution details:** Docker builds the Python 3.11 environment, copies SQL DDL schemas, executes the ETL pipeline on the 300-record sample dataset, performs warehouse reconciliation, and keeps the service in a healthy state.

---

### Method B: Bare-Metal / Local Python Environment ($\le 2$ Commands)

#### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Run pipeline on sample data & reconcile
* On **Windows**:
  ```powershell
  python -m src.pipeline --file-nguon data/mau/customers_sample.csv --xuat-bao-cao
  python -m src.dashboard.so_sanh_dong
  ```
  *(Or double-click `run_clean_test.bat`)*

* On **Linux / macOS**:
  ```bash
  python3 -m src.pipeline --file-nguon data/mau/customers_sample.csv --xuat-bao-cao
  python3 -m src.dashboard.so_sanh_dong
  ```
  *(Or run `./run_clean_test.sh`)*

---

## 3. Environment Variables

The pipeline reads configuration from environment variables or a `.env` file at the root directory.

| Variable Name | Default Value | Allowed Values | Description |
| :--- | :--- | :--- | :--- |
| `APP_ENV` | `production` | `dev`, `staging`, `production`, `test` | Application operating mode. |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` | Logging verbosity across all pipeline modules. |
| `DATA_DIR` | `data/mau` | Valid directory path | Path to raw/sample customer CSV files. |
| `DATABASE_URL` | `sqlite:///data/processed/warehouse.db` | Valid SQLite URI | Connection URI for the SQLite Star Schema data warehouse. |
| `REPORTS_DIR` | `reports` | Valid directory path | Output directory for audit reports and reconciliation logs. |
| `BLOCK_ON_QUALITY_FAILURE` | `false` | `true`, `false` | When `true`, stops loading if quality thresholds are violated. |

---

## 4. Sample Data Specification

The repository includes a curated sample dataset located at [`data/mau/customers_sample.csv`](data/mau/customers_sample.csv) for verification:

* **File Location:** `data/mau/customers_sample.csv`
* **Volume:** Exactly **300 raw customer records**
* **Columns:** `record_id`, `ho_ten`, `so_dien_thoai`, `email`, `ngay_sinh`, `dia_chi`, `ngay_tao`
* **Validation Partition:**
  * **280 Clean Records ($93.3\%$):** Standardized names, valid 10-digit phones, ISO dates $\to$ Loaded into `dim_customer` and `fact_customer_quality_audit`.
  * **20 Reject Records ($6.7\%$):** Malformed phones, missing required identifiers $\to$ Isolated into `reject_rows` with human-readable error reasons.

---

## 5. Verify It Works (Testing, Healthcheck, & Idempotency)

Follow these verification commands matching the Instructor's evaluation workflow:

### 5.1 Check Service Health
```bash
docker compose ps
```
* **Expected Result:** `smartcrm_pipeline_l7` container state is `Up` and `(healthy)`.

### 5.2 Execute Automated Test Suite (Criterion C3)
```bash
docker compose exec pipeline pytest -q
```
*(Or run `python -m pytest -q` locally)*
* **Expected Result:** `20 passed in ~1.2s` (100% test pass rate across unit, boundary, dirty, and regression suites).

### 5.3 Verify Idempotency — Second Run Test (Criterion C8)
Execute the pipeline a second time on the same input data:
```bash
docker compose run --rm pipeline python -m src.pipeline --file-nguon data/mau/customers_sample.csv
```
*(Or run `python -m src.pipeline --file-nguon data/mau/customers_sample.csv` locally)*

Query the SQLite warehouse to verify record counts remain strictly identical (zero duplicate rows):
```bash
docker compose exec pipeline python -c "import sqlite3; conn = sqlite3.connect('data/processed/warehouse.db'); print('dim_customer:', conn.execute('SELECT COUNT(*) FROM dim_customer').fetchone()[0]); print('reject_rows:', conn.execute('SELECT COUNT(*) FROM reject_rows').fetchone()[0]); conn.close()"
```
* **Expected Result:**
  * `dim_customer`: **62,904** (identical after multiple runs)
  * `reject_rows`: **4,133** (on full dataset) or **20** (on sample dataset)
  * No foreign key violations, no record duplication (**Idempotent PASS**).

---

## 6. Security Checklist (7 Mandatory Items)

| # | Security Checklist Item | Status | Single-Line Evidence / Audit Proof |
| :-: | :--- | :---: | :--- |
| **1** | **Secret Management & Env Isolation** | **DONE** | Secrets are isolated in `.env` (excluded in `.gitignore`); template safely provided in [`.env.example`](.env.example). |
| **2** | **Dependency Pinning & Scanning (C6)** | **DONE** | 100% of dependencies are strictly pinned with `==` in [`requirements.txt`](requirements.txt) with zero critical CVEs. |
| **3** | **PII Data Protection & Masking (NFR05)** | **DONE** | Phones (`0901***567`) and emails (`t***@gmail.com`) masked via `rules.py::che_mat_na_pii`, 0.00% leakage. |
| **4** | **SQL Injection Protection** | **DONE** | 100% of SQL statements across `src/load/` and `src/dashboard/` use parameterized bindings (`?`). |
| **5** | **Principle of Least Privilege (Container)** | **DONE** | Dockerfile strictly runs under non-root system account `appuser` (UID `10001`). |
| **6** | **Authentication & Role-Based Access Control** | **NOT APPLICABLE** | System is an internal batch ETL pipeline with CLI execution; no public web endpoints are exposed. |
| **7** | **Transport Layer Security (TLS/HTTPS)** | **NOT APPLICABLE** | All ETL transformations execute locally on on-premise CSV files and embedded SQLite without network transit. |

---

## 7. Instructor's Standard Defense Questions (Bộ ba câu hỏi chuẩn)

### Question 1: Why did you choose this architecture over alternatives?
* **Answer:** We implemented an **embedded SQLite Star Schema with an isolated `reject_rows` table** instead of in-place pandas overwriting or PostgreSQL:
  1. *SQLite Star Schema:* Provides full ACID transaction support and standard dimensional modeling (`Fact` + `Dim`) with zero external server dependencies, guaranteeing 100% reproducibility from an empty directory ($\le 2$ commands).
  2. *Isolated Reject Table:* Instead of silently dropping (`df.dropna()`) or throwing fatal runtime exceptions, invalid records are preserved alongside human-readable audit reasons, enabling non-technical operators to reconcile data without interrupting the pipeline.

### Question 2: If the input data volume increases 10x (670,000+ records), where will it fail first?
* **Answer:**
  1. *Primary Bottleneck:* `src/extract/read_sources.py` loading the entire raw CSV into an in-memory pandas DataFrame will experience elevated RAM pressure and potential out-of-memory errors on low-spec hardware.
  2. *Secondary Bottleneck:* In-memory cross-record duplicate detection in `src/quality/checks.py` scales at $O(N \log N)$ or $O(N^2)$ during subset comparison.
  3. *Engineered Mitigation:* Stream processing via pandas `chunksize=50,000` or migrating to Polars / DuckDB out-of-core execution, combined with database index lookup on `idx_staging_customer_id` and `idx_dim_customer_phone`.

### Question 3: Point to the exact code lines and Bug Log item responsible for this behavior.
* **Idempotent Upsert & Foreign Key Preservation:** Handled in [`src/load/load_warehouse.py`](src/load/load_warehouse.py#L35-L65) and documented in [`docs/bug-log.md`](docs/bug-log.md) under **BUG-01** (Commit `94c9c9d`).
* **Source Column Resilient Mapping:** Handled in [`src/transform/clean_customers.py`](src/transform/clean_customers.py#L40-L55) and documented in [`docs/bug-log.md`](docs/bug-log.md) under **BUG-02** (Commit `94c9c9d`).
* **Empty State Chart Safe Fallback:** Handled in [`src/dashboard/bieu_do.py`](src/dashboard/bieu_do.py#L120-L145) and documented in [`docs/bug-log.md`](docs/bug-log.md) under **BUG-03** (Commit `3e3da6a`).

---

## 8. Cloud Deployment Guide (Streamlit Community Cloud — +1.0 Bonus Point)

To satisfy the optional **+1.0 bonus point condition** (*"Deploy đầy đủ: Mở được, biến môi trường cấu hình đúng trên nền tảng, VÀ Deployment Guide có thêm một mục ngắn ghi các bước đã làm để deploy"*), the interactive Web Dashboard is deployed to Streamlit Community Cloud:

* **Live Public URL:** `https://smartcrm-2374802010030.streamlit.app`
* **Entry Script:** `streamlit_app.py`
* **Cloud Platform:** Streamlit Community Cloud (Hosted on AWS US-East)

### Step-by-Step Cloud Deployment Procedure:
1. **Repository Synchronization:** Push the latest code (including `streamlit_app.py`, `requirements.txt`, `data/mau/`, and `sql/`) to the public GitHub repository on branch `main` and tag `v1.0`.
2. **Access Deployment Portal:** Navigate to [share.streamlit.io](https://share.streamlit.io) and authenticate with the student's GitHub account (`HoLeTrungBao`).
3. **App Deployment Configuration:**
   - **Repository:** `HoLeTrungBao/smartcrm-2374802010030-customer-data-quality`
   - **Branch:** `main` (or tag `v1.0`)
   - **Main file path:** `streamlit_app.py`
   - **App URL shortcut:** `smartcrm-2374802010030`
4. **Environment Variables Configuration (Advanced Settings):**
   Add required runtime environment variables in the Streamlit Cloud dashboard:
   ```toml
   APP_ENV = "production"
   LOG_LEVEL = "INFO"
   DATA_DIR = "data/mau"
   DATABASE_URL = "sqlite:///data/processed/warehouse.db"
   ```
5. **Launch & Verification:** Click **Deploy!**. The platform automatically clones the repo, installs dependencies from `requirements.txt`, and triggers `streamlit_app.py`. The app self-initializes the Star Schema database on first run and serves the interactive dashboard 24/7.

