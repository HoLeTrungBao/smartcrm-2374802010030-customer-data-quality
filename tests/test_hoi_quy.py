"""TEST HỒI QUY (REGRESSION TESTS) CHO CÁC BUG ĐÃ SỬA

Bảo đảm các lỗi kỹ thuật đã phát hiện và xử lý không bị tái phát:
  - HQ-01: Hồi quy BUG-01 (Tính Idempotent: mã lô xác định theo phạm vi dữ liệu, chạy lại không lỗi Foreign Key).
  - HQ-02: Hồi quy BUG-02 (Hợp đồng dữ liệu nguồn: tự động ánh xạ linh hoạt tên cột record_id và ngay_tao).
  - HQ-03: Hồi quy BUG-03 (Truy vấn CSDL: sử dụng đúng tên cột thoi_gian_tao trong bảng reject_rows).
"""
import sqlite3
import pathlib
import pytest
import pandas as pd
from src.pipeline import sinh_ma_lo
from src.transform.clean_customers import xu_ly_lam_sach_khach_hang
from src.dashboard.bieu_do import bieu_do_loi_dq


# ============================================================================
# HQ-01: HỒI QUY BUG-01 — TÍNH XÁC ĐỊNH CỦA MÃ LÔ ĐẢM BẢO IDEMPOTENT
# ============================================================================
def test_hq01_sinh_ma_lo_xac_dinh():
    """Hồi quy BUG-01: sinh_ma_lo phải trả về cùng kết quả khi gọi nhiều lần

    với cùng tham số, không được dùng datetime ngẫu nhiên gây phình to bảng staging/reject.
    """
    assert sinh_ma_lo() == 'lo-toan-bo'
    assert sinh_ma_lo() == 'lo-toan-bo'
    assert sinh_ma_lo('2025-01-01', '2025-12-31') == 'lo-2025-01-01_2025-12-31'
    assert sinh_ma_lo('2025-01-01', '2025-12-31') == 'lo-2025-01-01_2025-12-31'


# ============================================================================
# HQ-02: HỒI QUY BUG-02 — TỰ ĐỘNG ÁNH XẠ LINH HOẠT TÊN CỘT NGUỒN CSV
# ============================================================================
def test_hq02_anh_xa_cot_nguon_record_id_ngay_tao():
    """Hồi quy BUG-02: Pipeline phải xử lý trơn tru cả hai biến thể tên cột

    (record_id / customer_id và ngay_tao / ngay_dang_ky) mà không văng KeyError.
    """
    df_bien_the = pd.DataFrame([
        {
            'record_id': 'REC001',
            'ho_ten': 'Nguyễn Văn An',
            'so_dien_thoai': '0901234567',
            'email': 'an@gmail.com',
            'dia_chi': 'TP.HCM',
            'ngay_tao': '2025-05-15'
        }
    ])
    df_sach, df_reject = xu_ly_lam_sach_khach_hang(df_bien_the)

    assert len(df_sach) == 1
    assert len(df_reject) == 0
    assert 'customer_id' in df_sach.columns
    assert df_sach.iloc[0]['customer_id'] == 'REC001'
    assert df_sach.iloc[0]['so_dien_thoai_clean'] == '0901234567'


# ============================================================================
# HQ-03: HỒI QUY BUG-03 — TRUY VẤN ĐÚNG CỘT THỜI GIAN TRONG REJECT_ROWS
# ============================================================================
def test_hq03_truy_van_dung_cot_thoi_gian_tao(tmp_path: pathlib.Path):
    """Hồi quy BUG-03: bieu_do_loi_dq phải truy vấn bằng cột thoi_gian_tao

    (theo đúng DDL 002_reject.sql), không được gọi cột ngay_nap gây OperationalError.
    """
    db_path = tmp_path / 'test_hq03.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    conn.execute("""
        CREATE TABLE reject_rows (
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
    """)
    conn.execute("""
        CREATE TABLE staging_customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id VARCHAR(50)
        );
    """)
    conn.execute("INSERT INTO staging_customers (batch_id) VALUES ('lo-test');")
    conn.execute("""
        INSERT INTO reject_rows (batch_id, customer_id, ma_quy_tac, ly_do_loi, thoi_gian_tao)
        VALUES ('lo-test', 'CUS01', 'DQ02_PHONE', 'Lỗi SĐT', '2025-05-15 10:00:00');
    """)
    conn.commit()

    anh_dich = tmp_path / 'test_bieu_do_hq03.png'
    # Gọi với tham số lọc ngày - nếu truy vấn nhầm ngay_nap sẽ bị bắt lỗi
    ket_qua = bieu_do_loi_dq(conn, anh_dich, tu_ngay='2025-01-01', den_ngay='2025-12-31')
    assert ket_qua.exists()
    assert ket_qua.stat().st_size > 0
    conn.close()
