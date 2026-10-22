-- Bảng Reject lưu trữ các dòng không thể tự động làm sạch kèm lý do chi tiết cho người đọc
-- Bảng Quality Measures lưu kết quả định lượng của các phép đo chất lượng qua từng phiên chạy

CREATE TABLE IF NOT EXISTS reject_rows (
    reject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50),
    ho_ten_goc VARCHAR(255),
    so_dien_thoai_goc VARCHAR(50),
    email_goc VARCHAR(255),
    ma_quy_tac VARCHAR(20) NOT NULL,
    ly_do_loi TEXT NOT NULL,
    thoi_gian_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reject_batch_id ON reject_rows(batch_id);
CREATE INDEX IF NOT EXISTS idx_reject_rule ON reject_rows(ma_quy_tac);

CREATE TABLE IF NOT EXISTS quality_measures (
    measure_id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id VARCHAR(50) NOT NULL,
    chieu_chat_luong VARCHAR(50) NOT NULL,
    doi_tuong VARCHAR(100) NOT NULL,
    so_kiem INTEGER NOT NULL,
    so_dat INTEGER NOT NULL,
    so_loi INTEGER NOT NULL,
    ti_le_dat REAL NOT NULL,
    nguong_yeu_cau REAL NOT NULL,
    ket_luan VARCHAR(20) NOT NULL,
    thoi_gian_do TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_measures_batch_id ON quality_measures(batch_id);
