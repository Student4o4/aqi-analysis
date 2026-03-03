# Scripts 目錄檔案分析

## 📁 當前檔案列表 (13個檔案)

### 🔥 **核心必要檔案** (保留)
1. **`aqi_visualizer.py`** (15KB) - ✅ 核心 AQI 視覺化工具
2. **`distance_calculator.py`** (15KB) - ✅ 距離計算功能
3. **`complete_aqi_data.py`** (22KB) - ✅ 完整台灣監測站數據
4. **`run_complete_aqi_analysis.py`** (8KB) - ✅ 主要執行腳本 (完整版)
5. **`README.md`** (4KB) - ✅ 專案說明文檔

### 🤔 **重複/相似檔案** (可合併或刪除)

#### AQI API 客戶端 (3個相似檔案)
6. **`aqi_api_client.py`** (6KB) - ❌ EPA API 客戶端 (未使用)
7. **`cwa_aqi_client.py`** (5KB) - ❌ CWA AQI 客戶端 (功能重複)
8. **`cwa_api_client.py`** (10KB) - ⚠️ CWA 天氣 API 客戶端 (保留但可合併)

#### 執行腳本 (3個相似檔案)
9. **`run_aqi_analysis.py`** (5KB) - ❌ EPA 分析腳本 (未使用)
10. **`run_cwa_aqi_demo.py`** (10KB) - ⚠️ CWA 演示腳本 (可合併)
11. **`test_aqi_map.py`** (5KB) - ⚠️ 測試腳本 (可合併到主腳本)

### 🌤️ **天氣相關檔案** (獨立功能)
12. **`weather_data_processor.py`** (15KB) - ⚠️ 天氣數據處理 (獨立功能)
13. **`run_weather_analysis.py`** (5KB) - ⚠️ 天氣分析執行 (獨立功能)

## 🎯 **建議清理方案**

### 📋 **方案 A: 最小化清理** (推薦)
**保留 8 個檔案，刪除 5 個重複檔案**

#### ✅ **保留檔案**
- `aqi_visualizer.py` - 核心 AQI 視覺化
- `distance_calculator.py` - 距離計算
- `complete_aqi_data.py` - 完整數據
- `run_complete_aqi_analysis.py` - 主執行腳本
- `cwa_api_client.py` - CWA API (天氣功能)
- `weather_data_processor.py` - 天氣處理
- `run_weather_analysis.py` - 天氣分析
- `README.md` - 說明文檔

#### ❌ **刪除檔案**
- `aqi_api_client.py` - EPA API (未使用)
- `cwa_aqi_client.py` - 重複的 CWA AQI 客戶端
- `run_aqi_analysis.py` - EPA 分析腳本
- `run_cwa_aqi_demo.py` - 可合併到主腳本
- `test_aqi_map.py` - 可合併到主腳本

### 📋 **方案 B: 極簡清理**
**保留 6 個檔案，刪除 7 個檔案**

#### ✅ **保留檔案**
- `aqi_visualizer.py` - 核心 AQI 視覺化
- `distance_calculator.py` - 距離計算
- `complete_aqi_data.py` - 完整數據
- `run_complete_aqi_analysis.py` - 主執行腳本
- `README.md` - 說明文檔
- `weather_data_processor.py` - 保留天氣功能

#### ❌ **刪除檔案**
- `aqi_api_client.py` - EPA API
- `cwa_aqi_client.py` - 重複 CWA 客戶端
- `cwa_api_client.py` - CWA API (可整合到主腳本)
- `run_aqi_analysis.py` - EPA 分析
- `run_cwa_aqi_demo.py` - 演示腳本
- `test_aqi_map.py` - 測試腳本
- `run_weather_analysis.py` - 可整合到主腳本

### 📋 **方案 C: 功能分組清理**
**按功能分組，每組保留一個主檔案**

#### 🌍 **AQI 組** (保留 3 個)
- `aqi_visualizer.py` - 視覺化核心
- `distance_calculator.py` - 距離計算
- `run_complete_aqi_analysis.py` - 主執行

#### 🌤️ **天氣組** (保留 2 個)
- `weather_data_processor.py` - 天氣處理
- `cwa_api_client.py` - CWA API

#### 📊 **數據組** (保留 1 個)
- `complete_aqi_data.py` - 完整數據

#### 📝 **文檔組** (保留 1 個)
- `README.md` - 說明文檔

#### ❌ **刪除檔案** (8 個)
- `aqi_api_client.py`
- `cwa_aqi_client.py`
- `run_aqi_analysis.py`
- `run_cwa_aqi_demo.py`
- `test_aqi_map.py`
- `run_weather_analysis.py`

## 🔧 **具體執行建議**

### 步驟 1: 備份重要檔案
```bash
# 建立備份目錄
mkdir backup_scripts
cp aqi_visualizer.py backup_scripts/
cp distance_calculator.py backup_scripts/
cp complete_aqi_data.py backup_scripts/
cp run_complete_aqi_analysis.py backup_scripts/
```

### 步驟 2: 刪除不需要的檔案
```bash
# 刪除重複的 EPA 相關檔案
rm aqi_api_client.py
rm run_aqi_analysis.py

# 刪除重複的 CWA 客戶端
rm cwa_aqi_client.py

# 刪除可合併的測試和演示檔案
rm test_aqi_map.py
rm run_cwa_aqi_demo.py
```

### 步驟 3: 更新 README 和執行腳本
- 更新 `README.md` 移除已刪除檔案的說明
- 在 `run_complete_aqi_analysis.py` 中整合測試功能

## 📊 **清理後效果**

### 🎯 **方案 A 效果**
- **檔案數量**: 13 → 8 (減少 38%)
- **程式碼行數**: 約 100KB → 85KB
- **功能完整性**: 100% 保持
- **維護複雜度**: 顯著降低

### 🎯 **方案 B 效果**
- **檔案數量**: 13 → 6 (減少 54%)
- **程式碼行數**: 約 100KB → 70KB
- **功能完整性**: 95% 保持
- **維護複雜度**: 大幅降低

## 🚀 **推薦執行**

**建議採用方案 A**，因為：
1. 保留所有核心功能
2. 刪除明顯重複的檔案
3. 維護獨立的天氣分析功能
4. 風險最低，效果明顯

**執行後的 scripts 目錄將更加清晰易維護！**
