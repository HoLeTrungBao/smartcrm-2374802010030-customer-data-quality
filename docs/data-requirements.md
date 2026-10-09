# ĐẶC TẢ DỮ LIỆU VÀ KHO DỮ LIỆU (TRACK DA)
## LUỒNG NGHIỆP VỤ: L7 – KIỂM TRA VÀ LÀM SẠCH DỮ LIỆU KHÁCH HÀNG
**Học phần:** Chuyên đề Tốt nghiệp 1  
**Sinh viên thực hiện:** Hồ Lê Trung Bảo – MSSV: 2374802010030  
**Chuyên ngành (Track):** Data Analytics (DA)  

---

## 1. SƠ ĐỒ DATA FLOW (LUỒNG DỮ LIỆU)

Quy trình xử lý dữ liệu từ nguồn thô đến kho dữ liệu phục vụ phân tích chất lượng dữ liệu:

```text
+-----------------------------------------------------------------------------------+
| 1. NGUỒN DỮ LIỆU GỐC (DATA SOURCE)                                                |
|    Tập tin: data/raw/customers_raw.csv (67.037 dòng, 6 thuộc tính)                |
+-----------------------------------------------------------------------------------+
                                       │
                                       ▼ (Trích xuất / Ingestion)
+-----------------------------------------------------------------------------------+
| 2. VÙNG DỮ LIỆU TẠM (STAGING & DATA PROFILING)                                    |
|    - Đọc dữ liệu thô vào Pandas DataFrame                                         |
|    - Kiểm tra cấu trúc: record_id, ho_ten, so_dien_thoai, email, dia_chi, ngay_tao|
+-----------------------------------------------------------------------------------+
                                       │
                                       ▼ (Kiểm định & Phát hiện lỗi / Validation)
+-----------------------------------------------------------------------------------+
| 3. QUY TRÌNH KIỂM TRA CHẤT LƯỢNG (DATA QUALITY CHECKS)                            |
|    - [DQ01]: Phát hiện NULL (Thiếu SĐT: 4.133; Email: 30.157; Địa chỉ: 6.023)    |
|    - [DQ02]: Phát hiện sai định dạng SĐT (11.336 số có tiền tố 84 / +84 / dấu .)  |
|    - [DQ03]: Kiểm tra định dạng Email theo regex (4.716 giá trị email lặp lại)    |
|    - [DQ04]: Phát hiện bản ghi nghi ngờ trùng lặp (16.039 trùng SĐT, 9.004 trùng) |
|    - [DQ05]: Phát hiện họ tên sai chuẩn (1.346 có khoảng trắng, 4.584 sai hoa/thường)|
|    - [DQ06]: Kiểm tra tính hợp lệ của trường ngày tạo (100% hợp lệ 2024–2026)     |
+-----------------------------------------------------------------------------------+
                                       │
                                       ▼ (Chuẩn hóa / Standardization & Deduplication)
+-----------------------------------------------------------------------------------+
| 4. XỬ LÝ LÀM SẠCH VÀ CHUẨN HÓA (CLEANSING ENGINE)                                 |
|    - Đưa 100% SĐT hợp lệ về định dạng chuẩn 10 chữ số: 0xxxxxxxxx                 |
|    - Xóa khoảng trắng thừa họ tên, chuyển về chữ in hoa đầu từ (Title Case)       |
|    - Chuyển toàn bộ ký tự Email về chữ thường (lowercase)                         |
|    - Gán nhãn cờ trạng thái trùng lặp (is_duplicate) thay vì xóa bản ghi          |
+-----------------------------------------------------------------------------------+
                                       │
                                       ▼ (Chuyển đổi & Nạp vào Kho / Load to DW)
+-----------------------------------------------------------------------------------+
| 5. KHO DỮ LIỆU PHÂN TÍCH CHẤT LƯỢNG (DATA WAREHOUSE - STAR SCHEMA)                |
|    - dim_customer: Bảng chiều thông tin khách hàng đã làm sạch                     |
|    - dim_quality_rule: Bảng chiều danh mục 6 quy tắc chất lượng dữ liệu           |
|    - dim_audit_run: Bảng chiều phiên chạy kiểm định dữ liệu                       |
|    - fact_customer_quality_audit: Bảng sự kiện kiểm định chất lượng dữ liệu       |
+-----------------------------------------------------------------------------------+
                                       │
                                       ▼ (Phân tích & Trực quan hóa)
+-----------------------------------------------------------------------------------+
| 6. LỚP BÁO CÁO & DASHBOARD (BI REPORTING LAYER)                                   |
|    - Dashboard 1: Tổng quan chỉ số KPI chất lượng dữ liệu                         |
|    - Dashboard 2: Chi tiết trùng lặp và dữ liệu bất thường                        |
|    - Dashboard 3: Tiến độ làm sạch và tỷ lệ chuẩn hóa                             |
+-----------------------------------------------------------------------------------+
```

---

## 2. PHÁT BIỂU GRAIN (MỨC ĐỘ HẠT) CỦA BẢNG FACT

> **GRAIN (MỨC ĐỘ HẠT):**  
> Mỗi dòng trong bảng sự kiện `fact_customer_quality_audit` đại diện cho **kết quả kiểm định chất lượng của MỘT bản ghi khách hàng (`record_id`) trong MỘT phiên chạy kiểm định (`run_key`) theo MỘT quy tắc chất lượng cụ thể (`rule_key`)**.

* **Tính chất của mức hạt này:**
  * Cho phép truy vết chi tiết từng lỗi vi phạm của từng khách hàng cụ thể.
  * Hỗ trợ tổng hợp (aggregate) linh hoạt lên các cấp độ: theo toàn bộ tập dữ liệu, theo từng phiên chạy (run), hoặc theo từng quy tắc chất lượng (rule).

---

## 3. LƯỢC ĐỒ KHO DỮ LIỆU (STAR SCHEMA)

Kho dữ liệu được thiết kế theo mô hình hình sao (Star Schema) gồm **1 Bảng Fact trung tâm** và **3 Bảng Dimension** vệ tinh:

```text
                  +---------------------------+
                  |      dim_audit_run        |
                  +---------------------------+
                  | PK  run_key (INT)         |
                  |     run_date (TIMESTAMP)  |
                  |     total_records (INT)   |
                  |     run_by (VARCHAR)      |
                  +-------------+-------------+
                                │ 1
                                │
                                │ N
+-------------------+     +-----+-------------------------+     +------------------------+
|   dim_customer    |     | fact_customer_quality_audit   |     |    dim_quality_rule    |
+-------------------+     +-------------------------------+     +------------------------+
| PK customer_key   | 1   | PK  audit_id (BIGINT)         |   1 | PK rule_key (INT)      |
|    record_id      +─────┤ FK  customer_key (INT)        ├─────+    rule_code (VARCHAR) |
|    ho_ten_goc     |   N | FK  run_key (INT)             | N   |    rule_name (VARCHAR) |
|    ho_ten_clean   |     | FK  rule_key (INT)            |     |    target_column (STR) |
|    sdt_goc        |     |     is_passed (BOOLEAN)       |     |    severity (VARCHAR)  |
|    sdt_clean      |     |     is_missing (BOOLEAN)      |     +------------------------+
|    email_clean    |     |     is_invalid_format (BOOL)  |
|    dia_chi_clean  |     |     is_duplicate (BOOLEAN)    |
|    ngay_tao       |     |     is_auto_cleaned (BOOLEAN) |
|    status         |     |     quality_score (DECIMAL)   |
+-------------------+     +-------------------------------+
```

---

## 4. ĐẶC TẢ CHI TIẾT CÁC BẢNG TRONG KHO DỮ LIỆU

### 4.1. Bảng Fact: `fact_customer_quality_audit`
Bảng lưu trữ các chỉ số đo lường và cờ trạng thái kiểm định chất lượng dữ liệu của từng bản ghi khách hàng.

| Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả nghiệp vụ |
| :--- | :--- | :---: | :--- |
| `audit_id` | `BIGINT` | **PRIMARY KEY** | Khóa chính nhân tạo định danh từng dòng kiểm định. |
| `run_key` | `INT` | **FOREIGN KEY** | Tham chiếu đến phiên kiểm tra dữ liệu (`dim_audit_run.run_key`). |
| `customer_key` | `INT` | **FOREIGN KEY** | Tham chiếu đến bản ghi khách hàng (`dim_customer.customer_key`). |
| `rule_key` | `INT` | **FOREIGN KEY** | Tham chiếu đến quy tắc được áp dụng (`dim_quality_rule.rule_key`). |
| `is_passed` | `BOOLEAN` | `NOT NULL` | Trạng thái đạt (`1`) hoặc không đạt (`0`) quy tắc chất lượng. |
| `is_missing` | `BOOLEAN` | `NOT NULL` | Cờ báo trường dữ liệu bị thiếu (`NULL` hoặc rỗng). |
| `is_invalid_format` | `BOOLEAN` | `NOT NULL` | Cờ báo trường dữ liệu sai định dạng (ví dụ: SĐT có ký tự lạ, họ tên viết thường). |
| `is_duplicate` | `BOOLEAN` | `NOT NULL` | Cờ báo bản ghi có nguy cơ trùng lặp (trùng SĐT hoặc Email). |
| `is_auto_cleaned` | `BOOLEAN` | `NOT NULL` | Cờ báo bản ghi đã được tự động chuẩn hóa thành công bởi hệ thống. |
| `quality_score` | `DECIMAL(5,2)` | `DEFAULT 100.00` | Điểm chất lượng của bản ghi sau kiểm tra (thang 0 – 100 điểm). |

---

### 4.2. Bảng Dimension: `dim_customer`
Bảng chiều lưu trữ thông tin thuộc tính khách hàng đối chiếu giữa dữ liệu gốc và dữ liệu đã làm sạch.

| Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả nghiệp vụ |
| :--- | :--- | :---: | :--- |
| `customer_key` | `INT` | **PRIMARY KEY** | Khóa thay thế (Surrogate Key) tự tăng trong kho dữ liệu. |
| `record_id` | `BIGINT` | `NOT NULL` | Mã định danh gốc từ tập tin `customers_raw.csv`. |
| `ho_ten_goc` | `VARCHAR(255)` | `NOT NULL` | Họ tên khách hàng trước khi làm sạch. |
| `ho_ten_clean` | `VARCHAR(255)` | `NOT NULL` | Họ tên đã chuẩn hóa (xóa khoảng trắng thừa, viết hoa chữ cái đầu). |
| `so_dien_thoai_goc` | `VARCHAR(50)` | `NULL` | Số điện thoại gốc (có dấu chấm, mã `+84` hoặc khoảng trắng). |
| `so_dien_thoai_clean`| `VARCHAR(15)` | `NULL` | Số điện thoại chuẩn hóa 10 chữ số (định dạng `0xxxxxxxxx`). |
| `email_clean` | `VARCHAR(255)` | `NULL` | Email chuyển thành chữ in thường (lowercase). |
| `dia_chi_clean` | `VARCHAR(500)` | `NULL` | Địa chỉ đã cắt tỉa khoảng trắng. |
| `ngay_tao` | `DATE` | `NOT NULL` | Ngày tạo bản ghi (định dạng chuẩn `YYYY-MM-DD`). |
| `status` | `VARCHAR(50)` | `NOT NULL` | Trạng thái: "Hoàn toàn sạch", "Nghi ngờ trùng lặp", "Thiếu dữ liệu". |

---

### 4.3. Bảng Dimension: `dim_quality_rule`
Bảng chiều danh mục quy tắc chất lượng dữ liệu được định nghĩa trong hệ thống.

| Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả nghiệp vụ |
| :--- | :--- | :---: | :--- |
| `rule_key` | `INT` | **PRIMARY KEY** | Khóa chính danh mục quy tắc. |
| `rule_code` | `VARCHAR(10)` | `UNIQUE` | Mã quy tắc: `DQ01`, `DQ02`, `DQ03`, `DQ04`, `DQ05`, `DQ06`. |
| `rule_name` | `VARCHAR(100)` | `NOT NULL` | Tên quy tắc (ví dụ: "Kiểm tra dữ liệu thiếu", "Chuẩn hóa SĐT"). |
| `target_column` | `VARCHAR(50)` | `NOT NULL` | Tên cột áp dụng (`so_dien_thoai`, `email`, `ho_ten`, `dia_chi`). |
| `severity` | `VARCHAR(20)` | `NOT NULL` | Mức độ nghiêm trọng: "Cảnh báo" (Warning), "Lỗi định dạng" (Error), "Nghi ngờ" (Suspect). |

---

### 4.4. Bảng Dimension: `dim_audit_run`
Bảng chiều lưu thông tin các phiên thực thi pipeline kiểm tra và làm sạch dữ liệu.

| Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả nghiệp vụ |
| :--- | :--- | :---: | :--- |
| `run_key` | `INT` | **PRIMARY KEY** | Khóa chính của phiên kiểm định. |
| `run_date` | `TIMESTAMP` | `NOT NULL` | Ngày giờ thực hiện phiên chạy. |
| `total_records` | `INT` | `NOT NULL` | Tổng số lượng bản ghi nạp vào kiểm tra ($67.037$ bản ghi). |
| `run_by` | `VARCHAR(100)` | `NOT NULL` | Người vận hành (ví dụ: "Marketing", "ETL Batch Runner"). |

---

## 5. ĐỐI CHIẾU SỐ LIỆU THỰC TẾ TRÊN TẬP DỮ LIỆU `customers_raw.csv`

Bảng ánh xạ các giá trị thực tế sau khi phân tích khám phá dữ liệu (Data Profiling):

| Quy tắc DQ | Chỉ tiêu đánh giá | Số lượng bản ghi phát hiện | Tỷ lệ (%) trên tập 67.037 bản ghi |
| :---: | :--- | :---: | :---: |
| **DQ01** | Thiếu số điện thoại (NULL) | 4.133 | 6,17% |
| **DQ01** | Thiếu email (NULL) | 30.157 | 44,99% |
| **DQ01** | Thiếu địa chỉ (NULL) | 6.023 | 8,98% |
| **DQ02** | Số điện thoại có định dạng mã quốc gia `84` / `+84` | 11.336 | 16,91% |
| **DQ03** | Email lặp lại từ 2 lần trở lên | 4.716 | 7,03% |
| **DQ04** | Nhóm bản ghi trùng số điện thoại sau chuẩn hóa | 16.039 | 23,93% |
| **DQ04** | Nhóm bản ghi trùng email sau chuẩn hóa | 9.004 | 13,43% |
| **DQ05** | Họ tên có khoảng trắng thừa đầu/cuối | 1.346 | 2,01% |
| **DQ05** | Họ tên viết toàn chữ thường | 1.933 | 2,88% |
| **DQ05** | Họ tên viết toàn chữ in hoa | 2.651 | 3,95% |
| **DQ06** | Ngày tạo chuyển đổi thành công về YYYY-MM-DD | 67.037 | 100,00% |
