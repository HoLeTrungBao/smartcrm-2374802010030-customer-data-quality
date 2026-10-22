# BẢN ĐẶC TẢ YÊU CẦU PHẦN MỀM RÚT GỌN (SRS)
## LUỒNG NGHIỆP VỤ: L7 – KIỂM TRA VÀ LÀM SẠCH DỮ LIỆU KHÁCH HÀNG
**Học phần:** Chuyên đề Tốt nghiệp 1 (71ITGR40203)  
**Đề tài:** Smart CRM – Mekong Mobile  
**Sinh viên thực hiện:** Hồ Lê Trung Bảo – MSSV: 2374802010030  
**Chuyên ngành (Track):** Data Analytics (DA)  
**Khoa:** Công nghệ Thông tin – Trường Đại học Văn Lang  

---

## 1. GIỚI THIỆU VÀ PHẠM VI

### 1.1. Bối cảnh
Chuỗi bán lẻ thiết bị di động Mekong Mobile vận hành hệ thống Smart CRM nhằm quản lý và chăm sóc khách hàng. Tuy nhiên, dữ liệu khách hàng tích lũy từ nhiều kênh bán hàng và sự kiện tiếp thị xuất hiện tình trạng chất lượng kém: số điện thoại chứa định dạng mã quốc tế (`84`, `+84`), chứa dấu chấm phân cách; họ tên viết lộn xộn giữa chữ hoa và chữ thường hoặc có khoảng trắng thừa; trường email có tỷ lệ thiếu dữ liệu cao (44,99%) và phát hiện hơn 16.000 bản ghi nghi ngờ trùng lặp số điện thoại. Điều này ảnh hưởng tiêu cực đến hiệu quả chiến dịch gửi tin nhắn tiếp thị và gây lãng phí chi phí chăm sóc khách hàng.

### 1.2. Luồng nghiệp vụ lựa chọn
Luồng nghiệp vụ được phê duyệt: **L7 – Kiểm tra và làm sạch dữ liệu khách hàng (Customer Data Quality)**.  
* **Điểm bắt đầu:** Nạp dữ liệu khách hàng thô từ tập tin nguồn `customers_raw.csv` ($67.037$ bản ghi) vào hệ thống.  
* **Điểm kết thúc:** Dữ liệu sau khi kiểm định, phát hiện lỗi và chuẩn hóa được lưu trữ an toàn vào kho dữ liệu sạch theo mô hình Star Schema, bảng `reject_rows` lưu dòng lỗi kèm lý do, cùng báo cáo tổng hợp chất lượng dữ liệu phục vụ quản lý.

### 1.3. Phạm vi chủ ý KHÔNG làm (Mức WON'T theo MoSCoW)
Để đảm bảo bài toán vừa sức và tập trung đúng trọng tâm phân tích dữ liệu:
* **WON'T 1:** Không xây dựng hệ thống quản lý đơn hàng và giao dịch bán lẻ tại điểm bán (POS).
* **WON'T 2:** Không tiếp nhận, xử lý phiếu bảo hành và sửa chữa thiết bị di động.
* **WON'T 3:** Không tự động gửi tin nhắn SMS Brandname hoặc gửi Email tiếp thị trực tiếp đến khách hàng.
* **WON'T 4:** Không xây dựng mô hình Học máy (Machine Learning) dự đoán xác suất khách hàng rời bỏ (Churn Prediction).
* **WON'T 5:** Không tự ý xóa cứng (Hard Delete) các bản ghi khách hàng lỗi hoặc nghi ngờ trùng lặp khi chưa có đối soát từ con người.

### 1.4. Bảng thuật ngữ chuyên ngành bắt buộc (Glossary)

| Thuật ngữ tiếng Việt | Thuật ngữ tiếng Anh / Ký hiệu | Định nghĩa nghiệp vụ & Kỹ thuật chuẩn |
| :--- | :--- | :--- |
| **Bản ghi khách hàng** | Customer Record | Một hàng dữ liệu đại diện cho một khách hàng, có mã tự nhiên `customer_id`. |
| **Dữ liệu thô** | Raw Data / Staging | Dữ liệu ban đầu chưa xử lý, đọc từ tập tin `customers_raw.csv`. |
| **Khám phá dữ liệu** | Data Profiling | Thao tác khảo sát phân bố, kiểu dữ liệu, tỷ lệ rỗng và giá trị bất thường. |
| **Làm sạch dữ liệu** | Data Cleansing | Quy trình chuẩn hóa định dạng SĐT, họ tên, email và xử lý các lỗi dữ liệu. |
| **Quy tắc chất lượng** | Data Quality Rule (DQ Rule) | Bộ tiêu chí kiểm định gồm 6 quy tắc (DQ01 $\rightarrow$ DQ06) đo lường các chiều chất lượng. |
| **Dòng từ chối** | Reject Rows | Các bản ghi không thể chuẩn hóa hợp lệ, được giữ lại trong bảng `reject_rows` kèm lý do. |
| **Tính chạy lại được** | Idempotence | Khả năng chạy lại pipeline nhiều lần với cùng đầu vào mà không làm nhân đôi bản ghi. |
| **Kho dữ liệu Star Schema** | Star Schema Data Warehouse | Mô hình kho dữ liệu gồm bảng sự kiện trung tâm (Fact) và các bảng chiều (Dimension). |
| **Thông tin định danh PII** | Personally Identifiable Information | Dữ liệu nhạy cảm gồm SĐT và email, cần được che mặt nạ (Masking) khi hiển thị. |
| **Định dạng Title Case** | Title Case | Định dạng viết hoa chữ cái đầu mỗi từ và viết thường các chữ còn lại (ví dụ: `Nguyễn Văn A`). |

---

## 2. CÁC BÊN LIÊN QUAN VÀ VAI TRÒ (ACTORS)

Hệ thống xác định 3 vai trò người dùng chính:

| Actor | Quyền hạn và trách nhiệm (Làm được gì) | Ràng buộc phân quyền (Không được làm gì) |
| :--- | :--- | :--- |
| **Nhân viên Marketing** | - Xem và tìm kiếm danh sách khách hàng trong hệ thống.<br>- Chạy chức năng kiểm tra dữ liệu thiếu và sai định dạng theo các quy tắc chất lượng.<br>- Quét và phát hiện các nhóm khách hàng nghi ngờ trùng lặp.<br>- Thực hiện chuẩn hóa thông tin và đối soát dữ liệu. | - Không được xóa vĩnh viễn dữ liệu gốc trong vùng Staging.<br>- Không được thay đổi logic kiểm định chất lượng cốt lõi. |
| **Quản lý cửa hàng** | - Truy cập dashboard để theo dõi các chỉ số KPI chất lượng dữ liệu.<br>- Lọc báo cáo chất lượng theo từng phiên kiểm tra và theo loại lỗi.<br>- Phê duyệt danh sách khách hàng sau khi đã xử lý trùng lặp. | - Không trực tiếp can thiệp vào các thao tác tiền xử lý hoặc gán thuật toán chuẩn hóa dữ liệu thủ công. |
| **Quản trị viên hệ thống** | - Cấu hình lịch trình chạy pipeline ETL tự động.<br>- Giám sát hiệu năng thực thi, quản trị quyền truy cập và kiểm tra nhật ký lỗi.<br>- Vận hành sao lưu và bảo trì kho dữ liệu Star Schema. | - Không tự ý sửa đổi nội dung thông tin khách hàng mà không có yêu cầu từ bộ phận kinh doanh. |

---

## 3. YÊU CẦU CHỨC NĂNG (FR) VÀ USER STORY

### 3.1. Danh sách Yêu cầu chức năng (FR)
* **FR01 – Xem danh sách khách hàng:** Hiển thị danh sách khách hàng phân trang (50 dòng/trang) kèm bộ lọc theo trạng thái dữ liệu.
* **FR02 – Tìm kiếm khách hàng:** Tìm kiếm tức thời theo số điện thoại, email hoặc họ tên với thời gian phản hồi $\le 2{,}0\text{s}$.
* **FR03 – Kiểm tra dữ liệu thiếu hoặc sai định dạng:** Tự động phát hiện SĐT sai định dạng, họ tên chứa ký tự lạ hoặc email không hợp lệ theo quy tắc chất lượng.
* **FR04 – Phát hiện khách hàng bị trùng:** Tự động phân tích và gom nhóm các bản ghi khách hàng có cùng SĐT hoặc email sau chuẩn hóa.
* **FR05 – Chuẩn hóa thông tin khách hàng:** Quy đổi SĐT về 10 số (`0xxxxxxxxx`), cắt tỉa khoảng trắng và chuẩn hóa Title Case họ tên.
* **FR06 – Cập nhật dữ liệu khách hàng:** Cập nhật dữ liệu đã xử lý vào kho dữ liệu sạch, ghi nhận dòng lỗi vào bảng `reject_rows` và ghi nhật ký kiểm định vào bảng Fact.
* **FR07 – Xem kết quả chất lượng dữ liệu:** Trực quan hóa các chỉ số tổng hợp, biểu đồ phân bố lỗi và tỷ lệ làm sạch dữ liệu lên dashboard.

### 3.2. Danh sách User Story (US)
* **US01:** Là nhân viên Marketing, tôi muốn xem danh sách khách hàng phân trang để tra cứu dữ liệu dễ dàng. *(MUST)*
* **US02:** Là nhân viên Marketing, tôi muốn tìm kiếm khách hàng nhanh để kiểm tra thông tin từng người. *(MUST)*
* **US03:** Là nhân viên Marketing, tôi muốn hệ thống tự động gắn cờ lỗi để nắm được dữ liệu chưa đạt chuẩn. *(MUST)*
* **US04:** Là nhân viên Marketing, tôi muốn phát hiện khách hàng trùng lặp để lập danh sách bản ghi cần đối soát. *(MUST)*
* **US05:** Là nhân viên Marketing, tôi muốn chuẩn hóa thông tin khách hàng để đưa toàn bộ dữ liệu về định dạng thống nhất. *(MUST)*
* **US06:** Là nhân viên Marketing, tôi muốn cập nhật dữ liệu khách hàng sạch để phục vụ lưu trữ và phân tích lâu dài. *(MUST)*
* **US07:** Là Quản lý cửa hàng, tôi muốn xem kết quả chất lượng dữ liệu để nắm bắt độ tin cậy của tập dữ liệu. *(MUST)*

---

## 4. YÊU CẦU PHI CHỨC NĂNG (NFR) CÓ NGƯỠNG SỐ ĐO ĐƯỢC

| Mã NFR | Tiêu chí | Nội dung yêu cầu kỹ thuật & Ngưỡng số đo được cụ thể |
| :--- | :--- | :--- |
| **NFR01** | Hiệu năng tìm kiếm | Thời gian phản hồi khi tìm kiếm khách hàng theo SĐT/Email trên tập $67.037$ bản ghi phải $\le \mathbf{2{,}0\text{ giây}}$ trong 95% số lần truy vấn (Index Scan). |
| **NFR02** | Thời gian tải Dashboard | Thời gian tải trang Tổng quan chất lượng dữ liệu phải $\le \mathbf{3{,}0\text{ giây}}$ thông qua bảng tổng hợp sẵn (Pre-aggregated Table). |
| **NFR03** | Độ toàn vẹn dữ liệu | Tỷ lệ hao hụt dữ liệu qua pipeline kiểm định và làm sạch phải đạt **chính xác** $\mathbf{0{,}00\%}$ ($100\%$ bản ghi đều được ghi nhận tại Staging hoặc Reject, không xóa vật lý). |
| **NFR04** | Độ khả dụng hệ thống | Hệ thống lưu trữ và dashboard đạt thời gian hoạt động liên tục (Uptime) tối thiểu $\ge \mathbf{99{,}5\%}$ trong khung giờ làm việc hàng ngày. |
| **NFR05** | An toàn bảo mật PII | **$100\%$ màn hình hiển thị PII đối với người dùng không có quyền quản trị đều phải che mặt nạ (Masking)**: SĐT hiển thị `0912***678` và email hiển thị `a***@gmail.com`; tỷ lệ rò rỉ dữ liệu nhạy cảm là $\mathbf{0{,}00\%}$. |

---

## 5. RÀNG BUỘC VÀ QUY TẮC NGHIỆP VỤ (BUSINESS RULES)

* **BR01 (Chuẩn hóa số điện thoại):** Loại bỏ ký tự lạ, quy đổi đầu `84`/`+84` về `0`, kiểm tra độ dài chính xác 10 chữ số. Nếu không hợp lệ $\rightarrow$ đưa vào `reject_rows` với mã lỗi `PHONE_INVALID`.
* **BR02 (Chuẩn hóa họ tên):** Xóa khoảng trắng thừa, chuẩn hóa chữ hoa đầu mỗi từ (Title Case).
* **BR03 (Xác định trùng lặp):** Các bản ghi có cùng SĐT sạch hoặc email sạch được gom nhóm và gán cờ `is_duplicate = TRUE`.
* **BR04 (Bảo toàn dữ liệu nguồn):** Dữ liệu gốc trong `customers_raw.csv` không bị sửa đổi; các bản ghi lỗi được chuyển vào bảng `reject_rows` để người phụ trách xem xét.

---

## 6. BẢNG MA TRẬN TRUY VẾT GỘP ĐA CHIỀU (TRACEABILITY MATRIX)

Bảng ma trận truy vết tích hợp toàn diện nối kết từ Yêu cầu chức năng, User Story, Use Case, MoSCoW đến Module mã nguồn và Màn hình Wireframe phụ trách:

| Mã FR | Tên yêu cầu chức năng | User Story (US) | Use Case (UC) | Mức MoSCoW | Module mã nguồn phụ trách | Màn hình Wireframe |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| **FR01** | Xem danh sách khách hàng | US01 | UC01 | MUST | `src/load/load_warehouse.py` | Màn hình 2 (Danh sách & Đối soát) |
| **FR02** | Tìm kiếm khách hàng | US02 | UC02 | MUST | `src/load/load_warehouse.py` | Màn hình 2 (Danh sách & Đối soát) |
| **FR03** | Kiểm tra dữ liệu thiếu & sai định dạng | US03 | UC03 | MUST | `src/quality/checks.py` | Màn hình 1 (Tổng quan chất lượng) |
| **FR04** | Phát hiện khách hàng bị trùng | US04 | UC04 | MUST | `src/transform/clean_customers.py` | Màn hình 3 (Báo cáo & Tỷ lệ xử lý) |
| **FR05** | Chuẩn hóa thông tin khách hàng | US05 | UC05 | MUST | `src/transform/rules.py` | Màn hình 2 (Danh sách & Đối soát) |
| **FR06** | Cập nhật dữ liệu khách hàng | US06 | UC06 | MUST | `src/load/load_staging.py` | Màn hình 2 & Màn hình 3 |
| **FR07** | Xem kết quả chất lượng dữ liệu | US07 | UC07 | MUST | `src/pipeline.py` & Dashboard | Màn hình 1 (Tổng quan chất lượng) |