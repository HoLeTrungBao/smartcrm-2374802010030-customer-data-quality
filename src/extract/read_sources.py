"""PHA 1 — EXTRACT: Đọc dữ liệu nguồn từ các tập tin CSV.

Nguyên tắc: Đọc dữ liệu nguồn nguyên trạng, KHÔNG thực hiện làm sạch hay biến đổi ở pha này.
"""
import pathlib
import logging
import pandas as pd

log = logging.getLogger('extract')


def doc_khach_hang_tho(duong_dan_tep: pathlib.Path | str) -> pd.DataFrame:
    """Đọc dữ liệu khách hàng thô từ tập tin CSV.

    Đảm bảo đọc tất cả các cột dưới dạng chuỗi (string) để bảo toàn nguyên trạng
    các định dạng số điện thoại chứa số 0 đầu, mã vùng hoặc ký tự phân cách.
    """
    duong_dan = pathlib.Path(duong_dan_tep)
    if not duong_dan.exists():
        raise FileNotFoundError(f"Không tìm thấy tập tin dữ liệu nguồn: {duong_dan}")

    log.info("Bắt đầu đọc dữ liệu khách hàng thô từ: %s", duong_dan)
    # dtype=str để không bị mất số 0 ở đầu số điện thoại
    df = pd.read_csv(duong_dan, dtype=str, keep_default_na=False)
    log.info("Đã đọc thành công %d dòng dữ liệu từ tập tin nguồn.", len(df))
    return df


def doc_tat_ca(thu_muc_du_lieu: pathlib.Path) -> dict[str, pd.DataFrame]:
    """Đọc tất cả các nguồn dữ liệu cần thiết cho phân hệ L7."""
    tep_chinh = thu_muc_du_lieu / 'customers_raw.csv'
    if not tep_chinh.exists():
        # Thử tìm trong thư mục dữ liệu mẫu
        tep_mau = thu_muc_du_lieu.parent / 'mau' / 'customers_sample.csv'
        if tep_mau.exists():
            tep_chinh = tep_mau

    df_khach_hang = doc_khach_hang_tho(tep_chinh)
    return {
        'customers': df_khach_hang
    }
