"""KIỂM THỬ ĐƠN VỊ CÁC PHÉP ĐO CHẤT LƯỢNG (src/quality/checks.py)

Kiểm tra:
  - Hàm đo đầy đủ (do_day_du)
  - Hàm đo chính xác (do_chinh_xac)
  - Hàm đo nhất quán (do_nhat_quan)
  - Quy trình phân tách df_sach và df_reject trong clean_customers
"""
from src.transform.clean_customers import xu_ly_lam_sach_khach_hang
from src.quality.checks import do_tat_ca, Do


def test_xu_ly_lam_sach_va_reject(du_lieu_khach_hang_mau):
    """Kiểm tra phân tách dữ liệu sạch và dữ liệu reject trên tập dữ liệu mẫu."""
    df_sach, df_reject = xu_ly_lam_sach_khach_hang(du_lieu_khach_hang_mau)

    # Tập mẫu 6 dòng:
    # CUS001: chuẩn -> sạch
    # CUS002: +84 -> chuẩn hóa -> sạch
    # CUS003: 84 -> chuẩn hóa -> sạch (trùng SĐT với CUS001)
    # CUS004: thiếu SĐT -> reject
    # CUS005: SĐT 8 số -> reject
    # CUS006: thiếu họ tên -> reject
    assert len(df_sach) == 3
    assert len(df_reject) == 3

    # Kiểm tra cờ trùng lặp
    trung_ids = set(df_sach[df_sach['is_duplicate']]['customer_id'])
    assert 'CUS001' in trung_ids
    assert 'CUS003' in trung_ids

    # Kiểm tra bảng reject có lý do viết cho con người đọc
    for _, row in df_reject.iterrows():
        assert len(row['ly_do_loi']) > 0
        assert len(row['ma_quy_tac']) > 0


def test_do_tat_ca_chat_luong(du_lieu_khach_hang_mau):
    """Kiểm tra tổng hợp các phép đo chất lượng 3 chiều trả về dataclass Do có số đo cụ thể."""
    df_sach, _ = xu_ly_lam_sach_khach_hang(du_lieu_khach_hang_mau)

    nguong_kiem_thu = {
        'do_day_du': {'customers.customer_id': 1.0, 'customers.ho_ten': 0.8},
        'do_chinh_xac': {'sdt_chuan_hoa_duoc': 0.5},
        'do_nhat_quan': {'ty_le_sdt_duy_nhat': 0.3}
    }

    danh_sach_do = do_tat_ca(du_lieu_khach_hang_mau, df_sach, nguong_kiem_thu)
    assert len(danh_sach_do) >= 5

    for m in danh_sach_do:
        assert isinstance(m, Do)
        assert 0.0 <= m.ti_le <= 1.0
        assert m.so_loi >= 0
        assert isinstance(m.dat, bool)
        d = m.as_dict()
        assert 'ti_le' in d
        assert 'so_loi' in d
