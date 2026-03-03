# GIS Scripts

這個目錄包含用於地理信息系統分析和數據處理的 Python 腳本。

## 腳本說明

### 天氣分析腳本

#### 1. `cwa_api_client.py`
中央氣象局 API 客戶端，用於獲取台灣各地天氣數據。

**功能:**
- 獲取當前天氣觀測數據
- 獲取天氣預報
- 獲取地震資訊
- 獲取颱風資訊
- 獲取雷達圖像
- 數據導出功能

#### 2. `weather_data_processor.py`
天氣數據處理器，將 API 數據轉換為 GIS 格式並進行分析。

**功能:**
- 多地點天氣數據收集
- 創建 GeoDataFrame
- 溫度地圖生成
- 天氣模式分析
- 統計圖表生成
- 分析報告生成

#### 3. `run_weather_analysis.py`
主要執行腳本，運行完整的天氣數據分析工作流程。

### 空氣品質分析腳本

#### 4. `aqi_api_client.py`
環境部空氣品質指標 API 客戶端，用於獲取全台即時 AQI 數據。

**功能:**
- 獲取全台即時 AQI 數據
- 獲取特定監測站 AQI 數據
- 獲取特定縣市 AQI 數據
- 數據導出功能

#### 5. `aqi_visualizer.py`
空氣品質數據視覺化工具，創建交互式 AQI 地圖。

**功能:**
- AQI 數據收集和處理
- 創建 GeoDataFrame
- 生成交互式 Folium 地圖
- AQI 狀態顏色編碼
- 統計分析
- 詳細報告生成

#### 6. `run_aqi_analysis.py`
AQI 分析主要執行腳本，運行完整的空氣品質分析流程。

**功能:**
- 環境檢查和設定
- 自動化數據收集
- 完整分析流程
- 結果輸出

## 專案設定

### 自動設定
運行自動設定腳本：
```bash
python setup_aqi_project.py
```

這個腳本會：
- 檢查 Python 版本
- 安裝所有依賴
- 創建必要目錄
- 檢查環境設定
- 測試模組導入

### 手動設定
1. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```

2. 設定環境變數：
   在 `.env` 檔案中設定：
   ```env
   EPA_API_KEY=your_epa_api_key_here
   ```

3. 創建必要目錄：
   ```bash
   mkdir -p data/processed output/maps output/reports
   ```

## 使用方法

### 天氣分析
```bash
# 運行完整天氣分析
python run_weather_analysis.py

# 或單獨運行組件
python cwa_api_client.py
python weather_data_processor.py
```

### 空氣品質分析
```bash
# 運行完整 AQI 分析
python run_aqi_analysis.py

# 或單獨運行組件
python aqi_api_client.py
python aqi_visualizer.py
```

## 環境需求

### Python 套件
主要套件包括：
- `geopandas` - 地理數據處理
- `pandas` - 數據分析
- `folium` - 交互式地圖
- `requests` - HTTP 請求
- `matplotlib` - 圖表生成
- `python-dotenv` - 環境變數管理

### API 金鑰設定
需要以下 API 金鑰：
- `CWA_API_KEY` - 中央氣象局 API
- `EPA_API_KEY` - 環境部空氣品質 API

## 輸出檔案

### 數據檔案
- `data/processed/` - 處理後的數據 (CSV)
- `data/raw/` - 原始數據

### 視覺化輸出
- `output/maps/` - 交互式地圖 (HTML)
- `output/reports/` - 分析報告 (TXT)

### 日誌檔案
- `logs/` - 執行日誌

## 使用範例

### 天氣分析範例
```python
from weather_data_processor import WeatherDataProcessor

processor = WeatherDataProcessor()
df = processor.collect_weather_data(["臺北市", "新北市"])
map_path = processor.create_temperature_map(processor.create_geodataframe(df))
```

### AQI 分析範例
```python
from aqi_visualizer import AQIVisualizer

visualizer = AQIVisualizer()
df = visualizer.collect_aqi_data()
map_path = visualizer.create_aqi_map(visualizer.create_geodataframe(df))
```

## 注意事項

1. **API 限制**: 請遵守各 API 的使用限制
2. **網路連接**: 需要穩定的網路連接
3. **記憶體使用**: 大量數據處理可能需要較多記憶體
4. **座標系統**: 使用 WGS84 (EPSG:4326) 座標系統

## 故障排除

### 常見問題

**Q: API 金鑰錯誤**
A: 檢查 `.env` 檔案中的 API 金鑰設定

**Q: 模組導入失敗**
A: 重新安裝依賴：`pip install -r requirements.txt`

**Q: 地圖無法顯示**
A: 確保在瀏覽器中打開 HTML 檔案

**Q: 沒有數據返回**
A: 檢查網路連接和 API 金鑰有效性

## 擴展功能

可以考慮添加的功能：
- 歷史數據收集和時間序列分析
- 更多視覺化類型
- 數據預測模型
- 自動化定時執行
- 數據庫存儲
- Web 介面

請遵循相關 API 使用條款和數據使用規範。
