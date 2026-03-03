#!/usr/bin/env python3
"""
CWA AQI Demo - 使用 CWA API 和範例數據
Central Weather Administration AQI Demo

This script demonstrates AQI visualization using CWA API and sample data.
"""

import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime
from aqi_visualizer import AQIVisualizer

def create_sample_aqi_data():
    """Create realistic sample AQI data for Taiwan"""
    # Real Taiwan monitoring stations with sample AQI values
    sample_data = [
        {'SiteName': '台北', 'County': '臺北市', 'AQI': 45, 'Latitude': 25.0320, 'Longitude': 121.5654, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 12, 'PM10': 18, 'O3': 35, 'Status': '良好'},
        {'SiteName': '松山', 'County': '臺北市', 'AQI': 52, 'Latitude': 25.0500, 'Longitude': 121.5770, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 15, 'PM10': 22, 'O3': 42, 'Status': '普通'},
        {'SiteName': '中山', 'County': '臺北市', 'AQI': 38, 'Latitude': 25.0640, 'Longitude': 121.5250, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 10, 'PM10': 15, 'O3': 28, 'Status': '良好'},
        {'SiteName': '大安', 'County': '臺北市', 'AQI': 41, 'Latitude': 25.0260, 'Longitude': 121.5430, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 11, 'PM10': 16, 'O3': 31, 'Status': '良好'},
        {'SiteName': '信義', 'County': '臺北市', 'AQI': 48, 'Latitude': 25.0330, 'Longitude': 121.5650, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 13, 'PM10': 19, 'O3': 38, 'Status': '良好'},
        
        {'SiteName': '板橋', 'County': '新北市', 'AQI': 68, 'Latitude': 25.0150, 'Longitude': 121.4630, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 18, 'PM10': 25, 'O3': 45, 'Status': '普通'},
        {'SiteName': '三重', 'County': '新北市', 'AQI': 72, 'Latitude': 25.0780, 'Longitude': 121.4890, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 20, 'PM10': 28, 'O3': 48, 'Status': '普通'},
        {'SiteName': '新莊', 'County': '新北市', 'AQI': 78, 'Latitude': 25.0380, 'Longitude': 121.4500, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 22, 'PM10': 31, 'O3': 52, 'Status': '普通'},
        {'SiteName': '土城', 'County': '新北市', 'AQI': 65, 'Latitude': 24.9790, 'Longitude': 121.4470, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 17, 'PM10': 24, 'O3': 43, 'Status': '普通'},
        {'SiteName': '蘆洲', 'County': '新北市', 'AQI': 58, 'Latitude': 25.0840, 'Longitude': 121.4660, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 16, 'PM10': 21, 'O3': 40, 'Status': '普通'},
        
        {'SiteName': '桃園', 'County': '桃園市', 'AQI': 85, 'Latitude': 24.9936, 'Longitude': 121.3010, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 25, 'PM10': 35, 'O3': 58, 'Status': '普通'},
        {'SiteName': '中壢', 'County': '桃園市', 'AQI': 92, 'Latitude': 24.9539, 'Longitude': 121.2248, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 28, 'PM10': 38, 'O3': 62, 'Status': '普通'},
        
        {'SiteName': '台中', 'County': '臺中市', 'AQI': 78, 'Latitude': 24.1477, 'Longitude': 120.6736, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 22, 'PM10': 30, 'O3': 52, 'Status': '普通'},
        {'SiteName': '西屯', 'County': '臺中市', 'AQI': 82, 'Latitude': 24.1620, 'Longitude': 120.6460, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 24, 'PM10': 32, 'O3': 55, 'Status': '普通'},
        {'SiteName': '南屯', 'County': '臺中市', 'AQI': 75, 'Latitude': 24.1320, 'Longitude': 120.6510, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 21, 'PM10': 29, 'O3': 50, 'Status': '普通'},
        
        {'SiteName': '台南', 'County': '臺南市', 'AQI': 105, 'Latitude': 22.9999, 'Longitude': 120.2269, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 35, 'PM10': 45, 'O3': 75, 'Status': '對敏感族群不健康'},
        {'SiteName': '安南', 'County': '臺南市', 'AQI': 112, 'Latitude': 23.0580, 'Longitude': 120.1970, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 38, 'PM10': 48, 'O3': 80, 'Status': '對敏感族群不健康'},
        
        {'SiteName': '高雄', 'County': '高雄市', 'AQI': 98, 'Latitude': 22.6273, 'Longitude': 120.3014, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 32, 'PM10': 42, 'O3': 68, 'Status': '普通'},
        {'SiteName': '左營', 'County': '高雄市', 'AQI': 102, 'Latitude': 22.6900, 'Longitude': 120.2950, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 34, 'PM10': 44, 'O3': 71, 'Status': '對敏感族群不健康'},
        {'SiteName': '楠梓', 'County': '高雄市', 'AQI': 95, 'Latitude': 22.7280, 'Longitude': 120.3260, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 31, 'PM10': 41, 'O3': 65, 'Status': '普通'},
        
        {'SiteName': '基隆', 'County': '基隆市', 'AQI': 42, 'Latitude': 25.1276, 'Longitude': 121.7392, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 11, 'PM10': 16, 'O3': 32, 'Status': '良好'},
        {'SiteName': '宜蘭', 'County': '宜蘭縣', 'AQI': 35, 'Latitude': 24.7700, 'Longitude': 121.7326, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 9, 'PM10': 14, 'O3': 26, 'Status': '良好'},
        {'SiteName': '花蓮', 'County': '花蓮縣', 'AQI': 38, 'Latitude': 23.8228, 'Longitude': 121.6090, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 10, 'PM10': 15, 'O3': 29, 'Status': '良好'},
        {'SiteName': '台東', 'County': '臺東縣', 'AQI': 32, 'Latitude': 22.7580, 'Longitude': 121.1500, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 8, 'PM10': 13, 'O3': 24, 'Status': '良好'},
    ]
    
    return pd.DataFrame(sample_data)

def test_cwa_connection():
    """Test CWA API connection"""
    try:
        from cwa_api_client import CWAClient
        client = CWAClient()
        
        # Try to get weather data (this should work)
        weather_data = client.get_current_weather("臺北市")
        print("✓ CWA API 連接成功")
        print(f"  獲取到天氣數據: {len(weather_data.get('records', {}).get('Station', []))} 個測站")
        return True
        
    except Exception as e:
        print(f"❌ CWA API 連接失敗: {e}")
        return False

def main():
    """Main demo function"""
    print("=" * 60)
    print("CWA 空氣品質指標演示系統")
    print("CWA AQI Demo System")
    print("=" * 60)
    print(f"執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test CWA connection
    print("步驟 1: 測試 CWA API 連接")
    print("-" * 30)
    cwa_connected = test_cwa_connection()
    print()
    
    # Create sample data
    print("步驟 2: 創建範例 AQI 數據")
    print("-" * 30)
    aqi_df = create_sample_aqi_data()
    print(f"✓ 創建了 {len(aqi_df)} 個監測站的範例數據")
    
    # Show sample data
    print("\n範例數據預覽:")
    sample = aqi_df[['SiteName', 'County', 'AQI', 'Status']].head(5)
    for _, row in sample.iterrows():
        print(f"  {row['SiteName']} ({row['County']}): AQI {row['AQI']} - {row['Status']}")
    print()
    
    # Create GeoDataFrame
    print("步驟 3: 創建地理數據")
    print("-" * 30)
    geometry = [Point(xy) for xy in zip(aqi_df['Longitude'], aqi_df['Latitude'])]
    gdf = gpd.GeoDataFrame(aqi_df, geometry=geometry, crs='EPSG:4326')
    print(f"✓ 創建包含 {len(gdf)} 個地理點的 GeoDataFrame")
    print()
    
    # Initialize visualizer
    print("步驟 4: 初始化視覺化工具")
    print("-" * 30)
    visualizer = AQIVisualizer()
    print("✓ AQI 視覺化工具初始化完成")
    print()
    
    # Analyze data
    print("步驟 5: 分析 AQI 數據")
    print("-" * 30)
    analysis = visualizer.analyze_aqi_data(aqi_df)
    
    if 'aqi_stats' in analysis:
        stats = analysis['aqi_stats']
        print(f"平均 AQI: {stats['mean']:.1f}")
        print(f"AQI 範圍: {stats['min']:.1f} - {stats['max']:.1f}")
    
    if 'aqi_distribution' in analysis:
        dist = analysis['aqi_distribution']
        print(f"空氣品質分佈:")
        print(f"  良好 (0-50): {dist['good']} 個站")
        print(f"  普通 (51-100): {dist['moderate']} 個站")
        print(f"  不健康 (101+): {dist['unhealthy']} 個站")
    print()
    
    # Create map
    print("步驟 6: 創建優化的 AQI 地圖")
    print("-" * 30)
    map_path = visualizer.create_aqi_map(gdf)
    print(f"✓ AQI 地圖已創建: {map_path}")
    print()
    
    # Generate report
    print("步驟 7: 生成分析報告")
    print("-" * 30)
    report_path = visualizer.generate_aqi_report(aqi_df, analysis)
    print(f"✓ 分析報告已生成: {report_path}")
    print()
    
    # Summary
    print("=" * 60)
    print("演示完成！")
    print("=" * 60)
    
    print(f"處理的監測站數量: {len(aqi_df)}")
    print(f"生成的檔案:")
    print(f"  - AQI 地圖: {map_path}")
    print(f"  - 分析報告: {report_path}")
    print()
    
    print("主要發現:")
    if 'aqi_stats' in analysis:
        stats = analysis['aqi_stats']
        print(f"  - 全台平均 AQI: {stats['mean']:.1f}")
        print(f"  - 最高 AQI: {stats['max']:.1f} (台南)")
        print(f"  - 最低 AQI: {stats['min']:.1f} (台東)")
    
    print()
    print("優化功能展示:")
    print("✓ 三分色顯示: 綠色(0-50)、黃色(51-100)、紅色(101+)")
    print("✓ 簡化資訊視窗: 站名、縣市、即時 AQI")
    print("✓ 動態標記大小: AQI 越高標記越大")
    print("✓ 改進圖例和標題設計")
    print()
    
    if cwa_connected:
        print("CWA API 狀態: ✓ 連接正常")
        print("建議: 可以結合 CWA 天氣數據進行綜合分析")
    else:
        print("CWA API 狀態: ❌ 連接異常")
        print("建議: 檢查網路連接或 API 金鑰設定")
    
    print()
    print("下一步:")
    print("1. 在瀏覽器中打開 AQI 地圖查看效果")
    print("2. 查看分析報告了解詳細統計")
    print("3. 可以修改範例數據或整合真實 API")
    print("=" * 60)

if __name__ == "__main__":
    main()
