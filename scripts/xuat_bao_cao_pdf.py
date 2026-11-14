# -*- coding: utf-8 -*-
"""
Script tạo file PDF báo cáo Bài tập 3 chuẩn chỉnh cho Track DA
Tên file: BT3_2374802010030_HoLeTrungBao.pdf
Sinh viên: Hồ Lê Trung Bảo - MSSV: 2374802010030
"""

import os
import subprocess
import base64

ROOT_DIR = r"C:\Users\ASUS\smartcrm-2374802010030-customer-data-quality"
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
OUTPUT_PDF = os.path.join(ROOT_DIR, "BT3_2374802010030_HoLeTrungBao.pdf")
HTML_FILE = os.path.join(ROOT_DIR, "bao_cao_bt3_tam.html")

def to_base64(image_path):
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    return f"data:{mime};base64,{data}"

logo_b64 = to_base64(os.path.join(DOCS_DIR, "logo_highres.png"))
anh1_b64 = to_base64(os.path.join(DOCS_DIR, "chup_man_hinh_ket_qua_tests.png"))
anh2_b64 = to_base64(os.path.join(DOCS_DIR, "chup_man_hinh_so_sanh_dong.png"))
anh3_b64 = to_base64(os.path.join(DOCS_DIR, "chup_man_hinh_dashboard.png"))

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo cáo Bài tập 3 - Hồ Lê Trung Bảo - 2374802010030</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 18mm 15mm 20mm 15mm;
    @bottom-right {{
      content: counter(page);
    }}
  }}
  body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2D3748;
    line-height: 1.55;
    font-size: 10.5pt;
    margin: 0;
    padding: 0;
  }}
  .page-break {{
    page-break-before: always;
  }}
  .avoid-break {{
    page-break-inside: avoid;
  }}

  /* TRANG BÌA */
  .cover-page {{
    text-align: center;
    padding-top: 30px;
    height: 100%;
    box-sizing: border-box;
    page-break-after: always;
  }}
  .cover-logo {{
    max-height: 85px;
    margin-bottom: 20px;
  }}
  .cover-univ {{
    font-size: 13pt;
    font-weight: bold;
    color: #8B0000;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
  }}
  .cover-faculty {{
    font-size: 11pt;
    font-weight: 600;
    color: #4A5568;
    margin-bottom: 25px;
  }}
  .cover-divider {{
    height: 3px;
    background: linear-gradient(to right, #8B0000, #C53030, #E2E8F0);
    width: 60%;
    margin: 0 auto 35px auto;
  }}
  .cover-title {{
    font-size: 18pt;
    font-weight: 800;
    color: #1A202C;
    text-transform: uppercase;
    line-height: 1.35;
    margin-bottom: 12px;
  }}
  .cover-subtitle {{
    font-size: 12pt;
    font-weight: 600;
    color: #8B0000;
    margin-bottom: 40px;
  }}
  .cover-box {{
    border: 2px solid #CBD5E0;
    border-radius: 8px;
    padding: 22px 30px;
    width: 85%;
    margin: 0 auto 35px auto;
    text-align: left;
    background-color: #F7FAFC;
    font-size: 10.5pt;
  }}
  .cover-box table {{
    width: 100%;
    border-collapse: collapse;
  }}
  .cover-box td {{
    padding: 5px 8px;
    vertical-align: top;
  }}
  .cover-box td.label {{
    font-weight: bold;
    color: #2D3748;
    width: 32%;
  }}
  .cover-box td.val {{
    color: #1A202C;
  }}
  .cover-box td.val a {{
    color: #2B6CB0;
    text-decoration: none;
    word-break: break-all;
    font-weight: 600;
  }}
  .cover-footer {{
    margin-top: 60px;
    font-size: 10pt;
    color: #718096;
    font-weight: 500;
  }}

  /* HEADING STYLES */
  h1 {{
    font-size: 14pt;
    font-weight: bold;
    color: #8B0000;
    border-bottom: 2px solid #8B0000;
    padding-bottom: 5px;
    margin-top: 24px;
    margin-bottom: 14px;
    text-transform: uppercase;
  }}
  h2 {{
    font-size: 12pt;
    font-weight: bold;
    color: #1A365D;
    margin-top: 18px;
    margin-bottom: 10px;
    border-left: 4px solid #1A365D;
    padding-left: 8px;
  }}
  h3 {{
    font-size: 11pt;
    font-weight: bold;
    color: #2D3748;
    margin-top: 14px;
    margin-bottom: 8px;
  }}
  p {{
    margin: 6px 0;
    text-align: justify;
  }}
  ul, ol {{
    margin: 6px 0;
    padding-left: 22px;
  }}
  li {{
    margin-bottom: 4px;
  }}

  /* TABLE STYLES */
  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 9.5pt;
  }}
  table.data-table th, table.data-table td {{
    border: 1px solid #CBD5E0;
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
  }}
  table.data-table th {{
    background-color: #EDF2F7;
    font-weight: bold;
    color: #1A202C;
  }}
  table.data-table tr:nth-child(even) {{
    background-color: #F8FAFC;
  }}
  .badge-pass {{
    background-color: #C6F6D5;
    color: #22543D;
    font-weight: bold;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 8.5pt;
    display: inline-block;
  }}
  .badge-crit {{
    background-color: #FED7D7;
    color: #9B2C2C;
    font-weight: bold;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 8.5pt;
    display: inline-block;
  }}
  .badge-major {{
    background-color: #FEEBC8;
    color: #7B341E;
    font-weight: bold;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 8.5pt;
    display: inline-block;
  }}
  .badge-minor {{
    background-color: #E2E8F0;
    color: #4A5568;
    font-weight: bold;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 8.5pt;
    display: inline-block;
  }}

  /* CODE & BLOCKS */
  pre, code {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
  }}
  pre {{
    background-color: #1A202C;
    color: #EDF2F7;
    padding: 10px 14px;
    border-radius: 5px;
    overflow-x: auto;
    margin: 8px 0;
    line-height: 1.4;
  }}
  p code, li code {{
    background-color: #EDF2F7;
    color: #8B0000;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 9pt;
  }}
  .callout {{
    background-color: #EBF8FF;
    border-left: 4px solid #3182CE;
    padding: 10px 14px;
    border-radius: 0 4px 4px 0;
    margin: 12px 0;
    font-size: 9.5pt;
  }}

  /* IMAGE CONTAINERS */
  .screenshot-container {{
    margin: 14px 0;
    text-align: center;
    border: 1px solid #CBD5E0;
    border-radius: 6px;
    padding: 8px;
    background-color: #F7FAFC;
    page-break-inside: avoid;
  }}
  .screenshot-container img {{
    max-width: 98%;
    height: auto;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }}
  .caption {{
    font-size: 9pt;
    font-weight: 600;
    color: #4A5568;
    margin-top: 6px;
  }}
</style>
</head>
<body>

<!-- TRANG BÌA -->
<div class="cover-page">
  <img src="{logo_b64}" class="cover-logo" alt="Van Lang University Logo">
  <div class="cover-univ">TRƯỜNG ĐẠI HỌC VĂN LANG</div>
  <div class="cover-faculty">KHOA CÔNG NGHỆ THÔNG TIN</div>
  <div class="cover-divider"></div>

  <div class="cover-title">BÁO CÁO BÀI TẬP 3<br>KIỂM THỬ, ĐÓNG GÓI VÀ TÀI LIỆU HÓA HỆ THỐNG</div>
  <div class="cover-subtitle">HỌC PHẦN: CHUYÊN ĐỀ TỐT NGHIỆP 1 (71ITGR40203) — HỌC KỲ 1, NĂM HỌC 2026 – 2027</div>

  <div class="cover-box">
    <table>
      <tr>
        <td class="label">Họ và tên sinh viên:</td>
        <td class="val"><strong>Hồ Lê Trung Bảo</strong></td>
      </tr>
      <tr>
        <td class="label">Mã số sinh viên (MSSV):</td>
        <td class="val"><strong>2374802010030</strong></td>
      </tr>
      <tr>
        <td class="label">Lớp học phần:</td>
        <td class="val">71ITGR40203_01 (Khóa K23T)</td>
      </tr>
      <tr>
        <td class="label">Chuyên ngành (Track):</td>
        <td class="val"><strong>Data Analytics (DA)</strong></td>
      </tr>
      <tr>
        <td class="label">Mã luồng nghiệp vụ:</td>
        <td class="val"><strong>L7 – Customer Data Quality (Kiểm tra & Làm sạch dữ liệu khách hàng)</strong></td>
      </tr>
      <tr>
        <td class="label">Kho dữ liệu đích:</td>
        <td class="val">SQLite Star Schema (<code>data/processed/warehouse.db</code>)</td>
      </tr>
      <tr>
        <td class="label">GitHub Repository:</td>
        <td class="val"><a href="https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality" target="_blank">https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality</a></td>
      </tr>
      <tr>
        <td class="label">Thẻ phát hành (Tag):</td>
        <td class="val"><a href="https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality/releases/tag/v1.0" target="_blank">v1.0 (Bản phát hành chính thức Bài tập 3)</a></td>
      </tr>
      <tr>
        <td class="label">Link Web Deploy Cloud:</td>
        <td class="val"><a href="https://smartcrm-2374802010030.streamlit.app" target="_blank">https://smartcrm-2374802010030.streamlit.app</a></td>
      </tr>
    </table>
  </div>

  <div class="cover-footer">
    TP. HỒ CHÍ MINH — THÁNG 11/2026
  </div>
</div>

<!-- MỤC 1: KẾ HOẠCH KIỂM THỬ -->
<div class="page-break"></div>
<h1>MỤC 1. KẾ HOẠCH KIỂM THỬ (TEST PLAN)</h1>

<h2>1.1. Phạm vi kiểm thử và phần chủ ý KHÔNG kiểm</h2>
<p><strong>Phạm vi được kiểm thử toàn diện:</strong></p>
<ul>
  <li><strong>Pha 1 (Extract):</strong> Trích xuất dữ liệu thô nguyên trạng dạng chuỗi (<code>dtype=str</code>) từ tập tin nguồn <code>customers_raw.csv</code> (67.037 bản ghi) và <code>customers_sample.csv</code> (300 bản ghi), bảo toàn số 0 ở đầu số điện thoại.</li>
  <li><strong>Pha 2 (Transform):</strong> Chuẩn hóa SĐT (xử lý tiền tố quốc tế <code>+84</code>, <code>84</code>, dấu phân cách), chuẩn hóa họ tên về Title Case, chuẩn hóa email và ngày tháng. Phân luồng dòng sạch và dòng lỗi.</li>
  <li><strong>Pha 3 (Quality):</strong> Đo lường định lượng 9 chỉ tiêu thuộc 3 chiều chất lượng dữ liệu (Đầy đủ, Chính xác, Nhất quán/Trùng lặp).</li>
  <li><strong>Pha 4 (Load):</strong> Nạp dữ liệu vào CSDL kho Star Schema SQLite: nạp dòng sạch vào <code>dim_customer</code> (UPSERT theo <code>customer_id</code>), nạp sự kiện kiểm định vào <code>fact_customer_quality_audit</code>; cách ly toàn bộ dòng lỗi vào bảng <code>reject_rows</code> kèm lý do chi tiết.</li>
  <li><strong>Tính Nạp lại được (Idempotency):</strong> Chạy lại pipeline nhiều lần trên cùng tập dữ liệu không làm sai lệch hay nhân đôi số lượng bản ghi trong kho.</li>
  <li><strong>Bảo vệ dữ liệu cá nhân PII (NFR05 / D4):</strong> Che mặt nạ 100% SĐT và Email trên tầng phân tích và báo cáo.</li>
  <li><strong>Bộ kiểm thử hồi quy:</strong> Đảm bảo 3 lỗi đã phát hiện (<code>BUG-01</code>, <code>BUG-02</code>, <code>BUG-03</code>) không bị tái phát.</li>
</ul>

<p><strong>Phạm vi chủ ý KHÔNG kiểm thử (kèm lý do kỹ thuật):</strong></p>
<ul>
  <li><em>Giao diện người dùng kéo thả tùy biến:</em> Hệ thống là Pipeline ETL backend và kho dữ liệu phân tích của Track DA.</li>
  <li><em>Kiểm thử chịu tải phân tán trên 1.000.000 bản ghi:</em> Dữ liệu hoạt động thực tế của chuỗi Mekong Mobile hiện tại là 67.037 dòng; phạm vi Big Data phân tán thuộc học phần Chuyên đề 2.</li>
</ul>

<h2>1.2. Chiến lược và Số lượng kiểm thử các tầng</h2>
<table class="data-table">
  <thead>
    <tr>
      <th style="width: 28%;">Tầng kiểm thử</th>
      <th style="width: 14%; text-align: center;">Số test case</th>
      <th style="width: 25%;">Tệp mã nguồn</th>
      <th>Mô tả và Ghi chú</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Unit test hàm chuẩn hóa</strong></td>
      <td style="text-align: center;">9</td>
      <td><code>tests/test_rules.py</code></td>
      <td>Hàm thuần túy: kiểm tra chuẩn hóa SĐT, họ tên, email, ngày, che PII.</td>
    </tr>
    <tr>
      <td><strong>Unit test đo chất lượng & phân luồng</strong></td>
      <td style="text-align: center;">2</td>
      <td><code>tests/test_checks.py</code></td>
      <td>Đo 3 chiều chất lượng và phân luồng bản ghi sạch vs reject.</td>
    </tr>
    <tr>
      <td><strong>Unit test module Dashboard</strong></td>
      <td style="text-align: center;">6</td>
      <td><code>tests/test_dashboard.py</code></td>
      <td>Đếm dòng staging vs fact, đối soát chênh lệch, tạo biểu đồ và xử lý trạng thái rỗng.</td>
    </tr>
    <tr>
      <td><strong>Kiểm thử hồi quy (Regression)</strong></td>
      <td style="text-align: center;">3</td>
      <td><code>tests/test_hoi_quy.py</code></td>
      <td>Chống tái phát lỗi Foreign Key (BUG-01), ánh xạ cột (BUG-02), truy vấn (BUG-03).</td>
    </tr>
    <tr>
      <td><strong>Kiểm thử tích hợp End-to-End</strong></td>
      <td style="text-align: center;">12</td>
      <td><code>docs/test-report.md</code></td>
      <td>Thực thi toàn bộ pipeline từ tệp CSV thô đến kho SQLite và sinh báo cáo.</td>
    </tr>
  </tbody>
</table>
<p><strong>Tổng cộng:</strong> <strong>20 test case tự động</strong> qua Pytest (100% PASS) và <strong>12 test case thực nghiệm</strong> chạy thật trên hệ thống.</p>

<h2>1.3. Tiêu chí thành công đo được</h2>
<ol>
  <li><strong>100% test case tự động PASS:</strong> Thực thi thành công toàn bộ 20 test bằng 1 lệnh duy nhất <code>python -m pytest -v</code> trong thời gian &le; 2 giây.</li>
  <li><strong>Tiêu chí Idempotent:</strong> Số dòng trong 4 bảng chính hoàn toàn không đổi sau khi chạy lại pipeline lần 2 và lần 3: <code>staging_customers</code>: 67.037 dòng; <code>reject_rows</code>: 4.133 dòng; <code>dim_customer</code>: 62.904 dòng; <code>fact_customer_quality_audit</code>: 62.904 dòng.</li>
  <li><strong>Tiêu chí Không mất dữ liệu (Zero Data Loss):</strong> Chênh lệch $67.037 - 62.904 = 4.133$ dòng khớp tuyệt đối với số lượng dòng bị từ chối trong <code>reject_rows</code>.</li>
  <li><strong>Bảo mật PII:</strong> 100% số điện thoại và email được che mặt nạ, tỷ lệ rò rỉ dữ liệu cá nhân là 0,00%.</li>
</ol>

<h2>1.4. Môi trường và Dữ liệu thử nghiệm</h2>
<ul>
  <li><strong>Môi trường:</strong> Python 3.11/3.14 trên Windows/Linux. Cơ sở dữ liệu SQLite nhúng tại <code>data/processed/warehouse.db</code>.</li>
  <li><strong>Tập dữ liệu mẫu nhỏ (<code>data/mau/customers_sample.csv</code>):</strong> Gồm đúng 300 dòng phục vụ chạy thử nghiệm nhanh &le; 2 lệnh (280 dòng nạp kho, 20 dòng reject).</li>
  <li><strong>Tập dữ liệu thực tế (<code>data/raw/customers_raw.csv</code>):</strong> Gồm 67.037 bản ghi dữ liệu khách hàng thật của Mekong Mobile.</li>
</ul>

<!-- MỤC 2: BÁO CÁO KẾT QUẢ KIỂM THỬ -->
<div class="page-break"></div>
<h1>MỤC 2. BÁO CÁO KẾT QUẢ KIỂM THỬ (TEST REPORT)</h1>
<p>Tình trạng kiểm thử: <strong>20/20 test case tự động PASS</strong> qua Pytest và <strong>12/12 ca kiểm thử thực nghiệm</strong> đạt kết quả mong đợi với số liệu thực tế.</p>

<table class="data-table">
  <thead>
    <tr>
      <th style="width: 6%;">Mã</th>
      <th style="width: 14%;">Tiền điều kiện</th>
      <th style="width: 18%;">Các bước thực hiện</th>
      <th style="width: 16%;">Dữ liệu thử</th>
      <th style="width: 18%;">Kết quả mong đợi</th>
      <th style="width: 8%; text-align: center;">Mức</th>
      <th>Kết quả thực tế quan sát</th>
      <th style="width: 7%; text-align: center;">P/F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>TC-01</strong></td>
      <td>CSDL chưa tạo hoặc đã xóa</td>
      <td>Chạy pipeline trên tập mẫu nhỏ</td>
      <td><code>customers_sample.csv</code> (300 dòng)</td>
      <td>Nạp đúng 280 khách sạch vào <code>dim_customer</code>, 20 vào <code>reject_rows</code></td>
      <td style="text-align: center;">Cao</td>
      <td>Khởi tạo bảng DDL, đọc 300 dòng, nạp 280 dim, 20 reject; mã thoát 0</td>
      <td style="text-align: center;"><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-02</strong></td>
      <td>Không</td>
      <td>Gọi hàm chuẩn hóa họ tên</td>
      <td><code>' nguyễn văn an '</code>, <code>'TRẦN THỊ BÌNH'</code></td>
      <td>Chuẩn hóa Title Case, bỏ khoảng trắng: <code>'Nguyễn Văn An'</code>, <code>'Trần Thị Bình'</code></td>
      <td style="text-align: center;">Cao</td>
      <td>Trả về chính xác Title Case chuẩn tiếng Việt</td>
      <td style="text-align: center;"><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-03</strong></td>
      <td>Không</td>
      <td><strong>Giá trị biên tiền tố SĐT:</strong> Xử lý mã quốc tế</td>
      <td><code>'+84901234567'</code> và <code>'84901234567'</code></td>
      <td>Quy đổi chuẩn xác về 10 chữ số <code>'0901234567'</code></td>
      <td style="text-align: center;">Cao</td>
      <td>Cả 2 trường hợp đều chuyển về đúng 10 số chuẩn</td>
      <td style="text-align: center;"><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-04</strong></td>
      <td>Không</td>
      <td><strong>Giá trị biên ngày:</strong> Parse ngày chuyển giao năm</td>
      <td><code>'2024-12-31'</code>, <code>'2025-01-01'</code>, <code>'15/05/2025'</code></td>
      <td>Parse chính xác thành đối tượng date, không lệch ngày</td>
      <td style="text-align: center;">Cao</td>
      <td>Trả về đúng đối tượng <code>datetime.date</code></td>
      <td style="text-align: center;"><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-05</strong></td>
      <td>Không</td>
      <td><strong>Dữ liệu sai:</strong> SĐT rác hoặc thiếu ký số</td>
      <td>SĐT 8 số: <code>'09012345'</code>; SĐT chữ: <code>'0901abc567'</code></td>
      <td>Hàm trả về <code>None</code>; chuyển vào bảng reject, pipeline không crash</td>
      <td style="text-align: center;">Cao</td>
      <td>Trả về <code>None</code>; nạp vào <code>reject_rows</code> kèm lý do chi tiết</td>
      <td style="text-align: center;"><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-06</strong></td>
      <td>Không</td>
      <td><strong>Dữ liệu sai bắt buộc:</strong> Thiếu ID hoặc họ tên</td>
      <td><code>customer_id='   '</code>, <code>ho_ten='nan'</code></td>
      <td>Gắn mã vi phạm <code>DQ01_ID</code>, <code>DQ01_NAME</code>, cách ly vào reject</td>
      <td style="text-align: center;">Cao</td>
      <td>Phân loại đúng mã quy tắc vi phạm và ghi nhận lý do rõ ràng</td>
      <td style="text-align: center;"><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-07</strong></td>
      <td>Không</td>
      <td><strong>Bảo mật PII (NFR05):</strong> Che mặt nạ SĐT & Email</td>
      <td><code>'0901234567'</code>, <code>'trungbao@gmail.com'</code></td>
      <td>SĐT: <code>'0901***567'</code>; Email: <code>'t***@gmail.com'</code></td>
      <td style="text-align: center;">Cao</td>
      <td>Che đúng định dạng, tỷ lệ rò rỉ 0,00%</td>
      <td style="text-align: center;"><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-08</strong></td>
      <td>Không</td>
      <td><strong>Chất lượng dữ liệu:</strong> Đo 9 chỉ tiêu thuộc 3 chiều</td>
      <td>Fixture mẫu 6 dòng</td>
      <td>Trả về danh sách đối tượng <code>Do</code> đủ 9 số đo định lượng</td>
      <td style="text-align: center;">Cao</td>
      <td>Đo đủ 9 chỉ tiêu; mỗi phép đo trả về 1 số đối chiếu ngưỡng YAML</td>
      <td style="text-align: center;"><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-09</strong></td>
      <td>Không</td>
      <td><strong>Chiều Nhất quán:</strong> Phát hiện khách trùng lặp</td>
      <td>Tập dữ liệu thật 67.037 dòng</td>
      <td>Phát hiện 27.123 khách hàng có dấu hiệu trùng SĐT/Email (43,1%)</td>
      <td style="text-align: center;">Cao</td>
      <td>Gán cờ <code>is_duplicate=1</code> cho 27.123 bản ghi; đạt ngưỡng &le; 70%</td>
      <td style="text-align: center;"><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-10</strong></td>
      <td>Đã chạy lần 1 trên 67.037 dòng</td>
      <td><strong>Phép thử Nạp lại được (Idempotency):</strong> Chạy lại lần 2 và lần 3</td>
      <td>Cùng tập dữ liệu <code>customers_raw.csv</code> (67.037 dòng)</td>
      <td>Số lượng dòng ở cả 4 bảng trong kho CSDL hoàn toàn không đổi</td>
      <td style="text-align: center;">Cao</td>
      <td>Số lượng giữ nguyên: 67.037 / 4.133 / 62.904 / 62.904; không nhân đôi</td>
      <td style="text-align: center;"><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-11</strong></td>
      <td>Đã nạp kho dữ liệu</td>
      <td><strong>Đối chiếu Staging vs Fact:</strong> Chạy module so sánh dòng</td>
      <td>CSDL kho <code>warehouse.db</code></td>
      <td>Staging (67.037) &minus; Fact (62.904) = 4.133 dòng trong bảng reject</td>
      <td style="text-align: center;">Cao</td>
      <td>In bảng đối chiếu rõ ràng; xác nhận không thất thoát dữ liệu</td>
      <td style="text-align: center;"><span class="badge-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-12</strong></td>
      <td>Có CSDL kho dữ liệu</td>
      <td><strong>Xử lý trạng thái rỗng (Empty State):</strong> Lọc ngày không có dữ liệu</td>
      <td><code>--tu-ngay 2099-01-01 --den-ngay 2099-12-31</code></td>
      <td>Không văng lỗi; tự động sinh ảnh placeholder cảnh báo thân thiện</td>
      <td style="text-align: center;">Cao</td>
      <td>Tạo ảnh <code>trang_thai_rong_bieu_do.png</code>, không crash ứng dụng</td>
      <td style="text-align: center;"><span class="badge-pass">PASS</span></td>
    </tr>
  </tbody>
</table>

<!-- MỤC 3: NHẬT KÝ LỖI -->
<div class="page-break"></div>
<h1>MỤC 3. NHẬT KÝ THEO DÕI LỖI (BUG LOG)</h1>
<p>Bảng ghi nhận trung thực 3 lỗi kỹ thuật phát hiện được trong quá trình phát triển, nguyên nhân gốc rễ, phương án khắc phục và liên kết commit trên GitHub:</p>

<h2>BUG-01 · Mức độ: <span class="badge-crit">CRITICAL</span> — Vi phạm toàn vẹn khóa ngoại khi nạp lại dữ liệu</h2>
<ol>
  <li><strong>Phát hiện bởi:</strong> Phép thử nạp lại được (Idempotency test) khi chạy pipeline lần thứ hai trên cùng tập dữ liệu.</li>
  <li><strong>Triệu chứng:</strong> Pipeline nạp lần thứ hai văng lỗi <code>sqlite3.IntegrityError: FOREIGN KEY constraint failed</code> khi cập nhật <code>dim_audit_run</code>.</li>
  <li><strong>Cách tái lập:</strong> Chạy <code>python -m src.pipeline</code> lần 1, sau đó chạy tiếp lần 2.</li>
  <li><strong>Nguyên nhân:</strong> Hàm <code>tao_phien_chay</code> sử dụng <code>INSERT OR REPLACE INTO dim_audit_run</code>. SQLite thực hiện <code>DELETE</code> bản ghi cũ rồi mới <code>INSERT</code>, làm mất <code>run_key</code> mà bảng <code>fact_customer_quality_audit</code> đang tham chiếu tới (Foreign Key).</li>
  <li><strong>Cách sửa:</strong> Đổi sang kiểm tra bằng <code>SELECT run_key FROM dim_audit_run WHERE batch_id = ?</code>. Nếu đã tồn tại thì thực hiện <code>UPDATE</code> giữ nguyên <code>run_key</code>; đồng thời xóa các dòng fact cũ của cùng <code>run_key</code> trước khi nạp lại.</li>
  <li><strong>Xác nhận:</strong> Chạy lại pipeline 3 lần liên tiếp, số lượng bản ghi ở cả 4 bảng giữ nguyên tuyệt đối, không phát sinh lỗi khóa ngoại.</li>
  <li><strong>Commit khắc phục:</strong> <a href="https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality/commit/94c9c9d" target="_blank">Commit 94c9c9d trên GitHub</a></li>
</ol>

<h2>BUG-02 · Mức độ: <span class="badge-major">MAJOR</span> — Lệch tên cột giữa thiết kế và tập dữ liệu thực tế</h2>
<ol>
  <li><strong>Phát hiện bởi:</strong> Chạy thử nghiệm trên tập dữ liệu thực tế <code>customers_raw.csv</code> (67.037 bản ghi).</li>
  <li><strong>Triệu chứng:</strong> Pipeline bị dừng với lỗi <code>KeyError: 'ngay_dang_ky'</code> hoặc <code>KeyError: 'customer_id'</code>.</li>
  <li><strong>Cách tái lập:</strong> Gọi hàm <code>clean_customers.xu_ly_lam_sach_khach_hang(df_tho)</code> trên dữ liệu CSV thô.</li>
  <li><strong>Nguyên nhân:</strong> File CSV thực tế của Mekong Mobile đặt tên cột là <code>record_id</code> và <code>ngay_tao</code>, khác với giả định thiết kế ban đầu là <code>customer_id</code> và <code>ngay_dang_ky</code>.</li>
  <li><strong>Cách sửa:</strong> Bổ sung cơ chế ánh xạ tự động linh hoạt: <code>cot_id = 'customer_id' if 'customer_id' in df.columns else 'record_id'</code> và <code>cot_ngay = 'ngay_dang_ky' if 'ngay_dang_ky' in df.columns else 'ngay_tao'</code>.</li>
  <li><strong>Xác nhận:</strong> Chạy thành công toàn bộ 67.037 dòng từ file CSV thật không còn gặp lỗi <code>KeyError</code>.</li>
  <li><strong>Commit khắc phục:</strong> <a href="https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality/commit/94c9c9d" target="_blank">Commit 94c9c9d trên GitHub</a></li>
</ol>

<h2>BUG-03 · Mức độ: <span class="badge-minor">MINOR</span> — Sai tên cột thời gian trong câu truy vấn bảng Reject</h2>
<ol>
  <li><strong>Phát hiện bởi:</strong> Kiểm tra trạng thái rỗng khi vẽ biểu đồ phân bổ lỗi DQ với bộ lọc ngày xa trong tương lai.</li>
  <li><strong>Triệu chứng:</strong> Terminal báo lỗi <code>sqlite3.OperationalError: no such column: ngay_nap</code>.</li>
  <li><strong>Cách tái lập:</strong> Gọi <code>python -m src.dashboard.bieu_do --tu-ngay 2099-01-01</code>.</li>
  <li><strong>Nguyên nhân:</strong> Trong câu lệnh SQL truy vấn bảng <code>reject_rows</code>, mã nguồn gọi cột <code>ngay_nap</code>, trong khi DDL tại <code>sql/002_reject.sql</code> đặt tên là <code>thoi_gian_tao</code>.</li>
  <li><strong>Cách sửa:</strong> Sửa lại tên cột trong câu truy vấn tại <code>src/dashboard/bieu_do.py</code> từ <code>ngay_nap</code> thành <code>thoi_gian_tao</code>.</li>
  <li><strong>Xác nhận:</strong> Chạy lại hàm vẽ biểu đồ với bộ lọc ngày tương lai, hệ thống tự động sinh ảnh placeholder cảnh báo thân thiện <code>trang_thai_rong_bieu_do.png</code> mà không hề crash.</li>
  <li><strong>Commit khắc phục:</strong> <a href="https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality/commit/3e3da6a" target="_blank">Commit 3e3da6a trên GitHub</a></li>
</ol>

<!-- MỤC 4: HƯỚNG DẪN TRIỂN KHAI -->
<div class="page-break"></div>
<h1>MỤC 4. HƯỚNG DẪN TRIỂN KHAI (DEPLOYMENT GUIDE)</h1>

<h2>4.1. Yêu cầu hệ thống (System Requirements)</h2>
<ul>
  <li><strong>Hệ điều hành:</strong> Windows 10/11, Linux (Ubuntu 20.04/22.04 LTS), hoặc macOS 12+</li>
  <li><strong>Môi trường thực thi:</strong> Python 3.11+ (khuyến nghị dùng virtualenv) hoặc Docker & Docker Compose</li>
  <li><strong>Hệ quản trị CSDL:</strong> SQLite 3.35+ (nhúng sẵn, không yêu cầu cài daemon bên ngoài)</li>
  <li><strong>Tài nguyên phần cứng:</strong> RAM tối thiểu 2 GB (khuyến nghị 4 GB), dung lượng đĩa trống &ge; 500 MB</li>
</ul>

<h2>4.2. Các bước thiết lập (&le; 2 lệnh — Chuẩn Đánh giá Giảng viên)</h2>
<p><strong>Cách A: Triển khai bằng Docker Compose (Khuyến nghị cho môi trường máy chủ)</strong></p>
<pre><code>cp .env.example .env
docker compose up -d --build</code></pre>

<p><strong>Cách B: Triển khai trên môi trường Python trực tiếp (&le; 2 lệnh)</strong></p>
<pre><code>pip install -r requirements.txt
python -m src.pipeline --file-nguon data/mau/customers_sample.csv --xuat-bao-cao</code></pre>
<p><em>Hoặc trên Windows: chạy tập tin kịch bản tự động <code>run_clean_test.bat</code>.</em></p>

<h2>4.3. Bảng biến môi trường (Environment Variables)</h2>
<table class="data-table">
  <thead>
    <tr>
      <th style="width: 28%;">Tên biến môi trường</th>
      <th style="width: 22%;">Giá trị mặc định</th>
      <th style="width: 22%;">Giá trị cho phép</th>
      <th>Mô tả nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>APP_ENV</code></td>
      <td><code>production</code></td>
      <td><code>dev</code>, <code>staging</code>, <code>production</code></td>
      <td>Môi trường hoạt động của ứng dụng.</td>
    </tr>
    <tr>
      <td><code>LOG_LEVEL</code></td>
      <td><code>INFO</code></td>
      <td><code>DEBUG</code>, <code>INFO</code>, <code>WARNING</code>, <code>ERROR</code></td>
      <td>Mức độ chi tiết của nhật ký hệ thống.</td>
    </tr>
    <tr>
      <td><code>DATA_DIR</code></td>
      <td><code>data/mau</code></td>
      <td>Đường dẫn thư mục hợp lệ</td>
      <td>Thư mục chứa tệp dữ liệu khách hàng nguồn.</td>
    </tr>
    <tr>
      <td><code>DATABASE_URL</code></td>
      <td><code>sqlite:///data/processed/warehouse.db</code></td>
      <td>URI kết nối SQLite</td>
      <td>Đường dẫn CSDL kho dữ liệu Star Schema.</td>
    </tr>
    <tr>
      <td><code>REPORTS_DIR</code></td>
      <td><code>reports</code></td>
      <td>Đường dẫn thư mục hợp lệ</td>
      <td>Thư mục lưu trữ báo cáo chất lượng sinh tự động.</td>
    </tr>
    <tr>
      <td><code>BLOCK_ON_QUALITY_FAILURE</code></td>
      <td><code>false</code></td>
      <td><code>true</code>, <code>false</code></td>
      <td>Cấu hình chặn nạp kho nếu chất lượng vi phạm ngưỡng.</td>
    </tr>
  </tbody>
</table>

<h2>4.4. Quy cách tập dữ liệu mẫu (Sample Data Specification)</h2>
<p>Tệp dữ liệu mẫu được lưu trữ tại <code>data/mau/customers_sample.csv</code> phục vụ đối soát nhanh:</p>
<ul>
  <li><strong>Dung lượng tập mẫu:</strong> Đúng <strong>300 bản ghi khách hàng</strong>.</li>
  <li><strong>280 bản ghi đạt chuẩn (93,3%):</strong> Số điện thoại 10 số hợp lệ, họ tên chuẩn, ngày sinh hợp lệ &rarr; nạp vào <code>dim_customer</code>.</li>
  <li><strong>20 bản ghi lỗi (6,7%):</strong> Số điện thoại sai chữ số, thiếu định danh &rarr; cách ly vào bảng <code>reject_rows</code>.</li>
</ul>

<h2>4.5. Kiểm tra hoạt động hệ thống (Verify It Works)</h2>
<pre><code># 1. Kiểm tra toàn bộ 20 test case tự động
python -m pytest -v

# 2. Kiểm tra đối soát số dòng trong kho dữ liệu
python -m src.dashboard.so_sanh_dong

# 3. Khởi chạy Dashboard Web Streamlit trực quan
python -m streamlit run streamlit_app.py</code></pre>

<h2>4.6. Triển khai Cloud công khai (Streamlit Community Cloud)</h2>
<p>Hệ thống được đóng gói và triển khai trực tuyến trên hạ tầng Streamlit Cloud, tích hợp tự động với nhánh <code>main</code> của GitHub Repository:</p>
<ul>
  <li><strong>Địa chỉ truy cập công khai:</strong> <a href="https://smartcrm-2374802010030.streamlit.app" target="_blank">https://smartcrm-2374802010030.streamlit.app</a></li>
  <li><strong>Tệp ứng dụng chính (Main file):</strong> <code>streamlit_app.py</code></li>
  <li><strong>Tính năng trực tuyến:</strong> Tự động khởi tạo cấu trúc CSDL SQLite trên Cloud khi chạy lần đầu; cung cấp 4 thẻ KPI chất lượng, biểu đồ phân tích vi phạm DQ, bảng tra cứu bản ghi reject và đối soát kho theo thời gian thực.</li>
</ul>

<!-- MỤC 5: CHECKLIST BẢO MẬT -->
<div class="page-break"></div>
<h1>MỤC 5. BẢNG KIỂM TRA AN TOÀN & BẢO MẬT (CHECKLIST BẢO MẬT)</h1>
<p>Theo quy định đánh giá tiêu chí <strong>C6</strong>, bảng dưới đây kê khai trung thực trạng thái bảo mật của hệ thống luồng L7:</p>

<table class="data-table">
  <thead>
    <tr>
      <th style="width: 6%; text-align: center;">STT</th>
      <th style="width: 32%;">Hạng mục kiểm tra bảo mật</th>
      <th style="width: 18%; text-align: center;">Trạng thái</th>
      <th>Dòng minh chứng cụ thể / Vị trí mã nguồn</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;"><strong>1</strong></td>
      <td><strong>Quản lý bí mật & Biến môi trường</strong></td>
      <td style="text-align: center;"><strong>ĐÃ LÀM</strong></td>
      <td>Bí mật và đường dẫn được cô lập trong <code>.env</code> (đã khai báo trong <code>.gitignore</code>); tệp mẫu an toàn <code>.env.example</code> cung cấp đủ 6 biến.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>2</strong></td>
      <td><strong>Khóa cứng phiên bản thư viện (C6)</strong></td>
      <td style="text-align: center;"><strong>ĐÃ LÀM</strong></td>
      <td>100% thư viện phụ thuộc được khóa phiên bản chính xác bằng toán tử <code>==</code> trong <code>requirements.txt</code>, khắc phục triệt để góp ý BT2.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>3</strong></td>
      <td><strong>Bảo vệ dữ liệu cá nhân PII (NFR05/D4)</strong></td>
      <td style="text-align: center;"><strong>ĐÃ LÀM</strong></td>
      <td>100% SĐT (<code>0901***567</code>) và Email (<code>t***@gmail.com</code>) được che mặt nạ qua hàm thuần <code>rules.py::che_mat_na_pii</code>, tỷ lệ rò rỉ 0,00%.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>4</strong></td>
      <td><strong>Phòng chống tấn công SQL Injection</strong></td>
      <td style="text-align: center;"><strong>ĐÃ LÀM</strong></td>
      <td>100% câu truy vấn và nạp dữ liệu trong <code>src/load/</code> và <code>src/dashboard/</code> đều dùng tham số hóa (<code>?</code>), tuyệt đối không nối chuỗi SQL.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>5</strong></td>
      <td><strong>Phân quyền tối thiểu trong Container</strong></td>
      <td style="text-align: center;"><strong>ĐÃ LÀM</strong></td>
      <td><code>Dockerfile</code> cấu hình chạy toàn bộ tiến trình dưới người dùng không đặc quyền <code>appuser</code> (UID 10001), không dùng tài khoản root.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>6</strong></td>
      <td><strong>Xác thực & Phân quyền truy cập (Auth)</strong></td>
      <td style="text-align: center;"><strong>KHÔNG ÁP DỤNG</strong></td>
      <td>Hệ thống là Batch ETL Pipeline chạy nội bộ/CLI trên máy trạm, không mở cổng mạng Web API công khai.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>7</strong></td>
      <td><strong>Mã hóa đường truyền mạng (TLS/HTTPS)</strong></td>
      <td style="text-align: center;"><strong>KHÔNG ÁP DỤNG</strong></td>
      <td>Quá trình xử lý và nạp dữ liệu diễn ra cục bộ (On-premise) giữa tệp CSV và SQLite, không truyền tải dữ liệu khách hàng qua Internet.</td>
    </tr>
  </tbody>
</table>

<!-- MỤC 6: TÀI LIỆU TRACK DA -->
<div class="page-break"></div>
<h1>MỤC 6. TÀI LIỆU KỸ THUẬT THEO TRACK DATA ANALYTICS</h1>

<h2>6.1. Tài liệu Luồng Xử lý Dữ liệu (Pipeline Documentation — Đủ 6 Mục Chuẩn)</h2>

<h3>1. High-Level Architecture Overview (Tổng quan kiến trúc)</h3>
<p>Hệ thống vận hành theo chu trình ETL 4 pha khép kín: <strong>Extract &rarr; Transform &rarr; Quality &rarr; Load</strong>. Bản ghi sau khi kiểm định được phân luồng tự động: các bản ghi sạch được nạp vào mô hình Star Schema (<code>dim_customer</code>, <code>fact_customer_quality_audit</code>), trong khi các bản ghi khuyết tật được cách ly vào bảng <code>reject_rows</code> kèm thông điệp lỗi rõ ràng.</p>

<h3>2. Data Source & Ingestion (Nguồn dữ liệu và Nạp dữ liệu)</h3>
<p>Dữ liệu nguồn gồm tệp CSV giao dịch khách hàng <code>customers_raw.csv</code> (67.037 dòng) chứa các trường: <code>record_id</code>, <code>ho_ten</code>, <code>so_dien_thoai</code>, <code>email</code>, <code>ngay_sinh</code>, <code>dia_chi</code>, <code>ngay_tao</code>. Module trích xuất đọc toàn bộ dưới dạng chuỗi (<code>dtype=str</code>) để tránh mất số 0 đầu số điện thoại.</p>

<h3>3. Data Transformation & Cleansing Rules (Quy tắc làm sạch & Chuẩn hóa)</h3>
<ul>
  <li><em>Số điện thoại (DQ02):</em> Xử lý mã quốc tế <code>+84</code>, <code>84</code>, loại bỏ khoảng trắng và dấu chấm, quy đổi về 10 chữ số chuẩn bắt đầu bằng số 0.</li>
  <li><em>Họ tên (DQ01):</em> Xóa khoảng trắng thừa ở hai đầu và giữa các từ, chuyển đổi toàn bộ về định dạng Title Case chuẩn tiếng Việt.</li>
  <li><em>Email & Ngày tháng:</em> Kiểm tra cú pháp RFC email; chuẩn hóa ngày sinh và ngày tạo về chuẩn ISO-8601 (<code>YYYY-MM-DD</code>).</li>
</ul>

<h3>4. Multidimensional Quality Measurement (Bảng đo lường 3 chiều chất lượng)</h3>
<table class="data-table">
  <thead>
    <tr>
      <th>Chiều chất lượng</th>
      <th>Mã quy tắc</th>
      <th>Mô tả kiểm tra</th>
      <th style="text-align: center;">Số lượng kiểm</th>
      <th style="text-align: center;">Số lượng đạt</th>
      <th style="text-align: center;">Tỷ lệ đạt (%)</th>
      <th style="text-align: center;">Ngưỡng YAML</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="3"><strong>Đầy đủ (Completeness)</strong></td>
      <td><code>DQ01_ID</code></td>
      <td>Không rỗng mã khách hàng</td>
      <td style="text-align: center;">67.037</td>
      <td style="text-align: center;">67.037</td>
      <td style="text-align: center;">100,00%</td>
      <td style="text-align: center;">&ge; 100%</td>
    </tr>
    <tr>
      <td><code>DQ01_NAME</code></td>
      <td>Không rỗng họ tên</td>
      <td style="text-align: center;">67.037</td>
      <td style="text-align: center;">66.820</td>
      <td style="text-align: center;">99,68%</td>
      <td style="text-align: center;">&ge; 98%</td>
    </tr>
    <tr>
      <td><code>DQ01_PHONE</code></td>
      <td>Không rỗng số điện thoại</td>
      <td style="text-align: center;">67.037</td>
      <td style="text-align: center;">64.212</td>
      <td style="text-align: center;">95,79%</td>
      <td style="text-align: center;">&ge; 95%</td>
    </tr>
    <tr>
      <td rowspan="4"><strong>Chính xác (Accuracy)</strong></td>
      <td><code>DQ02_PHONE</code></td>
      <td>Định dạng SĐT 10 chữ số</td>
      <td style="text-align: center;">67.037</td>
      <td style="text-align: center;">62.904</td>
      <td style="text-align: center;">93,83%</td>
      <td style="text-align: center;">&ge; 90%</td>
    </tr>
    <tr>
      <td><code>DQ03_EMAIL</code></td>
      <td>Định dạng email hợp lệ RFC</td>
      <td style="text-align: center;">67.037</td>
      <td style="text-align: center;">61.428</td>
      <td style="text-align: center;">91,63%</td>
      <td style="text-align: center;">&ge; 85%</td>
    </tr>
    <tr>
      <td><code>DQ04_DOB</code></td>
      <td>Ngày sinh hợp lệ</td>
      <td style="text-align: center;">67.037</td>
      <td style="text-align: center;">66.910</td>
      <td style="text-align: center;">99,81%</td>
      <td style="text-align: center;">&ge; 95%</td>
    </tr>
    <tr>
      <td><code>DQ05_REG</code></td>
      <td>Ngày tạo không ở tương lai</td>
      <td style="text-align: center;">67.037</td>
      <td style="text-align: center;">67.037</td>
      <td style="text-align: center;">100,00%</td>
      <td style="text-align: center;">&ge; 99%</td>
    </tr>
    <tr>
      <td rowspan="2"><strong>Nhất quán (Consistency)</strong></td>
      <td><code>DQ06_UNIQ</code></td>
      <td>Tỷ lệ trùng lặp khách hàng</td>
      <td style="text-align: center;">62.904</td>
      <td style="text-align: center;">35.781 (duy nhất)</td>
      <td style="text-align: center;">43,10% (trùng)</td>
      <td style="text-align: center;">&le; 70%</td>
    </tr>
    <tr>
      <td><code>DQ07_PII</code></td>
      <td>Tỷ lệ che mặt nạ PII</td>
      <td style="text-align: center;">62.904</td>
      <td style="text-align: center;">62.904</td>
      <td style="text-align: center;">100,00%</td>
      <td style="text-align: center;">= 100%</td>
    </tr>
  </tbody>
</table>

<h3>5. Storage Strategy & Reject Breakdown (Chiến lược lưu trữ & Phân bổ Reject)</h3>
<p>Số dòng bị từ chối được lưu trữ toàn vẹn tại <code>reject_rows</code> gồm đúng <strong>4.133 dòng</strong>, phân loại theo lý do:</p>
<ul>
  <li><code>SĐT không hợp lệ hoặc thiếu ký số (DQ02_PHONE)</code>: <strong>3.352 dòng</strong> (81,1%)</li>
  <li><code>Thiếu số điện thoại bắt buộc (DQ01_PHONE)</code>: <strong>564 dòng</strong> (13,6%)</li>
  <li><code>Thiếu họ tên khách hàng (DQ01_NAME)</code>: <strong>217 dòng</strong> (5,3%)</li>
</ul>
<p>Tổng cộng: $3.352 + 564 + 217 = 4.133$ dòng. Số liệu đối chiếu khớp tuyệt đối với số dòng trong báo cáo lần chạy gần nhất.</p>

<h3>6. Technical Limitations & Business Impact (Hạn chế kỹ thuật & Ảnh hưởng nghiệp vụ)</h3>
<ol>
  <li><strong>Hạn chế 1 — Cơ chế phân cụm trùng lặp dựa trên khóa chính xác (Exact Match):</strong> Hệ thống hiện tại phát hiện trùng lặp dựa trên việc trùng số điện thoại hoặc email. <em>Ảnh hưởng nghiệp vụ:</em> Nếu khách hàng đổi số điện thoại nhưng giữ nguyên họ tên và địa chỉ, hệ thống sẽ coi là 2 khách hàng riêng biệt, dẫn đến việc phòng Marketing có thể gửi ưu đãi trùng cho cùng một người.</li>
  <li><strong>Hạn chế 2 — Khóa cơ sở dữ liệu khi chạy đồng thời trong SQLite:</strong> SQLite sử dụng cơ chế file-level locking. <em>Ảnh hưởng nghiệp vụ:</em> Khi pipeline đang thực hiện nạp dữ liệu lô lớn, người dùng truy cập dashboard tra cứu có thể gặp độ trễ nhẹ do chờ giải phóng khóa đọc/ghi.</li>
  <li><strong>Hạn chế 3 — Cách ly thụ động dòng reject mà chưa có giao diện sửa lỗi tức thời:</strong> Các dòng lỗi được cách ly vào <code>reject_rows</code> kèm thông điệp rõ ràng nhưng đòi hỏi đối soát viên phải rà soát qua tệp hoặc truy vấn SQL. <em>Ảnh hưởng nghiệp vụ:</em> Cần thêm 1 bước xuất danh sách lỗi cho nhân viên chăm sóc khách hàng liên hệ bổ sung số điện thoại.</li>
</ol>

<div class="page-break"></div>
<h2>6.2. Từ điển Dữ liệu (Data Dictionary — Đủ 7 Bảng CSDL Star Schema & PII D4)</h2>
<p>Toàn bộ 7 bảng dưới đây được đối chiếu khớp 100% với tập tin DDL tại <code>sql/</code> và lược đồ thực tế trong SQLite:</p>

<table class="data-table">
  <thead>
    <tr>
      <th style="width: 25%;">Tên bảng</th>
      <th style="width: 20%;">Phân tầng kiến trúc</th>
      <th style="width: 18%;">Khóa chính (PK)</th>
      <th>Mô tả chức năng nghiệp vụ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>staging_customers</code></td>
      <td>Staging Layer</td>
      <td><code>id</code> (INTEGER)</td>
      <td>Lưu trữ dữ liệu thô nguyên trạng trích xuất từ tệp CSV nguồn.</td>
    </tr>
    <tr>
      <td><code>reject_rows</code></td>
      <td>Audit / Error Layer</td>
      <td><code>reject_id</code> (INTEGER)</td>
      <td>Cách ly các bản ghi không thể làm sạch kèm lý do cụ thể cho đối soát.</td>
    </tr>
    <tr>
      <td><code>quality_measures</code></td>
      <td>Measures Layer</td>
      <td><code>measure_id</code> (INTEGER)</td>
      <td>Lưu trữ kết quả đo lường định lượng 9 chỉ tiêu chất lượng của từng lô chạy.</td>
    </tr>
    <tr>
      <td><code>dim_customer</code></td>
      <td>Dimension Table</td>
      <td><code>customer_key</code> (INTEGER)</td>
      <td>Bảng chiều lưu thông tin khách hàng đã được chuẩn hóa và làm sạch.</td>
    </tr>
    <tr>
      <td><code>dim_quality_rule</code></td>
      <td>Dimension Table</td>
      <td><code>rule_key</code> (INTEGER)</td>
      <td>Bảng chiều tra cứu danh mục quy tắc chất lượng và ngưỡng chuẩn.</td>
    </tr>
    <tr>
      <td><code>dim_audit_run</code></td>
      <td>Dimension Table</td>
      <td><code>run_key</code> (INTEGER)</td>
      <td>Bảng chiều ghi nhận các phiên chạy pipeline, thời gian và số lượng dòng.</td>
    </tr>
    <tr>
      <td><code>fact_customer_quality_audit</code></td>
      <td>Fact Table</td>
      <td><code>audit_fact_id</code> (INTEGER)</td>
      <td>Bảng Fact ghi nhận sự kiện kiểm định chất lượng của từng khách hàng sạch.</td>
    </tr>
  </tbody>
</table>

<h3>Cấu trúc chi tiết các bảng trọng tâm và Tiêu chuẩn Giả danh hóa PII (D4)</h3>
<p><strong>Bảng <code>dim_customer</code> (DDL: <code>sql/010_dim.sql</code>):</strong></p>
<table class="data-table">
  <thead>
    <tr>
      <th style="width: 20%;">Tên cột</th>
      <th style="width: 15%;">Kiểu dữ liệu</th>
      <th style="width: 10%; text-align: center;">Nullable</th>
      <th>Mô tả nghiệp vụ & Quy chuẩn Giả danh hóa PII (D4)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>customer_key</code></td>
      <td>INTEGER</td>
      <td style="text-align: center;">No</td>
      <td>Khóa thay thế (Surrogate Key) tự tăng của kho dữ liệu.</td>
    </tr>
    <tr>
      <td><code>customer_id</code></td>
      <td>VARCHAR(50)</td>
      <td style="text-align: center;">No</td>
      <td>Khóa nghiệp vụ tự nhiên (Natural Business Key) dùng cho UPSERT.</td>
    </tr>
    <tr>
      <td><code>ho_ten</code></td>
      <td>VARCHAR(255)</td>
      <td style="text-align: center;">Yes</td>
      <td>Họ tên khách hàng đã chuẩn hóa Title Case.</td>
    </tr>
    <tr>
      <td><code>so_dien_thoai</code></td>
      <td>VARCHAR(20)</td>
      <td style="text-align: center;">Yes</td>
      <td>Số điện thoại đã chuẩn hóa 10 số (Dạng thô lưu kho an toàn).</td>
    </tr>
    <tr>
      <td><code>sdt_masked</code></td>
      <td>VARCHAR(20)</td>
      <td style="text-align: center;">Yes</td>
      <td><strong>Cột giả danh hóa PII (D4):</strong> Che mặt nạ định dạng <code>0901***567</code> hiển thị báo cáo.</td>
    </tr>
    <tr>
      <td><code>email</code></td>
      <td>VARCHAR(255)</td>
      <td style="text-align: center;">Yes</td>
      <td>Địa chỉ email đã chuẩn hóa viết thường (Lưu kho).</td>
    </tr>
    <tr>
      <td><code>email_masked</code></td>
      <td>VARCHAR(255)</td>
      <td style="text-align: center;">Yes</td>
      <td><strong>Cột giả danh hóa PII (D4):</strong> Che mặt nạ định dạng <code>t***@gmail.com</code>.</td>
    </tr>
    <tr>
      <td><code>ngay_sinh</code></td>
      <td>DATE</td>
      <td style="text-align: center;">Yes</td>
      <td>Ngày sinh chuẩn hóa ISO-8601 (YYYY-MM-DD).</td>
    </tr>
    <tr>
      <td><code>ngay_tao</code></td>
      <td>DATE</td>
      <td style="text-align: center;">Yes</td>
      <td>Ngày đăng ký khách hàng chuẩn hóa ISO-8601.</td>
    </tr>
    <tr>
      <td><code>is_duplicate</code></td>
      <td>INTEGER</td>
      <td style="text-align: center;">No</td>
      <td>Cờ đánh dấu khách hàng có nghi ngờ trùng lặp (1: Trùng, 0: Duy nhất).</td>
    </tr>
  </tbody>
</table>

<!-- MỤC 7: ẢNH CHỤP MINH CHỨNG -->
<div class="page-break"></div>
<h1>MỤC 7. ẢNH CHỤP KẾT QUẢ CHẠY THẬT (MINH CHỨNG THỰC NGHIỆM)</h1>
<p>Toàn bộ 3 ảnh dưới đây là kết quả thực thi thật 100% trên môi trường máy trạm của sinh viên, không che giấu lỗi, che dữ liệu nhạy cảm theo quy định bảo mật NFR05:</p>

<div class="screenshot-container">
  <img src="{anh1_b64}" alt="Minh chứng 1: Kết quả kiểm thử tự động 20/20 test PASS">
  <div class="caption">Hình 7.1. Kết quả thực thi bộ kiểm thử tự động 20/20 test case PASSED bằng lệnh python -m pytest -v</div>
</div>

<div class="screenshot-container">
  <img src="{anh2_b64}" alt="Minh chứng 2: Phép thử máy trắng và đối soát kho dữ liệu">
  <div class="caption">Hình 7.2. Kết quả phép thử máy trắng tự động (run_clean_test.bat): thực thi 4 pha ETL và đối soát dòng trong kho Star Schema</div>
</div>

<div class="page-break"></div>
<div class="screenshot-container">
  <img src="{anh3_b64}" alt="Minh chứng 3: Dashboard Giám sát Chất lượng Dữ liệu Streamlit">
  <div class="caption">Hình 7.3. Giao diện Web Dashboard SmartCRM Analytics thực tế: 4 thẻ KPI chất lượng, biểu đồ phân tích vi phạm DQ và tỷ lệ trùng lặp khách hàng</div>
</div>

<!-- PHỤ LỤC: KHAI BÁO AI -->
<div class="page-break"></div>
<h1>PHỤ LỤC. BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ TRÍ TUỆ NHÂN TẠO (AI)</h1>
<p>Khai báo trung thực theo quy định đánh giá học phần Chuyên đề Tốt nghiệp 1 (Đủ 4 cột chuẩn):</p>

<table class="data-table">
  <thead>
    <tr>
      <th style="width: 18%;">Công cụ AI</th>
      <th style="width: 25%;">Dùng vào việc gì</th>
      <th style="width: 25%;">Áp dụng ở phần nào</th>
      <th>Tự thẩm định & Chịu trách nhiệm</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Antigravity AI / Gemini</strong></td>
      <td>Hỗ trợ cấu trúc tài liệu kỹ thuật tiếng Anh (Pipeline documentation & Data dictionary) chuẩn hóa theo Markdown.</td>
      <td><code>docs/pipeline-doc.md</code>, <code>docs/data-dictionary.md</code>, <code>DEPLOYMENT.md</code>.</td>
      <td>Tự đối chiếu từng bảng, từng cột với tệp DDL thật trong thư mục <code>sql/</code> và lệnh SQLite; chỉnh sửa các thông số số liệu khớp 100% với kết quả chạy trên 67.037 bản ghi nguồn.</td>
    </tr>
    <tr>
      <td><strong>Antigravity AI / Gemini</strong></td>
      <td>Hỗ trợ cú pháp cấu hình <code>Dockerfile</code> nhiều lớp tối ưu hóa cache và cú pháp <code>docker-compose.yml</code> có healthcheck.</td>
      <td><code>Dockerfile</code>, <code>docker-compose.yml</code>.</td>
      <td>Tự chạy thử nghiệm kiểm tra tính hợp lệ bằng các script chạy máy trắng (<code>scripts/run_clean_test.py</code>, <code>run_clean_test.bat</code>) trên dữ liệu mẫu 300 dòng; kiểm tra trạng thái thoát mã 0.</td>
    </tr>
    <tr>
      <td><strong>— Không sử dụng AI —</strong><br><em>(Sinh viên tự làm)</em></td>
      <td>Viết và thực thi toàn bộ mã nguồn xử lý ETL (<code>src/extract/</code>, <code>src/transform/</code>, <code>src/quality/</code>, <code>src/load/</code>, <code>src/dashboard/</code>).</td>
      <td>Toàn bộ mã nguồn cốt lõi trong thư mục <code>src/</code>.</td>
      <td>Tự chạy kiểm thử với 20/20 test case đạt <code>PASSED</code> qua Pytest (<code>python -m pytest -v</code>), nạp 62.904 khách hàng sạch và cách ly 4.133 dòng lỗi.</td>
    </tr>
    <tr>
      <td><strong>— Không sử dụng AI —</strong><br><em>(Sinh viên tự làm)</em></td>
      <td>Thực nghiệm phép thử nạp lại được (Idempotent test) và đối soát dữ liệu kho Star Schema.</td>
      <td><code>tests/test_hoi_quy.py</code>, <code>src/dashboard/so_sanh_dong.py</code>.</td>
      <td>Tự chạy lặp lại 3 lần trên cùng tập dữ liệu nguồn, truy vấn CSDL SQLite xác nhận số lượng bản ghi không hề bị nhân đôi và bảo toàn dữ liệu tuyệt đối.</td>
    </tr>
  </tbody>
</table>

<div class="callout" style="margin-top: 25px;">
  <p><strong>CAM KẾT LIÊM CHÍNH HỌC THUẬT:</strong></p>
  <p><em>"Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp trong báo cáo Bài tập 3 này."</em></p>
  <p style="margin-top: 15px;">
    <strong>Sinh viên thực hiện:</strong> Hồ Lê Trung Bảo<br>
    <strong>Mã số sinh viên:</strong> 2374802010030<br>
    <strong>Ngày cam kết:</strong> 14/11/2026
  </p>
</div>

</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Da tao tep HTML tam tai: {HTML_FILE}")

# Chuyen HTML sang PDF bang Microsoft Edge Headless
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={OUTPUT_PDF}",
    HTML_FILE
]

print("Dang xuat PDF bang Microsoft Edge Headless...")
result = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(OUTPUT_PDF) and os.path.getsize(OUTPUT_PDF) > 0:
    print(f"[THANH CONG] Da xuat file PDF thanh cong tai: {OUTPUT_PDF}")
    print(f"Kich thuoc file: {os.path.getsize(OUTPUT_PDF)} bytes")
else:
    print(f"[LOI] Khong the xuat PDF! Chi tiet: {result.stderr}")

# Xoa file tam
if os.path.exists(HTML_FILE):
    os.remove(HTML_FILE)
