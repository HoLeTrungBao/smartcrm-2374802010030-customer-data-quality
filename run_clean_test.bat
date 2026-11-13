@echo off
REM ==============================================================================
REM run_clean_test.bat — Phép thử máy trắng tự động trên Windows (<= 2 lệnh)
REM Học phần: Chuyên đề Tốt nghiệp 1 (Track DA) · MSSV: 2374802010030
REM ==============================================================================
echo [1/2] Dang chay Pipeline ETL tren tap du lieu mau...
python -m src.pipeline --file-nguon data/mau/customers_sample.csv --xuat-bao-cao
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Pipeline gap su co! Ma thoat: %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

echo [2/2] Dang doi soat so dong du lieu kho...
python -m src.dashboard.so_sanh_dong
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Doi soat du lieu that bai! Ma thoat: %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

echo.
echo ==============================================================================
echo [THANH CONG] Phep thu may trang hoan tat xuat sac! (PASS)
echo ==============================================================================
