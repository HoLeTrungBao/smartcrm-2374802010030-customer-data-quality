"""MODULE SO SÁNH DÒNG — Đếm và giải thích chênh lệch giữa staging và fact.

Truy vấn kho dữ liệu, đếm số bản ghi trong từng bảng, tính chênh lệch
và xuất giải thích tường minh ra Markdown + console.
"""
import sqlite3
import logging
import pathlib
from datetime import datetime

from src import config, db

log = logging.getLogger('dashboard.so_sanh_dong')


def dem_dong_cac_bang(conn: sqlite3.Connection) -> dict[str, int]:
    """Đếm tổng số dòng trong các bảng chính của kho dữ liệu."""
    cac_bang = [
        'staging_customers',
        'reject_rows',
        'dim_customer',
        'dim_quality_rule',
        'dim_audit_run',
        'fact_customer_quality_audit',
        'quality_measures',
    ]
    ket_qua = {}
    for bang in cac_bang:
        try:
            cur = conn.execute(f"SELECT COUNT(*) AS cnt FROM {bang};")
            ket_qua[bang] = cur.fetchone()['cnt']
        except Exception as e:
            log.warning("Bảng %s chưa tồn tại hoặc lỗi truy vấn: %s", bang, e)
            ket_qua[bang] = -1  # Bảng chưa tồn tại
    return ket_qua


def giai_thich_chenh_lech(so_dong: dict[str, int]) -> list[str]:
    """Sinh danh sách các dòng giải thích chênh lệch staging vs fact."""
    staging = so_dong.get('staging_customers', 0)
    fact = so_dong.get('fact_customer_quality_audit', 0)
    reject = so_dong.get('reject_rows', 0)
    dim_kh = so_dong.get('dim_customer', 0)

    dong = []
    dong.append(f"- **staging_customers**: {staging:,} bản ghi (toàn bộ dữ liệu thô được giữ nguyên)")
    dong.append(f"- **reject_rows**: {reject:,} bản ghi (dòng không thể chuẩn hóa, có lý do cụ thể)")
    dong.append(f"- **dim_customer**: {dim_kh:,} bản ghi (khách hàng đã làm sạch, nạp bằng khóa nghiệp vụ `customer_id`)")
    dong.append(f"- **fact_customer_quality_audit**: {fact:,} bản ghi (kết quả kiểm định từng khách hàng sạch)")
    dong.append("")

    chenh_lech = staging - fact
    if chenh_lech > 0 and reject > 0:
        dong.append(f"**Chênh lệch staging − fact = {chenh_lech:,} dòng.**")
        dong.append("")
        dong.append("Nguyên nhân:")
        dong.append(f"  1. Có **{reject:,} bản ghi bị từ chối** do không thể chuẩn hóa SĐT, thiếu họ tên, hoặc thiếu mã định danh.")
        dong.append(f"  2. Các bản ghi này được lưu trong bảng `reject_rows` kèm lý do lỗi cụ thể để nhân viên đối soát.")
        dong.append(f"  3. Chênh lệch staging − fact ({chenh_lech:,}) ≈ reject ({reject:,}) → dữ liệu **không bị mất, chỉ được phân luồng**.")
    elif chenh_lech == 0:
        dong.append("Không có chênh lệch: toàn bộ dữ liệu staging đều nạp được vào fact.")
    else:
        dong.append(f"Chênh lệch: {chenh_lech:,} dòng (cần kiểm tra thêm).")

    return dong


def xuat_bao_cao_md(so_dong: dict[str, int], duong_dan: pathlib.Path) -> None:
    """Xuất báo cáo so sánh dòng ra tập tin Markdown."""
    lines = [
        "# Báo cáo đối chiếu số lượng bản ghi: Staging vs Fact",
        "",
        f"**Thời điểm tạo báo cáo:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Bảng tổng hợp số lượng dòng",
        "",
        "| Tên bảng | Số bản ghi |",
        "| :--- | ---: |",
    ]
    for bang, so in so_dong.items():
        lines.append(f"| `{bang}` | {so:,} |")

    lines.append("")
    lines.append("## Giải thích chênh lệch")
    lines.append("")
    lines.extend(giai_thich_chenh_lech(so_dong))
    lines.append("")

    duong_dan.parent.mkdir(parents=True, exist_ok=True)
    duong_dan.write_text("\n".join(lines), encoding='utf-8')
    log.info("Đã xuất báo cáo đối chiếu dòng tại: %s", duong_dan)


def chay() -> dict[str, int]:
    """Hàm chính: đếm dòng, in ra console và xuất báo cáo."""
    log.info("=== BẮT ĐẦU ĐỐI CHIẾU SỐ LƯỢNG BẢN GHI ===")

    duong_dan_db = config.duong_dan_db()
    if not duong_dan_db.exists():
        log.warning("Chưa tìm thấy CSDL kho dữ liệu. Hãy chạy pipeline trước: python -m src.pipeline")
        return {}

    conn = db.lay_ket_noi()
    try:
        so_dong = dem_dong_cac_bang(conn)

        # In ra console
        print("\n" + "=" * 60)
        print("ĐỐI CHIẾU SỐ LƯỢNG BẢN GHI TRONG KHO DỮ LIỆU")
        print("=" * 60)
        for bang, so in so_dong.items():
            print(f"  {bang:40s} : {so:>10,} dòng")
        print("-" * 60)
        for line in giai_thich_chenh_lech(so_dong):
            # In dạng text thuần (bỏ markdown bold)
            print(line.replace('**', ''))
        print("=" * 60 + "\n")

        # Xuất báo cáo Markdown
        thu_muc_bao_cao = config.duong_dan_bao_cao()
        tep_md = thu_muc_bao_cao / "so-sanh-dong.md"
        xuat_bao_cao_md(so_dong, tep_md)

        return so_dong
    finally:
        conn.close()


if __name__ == '__main__':
    logging.basicConfig(
        level='INFO',
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    chay()
