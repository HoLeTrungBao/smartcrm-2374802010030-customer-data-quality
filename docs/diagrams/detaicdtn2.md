# CHUYÊN NGÀNH: Khoa học dữ liệu

## Phân tích & dự báo xu hướng tuyển dụng ngành CNTT từ dữ liệu tin đăng việc làm

---

### 1. Mục tiêu
Thu thập, phân tích dữ liệu tin đăng tuyển dụng ngành CNTT nhằm xác định các kỹ năng/công nghệ đang có nhu cầu cao, xu hướng mức lương theo vị trí, và xây dựng mô hình dự báo xu hướng tuyển dụng theo thời gian, trình bày qua dashboard trực quan.

---

### 2. Phạm vi đề tài

#### Trong phạm vi:
1. Thu thập dữ liệu tin tuyển dụng CNTT (crawl từ nguồn công khai hoặc sử dụng dataset có sẵn, ví dụ: Kaggle/ITviec/TopCV).
2. Làm sạch, chuẩn hóa dữ liệu (xử lý dữ liệu thiếu, trùng lặp, chuẩn hóa tên kỹ năng/công nghệ).
3. Phân tích khám phá dữ liệu (EDA): kỹ năng/công nghệ phổ biến, mức lương theo vị trí/kinh nghiệm, phân bố theo khu vực.
4. Trích xuất kỹ năng/công nghệ từ mô tả công việc (text mining cơ bản).
5. Xây dựng mô hình dự báo/phân tích xu hướng theo thời gian (time series đơn giản hoặc phân tích xu hướng theo giai đoạn).
6. Xây dựng dashboard trực quan hóa kết quả.

#### Ngoài phạm vi (không bắt buộc):
7. Thu thập dữ liệu real-time liên tục (chỉ cần snapshot dữ liệu trong phạm vi thời gian làm đồ án).
8. Dự báo cá nhân hóa theo hồ sơ từng sinh viên.
9. Mô hình deep learning phức tạp cho time series (ưu tiên mô hình thống kê/ML cơ bản, dễ giải thích).

---

### 3. Công nghệ đề xuất
- **Thu thập dữ liệu:** Python (`requests` / `BeautifulSoup` hoặc `Scrapy`) hoặc dataset có sẵn.
- **Xử lý & phân tích:** `pandas`, `numpy`.
- **Trích xuất văn bản:** `regex` / `underthesea` (nếu dữ liệu tiếng Việt).
- **Mô hình dự báo:** `statsmodels` / `Prophet` hoặc mô hình hồi quy đơn giản.
- **Trực quan hóa/Dashboard:** `matplotlib` / `seaborn` kết hợp `Streamlit` hoặc `Power BI`.

---

### 4. Kế hoạch triển khai theo Sprint (10 buổi)

| Sprint | Buổi | Mục tiêu / Công việc chính | Sản phẩm bàn giao |
| :--- | :--- | :--- | :--- |
| **Sprint 0** | Buổi 1–3 | Xác định nguồn dữ liệu, phạm vi phân tích (khoảng thời gian, khu vực), lập kế hoạch thu thập | Kế hoạch thu thập dữ liệu + phạm vi phân tích |
| **Sprint 1** | Buổi 4–5 | Xây dựng pipeline thu thập & làm sạch dữ liệu, EDA sơ bộ | Bộ dữ liệu đã làm sạch + báo cáo EDA sơ bộ |
| **Sprint 2** | Buổi 6 | Hoàn thiện EDA, trích xuất kỹ năng/công nghệ từ mô tả công việc (feature engineering) | Bảng dữ liệu đặc trưng (feature table) |
| **Sprint 3** | Buổi 7 | Xây dựng mô hình dự báo/phân tích xu hướng theo thời gian | Mô hình dự báo baseline |
| **Sprint 4** | Buổi 8 | Đánh giá mô hình (so sánh baseline), tinh chỉnh tham số, phân tích lỗi | Kết quả đánh giá mô hình + bảng so sánh |
| **Sprint 5** | Buổi 9–10 | Xây dựng dashboard trực quan, hoàn thiện báo cáo, tập dượt bảo vệ | Dashboard hoạt động + báo cáo hoàn thiện |

---

### 5. Tiêu chí nghiệm thu / đánh giá sản phẩm
- Dữ liệu được thu thập/làm sạch minh bạch, có mô tả nguồn và quy trình xử lý.
- EDA thể hiện được insight rõ ràng (kỹ năng hot, xu hướng lương,...).
- Mô hình dự báo có đánh giá bằng chỉ số phù hợp (MAE/RMSE hoặc tương đương) và so sánh với baseline.
- Dashboard trực quan, dễ hiểu, phản ánh đúng kết quả phân tích.