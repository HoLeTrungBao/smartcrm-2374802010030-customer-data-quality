# ==============================================================================
# Dockerfile — SmartCRM Customer Data Quality Pipeline (Track DA)
# Mekong Mobile - L7 Customer Data Quality Module
# Sinh viên: Hồ Lê Trung Bảo | MSSV: 2374802010030
# ==============================================================================

FROM python:3.11-slim AS base

# Ngăn chặn tạo file .pyc và bật unbuffered output cho logging thời gian thực
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    LOG_LEVEL=INFO \
    DATA_DIR=data/mau \
    DATABASE_URL=sqlite:///data/processed/warehouse.db \
    REPORTS_DIR=reports

WORKDIR /app

# Cài đặt các gói hệ thống cần thiết (nếu có)
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Python dependencies trước để tận dụng Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Tạo người dùng không đặc quyền (Non-root user) để tuân thủ Security Checklist
RUN useradd -u 10001 -m -s /bin/bash appuser

# Sao chép mã nguồn, cấu hình, dữ liệu mẫu và câu lệnh SQL
COPY configs/ ./configs/
COPY sql/ ./sql/
COPY src/ ./src/
COPY data/mau/ ./data/mau/

# Tạo các thư mục làm việc và phân quyền cho appuser
RUN mkdir -p data/processed data/raw reports docs && \
    chown -R appuser:appuser /app

# Chuyển sang user không đặc quyền
USER appuser

# Healthcheck kiểm tra tính toàn vẹn của CSDL kho Star Schema
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sqlite3; conn = sqlite3.connect('data/processed/warehouse.db'); cur = conn.cursor(); cur.execute('SELECT COUNT(*) FROM dim_customer'); assert cur.fetchone()[0] >= 0; conn.close()" || exit 1

# Mặc định thực thi pipeline trên tập dữ liệu mẫu và xuất báo cáo đối soát
CMD ["python", "-m", "src.pipeline", "--file-nguon", "data/mau/customers_sample.csv", "--xuat-bao-cao"]
