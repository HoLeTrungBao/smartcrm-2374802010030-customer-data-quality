# BÁO CÁO BÀI TẬP 1: PHÂN TÍCH VÀ THIẾT KẾ
## HỌC PHẦN: CHUYÊN ĐỀ TỐT NGHIỆP 1 (71ITGR40203)
### HỌC KỲ 1, NĂM HỌC 2026 – 2027

---

### THÔNG TIN BÀI NỘP
* **Tên bài tập:** Bài tập 1: Phân tích và Thiết kế
* **Mã luồng nghiệp vụ:** L7 – Kiểm tra và làm sạch dữ liệu khách hàng (*Customer Data Quality*)
* **Chuyên ngành (Track):** Data Analytics (DA)
* **Họ và tên sinh viên:** Hồ Lê Trung Bảo
* **Mã số sinh viên (MSSV):** 2374802010030
* **Lớp:** Chuyên đề Tốt nghiệp 1 – Khoa Công nghệ Thông tin
* **Ngày nộp:** 09/10/2026
* **LINK GITHUB REPO CHÍNH THỨC:** [https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality](https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality)


---

# MỤC 1 – BẢN SRS RÚT GỌN

## 1.1. Giới thiệu và phạm vi
* **Bối cảnh:** Mekong Mobile là chuỗi bán lẻ thiết bị di động. Hệ thống Smart CRM thu thập dữ liệu khách hàng từ nhiều nguồn dẫn đến tình trạng suy giảm chất lượng dữ liệu: số điện thoại chứa định dạng quốc tế (`84`, `+84`) hoặc dấu chấm; họ tên viết lộn xộn hoa/thường và thừa khoảng trắng; trường email bị bỏ trống nhiều và xuất hiện hàng nghìn bản ghi nghi ngờ trùng lặp. Phân hệ L7 được xây dựng để kiểm định, chuẩn hóa và kiểm soát chất lượng dữ liệu khách hàng.
* **Luồng nghiệp vụ chọn:** L7 – Kiểm tra và làm sạch dữ liệu khách hàng. Bắt đầu từ khi nạp dữ liệu thô `customers_raw.csv` $\rightarrow$ kiểm tra chất lượng $\rightarrow$ chuẩn hóa $\rightarrow$ cập nhật vào kho dữ liệu sạch kèm báo cáo phân tích.
* **Phạm vi chủ ý KHÔNG làm (mức WON'T theo MoSCoW):**
  1. Không xây dựng hệ thống quản lý đơn hàng và giao dịch điểm bán (POS).
  2. Không xử lý tiếp nhận phiếu bảo hành và sửa chữa thiết bị.
  3. Không tự động gửi tin nhắn SMS Brandname hoặc Email Marketing đến khách hàng.
  4. Không xây dựng mô hình Học máy (Machine Learning) dự đoán rời bỏ (Churn).
  5. Không tự ý xóa cứng (Hard Delete) các bản ghi nghi ngờ trùng lặp khi chưa có xác nhận từ người dùng.
* **Bảng thuật ngữ dùng thống nhất trong toàn bộ tài liệu:**

| Thuật ngữ tiếng Việt | Thuật ngữ tiếng Anh / Viết tắt | Định nghĩa nghiệp vụ chuẩn |
| :--- | :--- | :--- |
| **Bản ghi khách hàng** | Customer Record | Một dòng thông tin đại diện cho một khách hàng, có mã `record_id`. |
| **Dữ liệu thô** | Raw Data | Dữ liệu ban đầu chưa xử lý, trích xuất từ `customers_raw.csv`. |
| **Quy tắc chất lượng** | Data Quality Rule (DQ Rule) | Bộ tiêu chí kiểm tra dữ liệu gồm 6 quy tắc (DQ01 đến DQ06). |
| **Chuẩn hóa dữ liệu** | Data Standardization | Quá trình quy đổi SĐT về 10 số (0xxxxxxxxx), xóa khoảng trắng họ tên và viết hoa chữ cái đầu. |
| **Khách hàng trùng lặp** | Duplicate Customer | Các bản ghi có cùng số điện thoại hoặc email sau khi chuẩn hóa. |
| **Dữ liệu sạch** | Clean Data | Dữ liệu khách hàng đã được kiểm tra, chuẩn hóa và gắn cờ hợp lệ. |
| **Kho dữ liệu** | Data Warehouse (DW) | Nơi lưu trữ dữ liệu phân tích theo mô hình Star Schema (Fact & Dim). |
| **Báo cáo chất lượng** | DQ Dashboard | Giao diện trực quan hóa các chỉ số đo lường chất lượng dữ liệu. |

## 1.2. Các bên liên quan và vai trò
Hệ thống xác định 2 vai trò người dùng chính:
* **Nhân viên Marketing:** Được phép xem, tìm kiếm danh sách khách hàng; thực hiện kiểm tra lỗi thiếu, sai định dạng; quét phát hiện trùng lặp; chạy chuẩn hóa và cập nhật dữ liệu. *Không được xóa vĩnh viễn dữ liệu gốc trong Staging và không can thiệp mã nguồn pipeline.*
* **Quản lý cửa hàng:** Được phép truy cập dashboard theo dõi các chỉ số KPI chất lượng dữ liệu; lọc báo cáo theo đợt kiểm tra; phê duyệt danh sách khách hàng sau xử lý trùng lặp. *Không can thiệp tiền xử lý thủ công.*

## 1.3. Yêu cầu chức năng (FR) và User Story
Hệ thống gồm 7 yêu cầu chức năng (FR) và 7 User Story chuẩn INVEST (100% mức MUST):
* **FR01 (US01 - MUST):** Xem danh sách khách hàng. Cho phép hiển thị danh sách toàn bộ khách hàng với đầy đủ thông tin: mã bản ghi, họ tên, số điện thoại, email, địa chỉ, ngày tạo có phân trang.
* **FR02 (US02 - MUST):** Tìm kiếm khách hàng. Cho phép tìm kiếm nhanh theo họ tên, số điện thoại hoặc email.
* **FR03 (US03 - MUST):** Kiểm tra dữ liệu thiếu hoặc sai định dạng. Tự động kiểm tra các trường rỗng (`NULL`) hoặc không khớp biểu thức chính quy (regex) theo quy tắc DQ01, DQ02, DQ03, DQ05, DQ06.
* **FR04 (US04 - MUST):** Phát hiện khách hàng bị trùng. Tự động gom nhóm các bản ghi khách hàng có cùng số điện thoại hoặc email sau chuẩn hóa.
* **FR05 (US05 - MUST):** Chuẩn hóa thông tin khách hàng. Quy đổi số điện thoại dạng `84`/`+84`/dấu chấm về 10 chữ số chuẩn (`0xxxxxxxxx`), xóa khoảng trắng thừa và viết hoa chữ cái đầu họ tên.
* **FR06 (US06 - MUST):** Cập nhật dữ liệu khách hàng. Cập nhật dữ liệu đã xử lý vào bảng khách hàng sạch và ghi nhận nhật ký kiểm định vào bảng Fact.
* **FR07 (US07 - MUST):** Xem kết quả chất lượng dữ liệu. Hiển thị các chỉ số tổng hợp, biểu đồ phân bố lỗi và tỷ lệ làm sạch dữ liệu trên dashboard.

## 1.4. Yêu cầu phi chức năng (NFR)
Tất cả các NFR đều có **ngưỡng số đo được cụ thể**:
* **NFR01 (Hiệu năng tìm kiếm):** Thời gian phản hồi thao tác tìm kiếm và lọc danh sách khách hàng $\le \mathbf{2{,}0\text{ giây}}$ trên tập dữ liệu $67.037$ bản ghi.
* **NFR02 (Hiệu năng Dashboard):** Thời gian tải và render toàn bộ 3 khung hiển thị của Dashboard chất lượng dữ liệu $\le \mathbf{3{,}0\text{ giây}}$ khi mở trang.
* **NFR03 (Toàn vẹn dữ liệu):** Tỷ lệ hao hụt bản ghi sau khi làm sạch và cập nhật bằng $\mathbf{0{,}00\%}$ (bảo toàn trọn vẹn $67.037$ bản ghi gốc).
* **NFR04 (Độ chính xác chuẩn hóa):** Tỷ lệ tuân thủ quy tắc chuẩn hóa đạt $\mathbf{100\%}$ trên các trường có dữ liệu (100% SĐT hợp lệ chuyển về 10 số; 100% họ tên chuyển về Title Case).
* **NFR05 (Thông lượng xử lý ETL):** Tốc độ xử lý pipeline kiểm tra và chuẩn hóa dữ liệu đạt tối thiểu $\ge \mathbf{1.000\text{ bản ghi/giây}}$.

## 1.5. Ràng buộc và quy tắc nghiệp vụ
* **BR01 (Chuẩn hóa số điện thoại):** Số điện thoại di động hợp lệ gồm 10 chữ số. Các số chứa mã quốc gia `84`/`+84` hoặc dấu chấm phân cách phải loại bỏ ký tự lạ và quy chuẩn về `0xxxxxxxxx`.
* **BR02 (Chuẩn hóa họ tên):** Họ tên khách hàng phải loại bỏ khoảng trắng đầu/cuối và khoảng trắng thừa giữa các từ; ký tự đầu tiên mỗi từ viết hoa (Title Case).
* **BR03 (Quy tắc xác định trùng lặp):** Bản ghi có cùng số điện thoại hoặc email chuẩn hóa được xếp vào nhóm "Trùng lặp tiềm năng". Bản ghi có `ngay_tao` sớm nhất được chọn làm bản ghi gốc (Master Record).
* **BR04 (Bảo toàn dữ liệu nguồn):** Dữ liệu gốc trong `customers_raw.csv` phải luôn được lưu trữ nguyên trạng trong vùng Staging, không được ghi đè trực tiếp lên tập tin nguồn.

## 1.6. Bảng truy vết yêu cầu (Traceability Matrix)

| Mã FR | Tên yêu cầu chức năng | User Story | Use Case | Mức MoSCoW |
| :---: | :--- | :---: | :---: | :---: |
| **FR01** | Xem danh sách khách hàng | US01 | UC01 | MUST |
| **FR02** | Tìm kiếm khách hàng | US02 | UC02 | MUST |
| **FR03** | Kiểm tra dữ liệu thiếu và sai định dạng | US03 | UC03 | MUST |
| **FR04** | Phát hiện khách hàng bị trùng | US04 | UC04 | MUST |
| **FR05** | Chuẩn hóa thông tin khách hàng | US05 | UC05 | MUST |
| **FR06** | Cập nhật dữ liệu khách hàng | US06 | UC06 | MUST |
| **FR07** | Xem kết quả chất lượng dữ liệu | US07 | UC07 | MUST |

*(Không có ô trống, đảm bảo tính nhất quán 100%).*

---

# MỤC 2 – USE CASE

## 2.1. Sơ đồ Use Case (Use Case Diagram)
*(Sơ đồ chi tiết được lưu trong file gốc: `docs/usecase.drawio`)*
* **Actor:** Marketing (bên ngoài ranh giới), Quản lý cửa hàng (bên ngoài ranh giới).
* **System Boundary:** "HỆ THỐNG KIỂM TRA VÀ LÀM SẠCH DỮ LIỆU KHÁCH HÀNG".
* **7 Use Case:** UC01 (Xem danh sách), UC02 (Tìm kiếm), UC03 (Kiểm tra thiếu/sai định dạng), UC04 (Phát hiện trùng), UC05 (Chuẩn hóa), UC06 (Cập nhật), UC07 (Xem kết quả chất lượng).
* **Quan hệ phụ thuộc:** `UC06` `<<include>>` `UC05`; `UC02` `<<extend>>` `UC01`.

## 2.2. Đặc tả chi tiết 2 Use Case quan trọng nhất

### Đặc tả UC04: Phát hiện khách hàng bị trùng
* **Actor chính:** Nhân viên Marketing.
* **Mục tiêu:** Nhận diện và gom nhóm các bản ghi khách hàng nghi ngờ cùng một người dựa trên số điện thoại hoặc email.
* **Điều kiện trước:** Dữ liệu khách hàng đã được nạp vào hệ thống và đã qua chuẩn hóa cơ bản.
* **Điều kiện sau:** Danh sách các nhóm trùng lặp được tạo lập và gán cờ `is_duplicate = TRUE` trong kho dữ liệu audit.
* **User Story liên quan:** US04 (MoSCoW: MUST).
* **Luồng chính (Main Flow):**
  1. Người dùng chọn chức năng "Phát hiện khách hàng trùng lặp".
  2. Người dùng chọn tiêu chí đối sánh (Mặc định: Số điện thoại chuẩn hóa, Email).
  3. Người dùng nhấn nút "Bắt đầu quét trùng lặp".
  4. Hệ thống thực hiện gom nhóm trên tập dữ liệu $67.037$ bản ghi, phát hiện các số điện thoại/email xuất hiện từ 2 lần trở lên.
  5. Hệ thống thống kê tổng số nhóm trùng ($16.039$ bản ghi trùng SĐT, $9.004$ bản ghi trùng email).
  6. Hệ thống hiển thị bảng danh sách các nhóm trùng lặp kèm thông tin chi tiết.
  7. Người dùng xem chi tiết từng cụm bản ghi và xác nhận danh sách trùng lặp.
* **Luồng ngoại lệ (Exception Flow):**
  * **3a. Dữ liệu chưa qua chuẩn hóa số điện thoại:**
    * 3a1. Hệ thống phát hiện số điện thoại còn chứa tiền tố `84`/`+84` hoặc ký tự lạ.
    * 3a2. Hệ thống cảnh báo: *"Dữ liệu chưa được chuẩn hóa, kết quả đối sánh có thể bị sai lệch. Bạn có muốn chuẩn hóa trước không?"*.
    * 3a3. Nếu người dùng chọn "Đồng ý", hệ thống chuyển sang UC05 rồi quay lại bước 4. Nếu "Bỏ qua", hệ thống tiếp tục bước 4 với cảnh báo.
  * **4a. Không phát hiện bản ghi nào trùng lặp:**
    * 4a1. Hệ thống hiển thị thông báo: *"Không phát hiện khách hàng trùng lặp theo tiêu chí đã chọn"*.
    * 4a2. Hệ thống kết thúc Use Case.

### Đặc tả UC05: Chuẩn hóa thông tin khách hàng
* **Actor chính:** Nhân viên Marketing.
* **Mục tiêu:** Áp dụng bộ quy tắc làm sạch để đưa số điện thoại về 10 chữ số (0xxxxxxxxx), xóa khoảng trắng thừa và viết hoa chữ cái đầu họ tên.
* **Điều kiện trước:** Tập dữ liệu khách hàng thô tồn tại trong hệ thống.
* **Điều kiện sau:** Dữ liệu tạm thời được đưa về định dạng thống nhất, sẵn sàng cập nhật vào kho sạch.
* **User Story liên quan:** US05 (MoSCoW: MUST).
* **Luồng chính (Main Flow):**
  1. Người dùng chọn chức năng "Chuẩn hóa thông tin khách hàng".
  2. Hệ thống hiển thị các quy tắc chuẩn hóa khả dụng (SĐT 10 số, Title Case họ tên, chữ thường email).
  3. Người dùng chọn các quy tắc cần thực thi và nhấn "Thực hiện chuẩn hóa".
  4. Hệ thống chạy thuật toán làm sạch tuần tự qua các trường dữ liệu:
     * Họ tên: Xóa khoảng trắng đầu/cuối, viết hoa chữ cái đầu mỗi từ.
     * Số điện thoại: Lọc bỏ ký tự lạ, chuyển tiền tố `84`/`+84` thành `0`.
     * Email: Chuyển về chữ thường.
  5. Hệ thống hiển thị bảng so sánh trước và sau chuẩn hóa kèm số bản ghi đã sửa thành công.
  6. Người dùng xác nhận kết quả chuẩn hóa.
* **Luồng ngoại lệ (Exception Flow):**
  * **4a. Bản ghi có số điện thoại không thể tự động sửa:**
    * 4a1. Hệ thống phát hiện SĐT sau khi lọc ký tự lạ có độ dài khác 10 chữ số.
    * 4a2. Hệ thống giữ nguyên số điện thoại gốc, gắn cờ `is_invalid_format = TRUE` và đưa vào danh sách kiểm tra thủ công.
    * 4a3. Hệ thống tiếp tục xử lý các bản ghi còn lại và xuất báo cáo số lượng bản ghi lỗi ở bước 5.

---

# MỤC 3 – THIẾT KẾ KIẾN TRÚC

## 3.1. Sơ đồ kiến trúc xử lý dữ liệu (Data Pipeline Architecture)
*(Sơ đồ chi tiết được lưu trong file gốc: `docs/architecture.drawio`)*
Hệ thống áp dụng kiến trúc phân tầng 5 lớp (Layered Data Architecture):
1. **Tầng Nguồn dữ liệu (Data Sources Layer):** Tập tin `customers_raw.csv` ($67.037$ bản ghi thô).
2. **Tầng Xử lý & Kiểm định chất lượng (ETL & DQ Engine):** Chạy bằng Python/Pandas, phụ trách Profiling (DQ01, DQ06), Cleansing (DQ02, DQ05) và Duplicate Detection (DQ04).
3. **Tầng Lưu trữ Kho dữ liệu (Data Warehouse Layer):** Mô hình Star Schema gồm bảng sự kiện `fact_customer_quality_audit` và các bảng chiều `dim_customer`, `dim_quality_rule`, `dim_audit_run`.
4. **Tầng Nghiệp vụ & Chỉ số phân tích (Semantic Layer):** Tính toán các chỉ số Completeness, Validity, Uniqueness và điểm chất lượng tổng hợp.
5. **Tầng Trình diễn (Presentation Layer / BI Dashboard):** 3 Khung Dashboard trực quan hóa cho người dùng.

* **Phần NGOÀI PHẠM VI (Out of Scope):** Hệ thống bán lẻ tại quầy POS, Cổng thanh toán Core Banking, Dịch vụ gửi SMS Brandname tự động, Hệ thống quản lý bảo hành.

## 3.2. Ba câu lập luận lựa chọn kiến trúc
* **Câu 1:** *"Vì **NFR01** yêu cầu thao tác tìm kiếm và lọc dữ liệu phản hồi dưới **2,0 giây** trên tập $67.037$ bản ghi, tôi chọn **tách biệt cơ sở dữ liệu lưu trữ khách hàng sạch (`dim_customer`) và đánh chỉ mục (Index) trên hai cột `so_dien_thoai_clean` và `email_clean`**, đánh đổi là **tốn thêm dung lượng bộ nhớ đĩa cho chỉ mục và làm chậm thời gian ghi dữ liệu ban đầu khi nạp hàng loạt (Bulk Insert)**."*
* **Câu 2:** *"Vì **NFR02** yêu cầu thời gian tải dashboard chất lượng dữ liệu phản hồi dưới **3,0 giây**, tôi chọn **tính toán trước các chỉ số tổng hợp (Pre-aggregated Metrics) trong bảng Fact `fact_customer_quality_audit` tại thời điểm chạy pipeline ETL thay vì tính toán động On-the-fly khi người dùng mở Dashboard**, đánh đổi là **dữ liệu dashboard chỉ phản ánh theo từng phiên chạy (Batch) chứ không cập nhật theo thời gian thực (Real-time)**."*
* **Câu 3:** *"Vì **NFR03** yêu cầu tỷ lệ hao hụt dữ liệu là **0,00%** (bảo toàn trọn vẹn $67.037$ bản ghi), tôi chọn **cơ chế lưu trữ dữ liệu đa tầng (Multi-hop Staging Architecture) giữ nguyên bản sao dữ liệu thô tại tầng Staging và áp dụng cờ trạng thái (Status Flags) thay vì xóa vật lý (Hard Delete) các bản ghi lỗi**, đánh đổi là **dung lượng kho dữ liệu tăng gấp đôi do phải lưu cả bản ghi gốc lẫn bản ghi đã chuẩn hóa**."*

---

# MỤC 4 – MÔ HÌNH DỮ LIỆU THEO CHUYÊN NGÀNH DA

*(Nội dung chi tiết được lưu trong file `docs/data-requirements.md` và sơ đồ gốc `docs/erd.drawio`)*

## 4.1. Sơ đồ Data Flow
`customers_raw.csv` $\rightarrow$ Trích xuất & Profiling $\rightarrow$ Kiểm định 6 quy tắc DQ $\rightarrow$ Chuẩn hóa SĐT/Họ tên $\rightarrow$ Quét trùng lặp $\rightarrow$ Nạp vào Data Warehouse (Fact & 3 Dim) $\rightarrow$ Dashboard.

## 4.2. Lược đồ kho dữ liệu (Star Schema) và Tuyên bố GRAIN
> **TUYÊN BỐ GRAIN (MỨC ĐỘ HẠT):**  
> Mỗi dòng trong bảng sự kiện `fact_customer_quality_audit` đại diện cho **kết quả kiểm định chất lượng của MỘT bản ghi khách hàng (`record_id`) trong MỘT phiên chạy kiểm định (`run_key`) theo MỘT quy tắc chất lượng cụ thể (`rule_key`)**.

## 4.3. Đặc tả chi tiết các bảng trong kho dữ liệu
* **Bảng Fact: `fact_customer_quality_audit`**
  * `audit_id` (`BIGINT`, PK): Khóa chính nhân tạo định danh dòng kiểm định.
  * `customer_key` (`INT`, FK): Khóa ngoại tham chiếu `dim_customer`.
  * `run_key` (`INT`, FK): Khóa ngoại tham chiếu `dim_audit_run`.
  * `rule_key` (`INT`, FK): Khóa ngoại tham chiếu `dim_quality_rule`.
  * `is_passed` (`BOOLEAN`): Trạng thái đạt (1) hoặc vi phạm (0) quy tắc.
  * `is_missing` (`BOOLEAN`): Cờ báo dữ liệu thiếu (NULL).
  * `is_invalid_format` (`BOOLEAN`): Cờ báo dữ liệu sai định dạng ban đầu.
  * `is_duplicate` (`BOOLEAN`): Cờ báo bản ghi có nguy cơ trùng lặp.
  * `is_auto_cleaned` (`BOOLEAN`): Cờ báo bản ghi đã được tự động chuẩn hóa.
  * `quality_score` (`DECIMAL(5,2)`): Điểm số chất lượng của bản ghi (0 – 100).
* **Bảng Dimension 1: `dim_customer`**
  * `customer_key` (`INT`, PK): Khóa thay thế của khách hàng trong kho dữ liệu.
  * `record_id` (`BIGINT`): Mã định danh gốc từ `customers_raw.csv`.
  * `ho_ten_goc` (`VARCHAR(255)`): Họ tên gốc chưa xử lý.
  * `ho_ten_clean` (`VARCHAR(255)`): Họ tên đã chuẩn hóa Title Case và xóa khoảng trắng thừa.
  * `so_dien_thoai_goc` (`VARCHAR(50)`): Số điện thoại gốc ban đầu.
  * `so_dien_thoai_clean` (`VARCHAR(15)`): Số điện thoại chuẩn hóa 10 số dạng `0xxxxxxxxx`.
  * `email_clean` (`VARCHAR(255)`): Email chuyển về chữ thường.
  * `dia_chi_clean` (`VARCHAR(500)`): Địa chỉ đã cắt tỉa khoảng trắng.
  * `ngay_tao` (`DATE`): Ngày tạo bản ghi (YYYY-MM-DD).
  * `status` (`VARCHAR(50)`): Trạng thái bản ghi ("Đạt chuẩn sạch", "Nghi ngờ trùng", "Thiếu dữ liệu").
* **Bảng Dimension 2: `dim_quality_rule`**
  * `rule_key` (`INT`, PK): Khóa chính danh mục quy tắc.
  * `rule_code` (`VARCHAR(10)`): Mã quy tắc (`DQ01` đến `DQ06`).
  * `rule_name` (`VARCHAR(100)`): Tên quy tắc chất lượng dữ liệu.
  * `target_column` (`VARCHAR(50)`): Cột dữ liệu áp dụng kiểm tra.
  * `severity` (`VARCHAR(20)`): Mức độ nghiêm trọng ("Cảnh báo", "Nghi ngờ", "Lỗi định dạng").
* **Bảng Dimension 3: `dim_audit_run`**
  * `run_key` (`INT`, PK): Khóa chính phiên kiểm định.
  * `run_date` (`TIMESTAMP`): Ngày giờ thực hiện phiên chạy.
  * `total_records` (`INT`): Tổng số bản ghi được nạp xử lý ($67.037$).
  * `run_by` (`VARCHAR(100)`): Người vận hành phiên chạy.

---

# MỤC 5 – WIREFRAME 3 MÀN HÌNH DASHBOARD DA

*(Hình ảnh Wireframe chi tiết được lưu trong file: `docs/wireframe.png`)*

Thiết kế bao gồm 3 khung Dashboard theo đúng yêu cầu chuyên ngành DA:

## 5.1. Khung 1: Dashboard Tổng quan Chỉ số Chất lượng Dữ liệu
* **Bố cục & Chỉ số tổng hợp:** Gồm 4 thẻ KPI chính ở trên cùng:
  * Tổng bản ghi nạp: $67.037$ bản ghi ($100\%$).
  * Đạt chuẩn sạch 100%: $35.858$ bản ghi ($53{,}49\%$).
  * Nguy cơ trùng lặp: $16.039$ bản ghi ($23{,}93\%$).
  * Thiếu thông tin (NULL): $30.157$ bản ghi ($44{,}99\%$).
* **Biểu đồ:** Biểu đồ 1.1 thể hiện tỷ lệ vi phạm theo từng quy tắc DQ (cột ngang); Biểu đồ 1.2 thể hiện phân bố xếp loại chất lượng bản ghi (Donut/Bar chart: Xuất sắc $53{,}5\%$, Đạt yêu cầu $22{,}6\%$, Cần xử lý $23{,}9\%$).
* **Bộ lọc:** Bộ lọc đợt kiểm định, bộ lọc trạng thái và bộ lọc quy tắc.
* **Ghi chú nguồn dữ liệu Khung 1:** Thẻ KPI tính từ `COUNT(customer_key)`, `SUM(is_passed)`, `SUM(is_duplicate)` từ `fact_customer_quality_audit`. Biểu đồ 1.1 nhóm theo `rule_code` từ `dim_quality_rule`. Biểu đồ 1.2 phân nhóm theo `quality_score`. Phục vụ Use Case **UC07**.

## 5.2. Khung 2: Chi tiết Trùng lặp & Dữ liệu Bất thường
* **Bố cục & Bộ lọc:** Bộ lọc tiêu chí trùng (Số điện thoại, Email) và bộ lọc số lần lặp ($\ge 2$ lần).
* **Biểu đồ:** Biểu đồ 2.1 thể hiện Top các số điện thoại bị trùng lặp nhiều nhất (Top SĐT lặp 6 lần, 5 lần...).
* **Bảng dữ liệu & Nút hành động:** Bảng 2.2 hiển thị danh sách các bản ghi nghi ngờ trùng lặp (Mã bản ghi, Họ tên chuẩn, SĐT chuẩn hóa, Email) cùng hai nút hành động: *[Xác nhận gộp nhóm]* và *[Giữ riêng biệt]*.
* **Ghi chú nguồn dữ liệu Khung 2:** Truy vấn từ `dim_customer` liên kết với `fact_customer_quality_audit` có điều kiện `is_duplicate = TRUE`. Các trường hiển thị lấy từ `dim_customer` (`record_id`, `ho_ten_clean`, `so_dien_thoai_clean`, `email_clean`). Phục vụ Use Case **UC04**.

## 5.3. Khung 3: Tiến độ Làm sạch & Chuẩn hóa Dữ liệu
* **Biểu đồ:** Biểu đồ 3.1 là biểu đồ cột đôi so sánh số lượng lỗi trước và sau khi chuẩn hóa (SĐT mã quốc gia: $11.336 \rightarrow 0$; Họ tên thừa khoảng trắng: $1.346 \rightarrow 0$; Họ tên sai viết hoa: $4.584 \rightarrow 0$). Biểu đồ 3.2 thể hiện tỷ lệ hoàn tất chuẩn hóa tự động đạt $100\%$.
* **Ghi chú nguồn dữ liệu Khung 3:** Đối chiếu giữa trường thô (`ho_ten_goc`, `so_dien_thoai_goc`) và trường sạch (`ho_ten_clean`, `so_dien_thoai_clean`) trong `dim_customer`; tỷ lệ hoàn tất lấy từ cờ `is_auto_cleaned` trong `fact_customer_quality_audit`. Phục vụ Use Case **UC05** và **UC06**.

---

# PHỤ LỤC – BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI

| Công cụ | Dùng vào việc gì | Áp dụng ở phần nào | Đã kiểm chứng thế nào |
| :--- | :--- | :--- | :--- |
| **ChatGPT / Antigravity AI** | Gợi ý cấu trúc bảng Fact và các bảng Dimension cho kho dữ liệu theo chuẩn Star Schema (Mô hình Kimball) phù hợp với bài toán Data Quality. | Mục 4 – Mô hình dữ liệu (`fact_customer_quality_audit`, `dim_customer`, `dim_quality_rule`, `dim_audit_run`). | Đối chiếu với lý thuyết Kimball về mô hình hóa kho dữ liệu; kiểm tra khóa chính, khóa ngoại, kiểu dữ liệu từng cột và tự phát biểu rõ ràng mức độ hạt (GRAIN) của bảng Fact. |
| **ChatGPT / Antigravity AI** | Hỗ trợ chuẩn hóa cấu trúc câu lập luận quyết định kiến trúc hệ thống theo đúng khuôn mẫu quy định của đề bài. | Mục 3 – Thiết kế kiến trúc (3 câu giải thích kiến trúc gắn với mã NFR và phân tích đánh đổi). | Tự đối chiếu với các yêu cầu phi chức năng (NFR01, NFR02, NFR03), rà soát ngưỡng số thực tế của tập dữ liệu $67.037$ bản ghi và tự thẩm định các đánh đổi kỹ thuật. |
| **— Không sử dụng AI —** *(Tự làm hoàn toàn)* | Khám phá dữ liệu thực tế (Data Profiling) trên tập tin nguồn `customers_raw.csv`, tính toán các tỷ lệ thiếu dữ liệu, sai định dạng số điện thoại, viết hoa họ tên và tỷ lệ trùng lặp. | Mục 1 (Phạm vi) và Mục 4 (Bộ quy tắc chất lượng dữ liệu DQ01 – DQ06). | Tự viết và thực thi mã nguồn Python bằng thư viện Pandas trên Jupyter Notebook (`notebooks/01_check_customers.ipynb`), đối chiếu trực tiếp kết quả với số liệu thực tế ($67.037$ dòng, $11.336$ SĐT mã 84, $4.716$ email lặp). |
| **— Không sử dụng AI —** *(Tự làm hoàn toàn)* | Xác định phạm vi nghiệp vụ L7, phân tích các Actor, viết User Story và xây dựng sơ đồ Use Case. | Mục 1 (Giới thiệu & phạm vi) và Mục 2 (Use Case). | Dựa trên đề cương bài học Buổi 2 và Buổi 4, tự vẽ sơ đồ Use Case trên draw.io và viết đặc tả luồng chính/ngoại lệ. |

### DÒNG CAM KẾT LIÊM CHÍNH HỌC THUẬT:
> **"Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp."**

* **Sinh viên:** Hồ Lê Trung Bảo  
* **Mã số sinh viên (MSSV):** 2374802010030  
* **Lớp:** Chuyên đề Tốt nghiệp 1 – Track DA  
* **Ngày:** 09/10/2026  
