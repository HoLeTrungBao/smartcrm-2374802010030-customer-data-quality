# -*- coding: utf-8 -*-
"""
Script tạo Slide thuyết trình Xu hướng công nghệ (Buổi 18) chuẩn 6 trang
Chuyên đề Tốt nghiệp 1 (71ITGR40203) - Khoa CNTT, Trường Đại học Văn Lang
Sinh viên: Hồ Lê Trung Bảo - MSSV: 2374802010030 - Track: DA
Chủ đề: Xu hướng ELT trong xử lý dữ liệu và đánh giá áp dụng cho SmartCRM
Tên file xuất: 2374802010030_HoLeTrungBao_DA_XuHuong.pdf
"""

import os
import subprocess

ROOT_DIR = r"C:\Users\ASUS\smartcrm-2374802010030-customer-data-quality"
OUTPUT_PDF = os.path.join(ROOT_DIR, "2374802010030_HoLeTrungBao_DA_XuHuong.pdf")
TEMP_HTML = os.path.join(ROOT_DIR, "slide_xuhuong_elt_tam.html")

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>2374802010030_HoLeTrungBao_DA_XuHuong</title>
<style>
  @page {{
    size: 297mm 167mm; /* Tỷ lệ màn hình 16:9 chuẩn trình chiếu */
    margin: 0;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #0F172A;
    color: #F8FAFC;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .slide {{
    width: 297mm;
    height: 167mm;
    padding: 13mm 18mm 11mm 18mm;
    position: relative;
    page-break-after: always;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: #0F172A;
  }}

  /* HEADER SLIDE */
  .slide-header {{
    margin-bottom: 5mm;
  }}
  .slide-category {{
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #38BDF8;
    margin-bottom: 1.5mm;
  }}
  .slide-title {{
    font-size: 17.5pt;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.25;
    margin: 0;
  }}
  .slide-subtitle {{
    font-size: 10pt;
    color: #94A3B8;
    margin-top: 1.5mm;
  }}

  /* FOOTER SLIDE */
  .slide-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #1E293B;
    padding-top: 3mm;
    font-size: 8pt;
    color: #64748B;
  }}
  .slide-footer .student-info {{
    font-weight: 600;
    color: #94A3B8;
  }}

  /* GRID LAYOUTS */
  .grid-3 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 5mm;
    flex: 1;
    margin-bottom: 4mm;
  }}
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6mm;
    flex: 1;
    margin-bottom: 4mm;
  }}

  /* CARDS */
  .card {{
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 5mm 6mm;
    display: flex;
    flex-direction: column;
  }}
  .card-blue {{
    border-top: 3px solid #38BDF8;
  }}
  .card-amber {{
    border-top: 3px solid #F59E0B;
  }}
  .card-slate {{
    border-top: 3px solid #64748B;
  }}
  .card-emerald {{
    border-top: 3px solid #10B981;
  }}
  .card-title {{
    font-size: 10.5pt;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 3mm;
  }}
  .card-content {{
    font-size: 9pt;
    line-height: 1.5;
    color: #CBD5E1;
    flex: 1;
  }}
  .card-content ul {{
    margin: 0;
    padding-left: 4.5mm;
  }}
  .card-content li {{
    margin-bottom: 2mm;
  }}

  /* COMPARISON BOX */
  .compare-box {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5mm;
    margin-bottom: 4mm;
    flex: 1;
  }}
  .compare-item {{
    background-color: #1E293B;
    border-radius: 6px;
    padding: 4.5mm 5.5mm;
    border: 1px solid #334155;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .compare-item.etl {{
    border-top: 3.5px solid #94A3B8;
  }}
  .compare-item.elt {{
    border-top: 3.5px solid #38BDF8;
  }}
  .compare-header {{
    font-size: 11pt;
    font-weight: 700;
    margin-bottom: 2.5mm;
  }}
  .compare-header.etl-title {{ color: #CBD5E1; }}
  .compare-header.elt-title {{ color: #38BDF8; }}

  .diagram-flow {{
    background-color: #0F172A;
    padding: 2.5mm 3.5mm;
    border-radius: 4px;
    font-family: Consolas, monospace;
    font-size: 8.5pt;
    color: #94A3B8;
    margin-top: 3mm;
  }}
  .diagram-flow.active {{
    color: #38BDF8;
  }}

  /* HIGHLIGHT CALLOUT */
  .callout-box {{
    background-color: #1E293B;
    border: 1px solid #334155;
    border-left: 4px solid #38BDF8;
    border-radius: 6px;
    padding: 3.5mm 5mm;
    font-size: 9pt;
    line-height: 1.45;
    color: #E2E8F0;
    margin-bottom: 4mm;
  }}
  .callout-box strong {{
    color: #38BDF8;
  }}

  /* TABLE STYLES */
  table.ref-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin-bottom: 3.5mm;
  }}
  table.ref-table th, table.ref-table td {{
    border: 1px solid #334155;
    padding: 3mm 4mm;
    text-align: left;
    vertical-align: top;
  }}
  table.ref-table th {{
    background-color: #0F172A;
    color: #38BDF8;
    font-weight: 700;
    font-size: 8pt;
    letter-spacing: 0.5px;
  }}
  table.ref-table td {{
    background-color: #1E293B;
    color: #CBD5E1;
    line-height: 1.45;
  }}
  table.ref-table tr:nth-child(even) td {{
    background-color: #162032;
  }}

  /* COVER SLIDE */
  .cover-slide {{
    background: radial-gradient(circle at 85% 20%, #1E293B 0%, #0F172A 70%);
    justify-content: center;
    align-items: flex-start;
    padding: 20mm 24mm;
  }}
  .cover-badge {{
    background-color: rgba(56, 189, 248, 0.12);
    border: 1px solid #38BDF8;
    color: #38BDF8;
    font-size: 8.5pt;
    font-weight: 700;
    padding: 1.8mm 4.5mm;
    border-radius: 16px;
    letter-spacing: 1.2px;
    margin-bottom: 6mm;
    display: inline-block;
  }}
  .cover-main-h1 {{
    font-size: 25pt;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.2;
    margin: 0 0 3mm 0;
  }}
  .cover-main-sub {{
    font-size: 13pt;
    font-weight: 600;
    color: #38BDF8;
    margin: 0 0 7mm 0;
  }}
  .cover-desc {{
    font-size: 10pt;
    color: #94A3B8;
    line-height: 1.55;
    max-width: 195mm;
    margin-bottom: 9mm;
  }}
  .cover-meta {{
    border-top: 1px solid #334155;
    padding-top: 5mm;
    display: flex;
    gap: 15mm;
    font-size: 9pt;
    color: #E2E8F0;
  }}
  .cover-meta-item strong {{
    color: #38BDF8;
    display: block;
    font-size: 7.5pt;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 1mm;
  }}

  .tag-info {{
    display: inline-block;
    padding: 0.6mm 2mm;
    border-radius: 4px;
    font-size: 7.5pt;
    font-weight: 600;
    background-color: #334155;
    color: #94A3B8;
    margin-right: 1.5mm;
  }}
</style>
</head>
<body>

<!-- SLIDE 1: TRANG BÌA -->
<div class="slide cover-slide">
  <div>
    <div class="cover-badge">BÁO CÁO CHUYÊN ĐỀ TỐT NGHIỆP 1 · BUỔI 18 (TRACK DA)</div>
    <h1 class="cover-main-h1">Xu Hướng Chuyển Đổi Từ ETL Sang ELT</h1>
    <div class="cover-main-sub">Mô hình xử lý dữ liệu với Cloud Data Warehouse & công cụ dbt</div>
    <div class="cover-desc">
      Tìm hiểu bản chất của mô hình ELT, các điểm cải thiện so với ETL truyền thống, những yếu tố cần cân nhắc về chi phí và an toàn dữ liệu, cùng đánh giá thực tế khi áp dụng cho hệ thống SmartCRM Mekong Mobile.
    </div>
  </div>

  <div class="cover-meta">
    <div class="cover-meta-item">
      <strong>Sinh viên thực hiện</strong>
      Hồ Lê Trung Bảo
    </div>
    <div class="cover-meta-item">
      <strong>Mã số sinh viên</strong>
      2374802010030
    </div>
    <div class="cover-meta-item">
      <strong>Lớp học phần</strong>
      71ITGR40203_01 (K23T)
    </div>
    <div class="cover-meta-item">
      <strong>Chuyên ngành</strong>
      Data Analytics (DA)
    </div>
    <div class="cover-meta-item">
      <strong>Giảng viên hướng dẫn</strong>
      ThS. Nguyễn Minh Tân
    </div>
    <div class="cover-meta-item">
      <strong>Thời gian</strong>
      Tháng 11/2026
    </div>
  </div>
</div>

<!-- SLIDE 2: MỤC 1 — LÀ GÌ & VÍ DỤ THẬT -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-category">MỤC 1 · KHÁI NIỆM & VÍ DỤ THỰC TẾ</div>
    <h2 class="slide-title">ELT là gì: Nạp dữ liệu thô vào kho trước, sau đó biến đổi bằng SQL</h2>
    <div class="slide-subtitle">Sự thay đổi thứ tự giữa bước biến đổi (Transform) và nạp dữ liệu (Load) dựa trên năng lực lưu trữ và tính toán của kho dữ liệu hiện đại.</div>
  </div>

  <div class="compare-box">
    <div class="compare-item etl">
      <div>
        <div class="compare-header etl-title">Mô hình truyền thống: ETL (Extract &rarr; Transform &rarr; Load)</div>
        <p style="font-size: 8.8pt; color: #CBD5E1; line-height: 1.5; margin: 0;">
          Dữ liệu được trích xuất từ nguồn &rarr; Chuyển qua máy chủ trung gian (chạy mã Python, Java hoặc Spark) để làm sạch, định dạng và lọc lỗi &rarr; Nạp dữ liệu đã xử lý vào kho dữ liệu.
        </p>
      </div>
      <div class="diagram-flow">
        Nguồn dữ liệu &rarr; [Máy chủ trung gian làm sạch] &rarr; Kho dữ liệu đích
      </div>
    </div>

    <div class="compare-item elt">
      <div>
        <div class="compare-header elt-title">Mô hình hiện đại: ELT (Extract &rarr; Load &rarr; Transform)</div>
        <p style="font-size: 8.8pt; color: #CBD5E1; line-height: 1.5; margin: 0;">
          Dữ liệu từ nguồn được nạp thẳng vào bảng tạm (Staging) trong kho dữ liệu đám mây (BigQuery, Snowflake, DuckDB) &rarr; Các phép làm sạch và mô hình hóa được thực hiện trực tiếp trong kho bằng câu lệnh SQL.
        </p>
      </div>
      <div class="diagram-flow active">
        Nguồn dữ liệu &rarr; Nạp vào bảng tạm trong kho &rarr; [Biến đổi bằng SQL/dbt]
      </div>
    </div>
  </div>

  <div class="callout-box">
    <strong>Ví dụ ứng dụng thực tế:</strong> Các công cụ như <strong>Fivetran</strong> hoặc <strong>Airbyte</strong> đóng vai trò đồng bộ dữ liệu thô từ các nguồn (CRM, cơ sở dữ liệu giao dịch) vào kho dữ liệu. Sau đó, công cụ <strong>dbt (data build tool)</strong> giúp các chuyên viên phân tích quản lý, kiểm thử và thực thi các câu lệnh SQL để xây dựng các bảng Fact và Dimension phục vụ báo cáo.
  </div>

  <div class="slide-footer">
    <span class="student-info">Hồ Lê Trung Bảo — 2374802010030 (Track DA)</span>
    <span>Trang 2 / 6</span>
  </div>
</div>

<!-- SLIDE 3: MỤC 2 — GIẢI QUYẾT VẤN ĐỀ GÌ -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-category">MỤC 2 · NHỮNG VẤN ĐỀ ELT GIÚP CẢI THIỆN</div>
    <h2 class="slide-title">Ba lợi thế thực tế của mô hình ELT trong quy trình phân tích dữ liệu</h2>
    <div class="slide-subtitle">Tận dụng năng lực tính toán phân tán của các kho dữ liệu hiện đại và tối ưu hóa sự phối hợp trong đội ngũ kỹ thuật.</div>
  </div>

  <div class="grid-3">
    <div class="card card-blue">
      <div class="card-title">1. Giảm tải cho máy chủ xử lý</div>
      <div class="card-content">
        <ul>
          <li><strong>Mô hình ETL:</strong> Máy chủ xử lý trung gian phải chịu tải toàn bộ các phép tính toán và lọc dữ liệu. Khi khối lượng dữ liệu tăng cao, hệ thống dễ gặp tình trạng thiếu bộ nhớ (RAM).</li>
          <li><strong>Mô hình ELT:</strong> Chuyển các tác vụ xử lý nặng sang kho dữ liệu đám mây vốn có khả năng tự động mở rộng tài nguyên tính toán theo nhu cầu.</li>
        </ul>
      </div>
    </div>

    <div class="card card-blue">
      <div class="card-title">2. Lưu giữ dữ liệu thô ban đầu</div>
      <div class="card-content">
        <ul>
          <li><strong>Mô hình ETL:</strong> Dữ liệu sau khi qua bước làm sạch mới được lưu trữ; nếu quy tắc làm sạch ban đầu có sai sót thì việc tái tạo lại dữ liệu gốc gặp khó khăn.</li>
          <li><strong>Mô hình ELT:</strong> Dữ liệu gốc được lưu nguyên vẹn tại tầng Staging. Khi cần điều chỉnh logic nghiệp vụ, người dùng chỉ cần cập nhật lại câu lệnh SQL và thực thi lại.</li>
        </ul>
      </div>
    </div>

    <div class="card card-blue">
      <div class="card-title">3. Tận dụng trực tiếp ngôn ngữ SQL</div>
      <div class="card-content">
        <ul>
          <li><strong>Mô hình ETL:</strong> Thường phụ thuộc vào mã nguồn của kỹ sư phần mềm (Python, Scala), khiến các chuyên viên phân tích nghiệp vụ khó can thiệp trực tiếp.</li>
          <li><strong>Mô hình ELT:</strong> Logic biến đổi được viết bằng câu lệnh SQL chuẩn kết hợp với dbt, giúp các bạn Data Analyst dễ dàng theo dõi và chủ động xây dựng dữ liệu.</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <span class="student-info">Hồ Lê Trung Bảo — 2374802010030 (Track DA)</span>
    <span>Trang 3 / 6</span>
  </div>
</div>

<!-- SLIDE 4: MỤC 3 — ĐÁNH ĐỔI & KHI NÀO KHÔNG DÙNG -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-category">MỤC 3 · NHỮNG ĐIỂM CẦN CÂN NHẮC & TRƯỜNG HỢP KHÔNG NÊN DÙNG</div>
    <h2 class="slide-title">Những điểm đánh đổi về chi phí hạ tầng và tính an toàn dữ liệu</h2>
    <div class="slide-subtitle">Bất kỳ kiến trúc nào cũng có giới hạn; việc lựa chọn cần căn cứ vào bài toán thực tế và yêu cầu bảo mật.</div>
  </div>

  <div class="grid-3">
    <div class="card card-amber">
      <div class="card-title">Chi phí lưu trữ và tính toán</div>
      <div class="card-content">
        <ul>
          <li><strong>Dung lượng lưu trữ tăng:</strong> Việc lưu đồng thời dữ liệu thô, các bảng trung gian và bảng kết quả khiến dung lượng lưu trữ tăng thêm khoảng 40% – 60% (theo báo cáo Fivetran 2024).</li>
          <li><strong>Chi phí truy vấn:</strong> Các nền tảng đám mây tính phí theo lượng dữ liệu được quét. Nếu các câu lệnh SQL viết chưa tối ưu, chi phí vận hành hàng tháng có thể tăng đáng kể.</li>
        </ul>
      </div>
    </div>

    <div class="card card-amber">
      <div class="card-title">Vấn đề bảo mật dữ liệu cá nhân</div>
      <div class="card-content">
        <ul>
          <li><strong>Lưu trữ dữ liệu thô:</strong> Đưa trực tiếp dữ liệu chưa qua xử lý vào kho có thể khiến các thông tin cá nhân (như SĐT, email, địa chỉ) tồn tại ở dạng rõ trong bảng Staging.</li>
          <li><strong>Yêu cầu tuân thủ:</strong> Theo các quy định về bảo vệ dữ liệu cá nhân (Nghị định 13/2023/NĐ-CP và Luật Bảo vệ dữ liệu cá nhân), thông tin định danh cần được phân quyền chặt chẽ hoặc che giấu phù hợp trước khi chia sẻ quyền truy cập.</li>
        </ul>
      </div>
    </div>

    <div class="card card-amber">
      <div class="card-title">Trường hợp nên giữ mô hình ETL</div>
      <div class="card-content">
        <ul>
          <li><strong>Dữ liệu nhạy cảm cao:</strong> Khi dữ liệu cần được ẩn danh hoặc mã hóa ngay từ nguồn trước khi lưu trữ diện rộng.</li>
          <li><strong>Quy mô dữ liệu vừa và nhỏ:</strong> Chạy trực tiếp script trên máy chủ hiện có nhanh và tiết kiệm hơn nhiều so với việc thuê hạ tầng đám mây.</li>
          <li><strong>Dữ liệu phi cấu trúc:</strong> Dữ liệu dạng tệp nhị phân, hình ảnh cần thư viện xử lý chuyên biệt mà SQL không hỗ trợ tốt.</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <span class="student-info">Hồ Lê Trung Bảo — 2374802010030 (Track DA)</span>
    <span>Trang 4 / 6</span>
  </div>
</div>

<!-- SLIDE 5: MỤC 4 — LIÊN HỆ PROTOTYPE SMARTCRM -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-category">MỤC 4 · LIÊN HỆ THỰC TẾ VỚI HỆ THỐNG SMARTCRM (LUỒNG L7)</div>
    <h2 class="slide-title">Đánh giá khả năng chuyển đổi mô hình cho đồ án SmartCRM Mekong Mobile</h2>
    <div class="slide-subtitle">Đối chiếu cụ thể giữa quy trình hiện tại và phương án ELT đối với tập dữ liệu 67.037 bản ghi khách hàng.</div>
  </div>

  <div class="grid-3">
    <div class="card card-slate">
      <div class="card-title">Nếu chuyển sang ELT cần thay đổi gì?</div>
      <div class="card-content">
        <ul>
          <li><strong>Tách bước xử lý:</strong> Module <code>read_sources.py</code> chỉ đọc file CSV và nạp toàn bộ vào bảng <code>staging_customers</code> trong cơ sở dữ liệu.</li>
          <li><strong>Viết lại logic bằng SQL:</strong> Chuyển các hàm xử lý Python trong <code>clean_customers.py</code> thành các model SQL dbt (<code>dim_customer.sql</code>, <code>reject_rows.sql</code>).</li>
          <li><strong>Chuyển đổi kiểm thử:</strong> Đổi các kiểm thử chất lượng dữ liệu trong <code>test_rules.py</code> sang dạng schema tests của dbt.</li>
        </ul>
      </div>
    </div>

    <div class="card card-slate">
      <div class="card-title">So sánh ưu điểm và hạn chế</div>
      <div class="card-content">
        <ul>
          <li><strong>Ưu điểm:</strong> Quy tắc phân loại dữ liệu (DQ01 &rarr; DQ09) được mô tả bằng cú pháp SQL quen thuộc, dễ đọc đối với các bạn làm phân tích.</li>
          <li><strong>Hạn chế:</strong> Thông tin số điện thoại chưa được che mặt nạ sẽ xuất hiện ở bảng Staging, làm tăng rủi ro lộ lọt dữ liệu khách hàng nếu chia sẻ quyền truy cập bảng này.</li>
        </ul>
      </div>
    </div>

    <div class="card card-emerald">
      <div class="card-title">Đề xuất lựa chọn cho đồ án</div>
      <div class="card-content">
        <p style="font-weight: 700; color: #10B981; margin-bottom: 2mm;">Lựa chọn phù hợp: Tiếp tục duy trì mô hình ETL hiện tại</p>
        <p>Quy mô dữ liệu thử nghiệm của đồ án gồm <strong>67.037 bản ghi</strong>. Quy trình ETL hiện tại viết bằng Python chạy hoàn tất chỉ trong <strong>khoảng 1,4 giây</strong> và thực hiện che số điện thoại (<code>sdt_masked</code>) ngay trong quá trình xử lý.</p>
        <p style="margin-top: 2.5mm;"><strong>Kết luận:</strong> Với bài toán ứng dụng nội bộ chạy cục bộ, việc duy trì ETL giúp đảm bảo an toàn thông tin khách hàng ngay từ đầu, đơn giản hóa hạ tầng cài đặt và không làm phát sinh thêm chi phí dịch vụ bên ngoài.</p>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <span class="student-info">Hồ Lê Trung Bảo — 2374802010030 (Track DA)</span>
    <span>Trang 5 / 6</span>
  </div>
</div>

<!-- SLIDE 6: MỤC 5 — TÀI LIỆU THAM KHẢO -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-category">MỤC 5 · TÀI LIỆU THAM KHẢO</div>
    <h2 class="slide-title">Danh mục tài liệu kỹ thuật và báo cáo nghiên cứu tham khảo</h2>
    <div class="slide-subtitle">Các tài liệu chính thức từ nhà cung cấp giải pháp, báo cáo ngành và văn bản quy định pháp lý.</div>
  </div>

  <table class="ref-table">
    <thead>
      <tr>
        <th style="width: 25%;">Tên tài liệu / Nguồn</th>
        <th style="width: 45%;">Nội dung tham khảo chính</th>
        <th>Loại tài liệu</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>dbt Labs Documentation</strong><br><em>docs.getdbt.com</em></td>
        <td>Nguyên lý xây dựng mô hình dữ liệu theo hướng ELT; cách tổ chức các tầng Staging, Intermediate, Marts bằng câu lệnh SELECT SQL.</td>
        <td>Tài liệu kỹ thuật chính thức</td>
      </tr>
      <tr>
        <td><strong>Fivetran Data Survey (2024)</strong></td>
        <td>Khảo sát về xu hướng dịch chuyển từ ETL sang ELT trong các doanh nghiệp và mức độ gia tăng dung lượng lưu trữ trung bình.</td>
        <td>Báo cáo khảo sát ngành</td>
      </tr>
      <tr>
        <td><strong>Gartner Research (2025)</strong><br><em>Cloud Data Management Trends</em></td>
        <td>Đánh giá về chi phí tài nguyên tính toán và các yếu tố cần quản lý khi mở rộng kho dữ liệu đám mây.</td>
        <td>Báo cáo phân tích thị trường</td>
      </tr>
      <tr>
        <td><strong>Quy định bảo vệ dữ liệu cá nhân tại Việt Nam</strong><br><em>(Nghị định 13/2023/NĐ-CP & Luật BV Dữ liệu cá nhân)</em></td>
        <td>Các yêu cầu về tối thiểu hóa phạm vi thu thập, bảo vệ thông tin nhận dạng cá nhân (PII) và trách nhiệm của đơn vị xử lý dữ liệu.</td>
        <td>Văn bản quy phạm pháp luật</td>
      </tr>
    </tbody>
  </table>

  <div class="callout-box" style="margin-top: 2mm; margin-bottom: 2mm;">
    <strong>Ghi chú:</strong> Nội dung báo cáo được tổng hợp, đối chiếu và chuẩn bị phục vụ phần thuyết trình Chuyên đề Tốt nghiệp 1 (Buổi 18).
  </div>

  <div class="slide-footer">
    <span class="student-info">Hồ Lê Trung Bảo — 2374802010030 (Track DA)</span>
    <span>Trang 6 / 6</span>
  </div>
</div>

</body>
</html>
"""

with open(TEMP_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"1. Da tao file HTML slide ELT tai: {TEMP_HTML}")

# Xuat sang PDF bang Edge Headless
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
    TEMP_HTML
]

print("2. Dang xuat Slide PDF bang Microsoft Edge Headless...")
subprocess.run(cmd, check=True)

if os.path.exists(OUTPUT_PDF) and os.path.getsize(OUTPUT_PDF) > 0:
    print(f"[THANH CONG] Da tao Slide PDF thanh cong tai: {OUTPUT_PDF}")
    print(f"Kich thuoc file: {os.path.getsize(OUTPUT_PDF)} bytes")
else:
    print(f"[LOI] Khong the tao PDF slide!")

# Don dep file tam
if os.path.exists(TEMP_HTML):
    os.remove(TEMP_HTML)
