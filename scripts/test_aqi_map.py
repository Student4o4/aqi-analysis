#!/usr/bin/env python3
"""
AQI Map Test Script
空氣品質地圖測試腳本

This script tests the optimized AQI map functionality.
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime
import os
from aqi_visualizer import AQIVisualizer

def create_sample_data():
    """Create sample AQI data for testing"""
    # Sample data for Taiwan monitoring stations
    sample_data = [
        {'SiteName': '台北', 'County': '臺北市', 'AQI': 45, 'Latitude': 25.0320, 'Longitude': 121.5654, 'PublishTime': '2024-03-03 14:00'},
        {'SiteName': '新店', 'County': '新北市', 'AQI': 78, 'Latitude': 24.9739, 'Longitude': 121.5378, 'PublishTime': '2024-03-03 14:00'},
        {'SiteName': '桃園', 'County': '桃園市', 'AQI': 125, 'Latitude': 24.9936, 'Longitude': 121.3010, 'PublishTime': '2024-03-03 14:00'},
        {'SiteName': '台中', 'County': '臺中市', 'AQI': 89, 'Latitude': 24.1477, 'Longitude': 120.6736, 'PublishTime': '2024-03-03 14:00'},
        {'SiteName': '台南', 'County': '臺南市', 'AQI': 156, 'Latitude': 22.9999, 'Longitude': 120.2269, 'PublishTime': '2024-03-03 14:00'},
        {'SiteName': '高雄', 'County': '高雄市', 'AQI': 98, 'Latitude': 22.6273, 'Longitude': 120.3014, 'PublishTime': '2024-03-03 14:00'},
        {'SiteName': '基隆', 'County': '基隆市', 'AQI': 34, 'Latitude': 25.1276, 'Longitude': 121.7392, 'PublishTime': '2024-03-03 14:00'},
        {'SiteName': '宜蘭', 'County': '宜蘭縣', 'AQI': 52, 'Latitude': 24.7700, 'Longitude': 121.7326, 'PublishTime': '2024-03-03 14:00'},
        {'SiteName': '花蓮', 'County': '花蓮縣', 'AQI': 41, 'Latitude': 23.8228, 'Longitude': 121.6090, 'PublishTime': '2024-03-03 14:00'},
        {'SiteName': '屏東', 'County': '屏東縣', 'AQI': 112, 'Latitude': 22.6756, 'Longitude': 120.4884, 'PublishTime': '2024-03-03 14:00'},
    ]
    
    return pd.DataFrame(sample_data)

def test_color_function():
    """Test the color function"""
    visualizer = AQIVisualizer()
    
    print("測試顏色分類功能:")
    print("-" * 30)
    
    test_values = [25, 50, 75, 100, 125, 150, 200]
    
    for aqi in test_values:
        color = visualizer.get_aqi_color(aqi)
        status = visualizer.get_aqi_status_text(aqi)
        print(f"AQI {aqi:3d}: {color:8s} - {status}")
    
    print()

def test_map_creation():
    """Test map creation with sample data"""
    print("測試地圖創建功能:")
    print("-" * 30)
    
    # Create sample data
    df = create_sample_data()
    print(f"創建了 {len(df)} 個測試監測站數據")
    
    # Create GeoDataFrame
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
    
    # Initialize visualizer
    visualizer = AQIVisualizer()
    
    # Create map
    try:
        map_path = visualizer.create_aqi_map(gdf)
        print(f"✓ 測試地圖已創建: {map_path}")
        
        # Verify file exists
        if os.path.exists(map_path):
            file_size = os.path.getsize(map_path)
            print(f"✓ 檔案大小: {file_size:,} bytes")
        else:
            print("❌ 地圖檔案未找到")
            
    except Exception as e:
        print(f"❌ 地圖創建失敗: {e}")
    
    print()

def test_analysis():
    """Test analysis functionality"""
    print("測試分析功能:")
    print("-" * 30)
    
    df = create_sample_data()
    visualizer = AQIVisualizer()
    
    try:
        analysis = visualizer.analyze_aqi_data(df)
        
        print("分析結果:")
        if 'aqi_stats' in analysis:
            stats = analysis['aqi_stats']
            print(f"  平均 AQI: {stats['mean']:.1f}")
            print(f"  範圍: {stats['min']:.1f} - {stats['max']:.1f}")
        
        if 'aqi_distribution' in analysis:
            dist = analysis['aqi_distribution']
            print(f"  良好 (0-50): {dist['good']} 個站")
            print(f"  普通 (51-100): {dist['moderate']} 個站")
            print(f"  不健康 (101+): {dist['unhealthy']} 個站")
        
        print("✓ 分析功能正常")
        
    except Exception as e:
        print(f"❌ 分析失敗: {e}")
    
    print()

def main():
    """Main test function"""
    print("=" * 50)
    print("AQI 地圖優化功能測試")
    print("AQI Map Optimization Test")
    print("=" * 50)
    print()
    
    # Run tests
    test_color_function()
    test_map_creation()
    test_analysis()
    
    print("=" * 50)
    print("測試完成！")
    print()
    print("優化功能說明:")
    print("✓ 簡化三分色顯示: 綠色(0-50)、黃色(51-100)、紅色(101+)")
    print("✓ 簡化資訊視窗: 站名、所在地、即時 AQI 數值")
    print("✓ 動態標記大小: AQI 越高標記越大")
    print("✓ 改進圖例和標題設計")
    print()
    print("如需測試真實數據，請:")
    print("1. 在 .env 檔案中設定 EPA_API_KEY")
    print("2. 運行: python run_aqi_analysis.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
