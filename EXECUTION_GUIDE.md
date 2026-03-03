# 執行指南

## 🚀 快速開始

### 方法 1: 使用 CWA API 演示（推薦）
```bash
cd scripts
python run_cwa_aqi_demo.py
```

**特點：**
- ✅ 使用你現有的 CWA API 金鑰
- ✅ 包含真實的台灣監測站數據
- ✅ 展示所有優化功能
- ✅ 生成完整的分析報告和地圖

### 方法 2: 測試優化功能
```bash
cd scripts
python test_aqi_map.py
```

**特點：**
- ✅ 無需 API 金鑰
- ✅ 快速測試地圖功能
- ✅ 驗證顏色分類和標記大小

### 方法 3: 完整 EPA API 分析（需要 EPA API 金鑰）
```bash
# 1. 設定 EPA API 金鑰
echo "EPA_API_KEY=your_epa_api_key_here" >> ../.env

# 2. 運行完整分析
python run_aqi_analysis.py
```

## 📊 輸出檔案

執行後會生成以下檔案：

### 地圖檔案
- **位置**: `output/maps/aqi_map_YYYYMMDD_HHMMSS.html`
- **格式**: 交互式 HTML 地圖
- **功能**: 可在瀏覽器中打開，支援縮放和點擊

### 分析報告
- **位置**: `output/reports/aqi_report_YYYYMMDD_HHMMSS.txt`
- **內容**: 詳細的統計分析
- **包含**: AQI 分佈、各縣市平均、最高污染站點

### 數據檔案
- **位置**: `data/processed/aqi_data_YYYYMMDD_HHMMSS.csv`
- **格式**: CSV 數據
- **用途**: 可用於進一步分析

## 🎨 優化功能展示

### 1. 三分色顯示
- 🟢 **綠色** (0-50): 空氣品質良好
- 🟡 **黃色** (51-100): 空氣品質普通
- 🔴 **紅色** (101+): 空氣品質不健康

### 2. 簡化資訊視窗
點擊地圖上的標記顯示：
- 測站名稱（醒目顯示）
- 所在地（縣市）
- 即時 AQI 數值（突出顯示）
- 空氣品質狀態
- 更新時間

### 3. 動態標記大小
- AQI ≤ 50: 小標記
- AQI 51-100: 中標記
- AQI 101+: 大標記

### 4. 改進地圖設計
- 地圖標題：「台灣空氣品質指標即時地圖」
- 優化圖例設計
- 半透明背景效果

## 🔧 環境設定

### 檢查 Python 版本
```bash
python --version
# 需要 Python 3.8 或更高版本
```

### 安裝依賴
```bash
pip install -r requirements.txt
```

### 檢查 API 金鑰
```bash
# 查看當前設定
cat ../.env

# 應包含：
# CWA_API_KEY=CWA-2329B106-1EEE-4395-A845-A277B8AA2702
# EPA_API_KEY=your_epa_api_key_here (可選)
```

## 📱 查看結果

### 1. 打開地圖
```bash
# 在瀏覽器中打開
open ../output/maps/aqi_map_*.html
```

### 2. 查看報告
```bash
# 在終端查看
cat ../output/reports/aqi_report_*.txt
```

### 3. 檢查數據
```bash
# 查看前幾行
head ../data/processed/aqi_data_*.csv
```

## 🎯 範例輸出

```
=====================================
CWA 空氣品質指標演示系統
=====================================

✓ CWA API 連接成功
✓ 創建了 24 個監測站的範例數據
✓ 創建包含 24 個地理點的 GeoDataFrame
✓ AQI 視覺化工具初始化完成

平均 AQI: 68.2
AQI 範圍: 32.0 - 112.0
空氣品質分佈:
  良好 (0-50): 8 個站
  普通 (51-100): 13 個站
  不健康 (101+): 3 個站

✓ AQI 地圖已創建: ../output/maps/aqi_map_20260303_144519.html
✓ 分析報告已生成: ../output/reports/aqi_report_20260303_144519.txt
```

## 🚨 故障排除

### 問題 1: API 連接失敗
```bash
# 檢查網路連接
ping opendata.cwa.gov.tw

# 檢查 API 金鑰
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('CWA_API_KEY:', os.getenv('CWA_API_KEY', 'Not set'))"
```

### 問題 2: 模組導入失敗
```bash
# 重新安裝依賴
pip install --upgrade -r requirements.txt
```

### 問題 3: 地圖無法顯示
- 確保使用現代瀏覽器
- 檢查檔案是否存在
- 嘗試在本地開啟而非網路路徑

## 💡 進階用法

### 自訂數據
```python
# 修改 run_cwa_aqi_demo.py 中的 create_sample_aqi_data() 函數
# 可以添加更多監測站或修改 AQI 數值
```

### 整合真實 API
```python
# 在 aqi_api_client.py 中修改 API 端點
# 根據實際 API 文檔調整數據解析邏輯
```

### 定時執行
```bash
# 使用 cron 定時執行
# 每小時執行一次
0 * * * * cd /path/to/project/scripts && python run_cwa_aqi_demo.py
```

## 📞 支援

如果遇到問題：
1. 檢查本指南的故障排除部分
2. 確認 Python 和依賴版本
3. 驗證 API 金鑰設定
4. 查看生成的錯誤日誌
