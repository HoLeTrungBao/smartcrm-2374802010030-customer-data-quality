# Software Requirements Specification (SRS)

## 1. Giới thiệu

### 1.1. Tên bài toán

Kiểm tra và làm sạch dữ liệu khách hàng.

### 1.2. Mục tiêu

Hệ thống hỗ trợ kiểm tra dữ liệu khách hàng, phát hiện dữ liệu trùng,
thiếu hoặc sai định dạng, sau đó xử lý, chuẩn hóa và cập nhật dữ liệu.

### 1.3. Phạm vi

Hệ thống tập trung vào việc kiểm tra và làm sạch dữ liệu khách hàng.

Các chức năng chính:

- Xem danh sách khách hàng
- Tìm kiếm khách hàng
- Kiểm tra dữ liệu thiếu hoặc sai định dạng
- Phát hiện khách hàng bị trùng
- Chuẩn hóa thông tin khách hàng
- Cập nhật dữ liệu khách hàng
- Xem kết quả chất lượng dữ liệu

### 1.4. Ngoài phạm vi

Hệ thống không bao gồm:

- Quản lý đơn hàng
- Quản lý bảo hành
- Quản lý chiến dịch Marketing
- Dự đoán khách hàng rời bỏ
- Dashboard doanh thu

## 2. Actor

### 2.1. Marketing

Marketing sử dụng hệ thống để xem, tìm kiếm, kiểm tra,
phát hiện trùng, chuẩn hóa và cập nhật dữ liệu khách hàng.

### 2.2. Quản lý cửa hàng

Quản lý cửa hàng sử dụng hệ thống để xem kết quả chất lượng dữ liệu.

## 3. Functional Requirements

| Mã | Yêu cầu chức năng | Actor |
|---|---|---|
| FR-01 | Hệ thống cho phép xem danh sách khách hàng. | Marketing |
| FR-02 | Hệ thống cho phép tìm kiếm khách hàng. | Marketing |
| FR-03 | Hệ thống cho phép kiểm tra dữ liệu thiếu hoặc sai định dạng. | Marketing |
| FR-04 | Hệ thống cho phép phát hiện khách hàng bị trùng. | Marketing |
| FR-05 | Hệ thống cho phép chuẩn hóa thông tin khách hàng. | Marketing |
| FR-06 | Hệ thống cho phép cập nhật dữ liệu khách hàng. | Marketing |
| FR-07 | Hệ thống cho phép xem kết quả chất lượng dữ liệu. | Quản lý cửa hàng |

## 4. Non-functional Requirements

> Các NFR và ngưỡng dưới đây là mức đề xuất cho bài tập,
> cần xác nhận lại với giảng viên nếu có yêu cầu riêng.

| Mã | Nhóm | Yêu cầu |
|---|---|---|
| NFR-01 | Hiệu năng | Thời gian phản hồi cho thao tác xem/tìm kiếm dữ liệu ≤ 3 giây với tập dữ liệu bài tập. |
| NFR-02 | Toàn vẹn dữ liệu | Không làm mất bản ghi trong quá trình cập nhật dữ liệu. |
| NFR-03 | Tính chính xác | Dữ liệu được xử lý phải tuân theo các quy tắc chất lượng dữ liệu đã định nghĩa. |
| NFR-04 | Khả năng sử dụng | Thông tin lỗi và dữ liệu cần xử lý phải được hiển thị rõ ràng. |
| NFR-05 | Môi trường | Notebook/Python phải chạy được trên môi trường đã cấu hình của dự án. |

## 5. Data Requirements

### 5.1. Nguồn dữ liệu

File dữ liệu đầu vào:

`customers_raw.csv`

Dữ liệu gồm 67.037 bản ghi và 6 cột:

- record_id
- ho_ten
- so_dien_thoai
- email
- dia_chi
- ngay_tao

### 5.2. Logic xử lý

Hệ thống thực hiện:

1. Kiểm tra dữ liệu thiếu.
2. Kiểm tra dữ liệu sai định dạng.
3. Phát hiện dữ liệu có khả năng trùng.
4. Chuẩn hóa thông tin khách hàng.
5. Cập nhật dữ liệu sau xử lý.
6. Tổng hợp kết quả chất lượng dữ liệu.

## 6. Traceability Matrix

| User Story | Use Case | Functional Requirement | Test Case |
|---|---|---|---|
| US01 | UC01 | FR-01 | TBD |
| US02 | UC02 | FR-02 | TBD |
| US03 | UC03 | FR-03 | TBD |
| US04 | UC04 | FR-04 | TBD |
| US05 | UC05 | FR-05 | TBD |
| US06 | UC06 | FR-06 | TBD |
| US07 | UC07 | FR-07 | TBD |