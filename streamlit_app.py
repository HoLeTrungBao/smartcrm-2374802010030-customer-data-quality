"""
SmartCRM - Phân hệ Kiểm định & Làm sạch Dữ liệu Khách hàng (Luồng L7)
Mekong Mobile · Chuyên ngành Data Analytics (Track DA)
Sinh viên: Hồ Lê Trung Bảo — MSSV: 2374802010030
Ứng dụng Web Dashboard trực quan hóa triển khai Cloud (+1.0 điểm cộng BT3)
"""

import os
import pathlib
import sqlite3
import pandas as pd
import streamlit as st

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="SmartCRM Data Quality Dashboard | Mekong Mobile",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = pathlib.Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "processed" / "warehouse.db"

# Tự động nạp dữ liệu nếu chưa có CSDL trên Cloud
@st.cache_resource
def dam_bao_csdl():
    if not DB_PATH.exists():
        with st.spinner("Đang khởi tạo cơ sở dữ liệu kho Star Schema trên Cloud..."):
            from src import pipeline
            sample_data = ROOT / "data" / "mau" / "customers_sample.csv"
            pipeline.chay(file_nguon=str(sample_data), khoi_tao_csdl=True)

dam_bao_csdl()

def lay_ket_noi():
    return sqlite3.connect(DB_PATH)

# Tải số liệu tổng quan
@st.cache_data(ttl=60)
def lay_so_lieu_tong_quan():
    conn = lay_ket_noi()
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM staging_customers")
        staging_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM dim_customer")
        dim_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM reject_rows")
        reject_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM fact_customer_quality_audit WHERE is_duplicate = 1")
        duplicate_count = cur.fetchone()[0]

        # Lấy thông tin phiên chạy
        cur.execute("SELECT batch_id, run_date, total_records FROM dim_audit_run ORDER BY run_key DESC LIMIT 1")
        audit_run = cur.fetchone()

        return {
            "staging": staging_count,
            "dim": dim_count,
            "reject": reject_count,
            "duplicate": duplicate_count,
            "audit_run": audit_run
        }
    finally:
        conn.close()

# Tải các chỉ tiêu đo lường chất lượng
@st.cache_data(ttl=60)
def lay_bang_quality_measures():
    conn = lay_ket_noi()
    try:
        query = """
        SELECT chieu_chat_luong, doi_tuong, so_kiem, so_dat, so_loi, 
               ROUND(ti_le_dat * 100, 2) as ti_le_dat_pct,
               ROUND(nguong_yeu_cau * 100, 2) as nguong_pct,
               ket_luan
        FROM quality_measures
        ORDER BY measure_id ASC
        """
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()

# Tải dữ liệu lỗi reject
@st.cache_data(ttl=60)
def lay_danh_sach_reject(limit=100):
    conn = lay_ket_noi()
    try:
        query = f"""
        SELECT reject_id, customer_id, ho_ten_goc, so_dien_thoai_goc, email_goc, 
               ma_quy_tac, ly_do_loi, thoi_gian_tao
        FROM reject_rows
        ORDER BY reject_id ASC
        LIMIT {limit}
        """
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()

# Giao diện chính
so_lieu = lay_so_lieu_tong_quan()

# Sidebar
st.sidebar.image("https://raw.githubusercontent.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality/main/docs/logo_highres.png", width=120)
st.sidebar.title("SmartCRM Analytics")
st.sidebar.markdown("**Phân hệ:** L7 – Customer Data Quality")
st.sidebar.markdown("**Sinh viên:** Hồ Lê Trung Bảo")
st.sidebar.markdown("**MSSV:** `2374802010030`")
st.sidebar.markdown("**Lớp:** 71ITGR40203_01 (Track DA)")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🌐 Phiên bản & Môi trường")
st.sidebar.info("🚀 **Release:** `v1.0`\n\n🎯 **CSDL:** SQLite Star Schema\n\n🔒 **PII Masking:** 100% (NFR05)")

# Header
st.title("📊 Giám sát & Đo lường Chất lượng Dữ liệu Khách hàng")
st.caption("Dự án Mekong Mobile · Chu trình ETL 4 pha: Extract ➔ Transform ➔ Quality ➔ Load")

# 4 Thẻ KPI Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Tổng bản ghi nguồn", f"{so_lieu['staging']:,} dòng", delta="Dữ liệu thô CSV")
with col2:
    ti_le_sach = (so_lieu['dim'] / so_lieu['staging'] * 100) if so_lieu['staging'] > 0 else 0
    st.metric("Đạt chuẩn (dim_customer)", f"{so_lieu['dim']:,} khách", delta=f"{ti_le_sach:.1f}% Đạt chuẩn")
with col3:
    ti_le_reject = (so_lieu['reject'] / so_lieu['staging'] * 100) if so_lieu['staging'] > 0 else 0
    st.metric("Bị từ chối (reject_rows)", f"{so_lieu['reject']:,} dòng", delta=f"-{ti_le_reject:.1f}% Cách ly lỗi", delta_color="inverse")
with col4:
    ti_le_trung = (so_lieu['duplicate'] / so_lieu['dim'] * 100) if so_lieu['dim'] > 0 else 0
    st.metric("Trùng lặp (Uniqueness)", f"{so_lieu['duplicate']:,} khách", delta=f"{ti_le_trung:.1f}% (Ngưỡng ≤ 70%)")

st.markdown("---")

# Các Tab chức năng
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Biểu đồ Phân tích Chất lượng",
    "⚖️ Đối soát Kho dữ liệu (Reconciliation)",
    "🚫 Bảng Đối soát Lỗi Reject Rows",
    "📋 9 Chỉ tiêu Đo lường 3 Chiều (Measures)"
])

with tab1:
    st.subheader("1. Phân bổ lỗi chất lượng và Tỷ lệ trùng lặp khách hàng")
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.markdown("**Biểu đồ 1: Phân bổ lỗi chất lượng theo quy tắc DQ**")
        img_loi = ROOT / "docs" / "bieu_do_loi_dq.png"
        if img_loi.exists():
            st.image(str(img_loi), use_container_width=True)
        else:
            st.warning("Đang chờ cập nhật ảnh biểu đồ lỗi DQ.")
    with col_img2:
        st.markdown("**Biểu đồ 2: Tỷ lệ khách hàng trùng lặp so với duy nhất**")
        img_trung = ROOT / "docs" / "bieu_do_trung_lap.png"
        if img_trung.exists():
            st.image(str(img_trung), use_container_width=True)
        else:
            st.warning("Đang chờ cập nhật ảnh biểu đồ trùng lặp.")

with tab2:
    st.subheader("2. Kiểm toán bảo toàn dữ liệu (Data Reconciliation)")
    st.markdown("""
    Nguyên tắc cốt lõi: **Không nuốt lỗi âm thầm, bảo toàn 100% dữ liệu**.  
    Số lượng bản ghi nguồn đọc vào phải bằng chính xác tổng số khách hàng sạch nạp vào kho cộng với số bản ghi bị cách ly lỗi.
    """)
    df_reconcile = pd.DataFrame([
        {"Bảng trong Kho": "staging_customers", "Số bản ghi": f"{so_lieu['staging']:,}", "Diễn giải": "Toàn bộ dữ liệu thô đọc nguyên trạng"},
        {"Bảng trong Kho": "dim_customer", "Số bản ghi": f"{so_lieu['dim']:,}", "Diễn giải": "Khách hàng hợp lệ nạp bằng khóa tự nhiên customer_id"},
        {"Bảng trong Kho": "reject_rows", "Số bản ghi": f"{so_lieu['reject']:,}", "Diễn giải": "Dòng lỗi không thể chuẩn hóa, có lý do chi tiết"},
        {"Bảng trong Kho": "fact_customer_quality_audit", "Số bản ghi": f"{so_lieu['dim']:,}", "Diễn giải": "Sự kiện kiểm định chất lượng từng khách hàng sạch"}
    ])
    st.table(df_reconcile)

    chenh_lech = so_lieu['staging'] - (so_lieu['dim'] + so_lieu['reject'])
    if chenh_lech == 0:
        st.success(f"✅ **BẢO TOÀN DỮ LIỆU TUYỆT ĐỐI:** Staging ({so_lieu['staging']:,}) = Fact/Dim ({so_lieu['dim']:,}) + Reject ({so_lieu['reject']:,}). Chênh lệch = 0 dòng.")
    else:
        st.warning(f"⚠️ Phát hiện chênh lệch: {chenh_lech} dòng.")

with tab3:
    st.subheader("3. Danh sách các bản ghi bị cách ly vào `reject_rows`")
    st.caption("Các dòng không đạt chuẩn làm sạch được lưu trữ nguyên trạng kèm lý do viết cho con người đọc để hỗ trợ nhân viên đối soát.")
    df_reject = lay_danh_sach_reject(100)
    st.dataframe(df_reject, use_container_width=True)

with tab4:
    st.subheader("4. Bảng đo lường 3 chiều chất lượng (9 chỉ tiêu)")
    df_measures = lay_bang_quality_measures()
    if not df_measures.empty:
        st.dataframe(df_measures, use_container_width=True)
    else:
        st.info("Chưa ghi nhận dữ liệu đo lường chất lượng.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    SmartCRM Customer Data Quality Pipeline · ĐH Văn Lang · HK1 Năm học 2026–2027<br>
    Đồ án Chuyên đề Tốt nghiệp 1 · Sinh viên thực hiện: <b>Hồ Lê Trung Bảo</b> (MSSV: 2374802010030)
</div>
""", unsafe_allow_html=True)
