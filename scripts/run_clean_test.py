"""
Script thực hiện Phép thử máy trắng (White-box / Clean Machine Test)
Mô phỏng chạy hệ thống từ một thư mục hoặc môi trường sạch với <= 2 lệnh.
Học phần: Chuyên đề Tốt nghiệp 1 (Track Data Analytics)
Sinh viên: Hồ Lê Trung Bảo - MSSV: 2374802010030
"""

import sys
import subprocess
import pathlib
import sqlite3

ROOT = pathlib.Path(__file__).resolve().parent.parent

def in_tieu_de(noi_dung):
    print("\n" + "=" * 80)
    print(f"  {noi_dung}")
    print("=" * 80)

def chay_lenh(lenh, mo_ta):
    print(f"\n[THỰC THI] {mo_ta}:")
    print(f"  $ {lenh}")
    ket_qua = subprocess.run(lenh, shell=True, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if ket_qua.stdout:
        print(ket_qua.stdout.strip())
    if ket_qua.stderr and ket_qua.returncode != 0:
        print(f"[LỖI STDERR]: {ket_qua.stderr.strip()}")
    if ket_qua.returncode != 0:
        print(f"❌ THẤT BẠI (Mã thoát: {ket_qua.returncode})")
        sys.exit(ket_qua.returncode)
    print("✅ THÀNH CÔNG")
    return ket_qua

def main():
    in_tieu_de("BẮT ĐẦU PHÉP THỬ MÁY TRẮNG (CLEAN MACHINE TEST) - SMARTCRM PIPELINE L7")
    
    # 1. Kiểm tra môi trường & dependencies
    print("1. Kiểm tra các thư mục và tập tin cấu hình thiết yếu...")
    tep_bat_buoc = [
        ROOT / "requirements.txt",
        ROOT / "configs" / "config.example.yaml",
        ROOT / "data" / "mau" / "customers_sample.csv",
        ROOT / "sql" / "001_staging.sql",
        ROOT / "sql" / "002_reject.sql",
        ROOT / "sql" / "010_dim.sql",
        ROOT / "sql" / "020_fact.sql",
        ROOT / "Dockerfile",
        ROOT / "docker-compose.yml"
    ]
    for p in tep_bat_buoc:
        if not p.exists():
            print(f"❌ Thiếu tệp bắt buộc: {p.relative_to(ROOT)}")
            sys.exit(1)
        print(f"   [OK] {p.relative_to(ROOT)}")

    # 2. Lệnh 1: Thực thi Pipeline trên dữ liệu mẫu
    chay_lenh(
        f"{sys.executable} -m src.pipeline --file-nguon data/mau/customers_sample.csv --xuat-bao-cao",
        "Lệnh 1 - Khởi chạy Pipeline ETL & Đo lường chất lượng dữ liệu"
    )

    # 3. Lệnh 2: Đối soát dữ liệu kho và kiểm toán tính toàn vẹn
    chay_lenh(
        f"{sys.executable} -m src.dashboard.so_sanh_dong",
        "Lệnh 2 - Đối soát dữ liệu Staging vs Fact vs Reject"
    )

    # 4. Kiểm tra CSDL SQLite trực tiếp bằng Python sqlite3
    print("\n[KIỂM TOÁN CSDL KHO] Truy vấn trực tiếp các bảng trong SQLite warehouse.db:")
    db_path = ROOT / "data" / "processed" / "warehouse.db"
    assert db_path.exists(), "Tệp CSDL warehouse.db không tồn tại!"
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    bang_dem = {}
    for b in ['staging_customers', 'reject_rows', 'dim_customer', 'fact_customer_quality_audit', 'quality_measures']:
        cur.execute(f"SELECT COUNT(*) FROM {b}")
        bang_dem[b] = cur.fetchone()[0]
        print(f"   - Bảng `{b}`: {bang_dem[b]:,} dòng.")
    conn.close()

    assert bang_dem['staging_customers'] > 0, "staging_customers rỗng!"
    assert bang_dem['dim_customer'] > 0, "dim_customer rỗng!"
    assert bang_dem['reject_rows'] >= 0, "reject_rows không hợp lệ!"
    assert bang_dem['fact_customer_quality_audit'] > 0, "fact_customer_quality_audit rỗng!"

    in_tieu_de("KẾT LUẬN: PHÉP THỬ MÁY TRẮNG THÀNH CÔNG 100%! HỆ THỐNG SẴN SÀNG TRIỂN KHAI")
    print("Mã thoát: 0 (PASS)")

if __name__ == "__main__":
    main()
