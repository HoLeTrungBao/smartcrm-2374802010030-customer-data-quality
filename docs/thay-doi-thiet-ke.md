# Nhật ký thay đổi thiết kế (Design Change Log)

Tài liệu này ghi nhận toàn bộ các điều chỉnh, cải tiến và hoàn thiện thiết kế hệ thống trong quá trình chuyển giao từ **Bài tập 1 (Phân tích & Thiết kế)** sang **Bài tập 2 (Hiện thực hóa module cốt lõi)**, dựa trên góp ý trực tiếp từ Giảng viên hướng dẫn và các bài học kiểm chứng thực tế trên dữ liệu khách hàng Mekong Mobile (Luồng L7).

Mỗi thay đổi được cấu trúc chặt chẽ theo 3 thành phần: **Thay đổi gì · Vì sao · Ảnh hưởng tới thành phần nào**.

---

## 1. Đồng bộ và thống nhất bộ tên cột duy nhất giữa Sơ đồ Star Schema, Từ điển dữ liệu và Mã nguồn

- **Thay đổi gì:** Thống nhất bộ tên cột chuẩn cho toàn bộ mô hình dữ liệu Star Schema. Cụ thể:
  - Khóa định danh khách hàng tự nhiên: dùng duy nhất `customer_id` (thay vì lẫn lộn `record_id`).
  - Dữ liệu họ tên và số điện thoại trước/sau làm sạch: dùng `ho_ten_raw`, `ho_ten_clean`, `so_dien_thoai_raw`, `so_dien_thoai_clean` (loại bỏ `ho_ten_goc`).
  - Cờ trạng thái kiểm định và số lượng lỗi trong bảng Fact: dùng `is_valid` và `error_count` (loại bỏ `is_passed`, `quality_score`).
  - Bổ sung trường `batch_id` vào `dim_audit_run`, `reject_rows` và `quality_measures` để quản lý theo lô dữ liệu.
- **Vì sao:** Khắc phục trực tiếp nhận xét của Giảng viên ở BT1 (*"Sơ đồ Star Schema không khớp từ điển dữ liệu 4.4"*). Việc chốt một bộ tên cột duy nhất là tiên quyết trước khi viết mã nguồn ETL để tránh lỗi truy vấn SQL và bảo đảm tính nhất quán (Consistency).
- **Ảnh hưởng:** `docs/erd.drawio`, `docs/data-requirements.md`, các tập tin DDL tại `sql/` (`010_dim.sql`, `020_fact.sql`), các module `src/load/` và từ điển dữ liệu.

---

## 2. Bổ sung Bảng thuật ngữ bắt buộc (Glossary) vào tài liệu phân tích

- **Thay đổi gì:** Bổ sung Bảng thuật ngữ chuyên ngành và nghiệp vụ vào Mục 1 tài liệu phân tích, định nghĩa rõ các khái niệm: Data Profiling, Data Cleansing, Duplicate Detection, Star Schema, Fact Table, Dimension Table, Idempotent Pipeline, Reject Rows, PII (Personally Identifiable Information), Title Case.
- **Vì sao:** Khắc phục nhận xét của Giảng viên ở BT1 (*"Mục 1 thiếu bảng thuật ngữ bắt buộc"*). Đảm bảo người đọc nghiệp vụ và kỹ thuật có cùng cách hiểu thống nhất về các khái niệm cốt lõi của luồng L7.
- **Ảnh hưởng:** `docs/srs.md` (Mục 1.0 Thuật ngữ), tài liệu báo cáo tổng hợp.

---

## 3. Bổ sung Bảng ma trận truy vết gộp (Traceability Matrix)

- **Thay đổi gì:** Bổ sung bảng ma trận truy vết đa chiều tích hợp trong một bảng duy nhất: `Mã FR` $\leftrightarrow$ `Mã User Story (US)` $\leftrightarrow$ `Mã Use Case (UC)` $\leftrightarrow$ `Mức ưu tiên MoSCoW` $\leftrightarrow$ `Module mã nguồn phụ trách`.
- **Vì sao:** Khắc phục nhận xét của Giảng viên ở BT1 (*"Chưa có mục 6 bảng truy vết FR ↔ US ↔ UC ↔ MoSCoW gộp trong một bảng"*). Giúp giảng viên và nhóm phát triển truy vết trực tiếp từ yêu cầu nghiệp vụ đến hàm mã nguồn tương ứng.
- **Ảnh hưởng:** `docs/srs.md` (Mục 6), cấu trúc phân rã module trong `src/transform/` và `src/quality/`.

---

## 4. Bổ sung Actor Quản trị viên hệ thống và chú thích ký hiệu trên Sơ đồ Use Case

- **Thay đổi gì:** Cập nhật sơ đồ Use Case (`docs/usecase.drawio`), bổ sung rõ ràng Actor **Quản trị viên hệ thống** kết nối với ca sử dụng cấu hình/giám sát pipeline; đồng thời thêm bảng chú thích (Legend) giải thích các ký hiệu Actor, Use Case, Association, Include/Extend trên sơ đồ.
- **Vì sao:** Khắc phục nhận xét của Giảng viên ở BT1 (*"Sơ đồ Use Case chưa có chú thích ký hiệu; actor Quản trị viên hệ thống có ở 1.2 nhưng không có trên sơ đồ"*).
- **Ảnh hưởng:** `docs/usecase.drawio`, `docs/usecase.png`, tài liệu `docs/use-case.md`.

---

## 5. Xác định ngưỡng số đo lường cụ thể cho yêu cầu phi chức năng NFR05 (Bảo mật PII)

- **Thay đổi gì:** Định lượng hóa tiêu chí NFR05 thành: *"100% màn hình giao diện và kết quả truy vấn đối với vai trò không có thẩm quyền đều phải che mặt nạ (Masking) số điện thoại (chỉ hiển thị 4 số cuối, ví dụ `******6789`) và email (ví dụ `a***@gmail.com`); tỷ lệ lộ PII là 0,00%"*.
- **Vì sao:** Khắc phục nhận xét của Giảng viên ở BT1 (*"NFR05 chưa có ngưỡng số đo được"*), tuân thủ nguyên tắc mọi NFR đều phải đo đạc và kiểm chứng được bằng số liệu.
- **Ảnh hưởng:** `docs/srs.md` (Mục 1.4 NFR05), thiết kế hàm che dữ liệu trong `src/transform/rules.py` và kiểm thử bảo mật.

---

## 6. Ghi chú rõ Use Case phục vụ cho từng màn hình Wireframe

- **Thay đổi gì:** Bổ sung ánh xạ trực tiếp trên từng màn hình Wireframe:
  - **Màn hình 1 (Tổng quan chất lượng dữ liệu):** Phục vụ trực tiếp cho **UC07** (Xem kết quả chất lượng dữ liệu).
  - **Màn hình 2 (Danh sách khách hàng & Đối soát lỗi):** Phục vụ trực tiếp cho **UC01** (Xem danh sách), **UC02** (Tìm kiếm) và **UC05** (Chuẩn hóa thông tin).
  - **Màn hình 3 (Quản lý tỷ lệ xử lý & Báo cáo):** Phục vụ trực tiếp cho **UC04** (Phát hiện khách hàng trùng) và **UC06** (Cập nhật dữ liệu sạch vào kho).
- **Vì sao:** Khắc phục nhận xét của Giảng viên ở BT1 (*"Wireframe chưa ghi mỗi màn hình phục vụ UC nào"*), đảm bảo tính kết nối giữa thiết kế giao diện và đặc tả chức năng.
- **Ảnh hưởng:** `docs/wireframe.drawio`, `docs/wireframe.png`, tài liệu mô tả wireframe.

---

## 7. Sinh mã lô (batch_id) theo phạm vi dữ liệu để đảm bảo tính Idempotent (Chạy lại được)

- **Thay đổi gì:** Mã lô (`batch_id`) được sinh xác định theo phạm vi dữ liệu đầu vào (ví dụ `lo-toan-bo`), thay vì dùng dấu thời gian `datetime.now()`.
- **Vì sao:** Bài học từ mô hình mẫu: Dấu thời gian khiến mỗi lần chạy tạo một lô mới làm bảng staging và bảng reject phình to liên tục khi chạy lại. Dùng mã lô cố định cho phép thực hiện cơ chế nạp lại an toàn (xóa bản ghi của lô cũ rồi nạp lại hoặc cập nhật), bảo đảm chạy lần 2 số lượng bản ghi không bị nhân đôi (thỏa mãn tiêu chí cốt lõi C5 của BT2).
- **Ảnh hưởng:** `src/pipeline.py`, `src/load/load_staging.py`, `sql/002_reject.sql`.

---

## 8. Bổ sung bảng `reject_rows` và `quality_measures` vào kho dữ liệu

- **Thay đổi gì:** Bổ sung bảng `reject_rows` (lưu trữ các dòng không thể tự động sửa kèm lý do viết cho con người đọc) và bảng `quality_measures` (lưu kết quả định lượng của từng phép đo chất lượng qua các phiên chạy).
- **Vì sao:** Đảm bảo nguyên tắc *"không nuốt lỗi âm thầm"* và đáp ứng trực tiếp tiêu chí D3 của BT2 (*"Bảng reject có dòng, lý do viết cho người"*).
- **Ảnh hưởng:** `sql/002_reject.sql`, `src/load/load_staging.py`, `src/quality/checks.py`.
