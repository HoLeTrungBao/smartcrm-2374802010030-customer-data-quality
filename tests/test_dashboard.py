"""KIỂM THỬ ĐƠN VỊ MODULE DASHBOARD (src/dashboard/)

Kiểm tra:
  - Đếm dòng staging vs fact đúng
  - Biểu đồ tạo thành công trả về file ảnh hợp lệ
  - BIÊN: Bộ lọc ngày không có dữ liệu → hàm trả về ảnh placeholder, không crash
"""
import sqlite3
import pathlib
import pytest
from unittest.mock import patch

from src.dashboard.so_sanh_dong import dem_dong_cac_bang, giai_thich_chenh_lech
from src.dashboard.bieu_do import _tao_hinh_thong_bao, bieu_do_loi_dq, bieu_do_trung_lap


@pytest.fixture
def db_kiem_thu(tmp_path: pathlib.Path):
    """Tạo CSDL SQLite tạm với cấu trúc và dữ liệu mẫu để kiểm thử."""
    db_path = tmp_path / 'test_warehouse.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    # Tạo bảng staging
    conn.execute("""
        CREATE TABLE staging_customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT, customer_id TEXT, ho_ten TEXT,
            so_dien_thoai TEXT, email TEXT, dia_chi TEXT, ngay_dang_ky TEXT
        );
    """)

    # Tạo bảng reject
    conn.execute("""
        CREATE TABLE reject_rows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT, customer_id TEXT, ho_ten_goc TEXT,
            so_dien_thoai_goc TEXT, email_goc TEXT, ma_quy_tac TEXT, ly_do_loi TEXT
        );
    """)

    # Tạo bảng dim
    conn.execute("""
        CREATE TABLE dim_customer (
            customer_key INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT UNIQUE NOT NULL,
            ho_ten_raw TEXT, ho_ten_clean TEXT, so_dien_thoai_raw TEXT,
            so_dien_thoai_clean TEXT, email_raw TEXT, email_clean TEXT,
            dia_chi TEXT, ngay_dang_ky DATE
        );
    """)
    conn.execute("""
        CREATE TABLE dim_quality_rule (
            rule_key INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_code TEXT UNIQUE, rule_name TEXT, dimension_name TEXT,
            nguong_chuan REAL, mo_ta TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE dim_audit_run (
            run_key INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT UNIQUE, run_date TIMESTAMP, total_records INTEGER, run_by TEXT
        );
    """)

    # Tạo bảng fact
    conn.execute("""
        CREATE TABLE fact_customer_quality_audit (
            audit_fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_key INTEGER, rule_key INTEGER, run_key INTEGER,
            is_valid BOOLEAN, is_auto_cleaned BOOLEAN DEFAULT 0,
            is_duplicate BOOLEAN DEFAULT 0, error_count INTEGER DEFAULT 0
        );
    """)

    # Tạo bảng quality_measures
    conn.execute("""
        CREATE TABLE quality_measures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT, chieu_chat_luong TEXT, doi_tuong TEXT,
            so_kiem INTEGER, so_dat INTEGER, so_loi INTEGER,
            ti_le_dat REAL, nguong_yeu_cau REAL, ket_luan TEXT
        );
    """)

    # Nạp dữ liệu mẫu
    # 10 dòng staging
    for i in range(1, 11):
        conn.execute(
            "INSERT INTO staging_customers (batch_id, customer_id, ho_ten, so_dien_thoai, email, dia_chi, ngay_dang_ky) "
            "VALUES (?, ?, ?, ?, ?, ?, ?);",
            ('lo-test', f'CUS{i:03d}', f'Nguyen Van {i}', f'090{i:07d}', f'user{i}@test.com', 'TP.HCM', '2025-01-01')
        )

    # 2 dòng reject
    conn.execute(
        "INSERT INTO reject_rows (batch_id, customer_id, ho_ten_goc, so_dien_thoai_goc, email_goc, ma_quy_tac, ly_do_loi) "
        "VALUES (?, ?, ?, ?, ?, ?, ?);",
        ('lo-test', 'CUS011', 'Tran B', '0912', '', 'DQ02_PHONE', 'SDT khong du 10 so')
    )
    conn.execute(
        "INSERT INTO reject_rows (batch_id, customer_id, ho_ten_goc, so_dien_thoai_goc, email_goc, ma_quy_tac, ly_do_loi) "
        "VALUES (?, ?, ?, ?, ?, ?, ?);",
        ('lo-test', 'CUS012', '', '0903333333', '', 'DQ01_NAME', 'Ho ten bi rong')
    )

    # Dim customer (8 khách = 10 staging - 2 reject)
    conn.execute("INSERT INTO dim_quality_rule (rule_code, rule_name, dimension_name, nguong_chuan, mo_ta) VALUES (?, ?, ?, ?, ?);",
                 ('DQ01', 'Kiem tra thieu', 'DAY_DU', 0.98, 'Kiem tra'))
    conn.execute("INSERT INTO dim_audit_run (batch_id, run_date, total_records, run_by) VALUES (?, ?, ?, ?);",
                 ('lo-test', '2025-01-01 10:00:00', 10, 'test'))

    for i in range(1, 9):
        conn.execute(
            "INSERT INTO dim_customer (customer_id, ho_ten_raw, ho_ten_clean, so_dien_thoai_raw, so_dien_thoai_clean, email_raw, email_clean, dia_chi, ngay_dang_ky) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (f'CUS{i:03d}', f'nguyen van {i}', f'Nguyen Van {i}', f'090{i:07d}', f'090{i:07d}', f'user{i}@test.com', f'user{i}@test.com', 'TP.HCM', '2025-01-01')
        )

    # Fact: 8 dòng, 3 trùng lặp, 5 duy nhất
    for i in range(1, 9):
        is_dup = 1 if i <= 3 else 0
        conn.execute(
            "INSERT INTO fact_customer_quality_audit (customer_key, rule_key, run_key, is_valid, is_duplicate, error_count) "
            "VALUES (?, ?, ?, ?, ?, ?);",
            (i, 1, 1, 1, is_dup, is_dup)
        )

    conn.commit()
    yield conn
    conn.close()


# ============================================================================
# TEST 1: Đếm dòng staging vs fact
# ============================================================================
def test_dem_dong_cac_bang(db_kiem_thu):
    """Kiểm tra hàm đếm dòng trả về đúng số bản ghi cho mỗi bảng."""
    so_dong = dem_dong_cac_bang(db_kiem_thu)

    assert so_dong['staging_customers'] == 10
    assert so_dong['reject_rows'] == 2
    assert so_dong['dim_customer'] == 8
    assert so_dong['fact_customer_quality_audit'] == 8

    # Chênh lệch staging - fact = reject
    assert so_dong['staging_customers'] - so_dong['fact_customer_quality_audit'] == so_dong['reject_rows']


# ============================================================================
# TEST 2: Giải thích chênh lệch
# ============================================================================
def test_giai_thich_chenh_lech_co_noi_dung():
    """Kiểm tra hàm giải thích chênh lệch tạo ra nội dung hợp lệ."""
    so_dong = {
        'staging_customers': 100,
        'reject_rows': 10,
        'dim_customer': 90,
        'fact_customer_quality_audit': 90,
    }
    dong = giai_thich_chenh_lech(so_dong)
    noi_dung = '\n'.join(dong)

    assert '10' in noi_dung
    assert 'reject' in noi_dung.lower() or 'từ chối' in noi_dung.lower() or 'tu choi' in noi_dung.lower()


# ============================================================================
# TEST 3: Biểu đồ lỗi DQ tạo thành công
# ============================================================================
def test_bieu_do_loi_dq_tao_file(db_kiem_thu, tmp_path):
    """Kiểm tra biểu đồ phân bổ lỗi DQ tạo ra file ảnh hợp lệ."""
    duong_dan = tmp_path / 'test_bieu_do_loi.png'
    ket_qua = bieu_do_loi_dq(db_kiem_thu, duong_dan)

    assert ket_qua.exists()
    assert ket_qua.stat().st_size > 0


# ============================================================================
# TEST 4: Biểu đồ trùng lặp tạo thành công
# ============================================================================
def test_bieu_do_trung_lap_tao_file(db_kiem_thu, tmp_path):
    """Kiểm tra biểu đồ tỷ lệ trùng lặp tạo ra file ảnh hợp lệ."""
    duong_dan = tmp_path / 'test_bieu_do_trung.png'
    ket_qua = bieu_do_trung_lap(db_kiem_thu, duong_dan)

    assert ket_qua.exists()
    assert ket_qua.stat().st_size > 0


# ============================================================================
# TEST 5 — BIÊN: Bộ lọc ngày rỗng → hình placeholder, không crash
# ============================================================================
def test_bieu_do_bo_loc_rong_khong_crash(db_kiem_thu, tmp_path):
    """LOẠI BIÊN: Khi lọc theo khoảng ngày không có dữ liệu, hàm tạo ảnh placeholder thay vì crash.

    Đây là test cho trạng thái 'rỗng' — một trong 3 trạng thái bắt buộc theo checklist.
    """
    duong_dan = tmp_path / 'test_rong.png'
    # Lọc theo ngày xa tương lai → chắc chắn không có dữ liệu
    ket_qua = bieu_do_trung_lap(db_kiem_thu, duong_dan, tu_ngay='2099-01-01', den_ngay='2099-12-31')

    assert ket_qua.exists()
    assert ket_qua.stat().st_size > 0  # File placeholder được tạo, không phải file rỗng


# ============================================================================
# TEST 6: Hàm tạo hình thông báo hoạt động
# ============================================================================
def test_tao_hinh_thong_bao_loi(tmp_path):
    """Kiểm tra hàm tạo hình placeholder hiển thị thông báo lỗi."""
    duong_dan = tmp_path / 'test_loi.png'
    ket_qua = _tao_hinh_thong_bao("Khong co du lieu", duong_dan, la_loi=True)

    assert ket_qua.exists()
    assert ket_qua.stat().st_size > 0
