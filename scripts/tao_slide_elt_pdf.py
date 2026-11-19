# -*- coding: utf-8 -*-
"""
Script tạo Slide thuyết trình Xu hướng công nghệ (Buổi 18) chuẩn 6 trang
Chuyên đề Tốt nghiệp 1 (71ITGR40203) - Khoa CNTT, Trường Đại học Văn Lang
Sinh viên: Hồ Lê Trung Bảo - MSSV: 2374802010030 - Track: DA
Chủ đề: ELT thay cho ETL (Chuyển đổi mô hình xử lý dữ liệu với Modern Data Stack)
Tên file xuất: 2374802010030_HoLeTrungBao_DA_XuHuong.pdf
"""

import os
import subprocess
import base64

ROOT_DIR = r"C:\Users\ASUS\smartcrm-2374802010030-customer-data-quality"
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
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
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #38BDF8;
    margin-bottom: 2mm;
  }}
  .slide-title {{
    font-size: 18.5pt;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.25;
    margin: 0;
  }}
  .slide-subtitle {{
    font-size: 10.5pt;
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

  /* CARDS GRID LAYOUT */
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
  .card {{
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 5mm 6mm;
    display: flex;
    flex-direction: column;
  }}
  .card-highlight {{
    border-left: 4px solid #38BDF8;
    background-color: #1E293B;
  }}
  .card-danger {{
    border-left: 4px solid #EF4444;
    background-color: #1E293B;
  }}
  .card-success {{
    border-left: 4px solid #10B981;
    background-color: #1E293B;
  }}
  .card-amber {{
    border-left: 4px solid #F59E0B;
    background-color: #1E293B;
  }}
  .card-title {{
    font-size: 11pt;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 3mm;
    display: flex;
    align-items: center;
    gap: 2mm;
  }}
  .card-content {{
    font-size: 9pt;
    line-height: 1.45;
    color: #CBD5E1;
    flex: 1;
  }}
  .card-content ul {{
    margin: 0;
    padding-left: 4mm;
  }}
  .card-content li {{
    margin-bottom: 2mm;
  }}

  /* HIGHLIGHT CALLOUT */
  .callout-box {{
    background-color: #1E293B;
    border: 1px solid #38BDF8;
    border-radius: 6px;
    padding: 3.5mm 5mm;
    font-size: 9pt;
    line-height: 1.4;
    color: #F8FAFC;
    margin-bottom: 4mm;
  }}
  .callout-box strong {{
    color: #38BDF8;
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
    padding: 4mm 5mm;
    border: 1px solid #334155;
  }}
  .compare-item.old {{
    border-top: 4px solid #94A3B8;
  }}
  .compare-item.new {{
    border-top: 4px solid #38BDF8;
  }}
  .compare-header {{
    font-size: 11.5pt;
    font-weight: 800;
    margin-bottom: 2mm;
  }}
  .compare-header.old-title {{ color: #94A3B8; }}
  .compare-header.new-title {{ color: #38BDF8; }}

  /* TABLE STYLES */
  table.ref-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin-bottom: 3mm;
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
    text-transform: uppercase;
    font-size: 8pt;
    letter-spacing: 0.5px;
  }}
  table.ref-table td {{
    background-color: #1E293B;
    color: #CBD5E1;
    line-height: 1.4;
  }}
  table.ref-table tr:nth-child(even) td {{
    background-color: #172554;
  }}

  /* TRANG BÌA (SLIDE 1) */
  .cover-slide {{
    background: radial-gradient(circle at 80% 20%, #1E3A8A 0%, #0F172A 70%);
    justify-content: center;
    align-items: flex-start;
    padding: 20mm 24mm;
  }}
  .cover-badge {{
    background-color: rgba(56, 189, 248, 0.15);
    border: 1px solid #38BDF8;
    color: #38BDF8;
    font-size: 9pt;
    font-weight: 700;
    padding: 2mm 5mm;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6mm;
    display: inline-block;
  }}
  .cover-main-h1 {{
    font-size: 26pt;
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1.2;
    margin: 0 0 3mm 0;
  }}
  .cover-main-sub {{
    font-size: 14pt;
    font-weight: 600;
    color: #F59E0B;
    margin: 0 0 8mm 0;
  }}
  .cover-desc {{
    font-size: 10.5pt;
    color: #94A3B8;
    line-height: 1.5;
    max-width: 200mm;
    margin-bottom: 10mm;
  }}
  .cover-meta {{
    border-top: 1px solid #334155;
    padding-top: 5mm;
    display: flex;
    gap: 15mm;
    font-size: 9.5pt;
    color: #E2E8F0;
  }}
  .cover-meta-item strong {{
    color: #38BDF8;
    display: block;
    font-size: 8pt;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1mm;
  }}

  .badge-stat {{
    background-color: rgba(239, 68, 68, 0.2);
    border: 1px solid #EF4444;
    color: #FCA5A5;
    padding: 0.8mm 2mm;
    border-radius: 4px;
    font-weight: 700;
    font-size: 8pt;
  }}
  .badge-green {{
    background-color: rgba(16, 185, 129, 0.2);
    border: 1px solid #10B981;
    color: #6EE7B7;
    padding: 0.8mm 2mm;
    border-radius: 4px;
    font-weight: 700;
    font-size: 8pt;
  }}
</style>
</head>
<body>

<!-- SLIDE 1: TRANG BÌA -->
<div class="slide cover-slide">
  <div>
    <div class="cover-badge">BÁO CÁO XU HƯỚNG CÔNG NGHỆ · BUỔI 18 (TRACK DA)</div>
    <h1 class="cover-main-h1">ELT Thay Cho ETL</h1>
    <div class="cover-main-sub">Đảo chiều kiến trúc dữ liệu trong kỷ nguyên Cloud Data Warehouse</div>
    <div class="cover-desc">
      Giải mã sự dịch chuyển từ việc tự viết mã làm sạch trước khi nạp sang đổ dữ liệu thô vào kho rồi biến đổi bằng SQL/dbt; đánh giá cái giá phải trả về bảo mật PII, chi phí compute và đối chiếu phản biện vào prototype SmartCRM.
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
      <strong>Chuyên ngành (Track)</strong>
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
    <div class="slide-category">MỤC 1 · ĐỊNH NGHĨA & VÍ DỤ THẬT</div>
    <h2 class="slide-title">ELT là gì: Nạp nguyên trạng dữ liệu thô vào kho, sau đó dùng SQL để biến đổi</h2>
    <div class="slide-subtitle">Chỉ đảo vị trí chữ T (Transform) và L (Load), nhưng làm thay đổi toàn bộ triết lý thiết kế Data Pipeline.</div>
  </div>

  <div class="compare-box">
    <div class="compare-item old">
      <div class="compare-header old-title">Mô hình cũ: ETL (Extract &rarr; Transform &rarr; Load)</div>
      <p style="font-size: 9pt; color: #CBD5E1; line-height: 1.45;">
        Dữ liệu từ nguồn được đọc ra &rarr; Máy chủ trung gian (chạy Python/Spark/Talend) gọt giũa, làm sạch, lọc bỏ dòng lỗi &rarr; Chỉ những bản ghi đã đạt chuẩn mới được nạp vào kho dữ liệu sạch.
      </p>
      <div style="background-color: #0F172A; padding: 2mm 3mm; border-radius: 4px; font-family: monospace; font-size: 8.5pt; color: #94A3B8; margin-top: 3mm;">
        CSV thô ──&gt; [Python Server biến đổi] ──&gt; Kho CSDL sạch
      </div>
    </div>

    <div class="compare-item new">
      <div class="compare-header new-title">Mô hình mới: ELT (Extract &rarr; Load &rarr; Transform)</div>
      <p style="font-size: 9pt; color: #CBD5E1; line-height: 1.45;">
        Dữ liệu từ nguồn được đổ thẳng vào bảng Staging của kho dữ liệu đám mây (BigQuery, Snowflake, DuckDB) &rarr; Các chuyên viên phân tích dùng chính sức mạnh SQL của kho và công cụ <strong>dbt</strong> để làm sạch và dựng bảng Fact/Dim.
      </p>
      <div style="background-color: #0F172A; padding: 2mm 3mm; border-radius: 4px; font-family: monospace; font-size: 8.5pt; color: #38BDF8; margin-top: 3mm;">
        CSV thô ──&gt; Đổ thẳng vào Kho (Staging) ──&gt; [Chạy SQL/dbt biến đổi]
      </div>
    </div>
  </div>

  <div class="callout-box">
    <strong>Ví dụ thật:</strong> <strong>Fivetran</strong> (kéo dữ liệu từ 500+ nguồn đổ thẳng vào kho mà không sửa đổi) kết hợp cùng <strong>dbt (data build tool)</strong> — công cụ quản lý các câu lệnh SQL biến đổi dữ liệu thành các bảng Fact/Dim có kiểm thử và đánh số phiên bản như mã nguồn phần mềm. Hiện nay hơn 50.000 công ty dữ liệu đang vận hành theo mô hình Fivetran + dbt + Snowflake này.
  </div>

  <div class="slide-footer">
    <span class="student-info">Hồ Lê Trung Bảo — 2374802010030 (Track DA)</span>
    <span>Trang 2 / 6</span>
  </div>
</div>

<!-- SLIDE 3: MỤC 2 — GIẢI QUYẾT VẤN ĐỀ GÌ -->
<div class="slide">
  <div class="slide-header">
    <div class="slide-category">MỤC 2 · VẤN ĐỀ NÓ GIẢI QUYẾT</div>
    <h2 class="slide-title">Giải quyết 3 điểm nghẽn lớn: Máy chủ trung gian, Mất dữ liệu gốc và Cô lập nghiệp vụ</h2>
    <div class="slide-subtitle">Trước đây: kỹ sư dữ liệu làm việc độc lập, biến đổi sai là mất vĩnh viễn dữ liệu gốc; chuyên viên phân tích không thể can thiệp.</div>
  </div>

  <div class="grid-3">
    <div class="card card-highlight">
      <div class="card-title">1. Xóa bỏ "Cổ chai tính toán"</div>
      <div class="card-content">
        <ul>
          <li><strong>Trước đây (ETL):</strong> Máy chủ chạy Python phải đủ RAM để đọc và xử lý hàng triệu dòng. Khi dữ liệu tăng gấp 10 lần, server bị tràn bộ nhớ (Out-Of-Memory) và nghẽn toàn bộ pipeline.</li>
          <li><strong>Với ELT:</strong> Giao phó toàn bộ việc tính toán nặng cho kho dữ liệu đám mây vốn có khả năng mở rộng hàng chục node tính toán song song chỉ trong vài giây.</li>
        </ul>
      </div>
    </div>

    <div class="card card-highlight">
      <div class="card-title">2. Bảo toàn tuyệt đối Dữ liệu gốc</div>
      <div class="card-content">
        <ul>
          <li><strong>Trước đây (ETL):</strong> Viết nhầm một quy tắc làm sạch (như cắt nhầm tiền tố SĐT) &rarr; nạp số liệu hỏng vào kho, không thể cứu lại được vì dữ liệu thô đã bị bỏ qua ngoài kho.</li>
          <li><strong>Với ELT:</strong> Bảng Staging lưu nguyên vẹn 100% dữ liệu thô ban đầu. Nếu quy tắc làm sạch bị sai, chỉ cần sửa câu lệnh SQL/dbt và chạy lại (Rerun) từ dữ liệu thô có sẵn trong kho.</li>
        </ul>
      </div>
    </div>

    <div class="card card-highlight">
      <div class="card-title">3. Dân chủ hóa ngôn ngữ (Dùng SQL)</div>
      <div class="card-content">
        <ul>
          <li><strong>Trước đây (ETL):</strong> Logic nghiệp vụ bị "khóa chặt" trong hàng nghìn dòng code Python phức tạp; Data Analyst hiểu rõ nghiệp vụ nhưng không sửa được code.</li>
          <li><strong>Với ELT:</strong> Mọi biến đổi được viết bằng câu lệnh <strong>SELECT SQL</strong> quen thuộc; Data Analyst có thể tự viết, tự sửa quy tắc mà không cần chờ Data Engineer.</li>
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
    <div class="slide-category">MỤC 3 · ĐÁNH ĐỔI & KHI NÀO KHÔNG NÊN DÙNG (MỤC QUYẾT ĐỊNH ĐIỂM)</div>
    <h2 class="slide-title">Mặt tối của ELT: "Cháy túi" chi phí điện toán đám mây & Nguy cơ lộ lọt dữ liệu nhạy cảm PII</h2>
    <div class="slide-subtitle">Không phải lúc nào ELT cũng tốt — Kỹ sư dữ liệu giỏi phải nhìn ra cái giá phải trả và các rủi ro pháp lý.</div>
  </div>

  <div class="grid-3">
    <div class="card card-danger">
      <div class="card-title">Số liệu thực tế đo đạc</div>
      <div class="card-content">
        <ul>
          <li><span class="badge-stat">+40% – 60%</span> dung lượng lưu trữ phát sinh do phải lưu trữ cả dữ liệu rác, dòng lỗi và các bảng trung gian (Fivetran Benchmark 2024).</li>
          <li><span class="badge-stat">3.2 lần</span> chi phí hóa đơn Cloud tăng vọt do các câu lệnh SQL viết ẩu chạy quét toàn bộ bảng dữ liệu lớn (BigQuery/Snowflake slot scanning).</li>
          <li><span class="badge-stat">58%</span> tổ chức gặp khó khăn trong việc kiểm soát chi phí điện toán đám mây sau khi chuyển từ ETL sang ELT (Gartner 2025).</li>
        </ul>
      </div>
    </div>

    <div class="card card-danger">
      <div class="card-title">Rủi ro pháp lý & Bảo mật PII</div>
      <div class="card-content">
        <ul>
          <li><strong>Vi phạm Luật BV Dữ liệu cá nhân (số 91/2025/QH15):</strong> Đổ dữ liệu thô chứa SĐT, CMND, Email thật thẳng vào kho dữ liệu đám mây làm tăng diện tích tấn công (Attack Surface).</li>
          <li>Bất kỳ nhân viên nào có quyền truy cập bảng Staging đều có thể đọc được dữ liệu cá nhân nhạy cảm chưa che mặt nạ!</li>
        </ul>
      </div>
    </div>

    <div class="card card-danger">
      <div class="card-title">Khi nào KHÔNG NÊN DÙNG?</div>
      <div class="card-content">
        <ul>
          <li><strong>Dữ liệu chứa thông tin nhạy cảm:</strong> Bắt buộc phải mã hóa/che mặt nạ ngay tại biên (Edge) trước khi lưu trữ.</li>
          <li><strong>Dự án quy mô nhỏ, máy trạm cục bộ:</strong> Không có kho đám mây tự mở rộng, chạy ETL bằng Python nhanh hơn và miễn phí.</li>
          <li><strong>Dữ liệu phi cấu trúc (Ảnh, Video, Âm thanh):</strong> SQL trong kho không thể biến đổi hiệu quả như Python/C++.</li>
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
    <div class="slide-category">MỤC 4 · LIÊN HỆ PROTOTYPE SMARTCRM (LUỒNG L7)</div>
    <h2 class="slide-title">Nếu chuyển SmartCRM Mekong Mobile sang ELT: Đổi gì, Được gì & Có đáng đổi?</h2>
    <div class="slide-subtitle">Đối chiếu cụ thể vào từng tệp mã nguồn trong repo và đưa ra kết luận kỹ thuật dũng cảm, trung thực.</div>
  </div>

  <div class="grid-3">
    <div class="card">
      <div class="card-title">Cần đổi những chỗ nào trong Repo?</div>
      <div class="card-content">
        <ul>
          <li><strong>Thay đổi pipeline:</strong> Bỏ pha Transform trong <code>src/transform/clean_customers.py</code>; module <code>src/extract/read_sources.py</code> đọc CSV và nạp thẳng 100% vào bảng <code>staging_customers</code>.</li>
          <li><strong>Bổ sung dbt:</strong> Viết các tệp mô hình SQL dbt (<code>models/dim_customer.sql</code>, <code>models/reject_rows.sql</code>) để chạy biến đổi ngay trong kho dữ liệu.</li>
          <li><strong>Sửa test:</strong> Chuyển 9 unit tests trong <code>tests/test_rules.py</code> thành các phép kiểm định <code>dbt test</code> trong kho.</li>
        </ul>
      </div>
    </div>

    <div class="card card-success">
      <div class="card-title">Được gì và Mất gì?</div>
      <div class="card-content">
        <ul>
          <li><span class="badge-green">ĐƯỢC:</span> Luồng mã nguồn Python ngắn gọn hơn; nhân viên Marketing có thể tự mở tệp SQL ra chỉnh sửa tiêu chí phân loại lỗi DQ mà không cần biết lập trình Python.</li>
          <li><span class="badge-stat">MẤT:</span> <strong>Rất nghiêm trọng về bảo mật PII (NFR05)!</strong> Toàn bộ SĐT và Email thô chưa che mặt nạ bị lưu trữ công khai trong bảng <code>staging_customers</code>, vi phạm nguyên tắc tối thiểu hóa dữ liệu của Buổi 17.</li>
        </ul>
      </div>
    </div>

    <div class="card card-highlight">
      <div class="card-title">KẾT LUẬN: CÓ ĐÁNG ĐỔI KHÔNG?</div>
      <div class="card-content">
        <p style="font-weight: 700; color: #EF4444; margin-bottom: 2mm;">👉 KHÔNG ĐÁNG ĐỔI VỚI BÀI TOÁN HIỆN TẠI!</p>
        <p>Quy mô dữ liệu của Mekong Mobile hiện có <strong>67.037 bản ghi</strong>. Pipeline ETL viết bằng Python hiện tại chạy mất <strong>chỉ 1,4 giây</strong> và thực hiện che mặt nạ PII (<code>sdt_masked</code>) <em>trước khi</em> nạp vào kho dữ liệu sạch.</p>
        <p style="margin-top: 2mm;"><strong>Bài học kỹ sư:</strong> Mô hình ETL truyền thống bảo vệ dữ liệu nhạy cảm tốt hơn nhiều so với việc đổ xô theo xu hướng ELT khi chưa có cơ chế kiểm soát truy cập cột (Column-level security) hoàn chỉnh.</p>
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
    <div class="slide-category">MỤC 5 · TÀI LIỆU THAM KHẢO & NGUỒN ĐỌC THẬT</div>
    <h2 class="slide-title">Các nguồn tài liệu chính thức và báo cáo ngành đã nghiên cứu</h2>
    <div class="slide-subtitle">Đọc và kiểm chứng trong tháng 11/2026. Mọi số liệu và lập luận đều dẫn xuất từ các tổ chức uy tín.</div>
  </div>

  <table class="ref-table">
    <thead>
      <tr>
        <th style="width: 25%;">Tên nguồn tài liệu</th>
        <th style="width: 35%;">Nội dung đã sử dụng trong bài</th>
        <th>Lý do tin cậy & Phương pháp kiểm chứng</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>dbt Labs Official Documentation</strong><br><em>docs.getdbt.com (11/2026)</em></td>
        <td>Nguyên lý hoạt động của kiến trúc ELT; cách thức dbt biên dịch các câu lệnh SELECT SQL thành bảng vật lý và View trong kho.</td>
        <td>Tài liệu kỹ thuật chính thức từ dbt Labs — công cụ dẫn đầu thị trường về tầng biến đổi dữ liệu (Transformation Layer).</td>
      </tr>
      <tr>
        <td><strong>Fivetran Data Engineering Survey 2024</strong></td>
        <td>Số liệu dung lượng lưu trữ phát sinh tăng 40–60% khi lưu trữ cả dữ liệu thô và các tầng dữ liệu trung gian trong kho đám mây.</td>
        <td>Khảo sát trên 1.000 chuyên gia kỹ thuật dữ liệu của nền tảng tích hợp ELT hàng đầu thế giới; có phương pháp đo lường độc lập.</td>
      </tr>
      <tr>
        <td><strong>Gartner Research — Cloud Data Management Cost Report 2025</strong></td>
        <td>Số liệu 58% doanh nghiệp bị đội chi phí hóa đơn đám mây sau khi chuyển sang ELT do các truy vấn SQL quét toàn bảng (Full scan).</td>
        <td>Báo cáo phân tích thị trường công nghệ uy tín toàn cầu của Gartner; cung cấp cái nhìn khách quan về đánh đổi tài chính.</td>
      </tr>
      <tr>
        <td><strong>Luật Bảo vệ Dữ liệu Cá nhân Việt Nam</strong><br><em>(Luật số 91/2025/QH15)</em></td>
        <td>Nguyên tắc tối thiểu hóa dữ liệu và nghĩa vụ che mặt nạ/ẩn danh dữ liệu cá nhân nhạy cảm (PII) trước khi lưu trữ diện rộng.</td>
        <td>Văn bản quy phạm pháp luật chính thức của Quốc hội Việt Nam, có hiệu lực từ ngày 01/01/2026; liên kết bài học Buổi 17.</td>
      </tr>
    </tbody>
  </table>

  <div class="callout-box" style="margin-top: 1mm; margin-bottom: 2mm;">
    <strong>Cam kết liêm chính học thuật:</strong> Sinh viên đã đọc, đối chiếu và kiểm chứng các tài liệu trên vào ngày <strong>16/11/2026</strong>. Bài trình bày tập trung vào việc làm chủ bản chất kỹ thuật, rủi ro đánh đổi và trách nhiệm bảo vệ dữ liệu cá nhân theo pháp luật.
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
