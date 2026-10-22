"""Mô-đun quản lý kết nối và khởi tạo cơ sở dữ liệu kho dữ liệu Star Schema."""
import sqlite3
import pathlib
import logging
from src import config

log = logging.getLogger('db')


def lay_ket_noi(duong_dan_db: pathlib.Path | None = None) -> sqlite3.Connection:
    """Tạo và trả về kết nối SQLite với cấu hình hỗ trợ khóa ngoại."""
    if duong_dan_db is None:
        duong_dan_db = config.duong_dan_db()

    duong_dan_db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(duong_dan_db))
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def khoi_tao_kho_du_lieu(conn: sqlite3.Connection | None = None) -> None:
    """Thực thi tuần tự các tập tin DDL trong thư mục sql/ để khởi tạo bảng."""
    dong_ket_noi_sau_khi_chay = False
    if conn is None:
        conn = lay_ket_noi()
        dong_ket_noi_sau_khi_chay = True

    thu_muc_sql = config.GOC / 'sql'
    cac_tap_tin_ddl = [
        '001_staging.sql',
        '002_reject.sql',
        '010_dim.sql',
        '020_fact.sql'
    ]

    try:
        cursor = conn.cursor()
        for ten_file in cac_tap_tin_ddl:
            duong_dan_file = thu_muc_sql / ten_file
            if duong_dan_file.exists():
                sql_script = duong_dan_file.read_text(encoding='utf-8')
                cursor.executescript(sql_script)
                log.info('Đã thực thi thành công tập tin DDL: %s', ten_file)
        conn.commit()
    finally:
        if dong_ket_noi_sau_khi_chay:
            conn.close()
