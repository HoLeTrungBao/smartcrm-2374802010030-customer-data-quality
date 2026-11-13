# Test Plan rút gọn — Pipeline kiểm tra và làm sạch dữ liệu khách hàng (Luồng L7)

**Học phần:** Chuyên đề Tốt nghiệp 1 (71ITGR40203) — HK1, Năm học 2026–2027  
**Chuyên ngành (Track):** Data Analytics (DA) · **Luồng nghiệp vụ:** L7 – Customer Data Quality  
**Sinh viên thực hiện:** Hồ Lê Trung Bảo — **MSSV:** 2374802010030  

---

## 1. Phạm vi kiểm thử và phần chủ ý KHÔNG kiểm

### Được kiểm thử toàn diện:
- **Pha 1 (Extract):** Đọc tệp CSV dữ liệu thô nguyên trạng dạng chuỗi (`dtype=str`), bảo toàn số 0 ở đầu số điện thoại và các ký tự đặc biệt.
- **Pha 2 (Transform):** Chuẩn hóa số điện thoại (4 định dạng thực tế về 10 số `0xxxxxxxxx`), chuẩn hóa họ tên về Title Case, chuẩn hóa email RFC và đọc ngày tháng theo 3 định dạng (`yyyy-mm-dd`, `dd/mm/yyyy`, `yyyy.mm.dd`).
- **Pha 3 (Quality):** Đo lường định lượng 9 chỉ tiêu thuộc 3 chiều chất lượng (Đầy đủ, Chính xác, Nhất quán); phát hiện tỷ lệ khách hàng trùng lặp.
- **Pha 4 (Load):** Phân luồng dòng hợp lệ nạp vào `dim_customer` bằng khóa nghiệp vụ `customer_id` (`ON CONFLICT DO UPDATE`), nạp sự kiện kiểm định vào `fact_customer_quality_audit`; cách ly toàn bộ dòng lỗi vào `reject_rows` kèm lý do cụ thể cho con người đọc.
- **Tính Idempotent:** Chạy lại pipeline lần 2 trên cùng tập dữ liệu không làm nhân đôi số dòng trong kho dữ liệu Star Schema.
- **Bảo mật PII (NFR05):** Che mặt nạ 100% SĐT và Email hiển thị trên tầng phân tích.
- **Bộ kiểm thử hồi quy:** Bảo đảm các lỗi đã xử lý (`BUG-01`, `BUG-02`, `BUG-03`) không bị tái phát (`tests/test_hoi_quy.py`).

### Chủ ý KHÔNG kiểm thử, kèm lý do:
- **Giao diện Web/UI người dùng cuối bên ngoài:** Đây là hệ thống xử lý dữ liệu backend và kho Star Schema của Track DA; giao diện dashboard tương tác kéo thả thuộc phạm vi của Power BI / Metabase ở Bài tập 3.
- **Kiểm thử chịu tải ngoài 100.000 bản ghi:** Dữ liệu thực tế của Mekong Mobile hiện có 67.037 dòng, việc kiểm thử tải quy mô Big Data phân tán thuộc học phần Chuyên đề Tốt nghiệp 2.
- **Họ tên khách hàng chứa ký tự ngoài bảng chữ cái tiếng Việt:** Dữ liệu khách hàng nội địa chỉ chứa ký tự tiếng Việt có dấu và không dấu.

---

## 2. Loại test và số lượng mỗi tầng

| Tầng kiểm thử | Số lượng test case | Tệp mã nguồn phụ trách | Mô tả và Ghi chú |
| :--- | :---: | :--- | :--- |
| **Unit test các hàm chuẩn hóa** | 9 | `tests/test_rules.py` | Hàm thuần túy (Pure Functions), kiểm tra chuẩn hóa SĐT, họ tên, email, ngày, che PII. Không cần CSDL. |
| **Unit test phép đo chất lượng** | 2 | `tests/test_checks.py` | Kiểm tra đo 3 chiều chất lượng và cơ chế phân luồng dòng sạch vs dòng reject. |
| **Unit test module Dashboard** | 6 | `tests/test_dashboard.py` | Kiểm tra đếm dòng staging vs fact, giải thích chênh lệch, tạo biểu đồ và xử lý trạng thái rỗng (Empty State). |
| **Test hồi quy (Regression)** | 3 | `tests/test_hoi_quy.py` | Kiểm tra chống tái phát BUG-01 (Idempotent), BUG-02 (ánh xạ cột), BUG-03 (truy vấn SQL). |
| **Test tích hợp thực tế (End-to-End)** | 12 | `docs/test-report.md` (TC-01...TC-12) | Thực thi toàn luồng từ CSV nguồn đến CSDL kho SQLite `warehouse.db`. |

**Tổng cộng:** **20 test case tự động** chạy qua Pytest và **12 test case chạy thực nghiệm** có ảnh chụp minh chứng.

---

## 3. Tiêu chí thành công đo được

1. **100% test case tự động PASS** bằng một lệnh duy nhất: `python -m pytest -v` (thời gian thực thi dưới 2,0 giây).
2. **Tiêu chí Idempotent:** Chạy pipeline liên tiếp nhiều lần trên cùng dữ liệu đầu vào, số dòng ở cả 4 bảng đích giữ nguyên tuyệt đối:
   - `staging_customers`: 67.037 dòng.
   - `reject_rows`: 4.133 dòng.
   - `dim_customer`: 62.904 dòng.
   - `fact_customer_quality_audit`: 62.904 dòng.
3. **Tiêu chí Bảo toàn dữ liệu (Zero Data Loss):** Tổng số bản ghi staging ($67.037$) bằng chính xác tổng số khách hàng sạch ($62.904$) cộng số dòng bị từ chối ($4.133$).
4. **Tiêu chí Bảo vệ PII (NFR05):** 100% số điện thoại và email sau khi gọi hàm che mặt nạ đều được ẩn thông tin định danh (`0901***567`, `t***@gmail.com`).
5. **Tiêu chí Xử lý ngoại lệ:** Không có lỗi crash unhandled; khi dữ liệu lọc rỗng, dashboard tự động hiển thị thông báo giải thích thân thiện.

---

## 4. Môi trường và dữ liệu thử

- **Môi trường thực thi:** Python 3.11+ trên hệ điều hành Windows (Shell PowerShell). CSDL SQLite 3 lưu tại `data/processed/warehouse.db`.
- **Dữ liệu thử nghiệm:**
  - *Tập mẫu nhỏ (`data/mau/customers_sample.csv`):* 300 dòng phục vụ chạy thử nghiệm nhanh và kiểm chứng độc lập khi clone repo.
  - *Tập dữ liệu thực tế (`data/raw/customers_raw.csv`):* 67.037 bản ghi dữ liệu khách hàng thật của Mekong Mobile, bảo toàn nguyên vẹn các khuyết tật: SĐT có mã quốc tế, SĐT 8 số, thiếu họ tên, email trùng lặp.
  - *Dữ liệu giả lập bộ nhớ (`tests/conftest.py`):* Fixture 6 dòng mẫu bao phủ đủ trường hợp Đúng, Biên, Lỗi và Trùng lặp phục vụ unit test độc lập với CSDL.
