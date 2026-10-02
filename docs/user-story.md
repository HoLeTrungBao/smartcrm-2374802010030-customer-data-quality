# User Story

## 1. Mục tiêu

Mô tả nhu cầu của từng actor đối với sản phẩm kiểm tra và làm sạch dữ liệu khách hàng.

## 2. Danh sách User Story

| Mã | Actor | User Story | Ưu tiên |
|---|---|---|---|
| US01 | Marketing | Là nhân viên Marketing, tôi muốn xem danh sách khách hàng để kiểm tra thông tin khách hàng hiện có. | MUST |
| US02 | Marketing | Là nhân viên Marketing, tôi muốn tìm kiếm khách hàng để nhanh chóng tìm được thông tin cần kiểm tra. | MUST |
| US03 | Marketing | Là nhân viên Marketing, tôi muốn kiểm tra dữ liệu thiếu hoặc sai định dạng để xác định những thông tin khách hàng cần xử lý. | MUST |
| US04 | Marketing | Là nhân viên Marketing, tôi muốn phát hiện khách hàng bị trùng để xác định các bản ghi cần xử lý. | MUST |
| US05 | Marketing | Là nhân viên Marketing, tôi muốn chuẩn hóa thông tin khách hàng để dữ liệu có định dạng thống nhất. | MUST |
| US06 | Marketing | Là nhân viên Marketing, tôi muốn cập nhật dữ liệu khách hàng để lưu lại thông tin đã được xử lý và chuẩn hóa. | MUST |
| US07 | Quản lý cửa hàng | Là quản lý cửa hàng, tôi muốn xem kết quả chất lượng dữ liệu để biết tình trạng dữ liệu khách hàng sau khi xử lý. | MUST |

## 3. Acceptance Criteria – GWT

### US01
- **Given:** Dữ liệu khách hàng đã được nạp.
- **When:** Marketing mở danh sách khách hàng.
- **Then:** Hệ thống hiển thị danh sách khách hàng.

### US02
- **Given:** Danh sách khách hàng tồn tại.
- **When:** Marketing nhập thông tin tìm kiếm.
- **Then:** Hệ thống hiển thị các khách hàng phù hợp.

### US03
- **Given:** Dữ liệu khách hàng cần kiểm tra.
- **When:** Marketing thực hiện kiểm tra chất lượng dữ liệu.
- **Then:** Hệ thống xác định dữ liệu bị thiếu hoặc sai định dạng.

### US04
- **Given:** Dữ liệu khách hàng cần kiểm tra.
- **When:** Marketing thực hiện kiểm tra trùng.
- **Then:** Hệ thống xác định các bản ghi có khả năng bị trùng.

### US05
- **Given:** Có thông tin khách hàng cần chuẩn hóa.
- **When:** Marketing thực hiện chuẩn hóa.
- **Then:** Thông tin khách hàng được đưa về định dạng thống nhất.

### US06
- **Given:** Dữ liệu khách hàng đã được xử lý.
- **When:** Marketing cập nhật dữ liệu.
- **Then:** Dữ liệu đã xử lý được lưu lại.

### US07
- **Given:** Dữ liệu đã được kiểm tra và xử lý.
- **When:** Quản lý cửa hàng xem kết quả chất lượng dữ liệu.
- **Then:** Hệ thống hiển thị kết quả chất lượng dữ liệu.