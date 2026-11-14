# PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI

**Học phần:** Chuyên đề Tốt nghiệp 1 (71ITGR40203) — Giảng viên hướng dẫn: ThS. Nguyễn Minh Tân  
**Sinh viên thực hiện:** Hồ Lê Trung Bảo — **MSSV:** 2374802010030  
**Chuyên ngành:** Data Analytics (DA) · **Luồng nghiệp vụ:** L7 – Customer Data Quality  
**Phiên bản phát hành:** `v1.0`

---

## 1. Khai báo AI cho Giai đoạn 3 (Bài tập 3: Kiểm thử, Đóng gói & Triển khai)

Theo quy định học phần, sinh viên khai báo trung thực việc sử dụng các công cụ Trí tuệ Nhân tạo (AI) trong quá trình thực hiện Bài tập 3:

| Công cụ | Dùng vào việc gì | Áp dụng ở phần nào | Đã kiểm chứng thế nào |
| :--- | :--- | :--- | :--- |
| **Antigravity AI / Gemini** | Hỗ trợ cấu trúc tài liệu kỹ thuật tiếng Anh (Pipeline documentation & Data dictionary) chuẩn hóa theo định dạng Markdown. | `docs/pipeline-doc.md`, `docs/data-dictionary.md`, `DEPLOYMENT.md`. | Tự đối chiếu và rà soát từng bảng, từng cột với tệp DDL thật trong thư mục `sql/` và lệnh `.schema` của SQLite; chỉnh sửa các thông số số liệu khớp $100\%$ với kết quả chạy trên $67.037$ bản ghi nguồn. |
| **Antigravity AI / Gemini** | Hỗ trợ cú pháp cấu hình `Dockerfile` nhiều lớp tối ưu hóa cache và cú pháp `docker-compose.yml` có healthcheck. | `Dockerfile`, `docker-compose.yml`. | Tự chạy thử nghiệm kiểm tra tính hợp lệ bằng các script chạy máy trắng (`scripts/run_clean_test.py`, `run_clean_test.bat`) trên dữ liệu mẫu $300$ dòng; kiểm tra trạng thái thoát mã 0 và đối soát số dòng. |
| **— Không sử dụng AI —** *(Sinh viên tự làm)* | Viết và thực thi toàn bộ mã nguồn xử lý ETL (`src/extract/`, `src/transform/`, `src/quality/`, `src/load/`, `src/dashboard/`). | Toàn bộ mã nguồn cốt lõi trong thư mục `src/`. | Tự chạy kiểm thử với $20/20$ test case đạt `PASSED` qua Pytest (`python -m pytest -v`), nạp $62.904$ khách hàng sạch và cách ly $4.133$ dòng lỗi. |
| **— Không sử dụng AI —** *(Sinh viên tự làm)* | Thực nghiệm phép thử nạp lại được (Idempotent test) và đối soát dữ liệu kho Star Schema. | `tests/test_hoi_quy.py`, `src/dashboard/so_sanh_dong.py`. | Tự chạy lặp lại 3 lần trên cùng tập dữ liệu nguồn, truy vấn CSDL SQLite xác nhận số lượng bản ghi không hề bị nhân đôi và bảo toàn dữ liệu tuyệt đối. |

---

## 2. Khai báo AI cho Giai đoạn 1 & Giai đoạn 2 (Phân tích, Thiết kế & Hiện thực hóa)

| Công cụ | Dùng vào việc gì | Áp dụng ở phần nào | Đã kiểm chứng thế nào |
| :--- | :--- | :--- | :--- |
| **ChatGPT / Antigravity AI** | Gợi ý cấu trúc bảng Fact và các bảng Dimension cho kho dữ liệu theo chuẩn Star Schema (Mô hình Kimball) phù hợp với bài toán Data Quality. | Mô hình dữ liệu (`fact_customer_quality_audit`, `dim_customer`, `dim_quality_rule`, `dim_audit_run`). | Đối chiếu với lý thuyết Kimball về mô hình hóa kho dữ liệu; kiểm tra khóa chính, khóa ngoại, kiểu dữ liệu từng cột và tự phát biểu rõ ràng mức độ hạt (GRAIN) của bảng Fact. |
| **ChatGPT / Antigravity AI** | Hỗ trợ chuẩn hóa cấu trúc câu lập luận quyết định kiến trúc hệ thống theo đúng khuôn mẫu quy định của đề bài. | Thiết kế kiến trúc (3 câu giải thích kiến trúc gắn với mã NFR và phân tích đánh đổi). | Tự đối chiếu với các yêu cầu phi chức năng (NFR01, NFR02, NFR03), rà soát ngưỡng số thực tế của tập dữ liệu $67.037$ bản ghi và tự thẩm định các đánh đổi kỹ thuật. |
| **— Không sử dụng AI —** *(Sinh viên tự làm)* | Khám phá dữ liệu thực tế (Data Profiling) trên tập tin nguồn `customers_raw.csv`, tính toán các tỷ lệ thiếu dữ liệu, sai định dạng số điện thoại, viết hoa họ tên và tỷ lệ trùng lặp. | Bộ quy tắc chất lượng dữ liệu DQ01 – DQ06. | Tự viết và thực thi mã nguồn Python bằng thư viện Pandas trên Jupyter Notebook (`notebooks/01_check_customers.ipynb`), đối chiếu trực tiếp kết quả với số liệu thực tế ($67.037$ dòng, $11.336$ SĐT mã 84, $4.716$ email lặp). |
| **— Không sử dụng AI —** *(Sinh viên tự làm)* | Xác định phạm vi nghiệp vụ L7, phân tích các Actor, viết User Story và xây dựng sơ đồ Use Case. | Giới thiệu phạm vi nghiệp vụ và Use Case. | Dựa trên đề cương bài học Buổi 2 và Buổi 4, tự vẽ sơ đồ Use Case trên draw.io và viết đặc tả luồng chính/ngoại lệ. |

---

### CAM KẾT LIÊM CHÍNH HỌC THUẬT

> **"Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp."**

* **Họ và tên sinh viên:** Hồ Lê Trung Bảo  
* **Mã số sinh viên (MSSV):** 2374802010030  
* **Lớp:** Chuyên đề Tốt nghiệp 1 (71ITGR40203_01) – Track DA  
* **Ngày cam kết:** 14/11/2026  
