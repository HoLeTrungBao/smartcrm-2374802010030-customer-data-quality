"""MODULE BIỂU ĐỒ PHÂN TÍCH — Dựng 2 biểu đồ gắn câu hỏi phân tích nghiệp vụ.

Biểu đồ 1: Phân bổ lỗi chất lượng theo quy tắc DQ (Bar Chart).
Biểu đồ 2: Tỷ lệ khách hàng trùng lặp vs duy nhất (Pie Chart).

Mỗi biểu đồ đều có:
  - Câu hỏi phân tích gắn kèm
  - Mốc tham chiếu (ngưỡng chuẩn)
  - Dòng ghi nguồn và thời điểm dữ liệu
  - Xử lý 3 trạng thái: đang tải / rỗng / lỗi
"""
import sqlite3
import logging
import pathlib
from datetime import datetime

import matplotlib
matplotlib.use('Agg')  # Chế độ không hiển thị cửa sổ — phù hợp chạy headless
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from src import config, db

log = logging.getLogger('dashboard.bieu_do')

# Cấu hình font hỗ trợ tiếng Việt
plt.rcParams.update({
    'font.size': 11,
    'axes.unicode_minus': False,
})


# ---------------------------------------------------------------------------
# HÀM HỖ TRỢ TRẠNG THÁI RỖNG VÀ LỖI
# ---------------------------------------------------------------------------

def _tao_hinh_thong_bao(thong_bao: str, duong_dan: pathlib.Path, *, la_loi: bool = False) -> pathlib.Path:
    """Tạo hình ảnh placeholder với thông báo khi không có dữ liệu hoặc gặp lỗi.

    Trả về đường dẫn file ảnh đã lưu.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    mau_nen = '#fff3cd' if not la_loi else '#f8d7da'
    mau_chu = '#856404' if not la_loi else '#721c24'
    fig.patch.set_facecolor(mau_nen)

    ax.text(
        0.5, 0.5, thong_bao,
        ha='center', va='center',
        fontsize=14, color=mau_chu,
        wrap=True,
        bbox=dict(boxstyle='round,pad=0.8', facecolor='white', edgecolor=mau_chu, alpha=0.8)
    )

    duong_dan.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(duong_dan), dpi=150, bbox_inches='tight')
    plt.close(fig)
    log.info("Đã tạo hình thông báo tại: %s", duong_dan)
    return duong_dan


# ---------------------------------------------------------------------------
# BIỂU ĐỒ 1: PHÂN BỔ LỖI CHẤT LƯỢNG THEO QUY TẮC DQ
# ---------------------------------------------------------------------------

def bieu_do_loi_dq(
    conn: sqlite3.Connection,
    duong_dan_anh: pathlib.Path,
    *,
    tu_ngay: str | None = None,
    den_ngay: str | None = None,
) -> pathlib.Path:
    """Vẽ biểu đồ cột phân bổ lỗi theo từng quy tắc DQ.

    Câu hỏi phân tích: "Phân bổ lỗi chất lượng dữ liệu khách hàng theo
    từng quy tắc DQ như thế nào? Quy tắc nào bị vi phạm nhiều nhất?"

    Xử lý 3 trạng thái:
      - Đang tải: log thông báo trước khi truy vấn
      - Rỗng: trả về hình placeholder giải thích
      - Lỗi: trả về hình placeholder lỗi
    """
    log.info("Đang truy vấn dữ liệu từ kho để tạo biểu đồ phân bổ lỗi DQ...")

    try:
        # Truy vấn dữ liệu reject phân nhóm theo quy tắc
        sql = "SELECT ma_quy_tac, COUNT(*) AS so_luong FROM reject_rows"
        dieu_kien = []
        tham_so: list = []

        if tu_ngay:
            dieu_kien.append("ngay_nap >= ?")
            tham_so.append(tu_ngay)
        if den_ngay:
            dieu_kien.append("ngay_nap <= ?")
            tham_so.append(den_ngay)

        if dieu_kien:
            sql += " WHERE " + " AND ".join(dieu_kien)
        sql += " GROUP BY ma_quy_tac ORDER BY so_luong DESC;"

        cur = conn.execute(sql, tham_so)
        du_lieu = cur.fetchall()

        # TRẠNG THÁI RỖNG
        if not du_lieu:
            thong_bao = ("Không có dữ liệu bản ghi bị từ chối trong khoảng thời gian đã chọn.\n"
                         "Vui lòng thử khoảng ngày khác hoặc chạy pipeline trước.")
            return _tao_hinh_thong_bao(thong_bao, duong_dan_anh)

        ten_quy_tac = [row['ma_quy_tac'] for row in du_lieu]
        so_luong = [row['so_luong'] for row in du_lieu]
        tong_reject = sum(so_luong)

        # Lấy tổng staging để tính mốc tham chiếu
        cur_stg = conn.execute("SELECT COUNT(*) AS cnt FROM staging_customers;")
        tong_staging = cur_stg.fetchone()['cnt']

        # Vẽ biểu đồ
        fig, ax = plt.subplots(figsize=(10, 6))

        mau_sac = ['#e74c3c', '#e67e22', '#f39c12', '#3498db', '#2ecc71', '#9b59b6']
        bars = ax.bar(
            range(len(ten_quy_tac)), so_luong,
            color=[mau_sac[i % len(mau_sac)] for i in range(len(ten_quy_tac))],
            edgecolor='white', linewidth=0.8
        )

        # Ghi số lượng lên mỗi cột
        for bar, sl in zip(bars, so_luong):
            ax.text(
                bar.get_x() + bar.get_width() / 2, bar.get_height() + max(so_luong) * 0.02,
                f'{sl:,}', ha='center', va='bottom', fontsize=10, fontweight='bold'
            )

        ax.set_xticks(range(len(ten_quy_tac)))
        ax.set_xticklabels(ten_quy_tac, rotation=0, fontsize=10)
        ax.set_ylabel('So luong ban ghi bi tu choi', fontsize=11)

        # MỐC THAM CHIẾU: đường ngang 5% tổng staging (ngưỡng chấp nhận được)
        nguong_5_phan_tram = tong_staging * 0.05
        ax.axhline(y=nguong_5_phan_tram, color='#e74c3c', linestyle='--', linewidth=1.5, alpha=0.7)
        ax.text(
            len(ten_quy_tac) - 0.5, nguong_5_phan_tram * 1.05,
            f'Nguong 5% staging ({nguong_5_phan_tram:,.0f})',
            ha='right', va='bottom', fontsize=9, color='#e74c3c', fontstyle='italic'
        )

        # Tiêu đề gắn câu hỏi phân tích
        ax.set_title(
            'Cau hoi phan tich: Phan bo loi chat luong du lieu khach hang\n'
            'theo tung quy tac DQ nhu the nao? Quy tac nao bi vi pham nhieu nhat?',
            fontsize=12, fontweight='bold', pad=15
        )

        # DÒNG GHI NGUỒN VÀ THỜI ĐIỂM
        thoi_diem = datetime.now().strftime('%Y-%m-%d %H:%M')
        fig.text(
            0.5, 0.01,
            f'Nguon: customers_raw.csv | {tong_staging:,} ban ghi | '
            f'Reject: {tong_reject:,} ({tong_reject/tong_staging*100:.1f}%) | '
            f'Thoi diem: {thoi_diem}',
            ha='center', fontsize=9, color='gray', fontstyle='italic'
        )

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.tight_layout(rect=[0, 0.04, 1, 1])

        duong_dan_anh.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(str(duong_dan_anh), dpi=150, bbox_inches='tight')
        plt.close(fig)
        log.info("Đã lưu biểu đồ phân bổ lỗi DQ tại: %s", duong_dan_anh)
        return duong_dan_anh

    except Exception as e:
        log.exception("Lỗi khi tạo biểu đồ phân bổ lỗi DQ: %s", e)
        return _tao_hinh_thong_bao(
            f"Loi khi tao bieu do: {e}\nVui long kiem tra ket noi CSDL va chay lai.",
            duong_dan_anh, la_loi=True
        )


# ---------------------------------------------------------------------------
# BIỂU ĐỒ 2: TỶ LỆ KHÁCH HÀNG TRÙNG LẶP VS DUY NHẤT
# ---------------------------------------------------------------------------

def bieu_do_trung_lap(
    conn: sqlite3.Connection,
    duong_dan_anh: pathlib.Path,
    *,
    tu_ngay: str | None = None,
    den_ngay: str | None = None,
) -> pathlib.Path:
    """Vẽ biểu đồ tròn tỷ lệ trùng lặp vs duy nhất.

    Câu hỏi phân tích: "Tỷ lệ khách hàng trùng lặp so với khách hàng duy nhất
    là bao nhiêu? Mức độ trùng lặp có đáng lo ngại không?"

    Xử lý 3 trạng thái tương tự biểu đồ 1.
    """
    log.info("Đang truy vấn dữ liệu từ kho để tạo biểu đồ tỷ lệ trùng lặp...")

    try:
        # Truy vấn phân nhóm trùng lặp
        sql = """
            SELECT
                CASE WHEN is_duplicate = 1 THEN 'Trung lap' ELSE 'Duy nhat' END AS nhom,
                COUNT(*) AS so_luong
            FROM fact_customer_quality_audit f
        """
        dieu_kien = []
        tham_so: list = []

        if tu_ngay or den_ngay:
            sql += " JOIN dim_audit_run r ON f.run_key = r.run_key"
            if tu_ngay:
                dieu_kien.append("r.run_date >= ?")
                tham_so.append(tu_ngay)
            if den_ngay:
                dieu_kien.append("r.run_date <= ?")
                tham_so.append(den_ngay)
            if dieu_kien:
                sql += " WHERE " + " AND ".join(dieu_kien)

        sql += " GROUP BY nhom ORDER BY nhom;"

        cur = conn.execute(sql, tham_so)
        du_lieu = cur.fetchall()

        # TRẠNG THÁI RỖNG
        if not du_lieu:
            thong_bao = ("Khong co du lieu kiem dinh trong khoang thoi gian da chon.\n"
                         "Vui long thu khoang ngay khac hoac chay pipeline truoc.")
            return _tao_hinh_thong_bao(thong_bao, duong_dan_anh)

        nhan = [row['nhom'] for row in du_lieu]
        so_luong = [row['so_luong'] for row in du_lieu]
        tong = sum(so_luong)

        # Tính số trùng lặp và duy nhất
        trung_lap = 0
        duy_nhat = 0
        for n, sl in zip(nhan, so_luong):
            if 'Trung' in n:
                trung_lap = sl
            else:
                duy_nhat = sl

        # Vẽ biểu đồ
        fig, (ax_pie, ax_info) = plt.subplots(1, 2, figsize=(12, 5.5),
                                               gridspec_kw={'width_ratios': [1.2, 1]})

        mau_sac = ['#e74c3c', '#2ecc71']  # Đỏ = trùng, Xanh = duy nhất
        explode = (0.05, 0)

        wedges, texts, autotexts = ax_pie.pie(
            so_luong,
            labels=nhan,
            autopct='%1.1f%%',
            startangle=90,
            colors=mau_sac,
            explode=explode,
            textprops={'fontsize': 11},
            pctdistance=0.75
        )
        for at in autotexts:
            at.set_fontweight('bold')
            at.set_color('white')

        ax_pie.set_title(
            'Cau hoi phan tich:\nTy le khach hang trung lap so voi\n'
            'khach hang duy nhat la bao nhieu?',
            fontsize=11, fontweight='bold', pad=10
        )

        # Bảng thông tin bên phải
        ax_info.axis('off')
        thong_tin = [
            f"Tong khach hang da kiem dinh: {tong:,}",
            f"Khach hang duy nhat: {duy_nhat:,} ({duy_nhat/tong*100:.1f}%)",
            f"Khach hang trung lap: {trung_lap:,} ({trung_lap/tong*100:.1f}%)",
            "",
            "Moc tham chieu:",
            f"  Nguong chuan: <= 70% trung lap",
            f"  Hien tai: {trung_lap/tong*100:.1f}% trung lap",
        ]

        # Đánh giá
        if trung_lap / tong <= 0.70:
            thong_tin.append(f"  => DAT nguong (duoi 70%)")
            mau_danh_gia = '#27ae60'
        else:
            thong_tin.append(f"  => VUOT NGUONG (tren 70%)")
            mau_danh_gia = '#e74c3c'

        y_start = 0.85
        for i, dong in enumerate(thong_tin):
            mau = 'black'
            fw = 'normal'
            if 'DAT' in dong or 'VUOT' in dong:
                mau = mau_danh_gia
                fw = 'bold'
            if 'Moc tham chieu' in dong:
                fw = 'bold'
            ax_info.text(0.05, y_start - i * 0.1, dong, fontsize=10,
                        va='top', color=mau, fontweight=fw,
                        transform=ax_info.transAxes)

        # DÒNG GHI NGUỒN VÀ THỜI ĐIỂM
        thoi_diem = datetime.now().strftime('%Y-%m-%d %H:%M')
        fig.text(
            0.5, 0.01,
            f'Nguon: fact_customer_quality_audit | {tong:,} ban ghi | Thoi diem: {thoi_diem}',
            ha='center', fontsize=9, color='gray', fontstyle='italic'
        )

        fig.tight_layout(rect=[0, 0.04, 1, 1])
        duong_dan_anh.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(str(duong_dan_anh), dpi=150, bbox_inches='tight')
        plt.close(fig)
        log.info("Đã lưu biểu đồ tỷ lệ trùng lặp tại: %s", duong_dan_anh)
        return duong_dan_anh

    except Exception as e:
        log.exception("Lỗi khi tạo biểu đồ tỷ lệ trùng lặp: %s", e)
        return _tao_hinh_thong_bao(
            f"Loi khi tao bieu do: {e}\nVui long kiem tra ket noi CSDL va chay lai.",
            duong_dan_anh, la_loi=True
        )


# ---------------------------------------------------------------------------
# HÀM CHÍNH: TẠO TẤT CẢ BIỂU ĐỒ
# ---------------------------------------------------------------------------

def tao_tat_ca_bieu_do(
    *,
    tu_ngay: str | None = None,
    den_ngay: str | None = None,
) -> list[pathlib.Path]:
    """Tạo toàn bộ biểu đồ phân tích và lưu vào thư mục docs/.

    Trả về danh sách đường dẫn các file ảnh đã tạo.
    """
    log.info("=== BẮT ĐẦU TẠO BIỂU ĐỒ PHÂN TÍCH ===")

    duong_dan_db = config.duong_dan_db()
    if not duong_dan_db.exists():
        log.warning("Chưa tìm thấy CSDL kho dữ liệu. Hãy chạy pipeline trước: python -m src.pipeline")
        return []

    thu_muc_docs = config.GOC / 'docs'
    thu_muc_docs.mkdir(parents=True, exist_ok=True)

    conn = db.lay_ket_noi()
    ket_qua = []
    try:
        # Biểu đồ 1: Phân bổ lỗi DQ
        anh1 = bieu_do_loi_dq(
            conn,
            thu_muc_docs / 'bieu_do_loi_dq.png',
            tu_ngay=tu_ngay,
            den_ngay=den_ngay
        )
        ket_qua.append(anh1)

        # Biểu đồ 2: Tỷ lệ trùng lặp
        anh2 = bieu_do_trung_lap(
            conn,
            thu_muc_docs / 'bieu_do_trung_lap.png',
            tu_ngay=tu_ngay,
            den_ngay=den_ngay
        )
        ket_qua.append(anh2)

        log.info("=== ĐÃ TẠO XONG %d BIỂU ĐỒ ===", len(ket_qua))
        return ket_qua
    finally:
        conn.close()


if __name__ == '__main__':
    import argparse
    logging.basicConfig(
        level='INFO',
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    parser = argparse.ArgumentParser(description="Tạo biểu đồ phân tích chất lượng dữ liệu khách hàng")
    parser.add_argument('--tu-ngay', help="Lọc từ ngày (YYYY-MM-DD)")
    parser.add_argument('--den-ngay', help="Lọc đến ngày (YYYY-MM-DD)")
    args = parser.parse_args()

    anh_da_tao = tao_tat_ca_bieu_do(tu_ngay=args.tu_ngay, den_ngay=args.den_ngay)
    for anh in anh_da_tao:
        print(f"  ✅ {anh}")
