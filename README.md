# Smart CRM – Customer Data Quality (Track DA)

**Học phần:** Chuyên đề Tốt nghiệp 1 (71ITGR40203) – Khoa CNTT, Trường Đại học Văn Lang  
**Sinh viên thực hiện:** Hồ Lê Trung Bảo – MSSV: 2374802010030  
**Chuyên ngành (Track):** Data Analytics (DA)  
**Giảng viên hướng dẫn:** TS. Nguyễn Trí Hải  

---

## 1. Mô tả bài toán

**Luồng nghiệp vụ:** L7 – Kiểm tra và làm sạch dữ liệu khách hàng (*Customer Data Quality*).

Bài toán tập trung vào việc tiếp nhận dữ liệu khách hàng từ chuỗi bán lẻ thiết bị di động Mekong Mobile, phân tích khám phá dữ liệu (Data Profiling) để phát hiện các vấn đề suy giảm chất lượng dữ liệu: dữ liệu bị thiếu (`NULL`), sai lệch định dạng số điện thoại (chứa mã `84`, `+84` hoặc dấu chấm), họ tên viết hoa lộn xộn hoặc thừa khoảng trắng, và phát hiện các bản ghi có nguy cơ trùng lặp khách hàng. Hệ thống thực hiện chuẩn hóa dữ liệu, nạp vào kho dữ liệu theo mô hình hình sao (Star Schema) và trực quan hóa kết quả kiểm định chất lượng lên Dashboard dành cho nhà quản lý.

---

## 2. Phạm vi

### 2.1. Trong phạm vi (Làm)
* Nạp và khám phá cấu trúc dữ liệu khách hàng từ tập tin nguồn `customers_raw.csv` ($67.037$ bản ghi, $6$ thuộc tính).
* Kiểm tra và thống kê các trường dữ liệu bị thiếu giá trị (NULL).
* Phát hiện và phân loại các bản ghi khách hàng có nguy cơ trùng lặp dựa trên số điện thoại và email sau chuẩn hóa.
* Chuẩn hóa định dạng số điện thoại về 10 chữ số chuẩn (`0xxxxxxxxx`) và chuẩn hóa họ tên về dạng Title Case (xóa khoảng trắng thừa).
* Thiết kế mô hình kho dữ liệu Star Schema gồm bảng sự kiện `fact_customer_quality_audit` và các bảng chiều (`dim_customer`, `dim_quality_rule`, `dim_audit_run`).
* Xây dựng wireframe 3 khung Dashboard trực quan hóa KPI chất lượng dữ liệu, chi tiết trùng lặp và tiến độ làm sạch dữ liệu.

### 2.2. Ngoài phạm vi (Không làm - Mức WON'T của MoSCoW)
* Không xây dựng hệ thống quản lý đơn hàng và thanh toán giao dịch bán lẻ (POS).
* Không tiếp nhận và xử lý phiếu bảo hành linh kiện di động.
* Không tự động gửi tin nhắn SMS Brandname hoặc Email Marketing đến khách hàng.
* Không xây dựng mô hình Học máy (Machine Learning) dự đoán rời bỏ (Churn).
* Không xóa vật lý (Hard Delete) các bản ghi nghi ngờ trùng lặp khi chưa có xác nhận từ người dùng.

---

## 3. Công nghệ sử dụng

| Thành phần | Công nghệ / Thư viện | Vai trò |
| :--- | :--- | :--- |
| **Ngôn ngữ lập trình** | Python 3.11+ | Ngôn ngữ phát triển pipeline xử lý dữ liệu |
| **Xử lý dữ liệu** | Pandas, NumPy | Đọc file CSV, tiền xử lý, kiểm tra regex và chuẩn hóa chuỗi |
| **Môi trường phân tích** | Jupyter Notebook | Môi trường thử nghiệm và khám phá dữ liệu (EDA) |
| **Mô hình hóa dữ liệu** | Star Schema (Kimball) | Thiết kế kho dữ liệu Data Warehouse phục vụ báo cáo |
| **Thiết kế sơ đồ** | draw.io | Vẽ Use Case, Kiến trúc dữ liệu và Star Schema |
| **Quản lý mã nguồn** | Git & GitHub | Quản lý phiên bản mã nguồn theo Conventional Commits |

---

## 4. Cấu trúc thư mục

```text
smartcrm-2374802010030-customer-data-quality/
├── data/
│   ├── raw/
│   │   └── customers_raw.csv         # Dữ liệu khách hàng thô (67.037 dòng)
│   └── processed/                    # Dữ liệu khách hàng đã làm sạch sau ETL
├── docs/
│   ├── srs.md                        # Bản đặc tả yêu cầu phần mềm rút gọn (SRS)
│   ├── architecture.drawio           # Sơ đồ kiến trúc Data Pipeline 5 tầng (file gốc)
│   ├── usecase.drawio                # Sơ đồ Use Case phân hệ chất lượng dữ liệu (file gốc)
│   ├── erd.drawio                    # Lược đồ kho dữ liệu Star Schema (file gốc)
│   ├── wireframe.png                 # Bản vẽ Wireframe 3 khung Dashboard chất lượng
│   ├── ai-disclosure.md              # Bảng khai báo sử dụng công cụ AI kèm cam kết
│   ├── data-requirements.md          # Đặc tả dữ liệu, Data Flow và Grain bảng Fact (DA)
│   ├── use-case.md                   # Đặc tả chi tiết Use Case UC04, UC05
│   └── user-story.md                 # Danh sách User Story và tiêu chí chấp nhận (GWT)
├── notebooks/
│   └── 01_check_customers.ipynb      # Khám phá và thống kê chất lượng dữ liệu thực tế
├── src/
│   └── etl/
│       ├── extract.py                # Trích xuất dữ liệu từ nguồn
│       ├── transform.py              # Xử lý chuẩn hóa và kiểm định chất lượng
│       └── load.py                   # Nạp dữ liệu vào kho phân tích
├── .env.example                      # Cấu hình biến môi trường mẫu
├── .gitignore                        # Cấu hình bỏ qua các tệp tin nhạy cảm/tạm thời
├── requirements.txt                  # Danh sách các thư viện phụ thuộc
└── README.md                         # Tài liệu hướng dẫn tổng quan dự án
```

---

## 5. Hướng dẫn cài đặt & chạy môi trường

### Bước 1: Khởi tạo và kích hoạt môi trường ảo Python
```powershell
# Trên Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Bước 2: Cài đặt các thư viện phụ thuộc
```powershell
pip install -r requirements.txt
```

### Bước 3: Khởi động Jupyter Notebook khám phá dữ liệu
```powershell
jupyter notebook
```
Mở file `notebooks/01_check_customers.ipynb` để chạy các đoạn mã phân tích dữ liệu trên tập tin `data/raw/customers_raw.csv`.

---

## 6. Khai báo sử dụng công cụ AI

Theo yêu cầu chuẩn mực học thuật của môn học Chuyên đề Tốt nghiệp 1:

| Công cụ | Dùng vào việc gì | Áp dụng ở phần nào | Đã kiểm chứng thế nào |
| :--- | :--- | :--- | :--- |
| **ChatGPT / Antigravity AI** | Gợi ý cấu trúc bảng Fact và các bảng Dimension cho kho dữ liệu theo chuẩn Star Schema (Mô hình Kimball) phù hợp với bài toán Data Quality. | Mục 4 – Mô hình dữ liệu (`fact_customer_quality_audit`, `dim_customer`, `dim_quality_rule`, `dim_audit_run`). | Đối chiếu với lý thuyết Kimball về mô hình hóa kho dữ liệu; kiểm tra khóa chính, khóa ngoại, kiểu dữ liệu từng cột và tự phát biểu rõ ràng mức độ hạt (GRAIN) của bảng Fact. |
| **ChatGPT / Antigravity AI** | Hỗ trợ chuẩn hóa cấu trúc câu lập luận quyết định kiến trúc hệ thống theo đúng khuôn mẫu quy định của đề bài. | Mục 3 – Thiết kế kiến trúc (3 câu giải thích kiến trúc gắn với mã NFR và phân tích đánh đổi). | Tự đối chiếu với các yêu cầu phi chức năng (NFR01, NFR02, NFR03), rà soát ngưỡng số thực tế của tập dữ liệu $67.037$ bản ghi và tự thẩm định các đánh đổi kỹ thuật. |
| **— Không sử dụng AI —** *(Tự làm hoàn toàn)* | Khám phá dữ liệu thực tế (Data Profiling) trên tập tin nguồn `customers_raw.csv`, tính toán các tỷ lệ thiếu dữ liệu, sai định dạng số điện thoại, viết hoa họ tên và tỷ lệ trùng lặp. | Mục 1 (Phạm vi) và Mục 4 (Bộ quy tắc chất lượng dữ liệu DQ01 – DQ06). | Tự viết và thực thi mã nguồn Python bằng thư viện Pandas trên Jupyter Notebook (`notebooks/01_check_customers.ipynb`), đối chiếu trực tiếp kết quả với số liệu thực tế ($67.037$ dòng, $11.336$ SĐT mã 84, $4.716$ email lặp). |
| **— Không sử dụng AI —** *(Tự làm hoàn toàn)* | Xác định phạm vi nghiệp vụ L7, phân tích các Actor, viết User Story và xây dựng sơ đồ Use Case. | Mục 1 (Giới thiệu & phạm vi) và Mục 2 (Use Case). | Dựa trên đề cương bài học Buổi 2 và Buổi 4, tự vẽ sơ đồ Use Case trên draw.io và viết đặc tả luồng chính/ngoại lệ. |

**Cam kết liêm chính học thuật:**
> *"Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp."*  
> **Sinh viên:** Hồ Lê Trung Bảo – **MSSV:** 2374802010030 – **Ngày:** 09/10/2026