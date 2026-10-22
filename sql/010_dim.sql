-- Bảng chiều (Dimension Tables) trong mô hình Star Schema cho Luồng L7

-- 1. Bảng chiều khách hàng
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    ho_ten_raw VARCHAR(255),
    ho_ten_clean VARCHAR(255) NOT NULL,
    so_dien_thoai_raw VARCHAR(50),
    so_dien_thoai_clean VARCHAR(20) NOT NULL,
    email_raw VARCHAR(255),
    email_clean VARCHAR(255),
    dia_chi VARCHAR(255),
    ngay_dang_ky DATE,
    thoi_gian_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_dim_customer_phone ON dim_customer(so_dien_thoai_clean);
CREATE INDEX IF NOT EXISTS idx_dim_customer_email ON dim_customer(email_clean);

-- 2. Bảng chiều quy tắc chất lượng
CREATE TABLE IF NOT EXISTS dim_quality_rule (
    rule_key INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_code VARCHAR(20) UNIQUE NOT NULL,
    rule_name VARCHAR(100) NOT NULL,
    dimension_name VARCHAR(50) NOT NULL,
    nguong_chuan REAL NOT NULL,
    mo_ta TEXT
);

-- 3. Bảng chiều phiên chạy kiểm định
CREATE TABLE IF NOT EXISTS dim_audit_run (
    run_key INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id VARCHAR(50) UNIQUE NOT NULL,
    run_date TIMESTAMP NOT NULL,
    total_records INTEGER NOT NULL,
    run_by VARCHAR(100) NOT NULL
);
