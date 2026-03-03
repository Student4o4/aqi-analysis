# GIS Scripts

這個目錄包含用於地理信息系統分析和數據處理的 Python 腳本。

## 📁 檔案結構 (清理後: 8個核心檔案)

### 🌍 **AQI 空氣品質分析** (核心功能)

#### 1. `aqi_visualizer.py` (15KB)
**核心 AQI 視覺化工具**
- AQI 數據收集和處理
- 創建 GeoDataFrame
- 生成交互式 Folium 地圖
- AQI 狀態顏色編碼 (三分色)
- 統計分析和報告生成

#### 2. `distance_calculator.py` (15KB)
**距離計算器**
- 計算監測站到台北車站的精確距離
- 使用 geodesic 演算法 (WGS84)
- 生成距離統計報告
- CSV 格式輸出結果

#### 3. `complete_aqi_data.py` (22KB)
**完整台灣監測站數據生成器**
- 116 個台灣完整監測站
- 涵蓋 22 個縣市
- 4 種區域類型 (都市、工業、郊區、離島)
- 真實 AQI 數據模擬

#### 4. `run_complete_aqi_analysis.py` (8KB)
**主要執行腳本** ⭐
- 完整 AQI 分析工作流程
- 整合所有 AQI 功能
- 生成地圖、報告、距離計算
- **推薦主要執行檔案**

### 🌤️ **天氣分析功能**

#### 5. `cwa_api_client.py` (10KB)
**中央氣象局 API 客戶端**
- 獲取當前天氣觀測數據
- 獲取天氣預報
- 獲取地震資訊
- 獲取颱風資訊

#### 6. `weather_data_processor.py` (15KB)
**天氣數據處理器**
- 多地點天氣數據收集
- 創建溫度地圖
- 天氣模式分析
- 統計圖表生成

#### 7. `run_weather_analysis.py` (5KB)
**天氣分析執行腳本**
- 完整天氣分析流程
- 溫度地圖生成
- 天氣統計報告

### 📝 **文檔**

#### 8. `README.md` (4KB)
**專案說明文檔** (本檔案)
- 完整的使用說明
- 環境設定指南
- 故障排除

## 🚀 **使用方法**

### 🌍 **AQI 分析 (推薦)**
```bash
# 完整的 116 個監測站分析
python run_complete_aqi_analysis.py

# 輸出檔案:
# - 地圖: ../output/maps/aqi_map_*.html
# - 報告: ../output/reports/aqi_report_*.txt
# - 距離: ../output/complete_analysis_distances_*.csv
```

### 🌤️ **天氣分析**
```bash
# 天氣數據分析
python run_weather_analysis.py

# 輸出檔案:
# - 溫度地圖: ../output/maps/temperature_map_*.html
# - 天氣報告: ../output/reports/weather_report_*.txt
```

### 📊 **單獨功能**
```bash
# 只生成距離計算
python distance_calculator.py

# 只生成完整數據
python complete_aqi_data.py
```

## 🎯 **核心功能展示**

### 🗺️ **優化地圖功能**
- ✅ **三分色顯示**: 綠色(0-50)、黃色(51-100)、紅色(101+)
- ✅ **簡化資訊視窗**: 站名、縣市、即時 AQI 數值
- ✅ **動態標記大小**: AQI 越高標記越大
- ✅ **改進圖例和標題設計**

### 📈 **數據完整性**
- ✅ **116 個完整監測站** (從 20 個擴展)
- ✅ **22 個縣市完整覆蓋**
- ✅ **4 種區域類型真實模擬**
- ✅ **精確空間距離計算**

## 🔧 **環境需求**

### Python 套件
```bash
pip install -r requirements.txt
```

主要套件：
- `geopandas` - 地理數據處理
- `pandas` - 數據分析
- `folium` - 交互式地圖
- `requests` - HTTP 請求
- `geopy` - 地理距離計算

### API 金鑰
在 `.env` 檔案中設定：
```env
CWA_API_KEY=CWA-2329B106-1EEE-4395-A845-A277B8AA2702
```

## 📁 **輸出檔案結構**

```
output/
├── maps/                    # 交互式地圖
│   ├── aqi_map_*.html      # AQI 地圖
│   └── temperature_map_*.html # 溫度地圖
├── reports/                 # 分析報告
│   ├── aqi_report_*.txt    # AQI 報告
│   └── weather_report_*.txt # 天氣報告
└── complete_analysis_distances_*.csv # 距離計算

data/processed/
└── complete_taiwan_aqi_*.csv # 完整監測站數據
```

## 🎯 **快速開始**

### 1. 環境檢查
```bash
python -c "import pandas, geopandas, folium; print('✓ 環境 OK')"
```

### 2. 執行完整分析
```bash
python run_complete_aqi_analysis.py
```

### 3. 查看結果
```bash
# 在瀏覽器中打開地圖
open ../output/maps/aqi_map_*.html
```

## 📊 **清理歷程**

**清理前**: 13 個檔案 (約 100KB)  
**清理後**: 8 個檔案 (約 85KB)  
**減少**: 38% 檔案數量，功能 100% 保持

### 🗑️ **已刪除的檔案**
- `aqi_api_client.py` - EPA API (未使用)
- `cwa_aqi_client.py` - 重複的 CWA 客戶端
- `run_aqi_analysis.py` - EPA 分析腳本
- `run_cwa_aqi_demo.py` - 演示腳本 (已整合)
- `test_aqi_map.py` - 測試腳本 (已整合)

## 🚨 **注意事項**

1. **API 限制**: 請遵守 CWA API 使用規範
2. **網路連接**: 需要穩定的網路連接
3. **記憶體使用**: 116 個監測站數據建議 4GB+ 記憶體
4. **座標系統**: 使用 WGS84 (EPSG:4326)

## 📞 **支援**

如需幫助：
1. 檢查 `SCRIPT_ANALYSIS.md` 了解詳細分析
2. 確認 Python 版本 (3.8+)
3. 驗證 API 金鑰設定
4. 查看生成的錯誤日誌

---
**最後更新**: 2024-03-03  
**狀態**: ✅ 已清理，功能完整
