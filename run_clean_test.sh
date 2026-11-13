#!/usr/bin/env bash
# ==============================================================================
# run_clean_test.sh — White-box / Clean Machine Test for Linux / macOS (<= 2 commands)
# SmartCRM Data Quality Pipeline (Track DA) · MSSV: 2374802010030
# ==============================================================================
set -e

echo "[1/2] Running ETL Pipeline on sample dataset..."
python3 -m src.pipeline --file-nguon data/mau/customers_sample.csv --xuat-bao-cao

echo "[2/2] Reconciling data warehouse records..."
python3 -m src.dashboard.so_sanh_dong

echo ""
echo "=============================================================================="
echo "[SUCCESS] White-box clean machine test completed successfully! (PASS)"
echo "=============================================================================="
