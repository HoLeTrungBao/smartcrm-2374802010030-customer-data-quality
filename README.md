# Smart CRM – Customer Data Quality

**Sinh viên:** Hồ Lê Trung Bảo – MSSV: 2374802010030  
**Track:** DA  
**Học phần:** Chuyên đề Tốt nghiệp 1 – Trường ĐH Văn Lang  

## 1. Mô tả bài toán

Luồng nghiệp vụ L7 – Quản lý chất lượng dữ liệu khách hàng.

Bài toán tập trung vào việc kiểm tra và cải thiện chất lượng dữ liệu khách hàng trong hệ thống Smart CRM. Dữ liệu khách hàng được đọc từ file CSV, sau đó phân tích để phát hiện các vấn đề về chất lượng dữ liệu như dữ liệu thiếu, trùng lặp và sai định dạng.

## 2. Phạm vi

- Làm:
  - Đọc dữ liệu khách hàng từ file CSV.
  - Khám phá cấu trúc và thông tin dữ liệu.
  - Kiểm tra dữ liệu thiếu.
  - Kiểm tra dữ liệu trùng lặp.
  - Kiểm tra định dạng số điện thoại và họ tên.
  - Chuẩn hóa dữ liệu khách hàng.
  - Lưu dữ liệu sau khi xử lý vào `data/processed/`.

- Không làm:
  - Không xây dựng toàn bộ hệ thống Smart CRM.
  - Không xử lý dữ liệu đơn hàng.
  - Không xử lý dữ liệu bảo hành.
  - Không xây dựng mô hình dự đoán khách hàng rời bỏ.
  - Không xây dựng hệ thống phân loại yêu cầu bảo hành bằng AI.
  - Không tập trung vào xây dựng dashboard.

## 3. Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Ngôn ngữ | Python |
| Phân tích dữ liệu | Pandas |
| Môi trường phân tích | Jupyter Notebook |
| Quản lý mã nguồn | Git |
| Lưu trữ mã nguồn | GitHub |

## 4. Cấu trúc thư mục

```text
smartcrm-2374802010030-customer-data-quality/
│
├── dashboard/
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
├── notebooks/
│
├── src/
│   └── etl/
│       ├── extract.py
│       ├── transform.py
│       └── load.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
5. Hướng dẫn cài đặt & chạy
Bước 1: Tạo môi trường ảo
python -m venv .venv
Bước 2: Kích hoạt môi trường

Trên Windows:

.venv\Scripts\activate
Bước 3: Cài đặt thư viện
pip install -r requirements.txt
Bước 4: Khởi động Jupyter Notebook
jupyter notebook
Bước 5: Đọc dữ liệu

Dữ liệu khách hàng được lưu tại:

data/raw/customers_raw.csv

Sử dụng Pandas để đọc dữ liệu:

import pandas as pd

df = pd.read_csv("data/raw/customers_raw.csv")

print("Số dòng:", len(df))
print("Số cột:", len(df.columns))

df.head()

Dữ liệu hiện có 67.037 dòng và 6 cột.

6. Khai báo sử dụng công cụ AI
Công cụ	Dùng vào việc gì	Cách tự kiểm chứng
ChatGPT	Hỗ trợ hiểu yêu cầu bài toán và hướng dẫn thực hiện	Tự chạy code và kiểm tra kết quả trên dữ liệu