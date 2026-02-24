# GIS Scripts

這個目錄包含用於地理信息系統分析和天氣數據處理的 Python 腳本。

## 腳本說明

### 1. `cwa_api_client.py`
中央氣象局 API 客戶端，用於獲取台灣各地天氣數據。

**功能:**
- 獲取當前天氣觀測數據
- 獲取天氣預報
- 獲取地震資訊
- 獲取颱風資訊
- 獲取雷達圖像
- 數據導出功能

**使用方法:**
```python
from cwa_api_client import CWAClient

client = CWAClient()
weather = client.get_current_weather("臺北市")
```

### 2. `weather_data_processor.py`
天氣數據處理器，將 API 數據轉換為 GIS 格式並進行分析。

**功能:**
- 多地點天氣數據收集
- 創建 GeoDataFrame
- 溫度地圖生成
- 天氣模式分析
- 統計圖表生成
- 分析報告生成

**使用方法:**
```python
from weather_data_processor import WeatherDataProcessor

processor = WeatherDataProcessor()
df = processor.collect_weather_data(["臺北市", "新北市"])
gdf = processor.create_geodataframe(df)
map_path = processor.create_temperature_map(gdf)
```

### 3. `run_weather_analysis.py`
主要執行腳本，運行完整的天氣數據分析工作流程。

**功能:**
- 環境設定檢查
- 自動化數據收集
- 完整分析流程
- 結果輸出

**使用方法:**
```bash
cd scripts
python run_weather_analysis.py
```

## 環境需求

### Python 套件
```bash
pip install -r requirements.txt
```

主要套件:
- `geopandas` - 地理數據處理
- `requests` - HTTP 請求
- `pandas` - 數據分析
- `matplotlib` - 圖表生成
- `folium` - 交互式地圖
- `python-dotenv` - 環境變數管理

### 環境變數設定
在專案根目錄的 `.env` 檔案中設定:

```env
CWA_API_KEY=your_api_key_here
```

## 輸出檔案

### 數據檔案
- `../data/processed/` - 處理後的天氣數據 (CSV)
- `../output/exports/` - 導出的原始數據

### 視覺化輸出
- `../output/maps/` - 交互式地圖 (HTML)
- `../output/reports/` - 分析報告 (TXT)

### 日誌檔案
- `../logs/` - 執行日誌

## 使用範例

### 基本使用
```python
# 獲取單一地點天氣
from cwa_api_client import CWAClient

client = CWAClient()
weather = client.get_current_weather("臺北市")
print(weather)

# 批量處理多地點
from weather_data_processor import WeatherDataProcessor

processor = WeatherDataProcessor()
locations = ["臺北市", "新北市", "桃園市"]
df = processor.collect_weather_data(locations)
```

### 完整分析
```bash
# 運行完整分析流程
python run_weather_analysis.py
```

## 注意事項

1. **API 限制**: CWA API 有請求頻率限制，請避免過於頻繁的請求
2. **數據品質**: 某些地點可能暫時無法提供數據，腳本會自動跳過
3. **網路連接**: 需要穩定的網路連接來獲取 API 數據
4. **記憶體使用**: 大量地點的數據處理可能需要較多記憶體

## 故障排除

### 常見問題

**Q: API 金鑰錯誤**
A: 檢查 `.env` 檔案中的 `CWA_API_KEY` 是否正確設定

**Q: 網路連接失敗**
A: 檢查網路連接和防火牆設定

**Q: 某些地點無數據**
A: 這是正常現象，某些監測站可能暫時離線

**Q: 地圖無法顯示**
A: 確保在瀏覽器中打開 HTML 檔案，並檢查網路連接

## 擴展功能

可以考慮添加的功能:
- 歷史數據收集和時間序列分析
- 更多視覺化類型 (風向圖、降雨圖等)
- 數據預測模型
- 自動化定時執行
- 數據庫存儲
- Web 介面

## 授權

請遵循相關 API 使用條款和數據使用規範。
