# PHỤ LỤC: BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI

Theo yêu cầu của đề bài Bài tập 1 – Phân tích và Thiết kế (Học phần Chuyên đề Tốt nghiệp 1, TS. Nguyễn Trí Hải), sinh viên khai báo trung thực việc sử dụng các công cụ Trí tuệ Nhân tạo (AI) trong quá trình thực hiện bài tập như sau:

| Công cụ | Dùng vào việc gì | Áp dụng ở phần nào | Đã kiểm chứng thế nào |
| :--- | :--- | :--- | :--- |
| **ChatGPT / Antigravity AI** | Gợi ý cấu trúc bảng Fact và các bảng Dimension cho kho dữ liệu theo chuẩn Star Schema (Mô hình Kimball) phù hợp với bài toán Data Quality. | Mục 4 – Mô hình dữ liệu (`fact_customer_quality_audit`, `dim_customer`, `dim_quality_rule`, `dim_audit_run`). | Đối chiếu với lý thuyết Kimball về mô hình hóa kho dữ liệu; kiểm tra khóa chính, khóa ngoại, kiểu dữ liệu từng cột và tự phát biểu rõ ràng mức độ hạt (GRAIN) của bảng Fact. |
| **ChatGPT / Antigravity AI** | Hỗ trợ chuẩn hóa cấu trúc câu lập luận quyết định kiến trúc hệ thống theo đúng khuôn mẫu quy định của đề bài. | Mục 3 – Thiết kế kiến trúc (3 câu giải thích kiến trúc gắn với mã NFR và phân tích đánh đổi). | Tự đối chiếu với các yêu cầu phi chức năng (NFR01, NFR02, NFR03), rà soát ngưỡng số thực tế của tập dữ liệu $67.037$ bản ghi và tự thẩm định các đánh đổi kỹ thuật. |
| **— Không sử dụng AI —** *(Sinh viên tự làm hoàn toàn)* | Khám phá dữ liệu thực tế (Data Profiling) trên tập tin nguồn `customers_raw.csv`, tính toán các tỷ lệ thiếu dữ liệu, sai định dạng số điện thoại, viết hoa họ tên và tỷ lệ trùng lặp. | Mục 1 (Phạm vi) và Mục 4 (Bộ quy tắc chất lượng dữ liệu DQ01 – DQ06). | Tự viết và thực thi mã nguồn Python bằng thư viện Pandas trên Jupyter Notebook (`notebooks/01_check_customers.ipynb`), đối chiếu trực tiếp kết quả với số liệu thực tế ($67.037$ dòng, $11.336$ SĐT mã 84, $4.716$ email lặp). |
| **— Không sử dụng AI —** *(Sinh viên tự làm hoàn toàn)* | Xác định phạm vi nghiệp vụ L7, phân tích các Actor, viết User Story và xây dựng sơ đồ Use Case. | Mục 1 (Giới thiệu & phạm vi) và Mục 2 (Use Case). | Dựa trên đề cương bài học Buổi 2 và Buổi 4, tự vẽ sơ đồ Use Case trên draw.io và viết đặc tả luồng chính/ngoại lệ. |

---

### CAM KẾT LIÊM CHÍNH HỌC THUẬT

> **"Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp."**

* **Họ và tên sinh viên:** Hồ Lê Trung Bảo  
* **Mã số sinh viên (MSSV):** 2374802010030  
* **Lớp:** Chuyên đề Tốt nghiệp 1 – Track DA  
* **Ngày cam kết:** 09/10/2026  
