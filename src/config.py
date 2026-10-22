"""Mô-đun quản lý cấu hình và ngưỡng chất lượng dữ liệu."""
import os
import pathlib
import yaml
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

GOC = pathlib.Path(__file__).resolve().parent.parent

# Ngưỡng chất lượng mặc định nếu không tìm thấy tập tin cấu hình
NGUONG_MAC_DINH = {
    'do_day_du': {
        'customers.customer_id': 1.00,
        'customers.ho_ten': 0.98,
        'customers.so_dien_thoai': 0.98,
        'customers.email': 0.50,
    },
    'do_chinh_xac': {
        'sdt_chuan_hoa_duoc': 0.95,
        'ho_ten_chuan_hoa_duoc': 0.98,
        'email_dung_dinh_dang': 0.95,
        'ngay_dang_ky_hop_le': 0.98,
    },
    'do_nhat_quan': {
        'ty_le_sdt_duy_nhat': 0.70,
    },
    'nguong_dung_pipeline': {
        'chan_khi_that_bai': False,
    }
}


def nap_nguong(duong_dan_yaml: pathlib.Path | None = None) -> dict:
    """Nạp các ngưỡng kiểm định chất lượng dữ liệu từ tập tin YAML."""
    if duong_dan_yaml is None:
        duong_dan_yaml = GOC / 'configs' / 'config.example.yaml'

    if duong_dan_yaml.exists():
        try:
            with open(duong_dan_yaml, 'r', encoding='utf-8') as f:
                cau_hinh = yaml.safe_load(f)
                if isinstance(cau_hinh, dict):
                    return cau_hinh
        except Exception:
            pass
    return NGUONG_MAC_DINH


def duong_dan_du_lieu() -> pathlib.Path:
    """Trả về đường dẫn chứa tập tin dữ liệu khách hàng thô."""
    env_dir = os.environ.get('DATA_DIR')
    if env_dir:
        p = pathlib.Path(env_dir)
        if not p.is_absolute():
            p = GOC / p
        return p
    return GOC / 'data' / 'raw'


def duong_dan_db() -> pathlib.Path:
    """Trả về đường dẫn tập tin cơ sở dữ liệu SQLite kho dữ liệu."""
    env_url = os.environ.get('DATABASE_URL', '')
    if env_url.startswith('sqlite:///'):
        rel = env_url.replace('sqlite:///', '')
        p = pathlib.Path(rel)
        if not p.is_absolute():
            p = GOC / p
        return p
    return GOC / 'data' / 'processed' / 'warehouse.db'


def duong_dan_bao_cao() -> pathlib.Path:
    """Trả về đường dẫn thư mục lưu báo cáo chất lượng sinh tự động."""
    env_dir = os.environ.get('REPORTS_DIR', 'reports')
    p = pathlib.Path(env_dir)
    if not p.is_absolute():
        p = GOC / p
    return p
