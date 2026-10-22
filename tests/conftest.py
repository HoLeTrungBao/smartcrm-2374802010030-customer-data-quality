"""Cấu hình các fixtures dữ liệu kiểm thử độc lập cho Pytest."""
import pytest
import pandas as pd


@pytest.fixture
def du_lieu_khach_hang_mau() -> pd.DataFrame:
    """Tạo DataFrame dữ liệu giả lập chứa đủ các trường hợp: chuẩn, biên, lỗi, trùng."""
    du_lieu = [
        # 1. Dòng đúng chuẩn
        {
            'customer_id': 'CUS001',
            'ho_ten': 'nguyễn văn an',
            'so_dien_thoai': '0901234567',
            'email': 'an.nguyen@gmail.com',
            'dia_chi': 'Quận 1, TP.HCM',
            'ngay_dang_ky': '2025-05-15'
        },
        # 2. Dòng cần chuẩn hóa SĐT (+84) và họ tên viết hoa
        {
            'customer_id': 'CUS002',
            'ho_ten': '  TRẦN   THỊ   BÌNH  ',
            'so_dien_thoai': '+84902345678',
            'email': 'BINH.TRAN@GMAIL.COM',
            'dia_chi': 'Quận 3, TP.HCM',
            'ngay_dang_ky': '15/05/2025'
        },
        # 3. Dòng trùng SĐT với CUS001 sau khi chuẩn hóa
        {
            'customer_id': 'CUS003',
            'ho_ten': 'Nguyễn Văn An',
            'so_dien_thoai': '84901234567',
            'email': 'an.duplicate@gmail.com',
            'dia_chi': 'Quận 1, TP.HCM',
            'ngay_dang_ky': '2025.05.20'
        },
        # 4. Dòng lỗi: Thiếu SĐT
        {
            'customer_id': 'CUS004',
            'ho_ten': 'Lê Hoàng C',
            'so_dien_thoai': '',
            'email': 'hoangc@gmail.com',
            'dia_chi': 'Bình Thạnh, TP.HCM',
            'ngay_dang_ky': '2025-06-01'
        },
        # 5. Dòng lỗi: SĐT sai định dạng (chỉ có 8 chữ số)
        {
            'customer_id': 'CUS005',
            'ho_ten': 'Phạm Thu D',
            'so_dien_thoai': '09123456',
            'email': 'thud@gmail.com',
            'dia_chi': 'Gò Vấp, TP.HCM',
            'ngay_dang_ky': '2025-06-10'
        },
        # 6. Dòng lỗi: Thiếu họ tên hoàn toàn
        {
            'customer_id': 'CUS006',
            'ho_ten': '   ',
            'so_dien_thoai': '0903333333',
            'email': 'noname@gmail.com',
            'dia_chi': 'Thủ Đức, TP.HCM',
            'ngay_dang_ky': '2025-06-12'
        }
    ]
    return pd.DataFrame(du_lieu)
