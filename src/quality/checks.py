"""PHA 3 — QUALITY: Đo lường 3 chiều chất lượng dữ liệu (Đầy đủ, Chính xác, Nhất quán).

NGUYÊN TẮC: Mọi phép đo đều trả về MỘT SỐ định lượng cụ thể (tỷ lệ, số dòng đạt, số lỗi),
không chỉ trả về True/False chung chung, giúp đối chiếu ngưỡng và so sánh giữa các lần chạy.
"""
from dataclasses import dataclass, asdict
import pandas as pd
from src.transform import rules


@dataclass
class Do:
    chieu: str         # DAY_DU | CHINH_XAC | NHAT_QUAN
    doi_tuong: str     # Tên bảng.cột hoặc mã quy tắc kiểm định
    so_kiem: int       # Tổng số bản ghi kiểm tra
    so_dat: int        # Số bản ghi đạt yêu cầu
    nguong: float      # Ngưỡng tỷ lệ tối thiểu yêu cầu (ví dụ 0.95)

    @property
    def ti_le(self) -> float:
        return self.so_dat / self.so_kiem if self.so_kiem else 1.0

    @property
    def so_loi(self) -> int:
        return self.so_kiem - self.so_dat

    @property
    def dat(self) -> bool:
        return self.ti_le >= self.nguong

    def as_dict(self) -> dict:
        d = asdict(self)
        d.update(
            ti_le=round(self.ti_le, 4),
            so_loi=self.so_loi,
            dat=self.dat
        )
        return d


def _co_gia_tri(sr: pd.Series) -> pd.Series:
    """Trả về mask boolean xác định các phần tử có giá trị thực (không rỗng)."""
    return ~sr.apply(rules._rong)


# ---------------- CHIỀU 1: ĐẦY ĐỦ (Completeness) — Đo theo từng cột ----------------
def do_day_du(df_tho: pd.DataFrame, nguong: dict) -> list[Do]:
    """Đo lường mức độ đầy đủ của từng cột dữ liệu quan trọng trong bảng khách hàng."""
    ket_qua = []
    tong_so = len(df_tho)
    nguong_day_du = nguong.get('do_day_du', {})

    cot_id = 'customer_id' if 'customer_id' in df_tho.columns else 'record_id'
    cac_cot_kiem_tra = [
        ('customers.customer_id', cot_id),
        ('customers.ho_ten', 'ho_ten'),
        ('customers.so_dien_thoai', 'so_dien_thoai'),
        ('customers.email', 'email')
    ]

    for doi_tuong, cot in cac_cot_kiem_tra:
        if cot in df_tho.columns:
            so_dat = int(_co_gia_tri(df_tho[cot]).sum())
            nguong_chuan = float(nguong_day_du.get(doi_tuong, 0.95))
            ket_qua.append(Do('DAY_DU', doi_tuong, tong_so, so_dat, nguong_chuan))

    return ket_qua


# ---------------- CHIỀU 2: CHÍNH XÁC (Validity) — Đo theo quy tắc nghiệp vụ ---------
def do_chinh_xac(df_tho: pd.DataFrame, df_sach: pd.DataFrame, nguong: dict) -> list[Do]:
    """Đo lường mức độ hợp lệ và chính xác về mặt định dạng của các trường thông tin."""
    ket_qua = []
    nguong_cx = nguong.get('do_chinh_xac', {})

    # 1. Đo tỷ lệ SĐT chuẩn hóa được về 10 chữ số (trên tổng số dòng có SĐT)
    co_sdt = _co_gia_tri(df_tho['so_dien_thoai'])
    so_kiem_sdt = int(co_sdt.sum())
    # Số SĐT chuẩn hóa thành công có trong df_sach
    so_dat_sdt = int(df_sach['so_dien_thoai_clean'].notna().sum())
    ket_qua.append(Do(
        'CHINH_XAC', 'sdt_chuan_hoa_duoc',
        so_kiem_sdt, so_dat_sdt,
        float(nguong_cx.get('sdt_chuan_hoa_duoc', 0.95))
    ))

    # 2. Đo tỷ lệ họ tên chuẩn hóa được Title Case
    co_ten = _co_gia_tri(df_tho['ho_ten'])
    so_kiem_ten = int(co_ten.sum())
    so_dat_ten = int(df_sach['ho_ten_clean'].notna().sum())
    ket_qua.append(Do(
        'CHINH_XAC', 'ho_ten_chuan_hoa_duoc',
        so_kiem_ten, so_dat_ten,
        float(nguong_cx.get('ho_ten_chuan_hoa_duoc', 0.98))
    ))

    # 3. Đo tỷ lệ email hợp lệ theo chuẩn regex (trên các bản ghi có email)
    co_email = _co_gia_tri(df_tho['email'])
    so_kiem_email = int(co_email.sum())
    so_dat_email = int(df_sach['email_clean'].notna().sum())
    ket_qua.append(Do(
        'CHINH_XAC', 'email_dung_dinh_dang',
        so_kiem_email, so_dat_email,
        float(nguong_cx.get('email_dung_dinh_dang', 0.95))
    ))

    # 4. Đo tỷ lệ ngày đăng ký hợp lệ
    cot_ngay = 'ngay_dang_ky' if 'ngay_dang_ky' in df_tho.columns else 'ngay_tao'
    if cot_ngay in df_tho.columns:
        co_ngay = _co_gia_tri(df_tho[cot_ngay])
        so_kiem_ngay = int(co_ngay.sum())
        so_dat_ngay = int(df_sach['ngay_dang_ky_chuan'].notna().sum())
        ket_qua.append(Do(
            'CHINH_XAC', 'ngay_dang_ky_hop_le',
            so_kiem_ngay, so_dat_ngay,
            float(nguong_cx.get('ngay_dang_ky_hop_le', 0.98))
        ))

    return ket_qua


# ---------------- CHIỀU 3: NHẤT QUÁN (Consistency / Uniqueness) -------------------
def do_nhat_quan(df_sach: pd.DataFrame, nguong: dict) -> list[Do]:
    """Đo lường mức độ nhất quán và tỷ lệ bản ghi duy nhất không trùng lặp."""
    ket_qua = []
    tong_so = len(df_sach)
    nguong_nq = nguong.get('do_nhat_quan', {})

    # Tỷ lệ khách hàng không bị trùng lặp số điện thoại
    so_duy_nhat = int((~df_sach['is_duplicate']).sum())
    ket_qua.append(Do(
        'NHAT_QUAN', 'ty_le_sdt_duy_nhat',
        tong_so, so_duy_nhat,
        float(nguong_nq.get('ty_le_sdt_duy_nhat', 0.70))
    ))

    return ket_qua


def do_tat_ca(df_tho: pd.DataFrame, df_sach: pd.DataFrame, nguong: dict) -> list[Do]:
    """Thực thi toàn bộ các phép đo trên cả 3 chiều chất lượng."""
    danh_sach_do = []
    danh_sach_do.extend(do_day_du(df_tho, nguong))
    danh_sach_do.extend(do_chinh_xac(df_tho, df_sach, nguong))
    danh_sach_do.extend(do_nhat_quan(df_sach, nguong))
    return danh_sach_do
