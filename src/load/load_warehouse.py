"""PHA 4 — LOAD: Nạp dữ liệu vào kho dữ liệu Star Schema (Dimension và Fact).

Bảo đảm tính IDEMPOTENT: Chạy lại lần 2 không làm nhân đôi số lượng bản ghi trong dim_customer và fact.
"""
import sqlite3
import logging
from datetime import datetime
import pandas as pd

log = logging.getLogger('load.warehouse')

CAC_QUY_TAC_CHAUAN = [
    ('DQ01', 'Kiểm tra giá trị thiếu bắt buộc', 'DAY_DU', 0.98, 'Bắt buộc không được rỗng mã khách hàng, số điện thoại, họ tên.'),
    ('DQ02', 'Chuẩn hóa định dạng số điện thoại', 'CHINH_XAC', 0.95, 'Quy đổi về 10 số (0xxxxxxxxx), loại bỏ tiền tố quốc tế 84/+84.'),
    ('DQ03', 'Kiểm tra định dạng email', 'CHINH_XAC', 0.95, 'Kiểm tra tính hợp lệ cú pháp email theo chuẩn RFC 5322.'),
    ('DQ04', 'Phát hiện khách hàng trùng lặp', 'NHAT_QUAN', 0.70, 'Gom nhóm và phát hiện các bản ghi trùng SĐT hoặc Email.'),
    ('DQ05', 'Chuẩn hóa họ tên khách hàng', 'CHINH_XAC', 0.98, 'Xóa khoảng trắng thừa và viết hoa chữ cái đầu (Title Case).'),
    ('DQ06', 'Kiểm tra ngày đăng ký hợp lệ', 'CHINH_XAC', 0.98, 'Ngày đăng ký phải đúng định dạng ngày và không vượt quá ngày hiện tại.')
]


def khoi_tao_quy_tac_chuan(conn: sqlite3.Connection) -> None:
    """Nạp các quy tắc chất lượng chuẩn vào dim_quality_rule nếu chưa có."""
    with conn:
        conn.executemany("""
            INSERT OR IGNORE INTO dim_quality_rule (
                rule_code, rule_name, dimension_name, nguong_chuan, mo_ta
            ) VALUES (?, ?, ?, ?, ?);
        """, CAC_QUY_TAC_CHAUAN)


def tao_phien_chay(conn: sqlite3.Connection, batch_id: str, tong_so_dong: int, nguoi_chay: str = 'ETL_Pipeline') -> int:
    """Ghi nhận phiên chạy kiểm định vào bảng dim_audit_run và trả về run_key (giữ nguyên run_key nếu đã tồn tại)."""
    with conn:
        cursor = conn.execute("SELECT run_key FROM dim_audit_run WHERE batch_id = ?;", (batch_id,))
        row = cursor.fetchone()
        thoi_gian_hien_tai = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if row:
            run_key = row['run_key']
            conn.execute("""
                UPDATE dim_audit_run
                SET run_date = ?, total_records = ?, run_by = ?
                WHERE run_key = ?;
            """, (thoi_gian_hien_tai, tong_so_dong, nguoi_chay, run_key))
            return run_key
        else:
            cur = conn.execute("""
                INSERT INTO dim_audit_run (batch_id, run_date, total_records, run_by)
                VALUES (?, ?, ?, ?);
            """, (batch_id, thoi_gian_hien_tai, tong_so_dong, nguoi_chay))
            return cur.lastrowid


def nap_dim_customer(conn: sqlite3.Connection, df_sach: pd.DataFrame) -> dict[str, int]:
    """Nạp dữ liệu khách hàng sạch vào bảng dim_customer (INSERT OR REPLACE để không nhân đôi).

    Trả về từ điển ánh xạ {customer_id: customer_key} phục vụ nạp bảng Fact.
    """
    log.info("Bắt đầu nạp %d khách hàng sạch vào dim_customer...", len(df_sach))

    with conn:
        du_lieu = [
            (
                str(row['customer_id']),
                str(row.get('ho_ten_raw', '')),
                str(row.get('ho_ten_clean', '')),
                str(row.get('so_dien_thoai_raw', '')),
                str(row.get('so_dien_thoai_clean', '')),
                str(row.get('email_raw', '')),
                str(row.get('email_clean', '')) if pd.notna(row.get('email_clean')) else None,
                str(row.get('dia_chi', '')),
                str(row.get('ngay_dang_ky_chuan', '')) if pd.notna(row.get('ngay_dang_ky_chuan')) else None
            )
            for _, row in df_sach.iterrows()
        ]

        conn.executemany("""
            INSERT INTO dim_customer (
                customer_id, ho_ten_raw, ho_ten_clean, so_dien_thoai_raw, so_dien_thoai_clean,
                email_raw, email_clean, dia_chi, ngay_dang_ky
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(customer_id) DO UPDATE SET
                ho_ten_clean = excluded.ho_ten_clean,
                so_dien_thoai_clean = excluded.so_dien_thoai_clean,
                email_clean = excluded.email_clean,
                thoi_gian_cap_nhat = CURRENT_TIMESTAMP;
        """, du_lieu)

    # Lấy ánh xạ customer_id -> customer_key
    cursor = conn.execute("SELECT customer_id, customer_key FROM dim_customer;")
    anh_xa = {row['customer_id']: row['customer_key'] for row in cursor.fetchall()}
    log.info("Nạp dim_customer hoàn tất. Tổng số khách hàng trong kho: %d.", len(anh_xa))
    return anh_xa


def nap_fact_quality(conn: sqlite3.Connection, df_sach: pd.DataFrame, anh_xa_kh: dict[str, int], run_key: int) -> int:
    """Nạp sự kiện kiểm định chất lượng vào bảng fact_customer_quality_audit."""
    log.info("Bắt đầu nạp dữ liệu kiểm định vào bảng Fact cho phiên %d...", run_key)

    # Lấy rule_key mặc định cho quy tắc tổng hợp
    cursor = conn.execute("SELECT rule_key FROM dim_quality_rule WHERE rule_code = 'DQ01';")
    row = cursor.fetchone()
    rule_key_dq01 = row['rule_key'] if row else 1

    with conn:
        # Xóa các dòng Fact cũ của phiên chạy này nếu chạy lại
        conn.execute("DELETE FROM fact_customer_quality_audit WHERE run_key = ?;", (run_key,))

        du_lieu = []
        for _, row_data in df_sach.iterrows():
            cid = str(row_data['customer_id'])
            ckey = anh_xa_kh.get(cid)
            if ckey:
                du_lieu.append((
                    ckey,
                    rule_key_dq01,
                    run_key,
                    1 if row_data.get('is_valid', True) else 0,
                    1 if row_data.get('is_auto_cleaned', False) else 0,
                    1 if row_data.get('is_duplicate', False) else 0,
                    int(row_data.get('error_count', 0))
                ))

        conn.executemany("""
            INSERT INTO fact_customer_quality_audit (
                customer_key, rule_key, run_key, is_valid, is_auto_cleaned, is_duplicate, error_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """, du_lieu)

    log.info("Nạp fact_customer_quality_audit hoàn tất: %d dòng.", len(du_lieu))
    return len(du_lieu)
