# Smart CRM – Customer Data Quality Pipeline (Track DA)

**Học phần:** Chuyên đề Tốt nghiệp 1 (71ITGR40203) – Khoa CNTT, Trường Đại học Văn Lang  
**Đề tài:** Smart CRM – Mekong Mobile  
**Luồng nghiệp vụ:** L7 – Kiểm tra và làm sạch dữ liệu khách hàng (*Customer Data Quality*)  
**Sinh viên thực hiện:** Hồ Lê Trung Bảo – MSSV: 2374802010030  
**Chuyên ngành (Track):** Data Analytics (DA)  
**Giảng viên hướng dẫn:** TS. Nguyễn Trí Hải  

---

## 1. Pipeline làm được gì

Hệ thống hiện thực hóa một Data Pipeline khép kín theo kiến trúc 4 pha độc lập:

```text
Nguồn CSV  ──>  Extract  ──>  Transform  ──>  Quality  ──>  Load  ──>  Kho dữ liệu Star Schema
                                                │                         (Staging / Fact / Dim)
                                                ▼
                                    Bảng reject_rows + Báo cáo tự động (reports/*.md)
```

- **extract (`src/extract/`):** Đọc an toàn $67.037$ dòng dữ liệu thô từ `customers_raw.csv`, **KHÔNG biến đổi**.
- **transform (`src/transform/`):** Chuẩn hóa số điện thoại (4 định dạng thực tế về 10 số `0xxxxxxxxx`), chuẩn hóa họ tên về Title Case, chuẩn hóa email và đọc ngày theo các định dạng thực tế. Mọi quy tắc trong `rules.py` đều là **HÀM THUẦN**, không đọc/ghi CSDL.
- **quality (`src/quality/`):** Đo lường **ba chiều chất lượng** (Đầy đủ · Chính xác · Nhất quán) với 9 phép đo định lượng — mỗi phép đo trả về số dòng kiểm, số dòng đạt, số dòng lỗi và tỷ lệ phần trăm cụ thể.
- **load (`src/load/`):** Nạp vào bảng `staging_customers`, `dim_customer` và `fact_customer_quality_audit`; mọi dòng không chuẩn hóa được đều chuyển vào `reject_rows` kèm lý do cụ thể viết cho con người đọc.

**Ba mục kiểm chứng cốt lõi của BT2:**
1. Chạy hoàn tất bằng **MỘT lệnh duy nhất**.
2. **Chạy lại lần hai không nhân đôi dữ liệu (Idempotent)** — số dòng trong kho dữ liệu giữ nguyên chính xác sau nhiều lần chạy.
3. Kiểm tra chất lượng chạy **TRƯỚC KHI NẠP**, sinh báo cáo chi tiết Markdown và JSON tự động.

---

## 2. Cài đặt môi trường

Yêu cầu: Python 3.11 trở lên.

```bash
# 1. Khởi tạo và kích hoạt môi trường ảo (tùy chọn)
python -m venv .venv
# Trên Windows:
.venv\Scripts\activate
# Trên Linux/macOS:
source .venv/bin/activate

# 2. Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

---

## 3. Chạy Pipeline — MỘT lệnh duy nhất

```bash
python -m src.pipeline
```

Lệnh này sẽ tự động khởi tạo cấu trúc CSDL SQLite kho dữ liệu (nếu chưa có), đọc dữ liệu thô, thực hiện làm sạch, đo lường 3 chiều chất lượng, nạp kho Star Schema và sinh báo cáo tự động tại thư mục `reports/`.

---

## 4. Phép thử NẠP LẠI ĐƯỢC (Idempotent) — Tiêu chí cốt lõi C5

Kiểm chứng khả năng chạy lại an toàn trên cùng một lô dữ liệu mà không làm nhân đôi số lượng bản ghi:

```bash
# Lần 1: Chạy pipeline
python -m src.pipeline

# Kiểm tra số lượng bản ghi sau Lần 1
python -c "import sqlite3; conn = sqlite3.connect('data/processed/warehouse.db'); print('Lần 1:', [row[0] for row in conn.execute('SELECT COUNT(*) FROM dim_customer UNION ALL SELECT COUNT(*) FROM fact_customer_quality_audit;').fetchall()]); conn.close()"

# Lần 2: Chạy lại pipeline lần thứ hai
python -m src.pipeline

# Kiểm tra số lượng bản ghi sau Lần 2 (PHẢI TRÙNG KHỚP HOÀN TOÀN với Lần 1)
python -c "import sqlite3; conn = sqlite3.connect('data/processed/warehouse.db'); print('Lần 2:', [row[0] for row in conn.execute('SELECT COUNT(*) FROM dim_customer UNION ALL SELECT COUNT(*) FROM fact_customer_quality_audit;').fetchall()]); conn.close()"
```

**Kết quả kiểm chứng thực tế:**
* `staging_customers`: 67.037 bản ghi (Lần 2 = Lần 1).
* `reject_rows`: 4.133 bản ghi (Lần 2 = Lần 1).
* `dim_customer`: 62.904 bản ghi (Lần 2 = Lần 1).
* `fact_customer_quality_audit`: 62.904 bản ghi (Lần 2 = Lần 1).

---

## 5. Chạy bộ kiểm thử tự động (Unit Tests)

Bộ kiểm thử gồm 11 test cases thuộc đủ **3 loại bắt buộc** (Luồng đúng · Giá trị biên · Dữ liệu sai), kiểm thử tính năng che mặt nạ PII (NFR05) và các phép đo chất lượng:

```bash
python -m pytest -q
```

Kết quả: `11 passed` toàn bộ trong dưới 0,2 giây.

---

## 6. Cấu trúc mã nguồn

Cấu trúc thư mục phân tầng ranh giới rõ ràng theo chuẩn Slide Buổi 7 (Track DA):

```text
smartcrm-2374802010030-customer-data-quality/
├── configs/
│   └── config.example.yaml          # Ngưỡng chất lượng DQ (Completeness, Validity...)
├── data/
│   ├── raw/customers_raw.csv        # Dữ liệu khách hàng thực tế (67.037 dòng)
│   ├── mau/customers_sample.csv     # Dữ liệu mẫu nhỏ (300 dòng) phục vụ chạy thử
│   └── processed/warehouse.db       # Cơ sở dữ liệu SQLite kho Star Schema
├── docs/
│   ├── thay-doi-thiet-ke.md         # [BẮT BUỘC] Nhật ký thay đổi thiết kế (khắc phục BT1)
│   ├── srs.md                       # Bản đặc tả SRS (bổ sung glossary, NFR05, ma trận truy vết)
│   ├── ai-disclosure.md             # Kê khai AI
│   └── ...                          # Sơ đồ .drawio và .png
├── reports/                         # Thư mục lưu trữ báo cáo chất lượng sinh tự động
│   ├── chat-luong-lo-toan-bo-*.md   # Báo cáo định dạng Markdown
│   └── chat-luong-lo-toan-bo-*.json # Báo cáo định dạng JSON
├── sql/                             # DDL tạo bảng cơ sở dữ liệu
│   ├── 001_staging.sql              # Bảng staging_customers
│   ├── 002_reject.sql               # Bảng reject_rows & quality_measures
│   ├── 010_dim.sql                  # Bảng dim_customer, dim_quality_rule, dim_audit_run
│   └── 020_fact.sql                 # Bảng fact_customer_quality_audit
├── src/
│   ├── config.py                    # Nạp ngưỡng cấu hình và đường dẫn dữ liệu
│   ├── db.py                        # Quản lý kết nối và thực thi DDL kho dữ liệu
│   ├── extract/
│   │   └── read_sources.py          # Pha 1: Đọc CSV nguồn nguyên trạng
│   ├── transform/
│   │   ├── rules.py                 # Hàm thuần chuẩn hóa SĐT, họ tên, email, PII
│   │   └── clean_customers.py       # Pha 2: Điều phối làm sạch & gán nhãn reject
│   ├── quality/
│   │   └── checks.py                # Pha 3: Đo lường 3 chiều chất lượng trả về số
│   ├── load/
│   │   ├── load_staging.py          # Pha 4: Nạp staging, reject và measures
│   │   └── load_warehouse.py        # Pha 4: Nạp dimension và fact
│   └── pipeline.py                  # Entrypoint điều phối toàn bộ 4 pha
├── tests/
│   ├── conftest.py                  # Fixtures dữ liệu kiểm thử độc lập
│   ├── test_rules.py                # Test đơn vị hàm thuần (Đúng, Biên, Sai, PII)
│   └── test_checks.py               # Test đơn vị phép đo chất lượng và bảng reject
├── .env.example                     # Biến môi trường mẫu
├── requirements.txt                 # Khóa phiên bản thư viện
└── README.md                        # Hướng dẫn chi tiết dự án
```

---

## 7. Bảng đối chiếu tiêu chí kỹ thuật tối thiểu BT2

| Mã tiêu chí | Nội dung tiêu chí kỹ thuật BT2 | Trạng thái đạt được |
| :---: | :--- | :---: |
| **C1** | Hệ thống chạy được từ trạng thái ban đầu theo đúng README (CỐT LÕI) | ✅ ĐẠT (`python -m src.pipeline`) |
| **C2** | Tách lớp đúng: ba lớp ở ba nơi, không gọi chéo sai chiều (CỐT LÕI) | ✅ ĐẠT (`extract` / `transform` / `quality` / `load`) |
| **C3** | $\ge 2$ quy tắc nghiệp vụ thật, không chỉ lưu và đọc dữ liệu | ✅ ĐẠT (Chuẩn hóa SĐT 4 dạng, họ tên Title Case, phát hiện trùng lặp) |
| **C4** | $\ge 3$ kiểm thử thuộc 3 loại khác nhau, PASS bằng 1 lệnh (CỐT LÕI) | ✅ ĐẠT (11 tests: Đúng, Biên, Sai, pass bằng `python -m pytest -q`) |
| **C5** | Chạy lại lần hai không lỗi, không nhân đôi dữ liệu (CỐT LÕI) | ✅ ĐẠT (Số dòng Lần 2 = Lần 1 chính xác 100%) |
| **C6** | Đã commit tệp khóa phiên bản; `.env.example` đủ biến; `.env` không commit | ✅ ĐẠT (`requirements.txt`, `.env.example` đầy đủ) |
| **C7** | Dữ liệu vào sai bị từ chối có thông báo rõ ràng, không sập, không lỗi thô | ✅ ĐẠT (4.133 dòng vào `reject_rows` kèm lý do cụ thể) |
| **D1** | Pipeline một lệnh, ba pha ba nơi | ✅ ĐẠT (`src/pipeline.py`) |
| **D2** | $\ge 5$ hàm kiểm chất lượng ra số định lượng | ✅ ĐẠT (9 phép đo trả về số dòng và tỷ lệ %) |
| **D3** | Bảng reject có dòng, lý do viết cho con người | ✅ ĐẠT (Cột `ly_do_loi` diễn giải chi tiết cho người đọc) |