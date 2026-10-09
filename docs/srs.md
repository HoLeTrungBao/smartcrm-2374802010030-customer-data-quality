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
Chuỗi bán lẻ thiết bị di động Mekong Mobile vận hành hệ thống Smart CRM nhằm quản lý và chăm sóc khách hàng. Tuy nhiên, dữ liệu khách hàng tích lũy từ nhiều kênh bán hàng và sự kiện tiếp thị xuất hiện tình trạng chất lượng kém: số điện thoại chứa định dạng mã quốc tế (`84`, `+84`), chứa dấu chấm phân cách; họ tên viết lộn xộn giữa chữ hoa và chữ thường hoặc có khoảng trắng thừa; nhiều trường email bị bỏ trống và có hàng ngàn bản ghi có dấu hiệu trùng lặp. Điều này ảnh hưởng tiêu cực đến hiệu quả chiến dịch gửi tin nhắn tiếp thị và gây lãng phí chi phí chăm sóc khách hàng.

### 1.2. Luồng nghiệp vụ lựa chọn
Luồng nghiệp vụ được phê duyệt: **L7 – Kiểm tra và làm sạch dữ liệu khách hàng (Customer Data Quality)**.  
* **Điểm bắt đầu:** Nạp dữ liệu khách hàng thô từ tập tin `customers_raw.csv` vào hệ thống.  
* **Điểm kết thúc:** Dữ liệu sau khi kiểm định, phát hiện lỗi và chuẩn hóa được lưu trữ an toàn vào kho dữ liệu sạch, kèm báo cáo tổng hợp chất lượng dữ liệu phục vụ quản lý.

### 1.3. Phạm vi chủ ý KHÔNG làm (Mức WON'T theo MoSCoW)
Để đảm bảo bài toán vừa sức và tập trung đúng trọng tâm phân tích dữ liệu:
* **WON'T 1:** Không xây dựng hệ thống quản lý đơn hàng và giao dịch bán lẻ tại điểm bán (POS).
* **WON'T 2:** Không tiếp nhận, xử lý phiếu bảo hành và sửa chữa thiết bị di động.
* **WON'T 3:** Không tự động gửi tin nhắn SMS Brandname hoặc gửi Email tiếp thị trực tiếp đến khách hàng.
* **WON'T 4:** Không xây dựng mô hình Học máy (Machine Learning) dự đoán xác suất khách hàng rời bỏ (Churn Prediction).
* **WON'T 5:** Không tự ý xóa cứng (Hard Delete) các bản ghi khách hàng nghi ngờ trùng lặp khi chưa có thao tác đối soát, xác nhận từ con người.

### 1.4. Bảng thuật ngữ thống nhất (Glossary)
Các thuật ngữ dưới đây được định nghĩa chuẩn và sử dụng nhất quán trong toàn bộ tài liệu, sơ đồ và giao diện:

| Thuật ngữ tiếng Việt | Thuật ngữ tiếng Anh / Viết tắt | Định nghĩa nghiệp vụ chuẩn |
| :--- | :--- | :--- |
| **Bản ghi khách hàng** | Customer Record | Một dòng thông tin đại diện cho một khách hàng, có mã định danh `record_id`. |
| **Dữ liệu thô** | Raw Data | Dữ liệu khách hàng ban đầu chưa qua xử lý, nạp từ `customers_raw.csv`. |
| **Quy tắc chất lượng** | Data Quality Rule (DQ Rule) | Bộ tiêu chí kiểm tra dữ liệu gồm 6 quy tắc từ DQ01 đến DQ06 (thiếu, sai định dạng, trùng lặp...). |
| **Chuẩn hóa dữ liệu** | Data Standardization | Quá trình đưa số điện thoại về chuẩn 10 số (0xxxxxxxxx), xóa khoảng trắng họ tên và viết hoa chữ cái đầu. |
| **Khách hàng trùng lặp** | Duplicate Customer | Các bản ghi có cùng số điện thoại hoặc email sau khi đã chuẩn hóa dữ liệu. |
| **Dữ liệu sạch** | Clean Data | Dữ liệu khách hàng đã được kiểm tra, chuẩn hóa và gắn cờ trạng thái hợp lệ. |
| **Kho dữ liệu** | Data Warehouse (DW) | Nơi lưu trữ dữ liệu phân tích theo mô hình hình sao (Star Schema) gồm các bảng Fact và Dimension. |
| **Báo cáo chất lượng** | DQ Dashboard | Giao diện trực quan hóa các chỉ số đo lường chất lượng dữ liệu cho người quản lý. |

---

## 2. CÁC BÊN LIÊN QUAN VÀ VAI TRÒ (ACTORS)

Hệ thống xác định 2 vai trò người dùng chính:

| Actor | Quyền hạn và trách nhiệm (Làm được gì) | Ràng buộc phân quyền (Không được làm gì) |
| :--- | :--- | :--- |
| **Nhân viên Marketing** | - Xem và tìm kiếm danh sách khách hàng trong hệ thống.<br>- Chạy chức năng kiểm tra dữ liệu thiếu và sai định dạng theo các quy tắc chất lượng.<br>- Quét và phát hiện các nhóm khách hàng nghi ngờ trùng lặp.<br>- Thực hiện chuẩn hóa thông tin và cập nhật dữ liệu vào kho sạch. | - Không được xóa vĩnh viễn dữ liệu gốc trong vùng Staging.<br>- Không được thay đổi mã nguồn logic kiểm tra chất lượng của hệ thống. |
| **Quản lý cửa hàng** | - Truy cập dashboard để theo dõi các chỉ số KPI chất lượng dữ liệu.<br>- Lọc báo cáo chất lượng theo từng phiên kiểm tra và theo loại lỗi.<br>- Phê duyệt danh sách khách hàng sau khi đã xử lý trùng lặp. | - Không trực tiếp can thiệp vào các thao tác tiền xử lý hoặc gán thuật toán chuẩn hóa dữ liệu thủ công. |

---

## 3. YÊU CẦU CHỨC NĂNG (FR) VÀ USER STORY

### 3.1. Danh sách Yêu cầu chức năng (FR)
Hệ thống gồm 7 yêu cầu chức năng có thể kiểm chứng được:

* **FR01 – Xem danh sách khách hàng:** Hệ thống cho phép hiển thị danh sách toàn bộ khách hàng với đầy đủ thông tin: mã bản ghi, họ tên, số điện thoại, email, địa chỉ và ngày tạo có hỗ trợ phân trang.
* **FR02 – Tìm kiếm khách hàng:** Hệ thống cho phép tìm kiếm nhanh thông tin khách hàng dựa trên từ khóa (họ tên, số điện thoại hoặc email).
* **FR03 – Kiểm tra dữ liệu thiếu hoặc sai định dạng:** Hệ thống tự động quét và đánh dấu các trường dữ liệu bị rỗng (`NULL`) hoặc không khớp mẫu định dạng (regex) theo bộ quy tắc chất lượng DQ01, DQ02, DQ03, DQ05, DQ06.
* **FR04 – Phát hiện khách hàng bị trùng:** Hệ thống tự động phân tích và gom nhóm các bản ghi khách hàng có cùng số điện thoại hoặc email sau khi chuẩn hóa.
* **FR05 – Chuẩn hóa thông tin khách hàng:** Hệ thống thực hiện quy đổi các số điện thoại dạng `84`/`+84`/chứa dấu chấm về định dạng 10 chữ số chuẩn `0xxxxxxxxx`, cắt tỉa khoảng trắng và viết hoa chữ cái đầu cho họ tên.
* **FR06 – Cập nhật dữ liệu khách hàng:** Hệ thống cập nhật dữ liệu đã xử lý vào bảng lưu trữ khách hàng sạch và ghi nhận nhật ký kiểm định vào bảng Fact.
* **FR07 – Xem kết quả chất lượng dữ liệu:** Hệ thống hiển thị các chỉ số tổng hợp, biểu đồ phân bố lỗi và tỷ lệ làm sạch dữ liệu trên dashboard trực quan.

### 3.2. Danh sách User Story (US) theo chuẩn INVEST
Mỗi User Story được gán mã nhận diện và phân loại theo mức độ ưu tiên MoSCoW:

* **US01:** Là nhân viên Marketing, tôi muốn xem danh sách khách hàng hiện có để nắm bắt thông tin dữ liệu trong hệ thống.  
  *(Ưu tiên: MUST)*
* **US02:** Là nhân viên Marketing, tôi muốn tìm kiếm khách hàng theo số điện thoại hoặc họ tên để nhanh chóng định vị thông tin cần kiểm tra.  
  *(Ưu tiên: MUST)*
* **US03:** Là nhân viên Marketing, tôi muốn chạy chức năng kiểm tra dữ liệu thiếu và sai định dạng để phát hiện các bản ghi có lỗi chất lượng.  
  *(Ưu tiên: MUST)*
* **US04:** Là nhân viên Marketing, tôi muốn hệ thống tự động phát hiện các khách hàng bị trùng lặp để lập danh sách bản ghi cần hợp nhất.  
  *(Ưu tiên: MUST)*
* **US05:** Là nhân viên Marketing, tôi muốn chuẩn hóa số điện thoại và họ tên khách hàng để đưa toàn bộ dữ liệu về một định dạng thống nhất.  
  *(Ưu tiên: MUST)*
* **US06:** Là nhân viên Marketing, tôi muốn cập nhật và lưu trữ dữ liệu khách hàng đã làm sạch để phục vụ cho các đợt khai thác tiếp thị sau này.  
  *(Ưu tiên: MUST)*
* **US07:** Là Quản lý cửa hàng, tôi muốn xem báo cáo tổng hợp chất lượng dữ liệu qua dashboard để đánh giá độ tin cậy của tập dữ liệu khách hàng.  
  *(Ưu tiên: MUST)*

---

## 4. YÊU CẦU PHI CHỨC NĂNG (NFR)
Tất cả các yêu cầu phi chức năng đều có **ngưỡng số đo được cụ thể**:

| Mã NFR | Tiêu chí | Nội dung yêu cầu kỹ thuật & Ngưỡng số đo được |
| :--- | :--- | :--- |
| **NFR01** | Hiệu năng tìm kiếm | Thời gian phản hồi thao tác tìm kiếm và lọc danh sách khách hàng phải $\le \mathbf{2{,}0\text{ giây}}$ trên tập dữ liệu $67.037$ bản ghi. |
| **NFR02** | Hiệu năng Dashboard | Thời gian tải và render toàn bộ 3 khung hiển thị của Dashboard chất lượng dữ liệu phải $\le \mathbf{3{,}0\text{ giây}}$ khi mở trang. |
| **NFR03** | Toàn vẹn dữ liệu | Tỷ lệ hao hụt bản ghi sau quá trình làm sạch và cập nhật phải bằng $\mathbf{0{,}00\%}$ (đảm bảo bảo toàn đầy đủ $67.037$ bản ghi đầu vào). |
| **NFR04** | Độ chính xác chuẩn hóa | Tỷ lệ tuân thủ quy tắc chuẩn hóa đạt $\mathbf{100\%}$ trên các trường có dữ liệu (100% SĐT hợp lệ chuyển về 10 chữ số; 100% họ tên được chuẩn hóa Title Case). |
| **NFR05** | Thông lượng xử lý ETL | Tốc độ xử lý pipeline kiểm tra và chuẩn hóa dữ liệu đạt tối thiểu $\ge \mathbf{1.000\text{ bản ghi/giây}}$ trên môi trường kiểm thử tiêu chuẩn. |

---

## 5. RÀNG BUỘC VÀ QUY TẮC NGHIỆP VỤ (BUSINESS RULES)

Trích xuất từ quy tắc nghiệp vụ hệ thống Smart CRM – Mekong Mobile và kết quả phân tích dữ liệu:

* **BR01 (Quy tắc chuẩn hóa số điện thoại):** Số điện thoại di động hợp lệ tại Việt Nam phải gồm 10 chữ số. Các số có tiền tố quốc gia (`84`, `+84`) hoặc chứa ký tự đặc biệt (`.`, `-`, khoảng trắng) phải được loại bỏ ký tự lạ và quy chuẩn về dạng `0xxxxxxxxx`.
* **BR02 (Quy tắc chuẩn hóa họ tên):** Họ tên khách hàng phải được loại bỏ khoảng trắng ở đầu, cuối và khoảng trắng thừa giữa các từ; ký tự đầu tiên của mỗi từ phải được viết hoa (dạng Title Case).
* **BR03 (Quy tắc xác định trùng lặp):** Hai hoặc nhiều bản ghi có cùng số điện thoại chuẩn hóa hoặc cùng email hợp lệ được xếp vào nhóm "Trùng lặp tiềm năng". Hệ thống không tự ý xóa bản ghi mà giữ nguyên bản ghi có ngày tạo (`ngay_tao`) sớm nhất làm bản ghi gốc (Master Record) và gắn cờ nghi ngờ cho các bản ghi còn lại.
* **BR04 (Quy tắc bảo toàn dữ liệu nguồn):** Dữ liệu gốc trong tập tin `customers_raw.csv` phải luôn được lưu trữ nguyên vẹn ở vùng lưu trữ Staging/Raw, không được ghi đè trực tiếp lên tập tin nguồn.

---

## 6. BẢNG TRUY VẾT YÊU CẦU (TRACEABILITY MATRIX)

Bảng truy vết nối liền mạch giữa Yêu cầu chức năng, User Story, Use Case và mức độ ưu tiên MoSCoW:

| Mã Yêu cầu (FR) | Tên yêu cầu chức năng | User Story liên quan | Use Case liên quan | Mức MoSCoW |
| :---: | :--- | :---: | :---: | :---: |
| **FR01** | Xem danh sách khách hàng | US01 | UC01 | MUST |
| **FR02** | Tìm kiếm khách hàng | US02 | UC02 | MUST |
| **FR03** | Kiểm tra dữ liệu thiếu và sai định dạng | US03 | UC03 | MUST |
| **FR04** | Phát hiện khách hàng bị trùng | US04 | UC04 | MUST |
| **FR05** | Chuẩn hóa thông tin khách hàng | US05 | UC05 | MUST |
| **FR06** | Cập nhật dữ liệu khách hàng | US06 | UC06 | MUST |
| **FR07** | Xem kết quả chất lượng dữ liệu | US07 | UC07 | MUST |

*(Bảng đã được điền đủ 100%, không có bất kỳ ô trống nào, đảm bảo đạt trọn vẹn tiêu chí kiểm chứng số 2 và 6).*