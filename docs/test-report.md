# Test Report — Pipeline kiểm tra và làm sạch dữ liệu khách hàng (Luồng L7)

**Học phần:** Chuyên đề Tốt nghiệp 1 (71ITGR40203) — HK1, Năm học 2026–2027  
**Chuyên ngành (Track):** Data Analytics (DA) · **Luồng nghiệp vụ:** L7 – Customer Data Quality  
**Sinh viên thực hiện:** Hồ Lê Trung Bảo — **MSSV:** 2374802010030  
**Tình trạng tổng quan:** **20/20 test tự động PASS** qua Pytest (`python -m pytest -v`) và **12/12 test case thực nghiệm đạt PASS**, có ảnh chụp minh chứng lưu tại `docs/screenshots/`.

---

## Bảng tổng hợp kết quả 12 Test Case chạy thật (Đủ 8 cột chuẩn)

| Mã | Tiền điều kiện | Các bước thực hiện | Dữ liệu thử | Kết quả mong đợi | Mức ưu tiên | Kết quả thực tế quan sát được | P/F |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **TC-01** | CSDL chưa khởi tạo hoặc đã xóa trống | Chạy `python -m src.pipeline` trên tập dữ liệu mẫu nhỏ | `data/mau/customers_sample.csv` (300 bản ghi) | Pipeline hoàn tất; nạp đúng 280 khách sạch vào `dim_customer` và 20 dòng vào `reject_rows` | **Cao** | Khởi tạo bảng DDL, đọc 300 dòng, nạp 280 dim_customer, 20 reject_rows; mã thoát 0 | **PASS** |
| **TC-02** | Không | Gọi hàm `chuan_hoa_ho_ten` với chuỗi chứa nhiều khoảng trắng và chữ hoa/thường lộn xộn | `' nguyễn văn an '`, `'TRẦN THỊ BÌNH'` | Chuẩn hóa về Title Case, xóa khoảng trắng thừa: `'Nguyễn Văn An'`, `'Trần Thị Bình'` | **Cao** | Trả về đúng `'Nguyễn Văn An'`, `'Trần Thị Bình'` | **PASS** |
| **TC-03** | Không | **Giá trị biên tiền tố quốc tế SĐT:** Gọi `chuan_hoa_dien_thoai` với mã `+84` và `84` | `'+84901234567'` (12 ký tự) và `'84901234567'` (11 ký tự) | Cắt tiền tố quốc tế, quy đổi chính xác về 10 số chuẩn `'0901234567'` | **Cao** | Cả hai trường hợp đều trả về `'0901234567'` | **PASS** |
| **TC-04** | Không | **Giá trị biên ngày:** Gọi `doc_ngay` tại mốc giao thừa chuyển giao năm | `'2024-12-31'`, `'2025-01-01'`, `'15/05/2025'` | Parse chính xác thành `date(2024,12,31)`, `date(2025,1,1)`, `date(2025,5,15)` | **Cao** | Trả về đúng đối tượng `datetime.date`, không lệch ngày | **PASS** |
| **TC-05** | Không | **Dữ liệu sai:** Dòng có số điện thoại rác hoặc thiếu chữ số | SĐT 8 chữ số: `'09012345'`, SĐT chứa chữ cái: `'0901abc567'` | Hàm trả về `None`; khi chạy pipeline dòng này bị cách ly vào `reject_rows`, pipeline không sập | **Cao** | Trả về `None`; nạp vào `reject_rows` kèm lý do chi tiết; pipeline chạy thông suốt | **PASS** |
| **TC-06** | Không | **Dữ liệu sai bắt buộc:** Dòng bị rỗng mã khách hàng hoặc thiếu họ tên | `customer_id='   '`, `ho_ten='nan'` | Nhận diện lỗi thiếu trường bắt buộc; gắn mã `DQ01_ID`, `DQ01_NAME` vào `reject_rows` | **Cao** | Phân loại đúng mã quy tắc vi phạm và ghi nhận lý do rõ ràng cho đối soát viên | **PASS** |
| **TC-07** | Không | **Bảo mật dữ liệu PII (NFR05):** Gọi hàm che mặt nạ SĐT và Email | SĐT `'0901234567'`, Email `'trungbao@gmail.com'` | SĐT hiển thị `'0901***567'`; Email hiển thị `'t***@gmail.com'`; tỷ lệ rò rỉ 0,00% | **Cao** | Kết quả che đúng định dạng, bảo vệ an toàn danh tính khách hàng trên báo cáo | **PASS** |
| **TC-08** | Không | **Chất lượng dữ liệu:** Đo 3 chiều Đầy đủ, Chính xác, Nhất quán qua `checks.do_tat_ca` | Fixture 6 dòng mẫu (`du_lieu_khach_hang_mau`) | Trả về danh sách dataclass `Do` có đủ 9 số đo định lượng (số kiểm, số đạt, tỷ lệ %) | **Cao** | Đo lường đủ 9 chỉ tiêu; mỗi phép đo trả về 1 số cụ thể đối chiếu với ngưỡng YAML | **PASS** |
| **TC-09** | Không | **Đo chiều Nhất quán (Uniqueness):** Phát hiện tỷ lệ khách hàng trùng lặp | Tập dữ liệu thực tế 67.037 dòng | Phát hiện 27.123 khách hàng có dấu hiệu trùng SĐT/Email ($43,1\%$ &le; ngưỡng $70\%$) | **Cao** | Gán cờ `is_duplicate=1` cho 27.123 bản ghi; tỷ lệ trùng lặp 43,1% đạt ngưỡng cho phép | **PASS** |
| **TC-10** | Đã chạy pipeline lần 1 trên 67.037 dòng thật | **Phép thử Nạp lại được (Idempotent):** Chạy lại `python -m src.pipeline` lần 2 và lần 3 | Cùng tập dữ liệu `customers_raw.csv` (67.037 dòng) | Số lượng bản ghi ở cả 4 bảng trong kho CSDL hoàn toàn không đổi: 67.037 / 4.133 / 62.904 / 62.904 | **Cao** | Lần 1: 67.037 / 4.133 / 62.904 / 62.904.<br>Lần 2: 67.037 / 4.133 / 62.904 / 62.904.<br>Không nhân đôi dữ liệu | **PASS** |
| **TC-11** | Đã hoàn tất nạp kho dữ liệu | **Đối chiếu dòng Staging vs Fact:** Chạy `python -m src.dashboard.so_sanh_dong` | CSDL kho `warehouse.db` | Staging ($67.037$) &minus; Fact ($62.904$) = $4.133$ dòng. Chênh lệch bằng số dòng trong `reject_rows` | **Cao** | In bảng đối chiếu rõ ràng; xác nhận $4.133$ dòng chênh lệch nằm trong bảng reject &rarr; Không mất dữ liệu | **PASS** |
| **TC-12** | Có CSDL kho dữ liệu | **Xử lý trạng thái rỗng (Empty State):** Vẽ biểu đồ với bộ lọc ngày không có dữ liệu | `--tu-ngay 2099-01-01 --den-ngay 2099-12-31` | Không phát sinh ngoại lệ; tự động tạo tệp ảnh placeholder giải thích thân thiện cho người dùng | **Cao** | Tạo ảnh `docs/trang_thai_rong_bieu_do.png` hiển thị hộp cảnh báo màu vàng, không crash ứng dụng | **PASS** |

---

## Ghi chú về tính trung thực và minh chứng thực nghiệm

- Toàn bộ 12 test case trên đều được chạy trực tiếp trên môi trường thực tế (Python 3.11+, CSDL SQLite `data/processed/warehouse.db`, dữ liệu nguồn `customers_raw.csv` gồm 67.037 bản ghi).
- Các ảnh chụp terminal và minh chứng trực quan cho từng ca kiểm thử được lưu trữ đầy đủ tại thư mục `docs/screenshots/` (đặt tên chuẩn từ `TC-01.png` đến `TC-12.png`).
- Kết quả đối soát số dòng trước và sau khi chạy:
  - `staging_customers`: **67.037 bản ghi** (giữ nguyên trạng dữ liệu nguồn).
  - `dim_customer`: **62.904 bản ghi** (khách hàng đạt chuẩn được làm sạch).
  - `reject_rows`: **4.133 bản ghi** (dòng không đạt chuẩn kèm lý do chi tiết).
  - `fact_customer_quality_audit`: **62.904 bản ghi** (sự kiện kiểm định chất lượng từng khách hàng sạch).
- Chênh lệch $67.037 - 62.904 = 4.133$ dòng khớp tuyệt đối với số dòng trong bảng reject, khẳng định hệ thống **bảo toàn dữ liệu 100%, không nuốt lỗi âm thầm**.
