# Use Case Specification

## 1. Tổng quan

Hệ thống kiểm tra và làm sạch dữ liệu khách hàng có 2 actor:

- Marketing
- Quản lý cửa hàng

Hệ thống gồm 7 Use Case chính.

## 2. Danh sách Use Case

| Mã | Use Case | Actor |
|---|---|---|
| UC01 | Xem danh sách khách hàng | Marketing |
| UC02 | Tìm kiếm khách hàng | Marketing |
| UC03 | Kiểm tra dữ liệu thiếu hoặc sai định dạng | Marketing |
| UC04 | Phát hiện khách hàng bị trùng | Marketing |
| UC05 | Chuẩn hóa thông tin khách hàng | Marketing |
| UC06 | Cập nhật dữ liệu khách hàng | Marketing |
| UC07 | Xem kết quả chất lượng dữ liệu | Quản lý cửa hàng |

## 3. Đặc tả Use Case

### UC01 – Xem danh sách khách hàng

**Actor:** Marketing

**Mục tiêu:** Xem danh sách dữ liệu khách hàng hiện có.

**Luồng chính:**
1. Marketing truy cập chức năng danh sách khách hàng.
2. Hệ thống đọc dữ liệu khách hàng.
3. Hệ thống hiển thị danh sách khách hàng.
4. Marketing xem thông tin khách hàng.

**Luồng ngoại lệ:**
- Không có dữ liệu: hệ thống thông báo không có dữ liệu khách hàng.

---

### UC02 – Tìm kiếm khách hàng

**Actor:** Marketing

**Mục tiêu:** Tìm nhanh thông tin khách hàng cần kiểm tra.

**Luồng chính:**
1. Marketing nhập thông tin tìm kiếm.
2. Hệ thống nhận điều kiện tìm kiếm.
3. Hệ thống tìm kiếm trong dữ liệu khách hàng.
4. Hệ thống hiển thị kết quả phù hợp.

**Luồng ngoại lệ:**
- Không tìm thấy khách hàng phù hợp: hệ thống thông báo không có kết quả.

---

### UC03 – Kiểm tra dữ liệu thiếu hoặc sai định dạng

**Actor:** Marketing

**Mục tiêu:** Xác định các dữ liệu khách hàng bị thiếu hoặc sai định dạng.

**Luồng chính:**
1. Marketing thực hiện kiểm tra dữ liệu.
2. Hệ thống đọc dữ liệu khách hàng.
3. Hệ thống kiểm tra các trường dữ liệu theo quy tắc chất lượng.
4. Hệ thống xác định dữ liệu bị thiếu hoặc sai định dạng.
5. Hệ thống hiển thị kết quả kiểm tra.

**Luồng ngoại lệ:**
- File dữ liệu không thể đọc: hệ thống thông báo lỗi.
- Không phát hiện lỗi: hệ thống thông báo dữ liệu không có lỗi theo các quy tắc đã kiểm tra.

---

### UC04 – Phát hiện khách hàng bị trùng

**Actor:** Marketing

**Mục tiêu:** Xác định các bản ghi có khả năng thuộc cùng một khách hàng.

**Luồng chính:**
1. Marketing thực hiện chức năng phát hiện trùng.
2. Hệ thống chuẩn hóa các trường dùng để đối chiếu.
3. Hệ thống so sánh thông tin khách hàng.
4. Hệ thống xác định các bản ghi có khả năng trùng.
5. Hệ thống hiển thị kết quả.

**Luồng ngoại lệ:**
- Không phát hiện bản ghi có khả năng trùng: hệ thống thông báo không có kết quả.

---

### UC05 – Chuẩn hóa thông tin khách hàng

**Actor:** Marketing

**Mục tiêu:** Đưa thông tin khách hàng về định dạng thống nhất.

**Luồng chính:**
1. Marketing chọn dữ liệu cần chuẩn hóa.
2. Hệ thống áp dụng các quy tắc chuẩn hóa.
3. Hệ thống xử lý thông tin khách hàng.
4. Hệ thống hiển thị dữ liệu sau chuẩn hóa.

**Luồng ngoại lệ:**
- Dữ liệu không đáp ứng quy tắc chuẩn hóa: hệ thống đánh dấu để kiểm tra thủ công.

---

### UC06 – Cập nhật dữ liệu khách hàng

**Actor:** Marketing

**Mục tiêu:** Lưu dữ liệu khách hàng sau khi đã xử lý.

**Luồng chính:**
1. Marketing kiểm tra dữ liệu sau xử lý.
2. Marketing thực hiện cập nhật.
3. Hệ thống kiểm tra dữ liệu trước khi lưu.
4. Hệ thống lưu dữ liệu.
5. Hệ thống thông báo cập nhật thành công.

**Luồng ngoại lệ:**
- Dữ liệu không hợp lệ: hệ thống không cập nhật và thông báo lỗi.
- Không thể lưu dữ liệu: hệ thống thông báo lỗi cập nhật.

---

### UC07 – Xem kết quả chất lượng dữ liệu

**Actor:** Quản lý cửa hàng

**Mục tiêu:** Theo dõi tình trạng chất lượng dữ liệu khách hàng.

**Luồng chính:**
1. Quản lý cửa hàng truy cập kết quả chất lượng dữ liệu.
2. Hệ thống tổng hợp kết quả kiểm tra.
3. Hệ thống hiển thị kết quả chất lượng dữ liệu.
4. Quản lý cửa hàng xem kết quả.

**Luồng ngoại lệ:**
- Chưa có kết quả kiểm tra: hệ thống thông báo chưa có dữ liệu để hiển thị.

## 4. Quan hệ truy vết

| User Story | Use Case |
|---|---|
| US01 | UC01 |
| US02 | UC02 |
| US03 | UC03 |
| US04 | UC04 |
| US05 | UC05 |
| US06 | UC06 |
| US07 | UC07 |