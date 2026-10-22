-- Bảng sự kiện (Fact Table) trong mô hình Star Schema cho Luồng L7
-- Grain: Mỗi dòng đại diện cho kết quả đánh giá 1 quy tắc kiểm định đối với 1 khách hàng trong 1 phiên chạy

CREATE TABLE IF NOT EXISTS fact_customer_quality_audit (
    audit_fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_key INTEGER NOT NULL,
    rule_key INTEGER NOT NULL,
    run_key INTEGER NOT NULL,
    is_valid BOOLEAN NOT NULL,
    is_auto_cleaned BOOLEAN NOT NULL DEFAULT 0,
    is_duplicate BOOLEAN NOT NULL DEFAULT 0,
    error_count INTEGER NOT NULL DEFAULT 0,
    thoi_gian_kiem_dinh TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (rule_key) REFERENCES dim_quality_rule(rule_key),
    FOREIGN KEY (run_key) REFERENCES dim_audit_run(run_key)
);

CREATE INDEX IF NOT EXISTS idx_fact_customer ON fact_customer_quality_audit(customer_key);
CREATE INDEX IF NOT EXISTS idx_fact_rule ON fact_customer_quality_audit(rule_key);
CREATE INDEX IF NOT EXISTS idx_fact_run ON fact_customer_quality_audit(run_key);
CREATE INDEX IF NOT EXISTS idx_fact_valid ON fact_customer_quality_audit(is_valid);
