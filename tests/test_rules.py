"""KIỂM THỬ ĐƠN VỊ CÁC HÀM QUY TẮC CHUẨN HÓA (src/transform/rules.py)

Bảo đảm đủ 3 loại kiểm thử bắt buộc theo tiêu chí C4 / Bảng kiểm chứng BT2:
  1. Luồng đúng (Happy Path)
  2. Giá trị biên (Boundary Value)
  3. Dữ liệu sai (Invalid / Negative Path)
"""
from datetime import date
from src.transform import rules


# ============================================================================
# 1. KIỂM THỬ HÀM _rong() — XỬ LÝ AN TOÀN MỌI DẠNG THIẾU DỮ LIỆU
# ============================================================================
def test_rong_voi_cac_dang_thieu_thuc_te():
    """Kiểm tra hàm _rong nhận diện đúng các dạng thiếu dữ liệu."""
    assert rules._rong(None) is True
    assert rules._rong('') is True
    assert rules._rong('   ') is True
    assert rules._rong('nan') is True
    assert rules._rong('NaN') is True
    assert rules._rong('null') is True
    assert rules._rong('None') is True
    assert rules._rong('Hồ Lê Trung Bảo') is False
    assert rules._rong('0901234567') is False


# ============================================================================
# 2. KIỂM THỬ HÀM chuan_hoa_dien_thoai()
# ============================================================================
def test_sdt_luong_dung():
    """LOẠI 1 — LUỒNG ĐÚNG: Số điện thoại chuẩn 10 số hoặc có dấu phân cách."""
    assert rules.chuan_hoa_dien_thoai('0901234567') == '0901234567'
    assert rules.chuan_hoa_dien_thoai('0901.234.567') == '0901234567'
    assert rules.chuan_hoa_dien_thoai('0901 234 567') == '0901234567'


def test_sdt_gia_tri_bien():
    """LOẠI 2 — GIÁ TRỊ BIÊN: Số có mã quốc tế 84 hoặc +84 quy đổi đúng về 10 số."""
    # Biên tiền tố quốc tế +84 (12 ký tự) -> về đúng 10 số
    assert rules.chuan_hoa_dien_thoai('+84901234567') == '0901234567'
    # Biên tiền tố quốc tế 84 (11 chữ số) -> về đúng 10 số
    assert rules.chuan_hoa_dien_thoai('84901234567') == '0901234567'


def test_sdt_du_lieu_sai():
    """LOẠI 3 — DỮ LIỆU SAI: Số thiếu chữ số, thừa chữ số, chứa chữ cái hoặc để trống."""
    assert rules.chuan_hoa_dien_thoai('09012345') is None         # 8 số (thiếu)
    assert rules.chuan_hoa_dien_thoai('090123456789') is None     # 12 số không phải mã vùng (thừa)
    assert rules.chuan_hoa_dien_thoai('0901abc567') is None       # Chứa chữ cái
    assert rules.chuan_hoa_dien_thoai('') is None                 # Chuỗi rỗng
    assert rules.chuan_hoa_dien_thoai('nan') is None              # Chuỗi nan


# ============================================================================
# 3. KIỂM THỬ HÀM chuan_hoa_ho_ten()
# ============================================================================
def test_ho_ten_luong_dung():
    """LOẠI 1 — LUỒNG ĐÚNG: Chuẩn hóa Title Case và xóa khoảng trắng thừa."""
    assert rules.chuan_hoa_ho_ten('  nguyễn   văn   an  ') == 'Nguyễn Văn An'
    assert rules.chuan_hoa_ho_ten('TRẦN THỊ BÌNH') == 'Trần Thị Bình'


def test_ho_ten_gia_tri_bien():
    """LOẠI 2 — GIÁ TRỊ BIÊN: Tên chỉ gồm 1 từ hoặc có dấu gạch ngang/tiếng Việt."""
    assert rules.chuan_hoa_ho_ten('bảo') == 'Bảo'
    assert rules.chuan_hoa_ho_ten('ĐẶNG LÊ NGUYÊN VŨ') == 'Đặng Lê Nguyên Vũ'


def test_ho_ten_du_lieu_sai():
    """LOẠI 3 — DỮ LIỆU SAI: Họ tên để trống hoặc toàn khoảng trắng."""
    assert rules.chuan_hoa_ho_ten('') is None
    assert rules.chuan_hoa_ho_ten('   ') is None
    assert rules.chuan_hoa_ho_ten('None') is None


# ============================================================================
# 4. KIỂM THỬ HÀM doc_ngay()
# ============================================================================
def test_doc_ngay_cac_dinh_dang():
    """Kiểm tra đọc ngày đúng theo 3 khuôn dạng thực tế của dữ liệu."""
    assert rules.doc_ngay('2025-05-15') == date(2025, 5, 15)
    assert rules.doc_ngay('15/05/2025') == date(2025, 5, 15)
    assert rules.doc_ngay('2025.05.15') == date(2025, 5, 15)
    assert rules.doc_ngay('sai-dinh-dang') is None
    assert rules.doc_ngay('') is None


# ============================================================================
# 5. KIỂM THỬ HÀM CHE MẶT NẠ PII (NFR05)
# ============================================================================
def test_che_mat_na_pii():
    """Kiểm tra che mặt nạ SĐT và Email bảo vệ PII (NFR05)."""
    assert rules.che_mat_na_sdt('0901234567') == '0901***567'
    assert rules.che_mat_na_email('trungbao@gmail.com') == 't***@gmail.com'
