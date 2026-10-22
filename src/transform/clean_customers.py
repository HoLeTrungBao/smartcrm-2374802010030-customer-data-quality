"""PHA 2 — TRANSFORM: Điều phối quá trình làm sạch dữ liệu khách hàng.

Áp dụng các quy tắc chuẩn hóa thuần vào DataFrame khách hàng, phân tách rõ ràng
giữa các bản ghi hợp lệ (đạt chuẩn) và các bản ghi không đạt (đưa vào bảng reject).
"""
import logging
import pandas as pd
from src.transform import rules

log = logging.getLogger('transform')


def xu_ly_lam_sach_khach_hang(df_tho: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Thực hiện chuẩn hóa dữ liệu khách hàng thô.

    Trả về:
      - `df_sach`: DataFrame chứa các khách hàng hợp lệ với đầy đủ cột raw và clean.
      - `df_reject`: DataFrame chứa các dòng lỗi không thể sửa kèm lý do.
    """
    log.info("Bắt đầu xử lý làm sạch tập dữ liệu khách hàng (%d dòng)...", len(df_tho))

    df = df_tho.copy()

    # Nhận diện tên cột nguồn linh hoạt
    cot_id = 'customer_id' if 'customer_id' in df.columns else 'record_id'
    cot_ngay = 'ngay_dang_ky' if 'ngay_dang_ky' in df.columns else 'ngay_tao'

    # Chuẩn hóa về customer_id và ngay_dang_ky thống nhất
    df['customer_id'] = df[cot_id].astype(str)
    if cot_ngay in df.columns:
        df['ngay_dang_ky'] = df[cot_ngay]
    else:
        df['ngay_dang_ky'] = None

    # Chuẩn hóa họ tên, SĐT, email và ngày đăng ký
    df['ho_ten_clean'] = df['ho_ten'].apply(rules.chuan_hoa_ho_ten)
    df['so_dien_thoai_clean'] = df['so_dien_thoai'].apply(rules.chuan_hoa_dien_thoai)
    df['email_clean'] = df['email'].apply(rules.chuan_hoa_email)
    df['ngay_dang_ky_chuan'] = df['ngay_dang_ky'].apply(rules.doc_ngay)

    # Đổi tên cột gốc thành _raw để phục vụ lưu trữ song song
    df['ho_ten_raw'] = df['ho_ten']
    df['so_dien_thoai_raw'] = df['so_dien_thoai']
    df['email_raw'] = df['email']

    # Xác định các điều kiện không hợp lệ nghiêm trọng cần đưa vào reject:
    # 1. Thiếu mã định danh customer_id
    loi_customer_id = df['customer_id'].apply(rules._rong)
    # 2. Không thể chuẩn hóa số điện thoại thành 10 chữ số
    loi_sdt = df['so_dien_thoai_clean'].isna()
    # 3. Thiếu họ tên
    loi_ten = df['ho_ten_clean'].isna()

    # Thu thập các dòng bị reject kèm lý do cụ thể
    danh_sach_reject = []

    for idx, row in df[loi_customer_id | loi_sdt | loi_ten].iterrows():
        ly_do = []
        ma_rule = []

        if loi_customer_id[idx]:
            ma_rule.append('DQ01_ID')
            ly_do.append("Thiếu mã định danh khách hàng (customer_id)")
        if loi_ten[idx]:
            ma_rule.append('DQ01_NAME')
            ly_do.append("Họ tên khách hàng bị rỗng hoặc không có giá trị hợp lệ")
        if loi_sdt[idx]:
            ma_rule.append('DQ02_PHONE')
            sdt_goc = row['so_dien_thoai_raw']
            if rules._rong(sdt_goc):
                ly_do.append("Số điện thoại bị để trống")
            else:
                ly_do.append(f"Số điện thoại '{sdt_goc}' không thể chuẩn hóa về 10 chữ số chuẩn")

        danh_sach_reject.append({
            'customer_id': row.get('customer_id', ''),
            'ho_ten_goc': row.get('ho_ten_raw', ''),
            'so_dien_thoai_goc': row.get('so_dien_thoai_raw', ''),
            'email_goc': row.get('email_raw', ''),
            'ma_quy_tac': '; '.join(ma_rule),
            'ly_do_loi': '; '.join(ly_do)
        })

    df_reject = pd.DataFrame(danh_sach_reject)

    # Tập hợp các bản ghi sạch (đạt chuẩn)
    mask_hop_le = ~(loi_customer_id | loi_sdt | loi_ten)
    df_sach = df[mask_hop_le].copy()

    # Phát hiện trùng lặp trên tập dữ liệu sạch:
    # Bản ghi bị coi là trùng lặp nếu trùng số điện thoại sạch đã xuất hiện trước đó
    trung_sdt = df_sach.duplicated(subset=['so_dien_thoai_clean'], keep=False)
    # Hoặc trùng email sạch (chỉ xét những dòng có email)
    co_email = df_sach['email_clean'].notna()
    trung_email = df_sach[co_email].duplicated(subset=['email_clean'], keep=False)
    trung_email = trung_email.reindex(df_sach.index, fill_value=False)

    df_sach['is_duplicate'] = (trung_sdt | trung_email)
    df_sach['is_valid'] = True
    df_sach['is_auto_cleaned'] = True
    df_sach['error_count'] = df_sach['is_duplicate'].astype(int)

    log.info("Làm sạch hoàn tất: %d dòng đạt chuẩn, %d dòng đưa vào bảng reject.",
             len(df_sach), len(df_reject))

    return df_sach, df_reject
