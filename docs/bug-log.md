# Nhật ký theo dõi lỗi (Bug Log) — Pipeline kiểm định và làm sạch dữ liệu khách hàng (Luồng L7)

Tài liệu này ghi nhận các lỗi kỹ thuật phát hiện được trong quá trình phát triển, kiểm thử và nạp kho dữ liệu Star Schema (Track DA), cách khắc phục và kiểm chứng.

---

## BUG-01 · Mức độ: **CRITICAL**

1. **Phát hiện bởi:** Phép thử nạp lại được (Idempotent test) khi chạy pipeline lần thứ hai trên cùng tập dữ liệu.
2. **Triệu chứng:** Pipeline nạp lần thứ hai gặp lỗi Foreign Key Constraint hoặc lỗi nhân đôi bản ghi: `sqlite3.IntegrityError: FOREIGN KEY constraint failed` khi cập nhật `dim_audit_run`.
3. **Cách tái lập:** Chạy `python -m src.pipeline` lần 1 thành công. Sau đó chạy tiếp `python -m src.pipeline` lần 2.
4. **Nguyên nhân:** Hàm `tao_phien_chay` ban đầu sử dụng `INSERT OR REPLACE INTO dim_audit_run`. Khi chạy lại, SQLite thực hiện `DELETE` bản ghi cũ có cùng `batch_id` rồi mới `INSERT` bản ghi mới. Thao tác xóa bản ghi cũ làm mất `run_key` mà bảng `fact_customer_quality_audit` đang tham chiếu đến (khóa ngoại Foreign Key), gây vi phạm toàn vẹn dữ liệu.
5. **Cách sửa:** Thay đổi cơ chế từ `INSERT OR REPLACE` sang kiểm tra trước bằng `SELECT run_key FROM dim_audit_run WHERE batch_id = ?`:
   - Nếu đã tồn tại: thực hiện lệnh `UPDATE dim_audit_run` để cập nhật thời gian chạy và số dòng, giữ nguyên `run_key` ban đầu.
   - Nếu chưa tồn tại: thực hiện `INSERT` mới.
   Đồng thời trong `nap_fact_quality`, xóa sạch các dòng fact cũ của cùng `run_key` trước khi nạp lại.
6. **Xác nhận:** Chạy lại pipeline 3 lần liên tiếp, số lượng bản ghi trong toàn bộ 4 bảng (`staging_customers`, `reject_rows`, `dim_customer`, `fact_customer_quality_audit`) hoàn toàn giữ nguyên, không lỗi Foreign Key &rarr; **PASS**.

---

## BUG-02 · Mức độ: **MAJOR**

1. **Phát hiện bởi:** Chạy thử nghiệm trên tập dữ liệu thực tế `customers_raw.csv` (67.037 bản ghi).
2. **Triệu chứng:** Pipeline bị văng lỗi `KeyError: 'ngay_dang_ky'` hoặc `KeyError: 'customer_id'`.
3. **Cách tái lập:** Gọi hàm `clean_customers.xu_ly_lam_sach_khach_hang(df_tho)` trực tiếp trên dữ liệu thô đọc từ CSV.
4. **Nguyên nhân:** File CSV thực tế của Mekong Mobile sử dụng tên cột là `record_id` và `ngay_tao`, trong khi mã nguồn thiết kế ban đầu giả định tên cột là `customer_id` và `ngay_dang_ky`.
5. **Cách sửa:** Trong hàm `xu_ly_lam_sach_khach_hang` và `src/quality/checks.py`, bổ sung cơ chế ánh xạ linh hoạt:
   - `cot_id = 'customer_id' if 'customer_id' in df.columns else 'record_id'`
   - `cot_ngay = 'ngay_dang_ky' if 'ngay_dang_ky' in df.columns else 'ngay_tao'`
   Sau đó chuẩn hóa thống nhất về `customer_id` và `ngay_dang_ky` trước khi chuyển sang các pha sau.
6. **Xác nhận:** Chạy thành công toàn bộ 67.037 dòng từ file CSV thật không còn gặp lỗi `KeyError` &rarr; **PASS**.

---

## BUG-03 · Mức độ: **MINOR**

1. **Phát hiện bởi:** Kiểm tra trạng thái rỗng khi vẽ biểu đồ phân bổ lỗi DQ với bộ lọc ngày xa trong tương lai.
2. **Triệu chứng:** Khi chạy `bieu_do_loi_dq(conn, p_rong, tu_ngay='2099-01-01')`, terminal báo lỗi `sqlite3.OperationalError: no such column: ngay_nap`.
3. **Cách tái lập:** Gọi `python -m src.dashboard.bieu_do --tu-ngay 2099-01-01`.
4. **Nguyên nhân:** Trong câu lệnh SQL truy vấn bảng `reject_rows`, mã nguồn gọi cột `ngay_nap`, trong khi định nghĩa DDL tại `sql/002_reject.sql` đặt tên cột thời gian là `thoi_gian_tao`.
5. **Cách sửa:** Sửa lại tên cột trong câu truy vấn tại `src/dashboard/bieu_do.py` từ `ngay_nap` thành `thoi_gian_tao`.
6. **Xác nhận:** Chạy lại hàm vẽ biểu đồ với bộ lọc ngày tương lai, hệ thống tự động sinh ảnh placeholder trạng thái rỗng `docs/trang_thai_rong_bieu_do.png` mà không hề crash &rarr; **PASS**.
