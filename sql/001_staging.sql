-- Bảng Staging lưu trữ dữ liệu khách hàng thô được nạp từ tập tin customers_raw.csv
-- Mục đích: Lưu trữ toàn bộ dữ liệu nguồn, phục vụ kiểm tra và làm sạch mà không sửa đổi file gốc.

CREATE TABLE IF NOT EXISTS staging_customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    ho_ten VARCHAR(255),
    so_dien_thoai VARCHAR(50),
    email VARCHAR(255),
    dia_chi VARCHAR(255),
    ngay_dang_ky VARCHAR(50),
    thoi_gian_nap TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_staging_batch_id ON staging_customers(batch_id);
CREATE INDEX IF NOT EXISTS idx_staging_customer_id ON staging_customers(customer_id);
