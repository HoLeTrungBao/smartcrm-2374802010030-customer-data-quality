# -*- coding: utf-8 -*-
"""
Script chuẩn hóa toàn bộ định dạng báo cáo Bài tập 3 theo Quy định của
Khoa Công nghệ Thông tin – Trường Đại học Văn Lang.

Quy định chuẩn:
- Font chữ: Times New Roman 100% toàn báo cáo
- Cỡ chữ nội dung: 13 pt
- Giãn dòng: 1.5 lines
- Căn lề: Trái 3 cm, Phải 2 cm, Trên 2 cm, Dưới 2 cm
- Căn đều 2 bên (Justify)
- Tiêu đề mục chính: IN HOA, in đậm, tối đa 3 cấp số Ả Rập
- Tiêu đề bảng ĐẶT PHÍA TRÊN, Chú thích hình ĐẶT PHÍA DƯỚI
- Đánh số trang: Chính giữa phía trên đầu trang (@top-center), trang 1 bắt đầu từ nội dung chính (bìa không đánh số)
- Trang bìa chuẩn luận văn ĐH Văn Lang có khung viền hoa văn (border_highres.png) giống bìa BT1
"""

import os
import subprocess
import base64
import io
import pypdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

ROOT_DIR = r"C:\Users\ASUS\smartcrm-2374802010030-customer-data-quality"
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
FINAL_PDF = os.path.join(ROOT_DIR, "BT3_2374802010030_HoLeTrungBao.pdf")
TEMP_PDF = os.path.join(ROOT_DIR, "bao_cao_chua_danh_so.pdf")
TEMP_HTML = os.path.join(ROOT_DIR, "bao_cao_chuan_hoa_tam.html")

def to_base64(image_path):
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    return f"data:{mime};base64,{data}"

border_b64 = to_base64(os.path.join(DOCS_DIR, "border_highres.png"))
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
    margin-top: 20mm;
    margin-bottom: 20mm;
    margin-left: 30mm;
    margin-right: 20mm;
  }}
  @page :first {{
    margin: 0;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 13pt;
    line-height: 1.5;
    color: #000000;
    margin: 0;
    padding: 0;
    text-align: justify;
    letter-spacing: normal;
  }}

  /* PHÂN TRANG */
  .page-break {{
    page-break-before: always;
  }}
  .avoid-break {{
    page-break-inside: avoid;
  }}

  /* TRANG BÌA CHUẨN ĐẠI HỌC VĂN LANG (GIỐNG BÌA BT1) */
  .cover-container {{
    position: relative;
    width: 210mm;
    height: 297mm;
    margin: 0 auto;
    padding: 22mm 24mm 20mm 24mm;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    page-break-after: always;
    overflow: hidden;
  }}
  .cover-border-img {{
    position: absolute;
    top: 6mm;
    left: 8mm;
    width: 194mm;
    height: 283mm;
    z-index: 1;
    pointer-events: none;
  }}
  .cover-inner {{
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 8mm 6mm;
  }}
  .cover-header-univ {{
    font-size: 13pt;
    font-weight: bold;
    color: #8B0000;
    text-transform: uppercase;
    line-height: 1.3;
    margin-bottom: 2px;
  }}
  .cover-header-faculty {{
    font-size: 12pt;
    font-weight: bold;
    color: #1A202C;
    text-transform: uppercase;
    line-height: 1.3;
  }}
  .cover-line {{
    width: 45%;
    height: 1.5px;
    background-color: #8B0000;
    margin: 8px auto 16px auto;
  }}
  .cover-logo-box {{
    margin: 12px 0 16px 0;
  }}
  .cover-logo {{
    max-height: 75px;
    width: auto;
  }}
  .cover-main-title {{
    font-size: 18pt;
    font-weight: bold;
    color: #8B0000;
    text-transform: uppercase;
    line-height: 1.35;
    margin-bottom: 6px;
  }}
  .cover-sub-title {{
    font-size: 13.5pt;
    font-weight: bold;
    color: #1A202C;
    text-transform: uppercase;
    line-height: 1.35;
    margin-bottom: 12px;
  }}
  .cover-course-title {{
    font-size: 12pt;
    font-weight: bold;
    color: #2D3748;
    line-height: 1.4;
  }}
  .cover-info-card {{
    width: 92%;
    margin: 18px auto 0 auto;
    border: 1px solid #718096;
    border-radius: 4px;
    padding: 12px 18px;
    background-color: #FFFFFF;
    text-align: left;
    font-size: 11pt;
    line-height: 1.45;
  }}
  .cover-info-card table {{
    width: 100%;
    border-collapse: collapse;
  }}
  .cover-info-card td {{
    padding: 3px 6px;
    vertical-align: top;
  }}
  .cover-info-card td.lbl {{
    font-weight: bold;
    color: #1A202C;
    width: 32%;
    white-space: nowrap;
  }}
  .cover-info-card td.val {{
    color: #000000;
  }}
  .cover-info-card td.val a {{
    color: #1A365D;
    text-decoration: underline;
    font-weight: bold;
    word-break: break-all;
  }}
  .cover-footer-text {{
    font-size: 11pt;
    font-weight: bold;
    color: #1A202C;
    text-transform: uppercase;
    margin-top: 15px;
  }}

  /* TIÊU ĐỀ THEO ĐÚNG QUY ĐỊNH KHOA CNTT */
  h1 {{
    font-size: 14pt;
    font-weight: bold;
    text-transform: uppercase;
    color: #000000;
    margin-top: 24pt;
    margin-bottom: 12pt;
    line-height: 1.4;
    page-break-after: avoid;
  }}
  h2 {{
    font-size: 13pt;
    font-weight: bold;
    color: #000000;
    margin-top: 16pt;
    margin-bottom: 8pt;
    line-height: 1.4;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 13pt;
    font-weight: bold;
    color: #000000;
    margin-top: 12pt;
    margin-bottom: 6pt;
    line-height: 1.4;
    page-break-after: avoid;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 8pt;
    text-indent: 0;
  }}
  ul, ol {{
    margin-top: 0;
    margin-bottom: 8pt;
    padding-left: 24pt;
  }}
  li {{
    margin-bottom: 4pt;
  }}

  /* BẢNG BIỂU CHUẨN HÓA */
  .table-title {{
    font-size: 11pt;
    font-weight: bold;
    color: #000000;
    margin-top: 12pt;
    margin-bottom: 4pt;
    text-align: left;
    page-break-after: avoid;
  }}
  table.content-table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 12pt;
    font-size: 10.5pt;
    line-height: 1.35;
    page-break-inside: auto;
  }}
  table.content-table th, table.content-table td {{
    border: 1px solid #4A5568;
    padding: 5pt 7pt;
    vertical-align: top;
  }}
  table.content-table th {{
    background-color: #EDF2F7;
    font-weight: bold;
    color: #000000;
    text-align: center;
  }}
  table.content-table tr:nth-child(even) {{
    background-color: #F8FAFC;
  }}

  /* HÌNH ẢNH VÀ CHÚ THÍCH */
  .image-wrapper {{
    text-align: center;
    margin-top: 12pt;
    margin-bottom: 14pt;
    page-break-inside: avoid;
  }}
  .image-wrapper img {{
    max-width: 100%;
    height: auto;
    border: 1px solid #CBD5E0;
    border-radius: 3px;
  }}
  .figure-caption {{
    font-size: 11pt;
    font-style: italic;
    color: #000000;
    margin-top: 6pt;
    text-align: center;
    page-break-before: avoid;
  }}

  /* ĐOẠN MÃ NGUỒN VÀ DÒNG LỆNH */
  pre {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 10pt;
    line-height: 1.35;
    background-color: #F7FAFC;
    border: 1px solid #CBD5E0;
    border-left: 3pt solid #1A365D;
    padding: 6pt 10pt;
    margin-top: 4pt;
    margin-bottom: 8pt;
    white-space: pre-wrap;
    word-break: break-all;
  }}
  code {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 11pt;
  }}

  /* HUY HIỆU PASS */
  .tag-pass {{
    font-weight: bold;
    color: #22543D;
  }}
</style>
</head>
<body>

<!-- TRANG BÌA THEO CHUẨN ĐẠI HỌC VĂN LANG (BÌA BT1) -->
<div class="cover-container">
  <img src="{border_b64}" class="cover-border-img" alt="Border">
  <div class="cover-inner">
    <div>
      <div class="cover-header-univ">TRƯỜNG ĐẠI HỌC VĂN LANG</div>
      <div class="cover-header-faculty">KHOA CÔNG NGHỆ THÔNG TIN</div>
      <div class="cover-line"></div>
    </div>

    <div>
      <div class="cover-logo-box">
        <img src="{logo_b64}" class="cover-logo" alt="Logo Van Lang">
      </div>
      <div class="cover-main-title">BÁO CÁO BÀI TẬP 3</div>
      <div class="cover-sub-title">KIỂM THỬ, ĐÓNG GÓI VÀ TÀI LIỆU HÓA HỆ THỐNG</div>
      <div class="cover-course-title">
        HỌC PHẦN: CHUYÊN ĐỀ TỐT NGHIỆP 1 (71ITGR40203)<br>
        HỌC KỲ 1, NĂM HỌC 2026 – 2027
      </div>
    </div>

    <div class="cover-info-card">
      <table>
        <tr>
          <td class="lbl">Chuyên ngành (Track):</td>
          <td class="val"><strong>Data Analytics (DA)</strong></td>
        </tr>
        <tr>
          <td class="lbl">Mã luồng nghiệp vụ:</td>
          <td class="val"><strong>L7 – Customer Data Quality (Kiểm tra & Làm sạch dữ liệu khách hàng)</strong></td>
        </tr>
        <tr>
          <td class="lbl">Giảng viên hướng dẫn:</td>
          <td class="val">ThS. Nguyễn Minh Tân</td>
        </tr>
        <tr>
          <td class="lbl">Sinh viên thực hiện:</td>
          <td class="val"><strong>Hồ Lê Trung Bảo</strong></td>
        </tr>
        <tr>
          <td class="lbl">Mã số sinh viên (MSSV):</td>
          <td class="val"><strong>2374802010030</strong></td>
        </tr>
        <tr>
          <td class="lbl">Lớp học phần:</td>
          <td class="val">71ITGR40203_01 (Khóa K23T)</td>
        </tr>
        <tr>
          <td class="lbl">GitHub Repository:</td>
          <td class="val"><a href="https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality" target="_blank">HoLeTrungBao/smartcrm-2374802010030-customer-data-quality</a></td>
        </tr>
        <tr>
          <td class="lbl">Thẻ phát hành (Release):</td>
          <td class="val"><a href="https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality/releases/tag/v1.0" target="_blank">v1.0 (Phiên bản chính thức Bài tập 3)</a></td>
        </tr>
        <tr>
          <td class="lbl">Link Web Deploy Cloud:</td>
          <td class="val"><a href="https://smartcrm-2374802010030.streamlit.app" target="_blank">https://smartcrm-2374802010030.streamlit.app</a></td>
        </tr>
      </table>
    </div>

    <div class="cover-footer-text">
      TP. HỒ CHÍ MINH, THÁNG 11/2026
    </div>
  </div>
</div>

<!-- NỘI DUNG CHÍNH (BẮT ĐẦU TỪ TRANG 1) -->
<div class="page-break"></div>

<h1>MỤC 1. KẾ HOẠCH KIỂM THỬ (TEST PLAN)</h1>

<h2>1.1. Phạm vi kiểm thử và phần chủ ý không kiểm</h2>

<h3>1.1.1. Phạm vi được kiểm thử toàn diện</h3>
<p>Hệ thống pipeline luồng L7 được kiểm thử toàn diện trên tất cả các pha xử lý dữ liệu và cấu phần kho dữ liệu:</p>
<ul>
  <li><strong>Pha 1 (Extract):</strong> Đọc dữ liệu thô nguyên trạng dạng chuỗi (<code>dtype=str</code>) từ tệp CSV nguồn nhằm bảo toàn tuyệt đối số 0 ở đầu các số điện thoại và giữ nguyên các định dạng ngày tháng thực tế.</li>
  <li><strong>Pha 2 (Transform):</strong> Làm sạch và chuẩn hóa dữ liệu khách hàng bao gồm: chuẩn hóa số điện thoại về 10 chữ số chuẩn (xử lý mã quốc tế <code>+84</code>, <code>84</code>, khoảng trắng và dấu chấm); chuẩn hóa họ tên về Title Case chuẩn tiếng Việt; chuẩn hóa email theo RFC; chuẩn hóa ngày sinh và ngày tạo theo ISO-8601; phân luồng rõ ràng dòng hợp lệ và dòng lỗi.</li>
  <li><strong>Pha 3 (Quality):</strong> Đo lường định lượng 9 chỉ tiêu thuộc 3 chiều chất lượng dữ liệu cốt lõi (Đầy đủ, Chính xác, Nhất quán/Trùng lặp) và đối chiếu với ngưỡng quy chuẩn cấu hình.</li>
  <li><strong>Pha 4 (Load):</strong> Nạp dữ liệu vào mô hình kho Star Schema SQLite: nạp dòng sạch vào <code>dim_customer</code> bằng khóa tự nhiên <code>customer_id</code> (UPSERT), nạp sự kiện kiểm định vào <code>fact_customer_quality_audit</code>; cách ly toàn bộ dòng lỗi vào bảng <code>reject_rows</code> kèm thông điệp lỗi chi tiết.</li>
  <li><strong>Tính Nạp lại được (Idempotency):</strong> Đảm bảo chạy lại pipeline nhiều lần trên cùng tập dữ liệu không gây ra lỗi khóa ngoại và không làm nhân đôi số dòng trong kho dữ liệu.</li>
  <li><strong>Bảo vệ dữ liệu cá nhân PII (NFR05 / D4):</strong> Che mặt nạ 100% số điện thoại và email hiển thị trên báo cáo và tầng trực quan hóa.</li>
  <li><strong>Kiểm thử hồi quy (Regression Testing):</strong> Đảm bảo 3 lỗi đã ghi nhận trong quá trình phát triển (BUG-01, BUG-02, BUG-03) không bị tái phát.</li>
</ul>

<h3>1.1.2. Phạm vi chủ ý không kiểm thử</h3>
<ul>
  <li><em>Giao diện kéo thả người dùng cuối:</em> Phạm vi của Track Data Analytics tập trung vào tính đúng đắn của đường ống ETL backend và tính toàn vẹn của kho dữ liệu Star Schema.</li>
  <li><em>Kiểm thử chịu tải ngoài 100.000 bản ghi:</em> Tập dữ liệu thực tế của chuỗi bán lẻ Mekong Mobile hiện tại là 67.037 bản ghi; phạm vi kiểm thử dữ liệu lớn phân tán thuộc học phần Chuyên đề Tốt nghiệp 2.</li>
</ul>

<h2>1.2. Chiến lược và số lượng ca kiểm thử</h2>
<div class="table-title">Bảng 1.1: Danh mục các tầng kiểm thử và số lượng ca kiểm thử</div>
<table class="content-table">
  <thead>
    <tr>
      <th style="width: 28%;">Tầng kiểm thử</th>
      <th style="width: 14%;">Số lượng ca</th>
      <th style="width: 26%;">Tệp mã nguồn</th>
      <th>Mục đích kiểm thử</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Hàm chuẩn hóa (Unit Test)</strong></td>
      <td style="text-align: center;">9</td>
      <td><code>tests/test_rules.py</code></td>
      <td>Kiểm tra các hàm thuần túy: chuẩn hóa SĐT, họ tên, email, ngày, che PII.</td>
    </tr>
    <tr>
      <td><strong>Đo lường & Phân luồng</strong></td>
      <td style="text-align: center;">2</td>
      <td><code>tests/test_checks.py</code></td>
      <td>Kiểm tra đo 3 chiều chất lượng và cơ chế phân luồng dòng sạch vs reject.</td>
    </tr>
    <tr>
      <td><strong>Dashboard & Đối soát</strong></td>
      <td style="text-align: center;">6</td>
      <td><code>tests/test_dashboard.py</code></td>
      <td>Kiểm tra đối soát số dòng, biểu đồ phân tích và xử lý trạng thái rỗng.</td>
    </tr>
    <tr>
      <td><strong>Kiểm thử hồi quy</strong></td>
      <td style="text-align: center;">3</td>
      <td><code>tests/test_hoi_quy.py</code></td>
      <td>Kiểm tra chống tái phát BUG-01 (Idempotent), BUG-02 (cột), BUG-03 (SQL).</td>
    </tr>
    <tr>
      <td><strong>Kiểm thử tích hợp End-to-End</strong></td>
      <td style="text-align: center;">12</td>
      <td><code>docs/test-report.md</code></td>
      <td>Thực thi toàn bộ luồng từ CSV thô đến kho SQLite và sinh báo cáo.</td>
    </tr>
  </tbody>
</table>
<p>Tổng cộng hệ thống sở hữu <strong>20 ca kiểm thử tự động</strong> thực thi qua Pytest (100% PASS) và <strong>12 ca kiểm thử thực nghiệm</strong> có minh chứng cụ thể.</p>

<h2>1.3. Tiêu chí thành công đo được</h2>
<ol>
  <li><strong>100% test case tự động PASS:</strong> Toàn bộ 20 ca kiểm thử vượt qua thành công với 1 lệnh duy nhất <code>python -m pytest -v</code> trong thời gian dưới 2 giây.</li>
  <li><strong>Tính nạp lại được tuyệt đối:</strong> Chạy lặp lại pipeline nhiều lần trên cùng dữ liệu đầu vào, số dòng tại cả 4 bảng đích giữ nguyên tuyệt đối: <code>staging_customers</code>: 67.037 dòng; <code>reject_rows</code>: 4.133 dòng; <code>dim_customer</code>: 62.904 dòng; <code>fact_customer_quality_audit</code>: 62.904 dòng.</li>
  <li><strong>Bảo toàn dữ liệu 100%:</strong> Không xảy ra hiện tượng mất mát dữ liệu. Số dòng trích xuất bằng tổng số dòng sạch cộng số dòng bị từ chối ($67.037 = 62.904 + 4.133$).</li>
  <li><strong>Bảo mật PII:</strong> 100% số điện thoại và email hiển thị qua hàm che mặt nạ đều được ẩn thông tin định danh, tỷ lệ rò rỉ là 0,00%.</li>
</ol>

<h2>1.4. Môi trường và dữ liệu thử nghiệm</h2>
<p>Hệ thống được kiểm thử trên môi trường Python 3.11/3.14 trên hệ điều hành Windows 11. Cơ sở dữ liệu kho Star Schema sử dụng SQLite 3 nhúng tại đường dẫn <code>data/processed/warehouse.db</code>. Dữ liệu thử nghiệm bao gồm: tập mẫu nhỏ 300 dòng (<code>customers_sample.csv</code>) dùng cho thử nghiệm máy trắng và tập thực tế 67.037 dòng (<code>customers_raw.csv</code>) của chuỗi Mekong Mobile.</p>

<!-- MỤC 2: BÁO CÁO KẾT QUẢ KIỂM THỬ -->
<div class="page-break"></div>

<h1>MỤC 2. BÁO CÁO KẾT QUẢ KIỂM THỬ (TEST REPORT)</h1>

<h2>2.1. Tổng quan tình trạng kiểm thử</h2>
<p>Bộ kiểm thử tự động đạt kết quả <strong>20/20 test case PASSED</strong> qua Pytest. Toàn bộ 12 ca kiểm thử thực nghiệm chạy trên môi trường thực tế đều đạt kết quả mong đợi với số liệu thực tế được ghi nhận chi tiết tại Bảng 2.1.</p>

<h2>2.2. Bảng tổng hợp kết quả 12 ca kiểm thử thực nghiệm</h2>
<div class="table-title">Bảng 2.1: Kết quả thực nghiệm 12 ca kiểm thử (Test Cases) luồng L7</div>
<table class="content-table">
  <thead>
    <tr>
      <th style="width: 7%;">Mã</th>
      <th style="width: 14%;">Tiền điều kiện</th>
      <th style="width: 18%;">Các bước thực hiện</th>
      <th style="width: 15%;">Dữ liệu thử</th>
      <th style="width: 18%;">Kết quả mong đợi</th>
      <th style="width: 7%;">Mức</th>
      <th>Kết quả thực tế quan sát</th>
      <th style="width: 6%;">P/F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>TC-01</strong></td>
      <td>CSDL chưa tạo hoặc đã xóa</td>
      <td>Chạy pipeline trên tập mẫu nhỏ</td>
      <td><code>customers_sample.csv</code> (300 bản ghi)</td>
      <td>Nạp 280 khách sạch vào <code>dim_customer</code>, 20 dòng vào <code>reject_rows</code></td>
      <td style="text-align: center;">Cao</td>
      <td>Khởi tạo DDL, đọc 300 dòng, nạp 280 dim, 20 reject; mã thoát 0</td>
      <td style="text-align: center;"><span class="tag-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-02</strong></td>
      <td>Không</td>
      <td>Gọi hàm chuẩn hóa họ tên</td>
      <td><code>' nguyễn văn an '</code>, <code>'TRẦN THỊ BÌNH'</code></td>
      <td>Chuẩn hóa Title Case: <code>'Nguyễn Văn An'</code>, <code>'Trần Thị Bình'</code></td>
      <td style="text-align: center;">Cao</td>
      <td>Trả về Title Case chính xác chuẩn tiếng Việt</td>
      <td style="text-align: center;"><span class="tag-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-03</strong></td>
      <td>Không</td>
      <td><strong>Giá trị biên SĐT:</strong> Xử lý mã quốc tế</td>
      <td><code>'+84901234567'</code> và <code>'84901234567'</code></td>
      <td>Quy đổi chuẩn xác về 10 chữ số <code>'0901234567'</code></td>
      <td style="text-align: center;">Cao</td>
      <td>Cả 2 trường hợp đều chuyển về đúng 10 số chuẩn</td>
      <td style="text-align: center;"><span class="tag-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-04</strong></td>
      <td>Không</td>
      <td><strong>Giá trị biên ngày:</strong> Mốc chuyển giao năm</td>
      <td><code>'2024-12-31'</code>, <code>'2025-01-01'</code></td>
      <td>Parse chính xác thành đối tượng date, không lệch ngày</td>
      <td style="text-align: center;">Cao</td>
      <td>Trả về đúng đối tượng <code>datetime.date</code></td>
      <td style="text-align: center;"><span class="tag-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-05</strong></td>
      <td>Không</td>
      <td><strong>Dữ liệu sai:</strong> SĐT rác hoặc thiếu ký số</td>
      <td>SĐT 8 số: <code>'09012345'</code>; SĐT chữ: <code>'0901abc567'</code></td>
      <td>Hàm trả về <code>None</code>; chuyển vào bảng reject, pipeline không dừng</td>
      <td style="text-align: center;">Cao</td>
      <td>Trả về <code>None</code>; nạp vào bảng <code>reject_rows</code> kèm lý do chi tiết</td>
      <td style="text-align: center;"><span class="tag-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-06</strong></td>
      <td>Không</td>
      <td><strong>Dữ liệu sai bắt buộc:</strong> Thiếu ID hoặc họ tên</td>
      <td><code>customer_id='   '</code>, <code>ho_ten='nan'</code></td>
      <td>Gắn mã vi phạm <code>DQ01_ID</code>, <code>DQ01_NAME</code>, cách ly vào reject</td>
      <td style="text-align: center;">Cao</td>
      <td>Phân loại đúng mã quy tắc vi phạm và ghi nhận lý do rõ ràng</td>
      <td style="text-align: center;"><span class="tag-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-07</strong></td>
      <td>Không</td>
      <td><strong>Bảo mật PII (NFR05):</strong> Che mặt nạ SĐT & Email</td>
      <td><code>'0901234567'</code>, <code>'trungbao@gmail.com'</code></td>
      <td>SĐT: <code>'0901***567'</code>; Email: <code>'t***@gmail.com'</code></td>
      <td style="text-align: center;">Cao</td>
      <td>Che đúng định dạng, tỷ lệ rò rỉ thông tin cá nhân là 0,00%</td>
      <td style="text-align: center;"><span class="tag-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-08</strong></td>
      <td>Không</td>
      <td><strong>Chất lượng:</strong> Đo 9 chỉ tiêu thuộc 3 chiều</td>
      <td>Fixture dữ liệu mẫu 6 dòng</td>
      <td>Trả về danh sách đối tượng <code>Do</code> đủ 9 số đo định lượng</td>
      <td style="text-align: center;">Cao</td>
      <td>Đo đủ 9 chỉ tiêu; mỗi phép đo trả về 1 số đối chiếu ngưỡng YAML</td>
      <td style="text-align: center;"><span class="tag-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-09</strong></td>
      <td>Không</td>
      <td><strong>Chiều Nhất quán:</strong> Phát hiện khách trùng lặp</td>
      <td>Tập dữ liệu thực tế 67.037 dòng</td>
      <td>Phát hiện 27.123 khách hàng có dấu hiệu trùng SĐT/Email (43,1%)</td>
      <td style="text-align: center;">Cao</td>
      <td>Gán cờ <code>is_duplicate=1</code> cho 27.123 bản ghi; đạt ngưỡng &le; 70%</td>
      <td style="text-align: center;"><span class="tag-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-10</strong></td>
      <td>Đã chạy lần 1 trên 67.037 dòng</td>
      <td><strong>Phép thử Idempotency:</strong> Chạy lại lần 2 và lần 3</td>
      <td>Cùng tập dữ liệu <code>customers_raw.csv</code> (67.037 dòng)</td>
      <td>Số lượng dòng ở cả 4 bảng trong kho CSDL hoàn toàn không đổi</td>
      <td style="text-align: center;">Cao</td>
      <td>Số lượng giữ nguyên: 67.037 / 4.133 / 62.904 / 62.904; không nhân đôi</td>
      <td style="text-align: center;"><span class="tag-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-11</strong></td>
      <td>Đã nạp kho dữ liệu</td>
      <td><strong>Đối chiếu Staging vs Fact:</strong> Chạy module so sánh dòng</td>
      <td>CSDL kho <code>warehouse.db</code></td>
      <td>Staging (67.037) &minus; Fact (62.904) = 4.133 dòng trong bảng reject</td>
      <td style="text-align: center;">Cao</td>
      <td>In bảng đối chiếu rõ ràng; xác nhận không thất thoát dữ liệu</td>
      <td style="text-align: center;"><span class="tag-pass">PASS</span></td>
    </tr>
    <tr>
      <td><strong>TC-12</strong></td>
      <td>Có CSDL kho dữ liệu</td>
      <td><strong>Xử lý trạng thái rỗng:</strong> Lọc ngày không có dữ liệu</td>
      <td><code>--tu-ngay 2099-01-01 --den-ngay 2099-12-31</code></td>
      <td>Không văng lỗi; tự động sinh ảnh placeholder cảnh báo thân thiện</td>
      <td style="text-align: center;">Cao</td>
      <td>Tạo ảnh cảnh báo trạng thái rỗng, không gây dừng ứng dụng</td>
      <td style="text-align: center;"><span class="tag-pass">PASS</span></td>
    </tr>
  </tbody>
</table>

<h2>2.3. Đánh giá tính trung thực và đối soát số dòng</h2>
<p>Toàn bộ các ca kiểm thử đều được thực thi trực tiếp trên hệ thống thật. Kết quả đối soát số dòng trước và sau khi chạy pipeline: <code>staging_customers</code>: 67.037 bản ghi; <code>dim_customer</code>: 62.904 bản ghi; <code>reject_rows</code>: 4.133 bản ghi; <code>fact_customer_quality_audit</code>: 62.904 bản ghi. Độ chênh lệch giữa dữ liệu nạp thô và dữ liệu sạch ($67.037 - 62.904 = 4.133$ dòng) khớp tuyệt đối với số dòng trong bảng reject, chứng minh hệ thống đạt tiêu chí không mất mát dữ liệu.</p>

<!-- MỤC 3: NHẬT KÝ LỖI -->
<div class="page-break"></div>

<h1>MỤC 3. NHẬT KÝ THEO DÕI LỖI (BUG LOG)</h1>
<p>Nhật ký ghi nhận trung thực 3 lỗi kỹ thuật được phát hiện trong quá trình phát triển và hoàn thiện hệ thống, nguyên nhân gốc rễ, phương án xử lý và minh chứng cam kết trên GitHub:</p>

<h2>3.1. BUG-01 (Mức độ Critical): Vi phạm toàn vẹn khóa ngoại khi nạp lại dữ liệu</h2>
<ol>
  <li><strong>Phát hiện bởi:</strong> Phép thử nạp lại được (Idempotency test) khi thực thi pipeline lần thứ hai trên cùng tập dữ liệu.</li>
  <li><strong>Triệu chứng:</strong> Pipeline nạp lần thứ hai gặp lỗi dừng: <code>sqlite3.IntegrityError: FOREIGN KEY constraint failed</code> khi cập nhật bảng <code>dim_audit_run</code>.</li>
  <li><strong>Cách tái lập:</strong> Chạy <code>python -m src.pipeline</code> lần 1 hoàn tất, sau đó chạy tiếp lần 2.</li>
  <li><strong>Nguyên nhân:</strong> Hàm <code>tao_phien_chay</code> sử dụng câu lệnh <code>INSERT OR REPLACE INTO dim_audit_run</code>. Khi chạy lại, SQLite thực hiện xóa bản ghi cũ trước rồi mới thêm bản ghi mới, dẫn đến mất <code>run_key</code> mà bảng <code>fact_customer_quality_audit</code> đang tham chiếu tới (Foreign Key).</li>
  <li><strong>Cách sửa:</strong> Chuyển sang cơ chế kiểm tra trước bằng <code>SELECT run_key FROM dim_audit_run WHERE batch_id = ?</code>. Nếu đã tồn tại thì thực hiện lệnh <code>UPDATE</code> giữ nguyên <code>run_key</code>; đồng thời xóa các dòng fact cũ của cùng <code>run_key</code> trước khi nạp lại.</li>
  <li><strong>Xác nhận:</strong> Chạy lại pipeline 3 lần liên tiếp, số lượng bản ghi ở cả 4 bảng đích giữ nguyên tuyệt đối, không phát sinh lỗi khóa ngoại.</li>
  <li><strong>Commit khắc phục:</strong> <a href="https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality/commit/94c9c9d" target="_blank">Commit 94c9c9d trên GitHub</a></li>
</ol>

<h2>3.2. BUG-02 (Mức độ Major): Lệch tên cột giữa thiết kế và tập dữ liệu thực tế</h2>
<ol>
  <li><strong>Phát hiện bởi:</strong> Thực thi thử nghiệm trên tập dữ liệu thực tế <code>customers_raw.csv</code> (67.037 bản ghi).</li>
  <li><strong>Triệu chứng:</strong> Pipeline bị dừng đột ngột với thông báo lỗi <code>KeyError: 'ngay_dang_ky'</code> hoặc <code>KeyError: 'customer_id'</code>.</li>
  <li><strong>Cách tái lập:</strong> Gọi hàm <code>clean_customers.xu_ly_lam_sach_khach_hang(df_tho)</code> trên dữ liệu CSV thô.</li>
  <li><strong>Nguyên nhân:</strong> Tệp CSV thực tế của Mekong Mobile sử dụng tên cột là <code>record_id</code> và <code>ngay_tao</code>, trong khi thiết kế ban đầu đặt tên là <code>customer_id</code> và <code>ngay_dang_ky</code>.</li>
  <li><strong>Cách sửa:</strong> Bổ sung cơ chế ánh xạ cột linh hoạt: <code>cot_id = 'customer_id' if 'customer_id' in df.columns else 'record_id'</code> và <code>cot_ngay = 'ngay_dang_ky' if 'ngay_dang_ky' in df.columns else 'ngay_tao'</code> trước khi thực hiện làm sạch.</li>
  <li><strong>Xác nhận:</strong> Chạy thành công toàn bộ 67.037 dòng từ tệp CSV thật không còn gặp lỗi <code>KeyError</code>.</li>
  <li><strong>Commit khắc phục:</strong> <a href="https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality/commit/94c9c9d" target="_blank">Commit 94c9c9d trên GitHub</a></li>
</ol>

<h2>3.3. BUG-03 (Mức độ Minor): Sai tên cột thời gian trong câu truy vấn bảng Reject</h2>
<ol>
  <li><strong>Phát hiện bởi:</strong> Kiểm thử trạng thái rỗng khi vẽ biểu đồ phân bổ lỗi DQ với bộ lọc ngày xa trong tương lai.</li>
  <li><strong>Triệu chứng:</strong> Cửa sổ terminal báo lỗi <code>sqlite3.OperationalError: no such column: ngay_nap</code>.</li>
  <li><strong>Cách tái lập:</strong> Gọi lệnh <code>python -m src.dashboard.bieu_do --tu-ngay 2099-01-01</code>.</li>
  <li><strong>Nguyên nhân:</strong> Trong câu lệnh SQL truy vấn bảng <code>reject_rows</code>, mã nguồn gọi tên cột <code>ngay_nap</code>, trong khi tệp DDL tại <code>sql/002_reject.sql</code> đặt tên là <code>thoi_gian_tao</code>.</li>
  <li><strong>Cách sửa:</strong> Sửa lại tên cột trong câu truy vấn tại <code>src/dashboard/bieu_do.py</code> từ <code>ngay_nap</code> thành <code>thoi_gian_tao</code>.</li>
  <li><strong>Xác nhận:</strong> Chạy lại hàm vẽ biểu đồ với bộ lọc ngày tương lai, hệ thống tự động sinh ảnh thông báo trạng thái rỗng mà không bị dừng đột ngột.</li>
  <li><strong>Commit khắc phục:</strong> <a href="https://github.com/HoLeTrungBao/smartcrm-2374802010030-customer-data-quality/commit/3e3da6a" target="_blank">Commit 3e3da6a trên GitHub</a></li>
</ol>

<!-- MỤC 4: HƯỚNG DẪN TRIỂN KHAI -->
<div class="page-break"></div>

<h1>MỤC 4. HƯỚNG DẪN TRIỂN KHAI (DEPLOYMENT GUIDE)</h1>

<h2>4.1. Yêu cầu hệ thống (System Requirements)</h2>
<ul>
  <li><strong>Hệ điều hành:</strong> Windows 10/11, Linux (Ubuntu 20.04/22.04 LTS), hoặc macOS 12+</li>
  <li><strong>Môi trường thực thi:</strong> Python 3.11+ (khuyến nghị dùng virtualenv) hoặc Docker & Docker Compose</li>
  <li><strong>Cơ sở dữ liệu:</strong> SQLite 3.35+ (nhúng sẵn trong Python, không yêu cầu cài dịch vụ ngoài)</li>
  <li><strong>Phần cứng tối thiểu:</strong> RAM 2 GB (khuyến nghị 4 GB), dung lượng ổ đĩa trống &ge; 500 MB</li>
</ul>

<h2>4.2. Các bước thiết lập hệ thống (&le; 2 lệnh)</h2>
<p><strong>Phương thức A: Triển khai thông qua Docker Compose (Môi trường chuẩn máy chủ)</strong></p>
<pre><code>cp .env.example .env
docker compose up -d --build</code></pre>

<p><strong>Phương thức B: Triển khai trực tiếp trên môi trường Python (&le; 2 lệnh — Chuẩn máy trắng)</strong></p>
<pre><code>pip install -r requirements.txt
python -m src.pipeline --file-nguon data/mau/customers_sample.csv --xuat-bao-cao</code></pre>
<p><em>(Hoặc trên môi trường Windows: thực thi tập lệnh kịch bản tự động <code>run_clean_test.bat</code>).</em></p>

<h2>4.3. Danh mục biến môi trường</h2>
<div class="table-title">Bảng 4.1: Danh mục biến môi trường hệ thống</div>
<table class="content-table">
  <thead>
    <tr>
      <th style="width: 28%;">Tên biến</th>
      <th style="width: 22%;">Giá trị mặc định</th>
      <th style="width: 20%;">Giá trị hợp lệ</th>
      <th>Mô tả chức năng nghiệp vụ</th>
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
      <td><code>DEBUG</code>, <code>INFO</code>, <code>WARNING</code></td>
      <td>Mức độ chi tiết của nhật ký hệ thống.</td>
    </tr>
    <tr>
      <td><code>DATA_DIR</code></td>
      <td><code>data/mau</code></td>
      <td>Đường dẫn thư mục</td>
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
      <td>Đường dẫn thư mục</td>
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

<h2>4.4. Quy cách tập dữ liệu mẫu</h2>
<p>Tệp dữ liệu mẫu được lưu trữ tại <code>data/mau/customers_sample.csv</code> phục vụ đối soát nhanh:</p>
<ul>
  <li><strong>Dung lượng tập mẫu:</strong> Đúng <strong>300 bản ghi khách hàng</strong>.</li>
  <li><strong>280 bản ghi đạt chuẩn (93,3%):</strong> Số điện thoại 10 số hợp lệ, họ tên chuẩn, ngày sinh hợp lệ &rarr; nạp vào <code>dim_customer</code>.</li>
  <li><strong>20 bản ghi lỗi (6,7%):</strong> Số điện thoại sai chữ số, thiếu định danh &rarr; cách ly vào bảng <code>reject_rows</code>.</li>
</ul>

<h2>4.5. Kiểm tra hoạt động hệ thống (Verify It Works)</h2>
<pre><code># 1. Kiểm tra toàn bộ 20 test case tự động qua Pytest
python -m pytest -v

# 2. Kiểm tra đối soát số dòng trong kho dữ liệu
python -m src.dashboard.so_sanh_dong

# 3. Khởi chạy Dashboard Web Streamlit trực quan
python -m streamlit run streamlit_app.py</code></pre>

<h2>4.6. Hướng dẫn triển khai trực tuyến trên Streamlit Cloud</h2>
<p>Hệ thống được đóng gói và triển khai trực tuyến trên hạ tầng Streamlit Community Cloud:</p>
<ul>
  <li><strong>Địa chỉ truy cập công khai:</strong> <a href="https://smartcrm-2374802010030.streamlit.app" target="_blank">https://smartcrm-2374802010030.streamlit.app</a></li>
  <li><strong>Tệp ứng dụng chính:</strong> <code>streamlit_app.py</code></li>
  <li><strong>Tính năng trực tuyến:</strong> Tự động khởi tạo cấu trúc CSDL SQLite trên Cloud khi chạy lần đầu; cung cấp 4 thẻ KPI chất lượng, biểu đồ phân tích vi phạm DQ, bảng tra cứu bản ghi reject và đối soát kho theo thời gian thực.</li>
</ul>

<!-- MỤC 5: CHECKLIST BẢO MẬT -->
<div class="page-break"></div>

<h1>MỤC 5. BẢNG KIỂM TRA AN TOÀN VÀ BẢO MẬT (CHECKLIST BẢO MẬT)</h1>

<h2>5.1. Bảng kê khai 7 hạng mục an toàn và bảo mật</h2>
<p>Theo quy định đánh giá tiêu chí C6, Bảng 5.1 kê khai trung thực trạng thái bảo mật của hệ thống luồng L7 kèm minh chứng cụ thể:</p>

<div class="table-title">Bảng 5.1: Bảng kiểm tra an toàn và bảo mật (Checklist bảo mật 7 mục)</div>
<table class="content-table">
  <thead>
    <tr>
      <th style="width: 7%;">STT</th>
      <th style="width: 32%;">Hạng mục kiểm tra bảo mật</th>
      <th style="width: 18%;">Trạng thái</th>
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
      <td>Quá trình xử lý và nạp dữ liệu diễn ra cục bộ giữa tệp CSV và SQLite, không truyền tải dữ liệu khách hàng qua Internet.</td>
    </tr>
  </tbody>
</table>

<h2>5.2. Cam kết và thẩm định bảo mật</h2>
<p>Sinh viên cam kết nội dung kê khai trên là hoàn toàn trung thực, có thể kiểm chứng trực tiếp qua mã nguồn và lịch sử commit của repository.</p>

<!-- MỤC 6: TÀI LIỆU TRACK DA -->
<div class="page-break"></div>

<h1>MỤC 6. TÀI LIỆU KỸ THUẬT THEO TRACK DATA ANALYTICS</h1>

<h2>6.1. Tài liệu luồng xử lý dữ liệu (Pipeline Documentation)</h2>

<h3>6.1.1. Tổng quan kiến trúc hệ thống (High-Level Architecture)</h3>
<p>Đường ống xử lý dữ liệu chất lượng khách hàng vận hành theo chu trình ETL 4 pha khép kín: <strong>Extract &rarr; Transform &rarr; Quality &rarr; Load</strong>. Bản ghi sau khi kiểm định được phân luồng tự động: các bản ghi sạch được nạp vào mô hình Star Schema (<code>dim_customer</code>, <code>fact_customer_quality_audit</code>), trong khi các bản ghi lỗi được cách ly vào bảng <code>reject_rows</code> kèm thông điệp lỗi rõ ràng.</p>

<h3>6.1.2. Nguồn dữ liệu và nạp dữ liệu (Data Source & Ingestion)</h3>
<p>Dữ liệu nguồn gồm tệp CSV giao dịch khách hàng <code>customers_raw.csv</code> (67.037 dòng) chứa các trường: <code>record_id</code>, <code>ho_ten</code>, <code>so_dien_thoai</code>, <code>email</code>, <code>ngay_sinh</code>, <code>dia_chi</code>, <code>ngay_tao</code>. Module trích xuất đọc toàn bộ dưới dạng chuỗi (<code>dtype=str</code>) để tránh mất số 0 đầu số điện thoại.</p>

<h3>6.1.3. Quy tắc làm sạch và chuẩn hóa dữ liệu</h3>
<ul>
  <li><em>Số điện thoại (DQ02):</em> Xử lý mã quốc tế <code>+84</code>, <code>84</code>, loại bỏ khoảng trắng và dấu chấm, quy đổi về 10 chữ số chuẩn bắt đầu bằng số 0.</li>
  <li><em>Họ tên (DQ01):</em> Xóa khoảng trắng thừa ở hai đầu và giữa các từ, chuyển đổi toàn bộ về định dạng Title Case chuẩn tiếng Việt.</li>
  <li><em>Email & Ngày tháng:</em> Kiểm tra cú pháp RFC email; chuẩn hóa ngày sinh và ngày tạo về chuẩn ISO-8601 (<code>YYYY-MM-DD</code>).</li>
</ul>

<h3>6.1.4. Đo lường đa chiều chất lượng dữ liệu (Quality Measurement)</h3>
<div class="table-title">Bảng 6.1: Kết quả đo lường 9 chỉ tiêu thuộc 3 chiều chất lượng dữ liệu</div>
<table class="content-table">
  <thead>
    <tr>
      <th style="width: 24%;">Chiều chất lượng</th>
      <th style="width: 14%;">Mã quy tắc</th>
      <th>Nội dung kiểm tra</th>
      <th style="width: 12%;">Số kiểm</th>
      <th style="width: 12%;">Số đạt</th>
      <th style="width: 13%;">Tỷ lệ (%)</th>
      <th style="width: 13%;">Ngưỡng</th>
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
      <td style="text-align: center;">35.781 duy nhất</td>
      <td style="text-align: center;">43,10% trùng</td>
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

<h3>6.1.5. Chiến lược lưu trữ và phân bổ dòng lỗi (Reject Breakdown)</h3>
<p>Số dòng bị từ chối được lưu trữ toàn vẹn tại bảng <code>reject_rows</code> gồm đúng <strong>4.133 dòng</strong>, phân loại theo nguyên nhân:</p>
<ul>
  <li><code>SĐT không hợp lệ hoặc thiếu ký số (DQ02_PHONE)</code>: <strong>3.352 dòng</strong> (chiếm 81,1%)</li>
  <li><code>Thiếu số điện thoại bắt buộc (DQ01_PHONE)</code>: <strong>564 dòng</strong> (chiếm 13,6%)</li>
  <li><code>Thiếu họ tên khách hàng (DQ01_NAME)</code>: <strong>217 dòng</strong> (chiếm 5,3%)</li>
</ul>
<p>Tổng cộng: $3.352 + 564 + 217 = 4.133$ dòng. Số liệu đối chiếu khớp tuyệt đối với số dòng trong báo cáo lần chạy gần nhất.</p>

<h3>6.1.6. Hạn chế kỹ thuật và ảnh hưởng nghiệp vụ</h3>
<ol>
  <li><strong>Hạn chế 1 — Cơ chế phân cụm trùng lặp dựa trên khóa chính xác (Exact Match):</strong> Hệ thống hiện tại phát hiện trùng lặp dựa trên việc trùng số điện thoại hoặc email. <em>Ảnh hưởng nghiệp vụ:</em> Nếu khách hàng đổi số điện thoại nhưng giữ nguyên họ tên và địa chỉ, hệ thống sẽ coi là 2 khách hàng riêng biệt, dẫn đến việc phòng Marketing có thể gửi ưu đãi trùng cho cùng một người.</li>
  <li><strong>Hạn chế 2 — Khóa cơ sở dữ liệu khi chạy đồng thời trong SQLite:</strong> SQLite sử dụng cơ chế file-level locking. <em>Ảnh hưởng nghiệp vụ:</em> Khi pipeline đang thực hiện nạp dữ liệu lô lớn, người dùng truy cập dashboard tra cứu có thể gặp độ trễ nhẹ do chờ giải phóng khóa đọc/ghi.</li>
  <li><strong>Hạn chế 3 — Cách ly thụ động dòng reject mà chưa có giao diện sửa lỗi tức thời:</strong> Các dòng lỗi được cách ly vào <code>reject_rows</code> kèm thông điệp rõ ràng nhưng đòi hỏi đối soát viên phải rà soát qua tệp hoặc truy vấn SQL. <em>Ảnh hưởng nghiệp vụ:</em> Cần thêm 1 bước xuất danh sách lỗi cho nhân viên chăm sóc khách hàng liên hệ bổ sung số điện thoại.</li>
</ol>

<div class="page-break"></div>

<h2>6.2. Từ điển dữ liệu (Data Dictionary)</h2>

<h3>6.2.1. Tổng quan 7 bảng cơ sở dữ liệu Star Schema</h3>
<div class="table-title">Bảng 6.2: Tổng quan 7 bảng cơ sở dữ liệu Star Schema</div>
<table class="content-table">
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

<h3>6.2.2. Cấu trúc chi tiết các bảng và tiêu chuẩn giả danh hóa PII (D4)</h3>
<div class="table-title">Bảng 6.3: Cấu trúc chi tiết bảng dim_customer và giả danh hóa PII (D4)</div>
<table class="content-table">
  <thead>
    <tr>
      <th style="width: 20%;">Tên cột</th>
      <th style="width: 15%;">Kiểu dữ liệu</th>
      <th style="width: 10%;">Nullable</th>
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
      <td>Cờ đánh dấu khách hàng nghi ngờ trùng lặp (1: Trùng, 0: Duy nhất).</td>
    </tr>
  </tbody>
</table>

<!-- MỤC 7: ẢNH CHỤP MINH CHỨNG -->
<div class="page-break"></div>

<h1>MỤC 7. ẢNH CHỤP KẾT QUẢ CHẠY THẬT (MINH CHỨNG THỰC NGHIỆM)</h1>
<p>Toàn bộ 3 ảnh dưới đây là kết quả thực thi thật 100% trên môi trường máy trạm của sinh viên, không che giấu lỗi, dữ liệu nhạy cảm được che theo quy định bảo mật NFR05:</p>

<h2>7.1. Minh chứng 1: Kết quả chạy bộ kiểm thử tự động (20/20 test PASS)</h2>
<div class="image-wrapper">
  <img src="{anh1_b64}" alt="Kết quả kiểm thử tự động 20 test PASS">
  <div class="figure-caption">Hình 7.1: Kết quả thực thi bộ kiểm thử tự động 20/20 test case PASSED bằng lệnh python -m pytest -v</div>
</div>

<h2>7.2. Minh chứng 2: Kết quả phép thử máy trắng và đối soát kho dữ liệu</h2>
<div class="image-wrapper">
  <img src="{anh2_b64}" alt="Kết quả phép thử máy trắng">
  <div class="figure-caption">Hình 7.2: Kết quả phép thử máy trắng tự động (run_clean_test.bat): thực thi 4 pha ETL và đối soát dòng trong kho Star Schema</div>
</div>

<div class="page-break"></div>

<h2>7.3. Minh chứng 3: Giao diện Web Dashboard SmartCRM Analytics thực tế</h2>
<div class="image-wrapper">
  <img src="{anh3_b64}" alt="Dashboard SmartCRM Analytics Streamlit">
  <div class="figure-caption">Hình 7.3: Giao diện Web Dashboard SmartCRM Analytics thực tế: 4 thẻ KPI chất lượng, biểu đồ phân tích vi phạm DQ và tỷ lệ trùng lặp khách hàng</div>
</div>

<!-- PHỤ LỤC: KHAI BÁO AI -->
<div class="page-break"></div>

<h1>PHỤ LỤC. BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ TRÍ TUỆ NHÂN TẠO (AI)</h1>

<h2>1. Khai báo AI cho Giai đoạn 3 (Bài tập 3)</h2>
<div class="table-title">Bảng 8.1: Bảng khai báo sử dụng công cụ Trí tuệ nhân tạo (AI) trong Bài tập 3</div>
<table class="content-table">
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
      <td>Hỗ trợ cấu trúc tài liệu kỹ thuật tiếng Anh (Pipeline documentation & Data dictionary) chuẩn hóa theo định dạng Markdown.</td>
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

<h2>2. Cam kết liêm chính học thuật</h2>
<div style="border: 1px solid #718096; background-color: #F8FAFC; padding: 12pt 16pt; margin-top: 14pt;">
  <p style="font-weight: bold; margin-bottom: 6pt;">CAM KẾT LIÊM CHÍNH HỌC THUẬT:</p>
  <p style="font-style: italic; margin-bottom: 12pt;">
    "Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp trong báo cáo Bài tập 3 này."
  </p>
  <p style="margin-bottom: 2pt;"><strong>Họ và tên sinh viên:</strong> Hồ Lê Trung Bảo</p>
  <p style="margin-bottom: 2pt;"><strong>Mã số sinh viên (MSSV):</strong> 2374802010030</p>
  <p style="margin-bottom: 2pt;"><strong>Lớp học phần:</strong> 71ITGR40203_01 (Khóa K23T) – Track DA</p>
  <p style="margin-bottom: 0;"><strong>Ngày cam kết:</strong> 14/11/2026</p>
</div>

</body>
</html>
"""

with open(TEMP_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"1. Da ghi file HTML tam tai: {TEMP_HTML}")

# Chuyen HTML sang PDF bang Microsoft Edge Headless (chua danh so trang)
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={TEMP_PDF}",
    TEMP_HTML
]

print("2. Dang xuat PDF co ban bang Microsoft Edge Headless...")
subprocess.run(cmd, check=True)

if not os.path.exists(TEMP_PDF):
    raise RuntimeError("Khong tao duoc file PDF tam!")

print("3. Dang danh so trang o chinh giua phia tren dau trang (@top-center) tu trang 1...")
# Dung reportlab tao overlay stamp danh so trang chinh giua tren cung
reader = pypdf.PdfReader(TEMP_PDF)
writer = pypdf.PdfWriter()
total_pages = len(reader.pages)
print(f"Tong so trang PDF: {total_pages}")

# Trang 0 la bia -> khong danh so
# Trang 1 tro di -> danh so 1, 2, 3...
for page_idx in range(total_pages):
    page = reader.pages[page_idx]
    if page_idx > 0:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        page_num_str = str(page_idx)  # Trang noi dung bat dau tu 1
        can.setFont("Times-Roman", 10)
        # Toa do x: o giua (210mm / 2), y: phia tren dau trang (297mm - 12mm)
        can.drawCentredString(210 * mm / 2.0, 297 * mm - 12 * mm, page_num_str)
        can.save()

        packet.seek(0)
        stamp_pdf = pypdf.PdfReader(packet)
        page.merge_page(stamp_pdf.pages[0])

    writer.add_page(page)

with open(FINAL_PDF, "wb") as f_out:
    writer.write(f_out)

print(f"[THANH CONG] Da xuat file PDF chuan hoa thanh cong: {FINAL_PDF}")
print(f"Kich thuoc file: {os.path.getsize(FINAL_PDF)} bytes")

# Don dep file tam
for p in [TEMP_HTML, TEMP_PDF]:
    if os.path.exists(p):
        os.remove(p)
