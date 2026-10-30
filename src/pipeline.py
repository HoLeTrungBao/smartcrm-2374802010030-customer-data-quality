"""ĐIỀU PHỐI PIPELINE ETL & KIỂM ĐỊNH CHẤT LƯỢNG DỮ LIỆU KHÁCH HÀNG (LUỒNG L7)

Kiến trúc 4 pha: EXTRACT -> TRANSFORM -> QUALITY -> LOAD.

Bốn quyết định thiết kế cốt lõi:
  1. Kiểm định chất lượng chạy TRƯỚC KHI NẠP vào kho dữ liệu sạch.
  2. Không nuốt lỗi: dòng không làm sạch được chuyển vào bảng reject_rows kèm lý do cụ thể.
  3. Báo cáo chất lượng Markdown và JSON LUÔN được sinh tự động sau mỗi phiên chạy.
  4. Tính Idempotent: chạy lại lần 2 trên cùng dữ liệu đầu vào không làm nhân đôi số bản ghi.
"""
import argparse
import json
import logging
import os
import pathlib
import sys
from datetime import datetime

from src import config, db
from src.extract import read_sources
from src.transform import clean_customers
from src.quality import checks
from src.load import load_staging, load_warehouse

logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', 'INFO'),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
log = logging.getLogger('pipeline')


def sinh_ma_lo(tu_ngay=None, den_ngay=None) -> str:
    """Sinh mã lô xác định theo phạm vi dữ liệu, không sinh theo dấu thời gian ngẫu nhiên.

    Giúp đảm bảo tính Chạy lại được (Idempotent): Cùng một phạm vi nạp sẽ dùng lại
    đúng mã lô đó để thay thế an toàn dữ liệu cũ.
    """
    if tu_ngay or den_ngay:
        return f"lo-{tu_ngay or 'dau'}_{den_ngay or 'cuoi'}"
    return 'lo-toan-bo'


def viet_bao_cao_md(bao_cao: dict, duong_dan: pathlib.Path) -> None:
    """Xuất báo cáo đánh giá chất lượng dữ liệu ra định dạng Markdown."""
    lines = [
        '# Báo cáo kết quả kiểm định & làm sạch dữ liệu khách hàng (Luồng L7)',
        '',
        f"- **Mã lô kiểm định:** `{bao_cao['ma_lo']}`",
        f"- **Thời gian thực hiện:** {bao_cao['bat_dau']}",
        f"- **Kết luận chung:** **{bao_cao['ket_luan']}**",
        ''
    ]

    if bao_cao.get('loi'):
        lines += [f"- **Thông báo lỗi:** `{bao_cao['loi']}`", '']

    lines += [
        '## 1. Thống kê số lượng bản ghi qua các pha xử lý',
        '',
        '| Pha xử lý | Trạng thái | Số lượng dòng xử lý |',
        '| :--- | :---: | :--- |'
    ]
    for pha in bao_cao['cac_pha']:
        lines.append(f"| {pha['pha']} | {pha['trang_thai']} | {json.dumps(pha.get('so_dong', {}), ensure_ascii=False)} |")

    lines += [
        '',
        '## 2. Kết quả đo lường 3 chiều chất lượng dữ liệu',
        '',
        '| Chiều chất lượng | Chỉ tiêu kiểm định | Số lượng kiểm | Số lượng đạt | Số lượng lỗi | Tỷ lệ đạt | Ngưỡng yêu cầu | Đánh giá |',
        '| :--- | :--- | ---: | ---: | ---: | ---: | ---: | :---: |'
    ]
    for m in bao_cao['ket_qua_kiem']:
        danh_gia = '✅ **ĐẠT**' if m['dat'] else '❌ **KHÔNG ĐẠT**'
        lines.append(
            f"| {m['chieu']} | `{m['doi_tuong']}` | {m['so_kiem']:,} | "
            f"{m['so_dat']:,} | {m['so_loi']:,} | {m['ti_le']:.2%} | "
            f"{m['nguong']:.2%} | {danh_gia} |"
        )

    khong_dat = [m for m in bao_cao['ket_qua_kiem'] if not m['dat']]
    lines += [
        '',
        f"**Tổng kết:** {len(bao_cao['ket_qua_kiem'])} phép đo chất lượng ({len(khong_dat)} phép đo dưới ngưỡng).",
        ''
    ]

    if bao_cao.get('reject_theo_quy_tac'):
        lines += [
            '## 3. Thống kê bản ghi đưa vào bảng từ chối (Reject Rows)',
            '',
            '| Quy tắc vi phạm | Số lượng bản ghi bị từ chối |',
            '| :--- | ---: |'
        ]
        for k, v in sorted(bao_cao['reject_theo_quy_tac'].items()):
            lines.append(f"| `{k}` | {v:,} dòng |")
        lines += [
            '',
            f"**Tổng cộng có {bao_cao['so_dong_reject']:,} bản ghi** không thể tự động chuẩn hóa.",
            "Tất cả các bản ghi này đều được lưu giữ nguyên vẹn trong bảng `reject_rows` kèm lý do lỗi cụ thể để nhân viên đối soát.",
            ''
        ]

    if bao_cao.get('so_dong_kho_du_lieu'):
        lines += [
            '## 4. Trạng thái các bảng trong Kho dữ liệu sau khi nạp',
            '',
            '| Tên bảng trong Kho dữ liệu | Tổng số bản ghi hiện có |',
            '| :--- | ---: |'
        ]
        for ten_bang, so_luong in bao_cao['so_dong_kho_du_lieu'].items():
            lines.append(f"| `{ten_bang}` | {so_luong:,} bản ghi |")
        lines += ['']

    duong_dan.parent.mkdir(parents=True, exist_ok=True)
    duong_dan.write_text('\n'.join(lines), encoding='utf-8')
    log.info("Đã xuất báo cáo Markdown thành công tại: %s", duong_dan)


def viet_bao_cao_json(bao_cao: dict, duong_dan: pathlib.Path) -> None:
    """Xuất báo cáo định dạng JSON phục vụ tích hợp dashboard hoặc API."""
    duong_dan.parent.mkdir(parents=True, exist_ok=True)
    duong_dan.write_text(json.dumps(bao_cao, ensure_ascii=False, indent=2), encoding='utf-8')
    log.info("Đã xuất báo cáo JSON thành công tại: %s", duong_dan)


def chay(tu_ngay=None, den_ngay=None, chi_kiem: bool = False, khoi_tao_csdl: bool = False, xuat_bao_cao: bool = False) -> tuple[dict, int]:
    """Điều phối thực thi toàn bộ pipeline."""
    ma_lo = sinh_ma_lo(tu_ngay, den_ngay)
    dau_thoi_gian = datetime.now().strftime('%Y%m%d_%H%M%S')
    bao_cao = {
        'ma_lo': ma_lo,
        'bat_dau': datetime.now().isoformat(timespec='seconds'),
        'cac_pha': [],
        'ket_qua_kiem': [],
        'ket_luan': 'ĐANG_XỬ_LÝ'
    }

    thu_muc_bao_cao = config.duong_dan_bao_cao()
    ma_thoat = 0

    try:
        nguong = config.nap_nguong()
        thu_muc_du_lieu = config.duong_dan_du_lieu()
        log.info("=== BẮT ĐẦU CHẠY PIPELINE (Mã lô: %s) ===", ma_lo)

        # Khởi tạo CSDL nếu được yêu cầu
        if khoi_tao_csdl or not config.duong_dan_db().exists():
            log.info("Khởi tạo cấu trúc bảng cơ sở dữ liệu kho...")
            db.khoi_tao_kho_du_lieu()

        # ---------- PHA 1: EXTRACT ----------
        log.info("--- PHA 1: EXTRACT (Trích xuất dữ liệu) ---")
        nguon = read_sources.doc_tat_ca(thu_muc_du_lieu)
        df_khach_hang_tho = nguon['customers']
        bao_cao['cac_pha'].append({
            'pha': 'EXTRACT',
            'trang_thai': 'THANH_CONG',
            'so_dong': {'customers_raw': len(df_khach_hang_tho)}
        })

        # ---------- PHA 2: TRANSFORM ----------
        log.info("--- PHA 2: TRANSFORM (Làm sạch & Gán nhãn lỗi) ---")
        df_sach, df_reject = clean_customers.xu_ly_lam_sach_khach_hang(df_khach_hang_tho)
        bao_cao['cac_pha'].append({
            'pha': 'TRANSFORM',
            'trang_thai': 'THANH_CONG',
            'so_dong': {
                'khach_hang_sach': len(df_sach),
                'khach_hang_reject': len(df_reject)
            }
        })
        bao_cao['so_dong_reject'] = len(df_reject)
        if not df_reject.empty:
            bao_cao['reject_theo_quy_tac'] = df_reject['ma_quy_tac'].value_counts().to_dict()

        # ---------- PHA 3: QUALITY ----------
        log.info("--- PHA 3: QUALITY (Đo lường 3 chiều chất lượng) ---")
        danh_sach_do = checks.do_tat_ca(df_khach_hang_tho, df_sach, nguong)
        bao_cao['ket_qua_kiem'] = [m.as_dict() for m in danh_sach_do]

        khong_dat = [m for m in danh_sach_do if not m.dat]
        co_loi_chat_luong = len(khong_dat) > 0

        bao_cao['cac_pha'].append({
            'pha': 'QUALITY',
            'trang_thai': 'CANH_BAO' if co_loi_chat_luong else 'THANH_CONG',
            'so_phep_do': len(danh_sach_do),
            'so_khong_dat': len(khong_dat)
        })

        # Kiểm tra ngưỡng chặn nạp dữ liệu
        chan_khi_that_bai = nguong.get('nguong_dung_pipeline', {}).get('chan_khi_that_bai', False)
        chan_env = os.environ.get('BLOCK_ON_QUALITY_FAILURE', '').lower() == 'true'
        if co_loi_chat_luong and (chan_khi_that_bai or chan_env):
            log.warning("Chất lượng dữ liệu không đạt ngưỡng. DỪNG PIPELINE KHÔNG NẠP KHO!")
            bao_cao['ket_luan'] = 'DUNG_VI_CHAT_LUONG_KHONG_DAT'
            ma_thoat = 2
            return bao_cao, ma_thoat

        # ---------- PHA 4: LOAD ----------
        if chi_kiem:
            log.info("Chế độ --chi-kiem được bật: Bỏ qua nạp vào CSDL kho dữ liệu.")
            bao_cao['cac_pha'].append({'pha': 'LOAD', 'trang_thai': 'BO_QUA'})
            bao_cao['ket_luan'] = 'KIEM_DINH_HOAN_TAT'
            return bao_cao, 0

        log.info("--- PHA 4: LOAD (Nạp vào CSDL kho Star Schema) ---")
        conn = db.lay_ket_noi()
        try:
            # 1. Nạp staging, reject và kết quả đo
            load_staging.nap_staging(conn, df_khach_hang_tho, ma_lo)
            load_staging.nap_reject(conn, df_reject, ma_lo)
            load_staging.nap_do_chat_luong(conn, danh_sach_do, ma_lo)

            # 2. Khởi tạo quy tắc và phiên chạy
            load_warehouse.khoi_tao_quy_tac_chuan(conn)
            run_key = load_warehouse.tao_phien_chay(conn, ma_lo, len(df_khach_hang_tho))

            # 3. Nạp Dimension và Fact
            anh_xa_kh = load_warehouse.nap_dim_customer(conn, df_sach)
            load_warehouse.nap_fact_quality(conn, df_sach, anh_xa_kh, run_key)

            # Đếm số dòng thực tế trong các bảng đích để đối soát
            so_dong_bang = {}
            for bang in ['staging_customers', 'reject_rows', 'dim_customer', 'fact_customer_quality_audit']:
                cur = conn.execute(f"SELECT COUNT(*) as cnt FROM {bang};")
                so_dong_bang[bang] = cur.fetchone()['cnt']
            bao_cao['so_dong_kho_du_lieu'] = so_dong_bang

            bao_cao['cac_pha'].append({
                'pha': 'LOAD',
                'trang_thai': 'THANH_CONG',
                'so_dong': so_dong_bang
            })
            bao_cao['ket_luan'] = 'HOAN_TAT_THANH_CONG'
            log.info("=== PIPELINE HOÀN TẤT THÀNH CÔNG ===")
        finally:
            conn.close()

    except Exception as e:
        log.exception("LỖI HỆ THỐNG KHI THỰC THI PIPELINE: %s", e)
        bao_cao['ket_luan'] = 'LOI_HE_THONG'
        bao_cao['loi'] = str(e)
        ma_thoat = 1
    finally:
        # Chỉ xuất báo cáo ra đĩa khi có cờ --xuat-bao-cao
        if xuat_bao_cao:
            thu_muc_bao_cao.mkdir(parents=True, exist_ok=True)
            tep_md = thu_muc_bao_cao / f"chat-luong-{ma_lo}-{dau_thoi_gian}.md"
            tep_json = thu_muc_bao_cao / f"chat-luong-{ma_lo}-{dau_thoi_gian}.json"
            viet_bao_cao_md(bao_cao, tep_md)
            viet_bao_cao_json(bao_cao, tep_json)

    return bao_cao, ma_thoat


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pipeline kiểm định và làm sạch dữ liệu khách hàng (Luồng L7)")
    parser.add_argument('--tu-ngay', help="Ngày bắt đầu phạm vi lọc dữ liệu (YYYY-MM-DD)")
    parser.add_argument('--den-ngay', help="Ngày kết thúc phạm vi lọc dữ liệu (YYYY-MM-DD)")
    parser.add_argument('--chi-kiem', action='store_true', help="Chỉ đo lường chất lượng, không nạp vào CSDL kho")
    parser.add_argument('--khoi-tao-db', action='store_true', help="Khởi tạo hoặc tạo lại cấu trúc bảng trong CSDL")
    parser.add_argument('--xuat-bao-cao', action='store_true', help="Tùy chọn xuất báo cáo markdown/json ra thư mục reports/")

    args = parser.parse_args()
    _, exit_code = chay(
        tu_ngay=args.tu_ngay,
        den_ngay=args.den_ngay,
        chi_kiem=args.chi_kiem,
        khoi_tao_csdl=args.khoi_tao_db,
        xuat_bao_cao=args.xuat_bao_cao
    )
    sys.exit(exit_code)
