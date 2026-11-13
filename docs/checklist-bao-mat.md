# Checklist Bảo Mật — SmartCRM Customer Data Quality (Luồng L7)

**Học phần:** Chuyên đề Tốt nghiệp 1 (71ITGR40203) — HK1, Năm học 2026–2027  
**Chuyên ngành:** Data Analytics (DA) · **Luồng nghiệp vụ:** L7 – Customer Data Quality  
**Sinh viên thực hiện:** Hồ Lê Trung Bảo — **MSSV:** 2374802010030  
**Repository:** [smartcrm-2374802010030-customer-data-quality](https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality)  
**Phiên bản phát hành:** `v1.0`

---

## Bảng Checklist Bảo Mật (Đủ 7 Mục — Mỗi Mục Một Dòng Minh Chứng Cụ Thể)

Theo quy định đánh giá tiêu chí **C6**, bảng dưới đây kê khai trung thực trạng thái bảo mật của hệ thống:

| STT | Hạng mục kiểm tra bảo mật | Trạng thái | Dòng minh chứng cụ thể / Vị trí mã nguồn |
| :-: | :--- | :---: | :--- |
| **1** | **Quản lý bí mật & Biến môi trường** | **ĐÃ LÀM** | Bí mật và đường dẫn được cô lập trong `.env` (đã khai báo trong `.gitignore`); tệp mẫu an toàn [`.env.example`](../.env.example) cung cấp đủ biến. |
| **2** | **Khóa cứng phiên bản thư viện (C6)** | **ĐÃ LÀM** | 100% thư viện phụ thuộc được khóa phiên bản chính xác bằng toán tử `==` trong [`requirements.txt`](../requirements.txt), không có cảnh báo CVE nghiêm trọng. |
| **3** | **Bảo vệ dữ liệu cá nhân PII (NFR05/D4)** | **ĐÃ LÀM** | 100% SĐT (`0901***567`) và Email (`t***@gmail.com`) được che mặt nạ qua hàm thuần `rules.py::che_mat_na_pii`, tỷ lệ rò rỉ $0,00\%$. |
| **4** | **Phòng chống tấn công SQL Injection** | **ĐÃ LÀM** | 100% câu truy vấn và nạp dữ liệu trong `src/load/` và `src/dashboard/` đều sử dụng tham số hóa (`?`), tuyệt đối không cộng chuỗi SQL. |
| **5** | **Phân quyền tối thiểu trong Container** | **ĐÃ LÀM** | `Dockerfile` cấu hình chạy toàn bộ tiến trình dưới người dùng không đặc quyền `appuser` (UID `10001`), không dùng root. |
| **6** | **Xác thực & Phân quyền truy cập (Auth)** | **KHÔNG ÁP DỤNG** | Hệ thống là Batch ETL Pipeline chạy nội bộ/CLI trên máy trạm, không mở cổng mạng Web API công khai. |
| **7** | **Mã hóa đường truyền mạng (TLS/HTTPS)** | **KHÔNG ÁP DỤNG** | Quá trình xử lý và nạp dữ liệu diễn ra cục bộ (On-premise) giữa tệp CSV và SQLite, không truyền tải dữ liệu khách hàng qua Internet. |

---

### Cam kết:
Nội dung khai báo trên hoàn toàn trung thực, có thể kiểm chứng trực tiếp qua mã nguồn và cấu hình trong repository.
