# ĐẶC TẢ USE CASE (USE CASE SPECIFICATION)
## LUỒNG NGHIỆP VỤ: L7 – KIỂM TRA VÀ LÀM SẠCH DỮ LIỆU KHÁCH HÀNG
**Học phần:** Chuyên đề Tốt nghiệp 1  
**Sinh viên thực hiện:** Hồ Lê Trung Bảo – MSSV: 2374802010030  
**Chuyên ngành (Track):** Data Analytics (DA)  

---

## 1. TỔNG QUAN

Hệ thống xác định 2 tác nhân (Actor):
* **Nhân viên Marketing:** Người dùng nghiệp vụ thực hiện kiểm tra, tìm kiếm, phát hiện trùng lặp và chuẩn hóa dữ liệu.
* **Quản lý cửa hàng:** Người dùng quản lý theo dõi dashboard kết quả chất lượng dữ liệu để ra quyết định khai thác.

Hệ thống bao gồm **7 Use Case chính** nằm bên trong ranh giới hệ thống:

| Mã Use Case | Tên Use Case | Actor chính | Mục đích nghiệp vụ |
| :---: | :--- | :---: | :--- |
| **UC01** | Xem danh sách khách hàng | Marketing | Xem danh sách thông tin khách hàng hiện có trong hệ thống có phân trang. |
| **UC02** | Tìm kiếm khách hàng | Marketing | Tìm nhanh thông tin khách hàng theo họ tên, số điện thoại hoặc email. |
| **UC03** | Kiểm tra dữ liệu thiếu hoặc sai định dạng | Marketing | Tự động quét và phát hiện các trường dữ liệu vi phạm quy tắc DQ01, DQ02, DQ05. |
| **UC04** | Phát hiện khách hàng bị trùng | Marketing | Nhận diện và nhóm các bản ghi khách hàng nghi ngờ trùng số điện thoại hoặc email. |
| **UC05** | Chuẩn hóa thông tin khách hàng | Marketing | Đưa số điện thoại về chuẩn 10 chữ số và chuẩn hóa họ tên về dạng viết hoa chữ cái đầu. |
| **UC06** | Cập nhật dữ liệu khách hàng | Marketing | Lưu trữ dữ liệu khách hàng đã làm sạch vào kho dữ liệu và ghi nhật ký kiểm định. |
| **UC07** | Xem kết quả chất lượng dữ liệu | Quản lý cửa hàng | Theo dõi trực quan các chỉ số KPI chất lượng dữ liệu qua dashboard tổng hợp. |

---

## 2. ĐẶC TẢ CHI TIẾT CÁC USE CASE QUAN TRỌNG NHẤT

### 2.1. Đặc tả chi tiết UC04 – Phát hiện khách hàng bị trùng

* **Mã Use Case:** UC04
* **Tên Use Case:** Phát hiện khách hàng bị trùng
* **Actor chính:** Nhân viên Marketing
* **Mục tiêu:** Nhận diện và gom nhóm các bản ghi khách hàng có khả năng thuộc cùng một cá nhân dựa trên sự trùng lặp số điện thoại hoặc email sau chuẩn hóa.
* **Điều kiện tiên quyết (Pre-condition):** Dữ liệu khách hàng đã được nạp vào hệ thống và các trường số điện thoại, email đã qua bước làm sạch định dạng cơ bản.
* **Điều kiện sau (Post-condition):** Hệ thống tạo danh sách các nhóm bản ghi trùng lặp và gắn cờ `is_duplicate = TRUE` trong kho dữ liệu audit.
* **User Story liên quan:** US04 (Mức MoSCoW: MUST)
* **Luồng chính (Main Flow):**
  1. Người dùng chọn chức năng "Phát hiện khách hàng trùng lặp" trên thanh menu.
  2. Người dùng chọn tiêu chí đối sánh (Mặc định: Số điện thoại chuẩn hóa, Email).
  3. Người dùng nhấn nút "Bắt đầu quét trùng lặp".
  4. Hệ thống thực thi thuật toán gom nhóm trên tập dữ liệu $67.037$ bản ghi, phát hiện các giá trị số điện thoại hoặc email xuất hiện từ 2 lần trở lên.
  5. Hệ thống thống kê tổng số nhóm trùng ($16.039$ bản ghi trùng SĐT, $9.004$ bản ghi trùng email).
  6. Hệ thống hiển thị bảng danh sách các nhóm nghi ngờ trùng lặp kèm thông tin chi tiết (mã bản ghi, họ tên, SĐT, email, ngày tạo).
  7. Người dùng xem chi tiết từng cụm bản ghi và nhấn "Xác nhận danh sách trùng lặp".
* **Luồng ngoại lệ (Exception Flow):**
  * **3a. Dữ liệu chưa qua chuẩn hóa số điện thoại:**
    * 3a1. Hệ thống phát hiện trường số điện thoại còn chứa tiền tố `84` / `+84` hoặc dấu chấm phân cách.
    * 3a2. Hệ thống hiển thị thông báo cảnh báo: *"Dữ liệu số điện thoại chưa được chuẩn hóa, kết quả đối sánh có thể bị sai lệch. Bạn có muốn chuẩn hóa tự động trước khi quét không?"*.
    * 3a3. Nếu người dùng chọn "Đồng ý", hệ thống tự động kích hoạt Use Case UC05 rồi quay lại bước 4. Nếu người dùng chọn "Bỏ qua", hệ thống tiếp tục bước 4 với cảnh báo đính kèm.
  * **4a. Không phát hiện bản ghi nào trùng lặp:**
    * 4a1. Hệ thống hiển thị thông báo: *"Không phát hiện khách hàng trùng lặp theo tiêu chí đã chọn"*.
    * 4a2. Hệ thống kết thúc Use Case và quay về màn hình chính.

---

### 2.2. Đặc tả chi tiết UC05 – Chuẩn hóa thông tin khách hàng

* **Mã Use Case:** UC05
* **Tên Use Case:** Chuẩn hóa thông tin khách hàng
* **Actor chính:** Nhân viên Marketing
* **Mục tiêu:** Áp dụng bộ quy tắc làm sạch để đưa số điện thoại về chuẩn 10 chữ số (0xxxxxxxxx), xóa khoảng trắng thừa và viết hoa chữ cái đầu cho họ tên.
* **Điều kiện tiên quyết (Pre-condition):** Tập dữ liệu khách hàng thô đã được nạp thành công vào hệ thống.
* **Điều kiện sau (Post-condition):** Dữ liệu tạm thời được chuẩn hóa hoàn tất, sẵn sàng để thực hiện cập nhật vào kho dữ liệu sạch.
* **User Story liên quan:** US05 (Mức MoSCoW: MUST)
* **Luồng chính (Main Flow):**
  1. Người dùng chọn chức năng "Chuẩn hóa thông tin khách hàng".
  2. Hệ thống hiển thị danh sách các quy tắc chuẩn hóa khả dụng (Chuẩn hóa SĐT 10 số, Xóa khoảng trắng họ tên, Viết hoa chữ cái đầu họ tên, Chuyển email về chữ thường).
  3. Người dùng tích chọn các quy tắc cần áp dụng và nhấn "Thực hiện chuẩn hóa".
  4. Hệ thống chạy thuật toán làm sạch tuần tự qua các bản ghi:
     * Quy tắc SĐT: Loại bỏ ký tự lạ, chuyển tiền tố `84`/`+84` thành `0`.
     * Quy tắc họ tên: Cắt tỉa khoảng trắng đầu/cuối, chuẩn hóa Title Case.
     * Quy tắc email: Chuyển toàn bộ về chữ in thường (lowercase).
  5. Hệ thống hiển thị màn hình đối chiếu kết quả trước và sau chuẩn hóa, kèm thống kê số lượng bản ghi đã được xử lý thành công.
  6. Người dùng kiểm tra mẫu kết quả và nhấn "Xác nhận kết quả chuẩn hóa".
* **Luồng ngoại lệ (Exception Flow):**
  * **4a. Bản ghi có số điện thoại không thể tự động sửa:**
    * 4a1. Hệ thống phát hiện số điện thoại sau khi lọc ký tự lạ có độ dài không bằng 10 chữ số (ví dụ: bị thiếu số hoặc thừa số do nhập liệu sai).
    * 4a2. Hệ thống không thay đổi trường số điện thoại gốc, gắn cờ `is_invalid_format = TRUE` và đưa vào danh sách *"Bản ghi lỗi cần kiểm tra thủ công"*.
    * 4a3. Hệ thống tiếp tục xử lý các bản ghi còn lại và xuất báo cáo số lượng bản ghi không thể tự động sửa ở bước 5.