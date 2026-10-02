# Track DA – Data Specification

## 1. Tổng quan

Track DA mô tả dữ liệu đầu vào, cấu trúc dữ liệu,
các quy tắc kiểm tra chất lượng dữ liệu và quá trình chuẩn hóa.

## 2. Data Source

**File:** `customers_raw.csv`

**Số bản ghi:** 67.037

**Số cột:** 6

| Cột | Kiểu dữ liệu | Mô tả |
|---|---|---|
| record_id | int64 | Mã bản ghi khách hàng |
| ho_ten | object | Họ và tên khách hàng |
| so_dien_thoai | object | Số điện thoại |
| email | object | Email khách hàng |
| dia_chi | object | Địa chỉ khách hàng |
| ngay_tao | object | Ngày tạo bản ghi |

## 3. Thống kê chất lượng dữ liệu

| Trường | Số lượng thiếu | Tỷ lệ thiếu |
|---|---:|---:|
| record_id | 0 | 0% |
| ho_ten | 0 | 0% |
| so_dien_thoai | 4.133 | 6,17% |
| email | 30.157 | 44,99% |
| dia_chi | 6.023 | 8,98% |
| ngay_tao | 0 | 0% |

## 4. Data Quality Rules

### DQ-01 – Kiểm tra dữ liệu thiếu

Kiểm tra các trường dữ liệu có giá trị NULL.

Các trường có dữ liệu thiếu:

- so_dien_thoai: 4.133 bản ghi.
- email: 30.157 bản ghi.
- dia_chi: 6.023 bản ghi.

### DQ-02 – Chuẩn hóa số điện thoại

Kiểm tra và chuẩn hóa số điện thoại.

Quy tắc:

- Loại bỏ ký tự không cần thiết.
- Các số bắt đầu bằng `84` hoặc `+84` được chuyển về dạng bắt đầu bằng `0`.
- Sau chuẩn hóa, số điện thoại hợp lệ có 10 chữ số.

Kết quả kiểm tra:

- 11.336 giá trị đang ở dạng mã quốc gia `84/+84`.

### DQ-03 – Kiểm tra email

Kiểm tra email theo định dạng cơ bản:

`ten@mien.tld`

Đồng thời chuẩn hóa email về chữ thường.

Kết quả:

- Không phát hiện email sai định dạng theo regex cơ bản.
- Có 4.716 giá trị email lặp.

### DQ-04 – Phát hiện khách hàng có khả năng trùng

Sử dụng số điện thoại và email sau khi chuẩn hóa
để phát hiện các bản ghi có khả năng thuộc cùng một khách hàng.

Kết quả:

- 16.039 bản ghi thuộc nhóm trùng số điện thoại chuẩn hóa.
- 9.004 bản ghi thuộc nhóm trùng email chuẩn hóa.

Các bản ghi này được xem là **có khả năng trùng**,
không tự động kết luận phải xóa.

### DQ-05 – Chuẩn hóa họ tên

Kiểm tra và chuẩn hóa họ tên.

Quy tắc:

- Loại bỏ khoảng trắng đầu/cuối.
- Chuẩn hóa cách viết hoa/chữ thường theo quy tắc của hệ thống.

Kết quả:

- 1.346 giá trị có khoảng trắng đầu/cuối.
- 1.933 tên viết toàn chữ thường.
- 2.651 tên viết toàn chữ hoa.

### DQ-06 – Kiểm tra ngày tạo

Kiểm tra khả năng chuyển đổi dữ liệu ngày tạo về kiểu ngày.

Kết quả:

- 100% giá trị có thể chuyển đổi thành ngày.
- Khoảng ngày: `2024-01-01` đến `2026-08-28`.

## 5. Data Flow

```text
customers_raw.csv
       ↓
Kiểm tra dữ liệu
       ↓
Phát hiện dữ liệu thiếu / sai định dạng / có khả năng trùng
       ↓
Chuẩn hóa dữ liệu
       ↓
Cập nhật dữ liệu
       ↓
Dữ liệu sạch
       ↓
Kết quả chất lượng dữ liệu