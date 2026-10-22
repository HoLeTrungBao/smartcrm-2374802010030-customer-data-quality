"""PHA 4 — LOAD: Nạp dữ liệu vào bảng Staging, bảng Reject và bảng Quality Measures.

Đảm bảo tính IDEMPOTENT (chạy lại được): Xóa dữ liệu cũ theo batch_id trước khi nạp lại.
"""
import sqlite3
import logging
import pandas as pd
from src.quality.checks import Do

log = logging.getLogger('load.staging')


def nap_staging(conn: sqlite3.Connection, df_tho: pd.DataFrame, batch_id: str) -> int:
    """Nạp dữ liệu thô vào bảng staging_customers."""
    log.info("Bắt đầu nạp %d bản ghi vào bảng staging_customers cho lô %s...", len(df_tho), batch_id)

    with conn:
        # Xóa dữ liệu cũ của cùng batch_id để đảm bảo idempotent
        conn.execute("DELETE FROM staging_customers WHERE batch_id = ?;", (batch_id,))

        du_lieu = [
            (
                batch_id,
                str(row.get('customer_id', '')),
                str(row.get('ho_ten', '')),
                str(row.get('so_dien_thoai', '')),
                str(row.get('email', '')),
                str(row.get('dia_chi', '')),
                str(row.get('ngay_dang_ky', ''))
            )
            for _, row in df_tho.iterrows()
        ]

        conn.executemany("""
            INSERT INTO staging_customers (
                batch_id, customer_id, ho_ten, so_dien_thoai, email, dia_chi, ngay_dang_ky
            ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """, du_lieu)

    log.info("Nạp staging thành công: %d dòng.", len(du_lieu))
    return len(du_lieu)


def nap_reject(conn: sqlite3.Connection, df_reject: pd.DataFrame, batch_id: str) -> int:
    """Nạp các dòng lỗi không thể làm sạch vào bảng reject_rows kèm lý do."""
    log.info("Bắt đầu nạp %d dòng từ chối vào bảng reject_rows cho lô %s...", len(df_reject), batch_id)

    with conn:
        conn.execute("DELETE FROM reject_rows WHERE batch_id = ?;", (batch_id,))

        if not df_reject.empty:
            du_lieu = [
                (
                    batch_id,
                    str(row.get('customer_id', '')),
                    str(row.get('ho_ten_goc', '')),
                    str(row.get('so_dien_thoai_goc', '')),
                    str(row.get('email_goc', '')),
                    str(row.get('ma_quy_tac', '')),
                    str(row.get('ly_do_loi', ''))
                )
                for _, row in df_reject.iterrows()
            ]

            conn.executemany("""
                INSERT INTO reject_rows (
                    batch_id, customer_id, ho_ten_goc, so_dien_thoai_goc, email_goc, ma_quy_tac, ly_do_loi
                ) VALUES (?, ?, ?, ?, ?, ?, ?);
            """, du_lieu)
        else:
            du_lieu = []

    log.info("Nạp bảng reject thành công: %d dòng.", len(du_lieu))
    return len(du_lieu)


def nap_do_chat_luong(conn: sqlite3.Connection, danh_sach_do: list[Do], batch_id: str) -> int:
    """Nạp kết quả đo chất lượng vào bảng quality_measures."""
    log.info("Lưu %d kết quả đo chất lượng vào bảng quality_measures cho lô %s...", len(danh_sach_do), batch_id)

    with conn:
        conn.execute("DELETE FROM quality_measures WHERE batch_id = ?;", (batch_id,))

        du_lieu = [
            (
                batch_id,
                m.chieu,
                m.doi_tuong,
                m.so_kiem,
                m.so_dat,
                m.so_loi,
                round(m.ti_le, 4),
                m.nguong,
                'DAT' if m.dat else 'KHONG_DAT'
            )
            for m in danh_sach_do
        ]

        conn.executemany("""
            INSERT INTO quality_measures (
                batch_id, chieu_chat_luong, doi_tuong, so_kiem, so_dat, so_loi,
                ti_le_dat, nguong_yeu_cau, ket_luan
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, du_lieu)

    return len(du_lieu)
