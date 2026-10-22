"""PHA 2 — TRANSFORM RULES: Các quy tắc làm sạch và chuẩn hóa dữ liệu.

NGUYÊN TẮC VÀNG: Mọi hàm trong mô-đun này đều là HÀM THUẦN (Pure Functions).
Không đọc ghi CSDL, không đọc tập tin, không biết HTTP.
Nhờ đó các hàm có thể được kiểm thử đơn vị cực kỳ nhanh và ổn định bằng Pytest.
"""
import re
import unicodedata
from datetime import date, datetime
import pandas as pd

# Các định dạng ngày có trong dữ liệu Mekong Mobile
DINH_DANG_NGAY = ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y.%m.%d', '%d-%m-%y')

# Biểu thức chính quy kiểm tra định dạng email chuẩn
REGEX_EMAIL = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


def _rong(gia_tri) -> bool:
    """Kiểm tra xem một giá trị có phải là RỖNG (missing) hay không.

    Xử lý an toàn mọi dạng rỗng trong thực tế:
      - `None`
      - Chuỗi rỗng hoặc chỉ có khoảng trắng
      - `NaN` của numpy, `NaT` của pandas, và `pd.NA` của kiểu nullable
      - Chuỗi ghi lại dạng text: 'nan', 'nat', 'none', '<na>', 'null'
    """
    if gia_tri is None:
        return True
    try:
        if bool(pd.isna(gia_tri)):
            return True
    except (TypeError, ValueError):
        pass
    return str(gia_tri).strip().lower() in ('', 'nan', 'none', 'nat', '<na>', 'null')


def chuan_hoa_dien_thoai(tho) -> str | None:
    """Chuẩn hóa số điện thoại về định dạng 10 chữ số bắt đầu bằng 0 (0xxxxxxxxx).

    Xử lý 4 định dạng phổ biến trong dữ liệu khách hàng Mekong Mobile:
      1. Đã chuẩn: '0912345678'
      2. Chứa dấu chấm hoặc khoảng trắng: '0912.345.678', '0912 345 678'
      3. Mã quốc tế có dấu cộng: '+84912345678'
      4. Mã quốc tế không dấu cộng: '84912345678'

    Trả về:
      - Chuỗi 10 chữ số (ví dụ: '0912345678') nếu hợp lệ.
      - `None` nếu số điện thoại rỗng hoặc không thể chuẩn hóa về 10 chữ số.
    """
    if _rong(tho):
        return None

    s = str(tho).strip()
    # Loại bỏ toàn bộ ký tự không phải chữ số
    chu_so = re.sub(r'\D', '', s)

    # Chuyển đầu 84xxxxxxxxx (11 số) thành 0xxxxxxxxx (10 số)
    if chu_so.startswith('84') and len(chu_so) == 11:
        chu_so = '0' + chu_so[2:]

    # Kiểm tra độ dài hợp lệ chính xác 10 chữ số và bắt đầu bằng số 0
    if len(chu_so) == 10 and chu_so.startswith('0'):
        return chu_so

    return None


def chuan_hoa_ho_ten(tho) -> str | None:
    """Chuẩn hóa họ tên khách hàng về định dạng Title Case và loại bỏ khoảng trắng thừa.

    Ví dụ:
      '  nguyễn  văn a ' -> 'Nguyễn Văn A'
      'LÊ THỊ B' -> 'Lê Thị B'

    Trả về:
      - Chuỗi họ tên chuẩn hóa nếu hợp lệ.
      - `None` nếu trường họ tên bị rỗng.
    """
    if _rong(tho):
        return None

    s = str(tho).strip()
    # Gộp nhiều khoảng trắng liên tiếp thành một khoảng trắng đơn
    s = re.sub(r'\s+', ' ', s)

    # Chuẩn hóa về Title Case (viết hoa chữ cái đầu mỗi từ)
    # Dùng title() kết hợp xử lý tiếng Việt
    tu_danh_sach = [tu.capitalize() for tu in s.split(' ')]
    return ' '.join(tu_danh_sach)


def chuan_hoa_email(tho) -> str | None:
    """Chuẩn hóa địa chỉ email về chữ thường và kiểm tra tính hợp lệ.

    Trả về:
      - Email đã chuẩn hóa dạng chữ thường nếu hợp lệ.
      - `None` nếu email rỗng hoặc sai cấu trúc cú pháp.
    """
    if _rong(tho):
        return None

    s = str(tho).strip().lower()
    if REGEX_EMAIL.match(s):
        return s
    return None


def doc_ngay(tho) -> date | None:
    """Thử lần lượt các định dạng ngày đã biết để chuyển đổi về kiểu date.

    Trả về:
      - Đối tượng datetime.date nếu phân tích cú pháp thành công.
      - `None` nếu giá trị rỗng hoặc không khớp với bất kỳ định dạng nào.
    """
    if _rong(tho):
        return None

    s = str(tho).strip()
    for dinh_dang in DINH_DANG_NGAY:
        try:
            return datetime.strptime(s, dinh_dang).date()
        except ValueError:
            continue
    return None


def che_mat_na_sdt(sdt: str | None) -> str:
    """Che mặt nạ số điện thoại để bảo vệ thông tin định danh cá nhân (PII - NFR05).

    Ví dụ: '0912345678' -> '0912***678'
    """
    if not sdt or len(sdt) < 7:
        return '***'
    return sdt[:4] + '***' + sdt[-3:]


def che_mat_na_email(email: str | None) -> str:
    """Che mặt nạ địa chỉ email để bảo vệ thông tin định danh cá nhân (PII - NFR05).

    Ví dụ: 'trungbao@gmail.com' -> 't***@gmail.com'
    """
    if not email or '@' not in email:
        return '***'
    ten_hop_thu, domain = email.split('@', 1)
    if len(ten_hop_thu) <= 1:
        return f'*@{domain}'
    return f'{ten_hop_thu[0]}***@{domain}'
