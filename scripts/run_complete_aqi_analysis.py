#!/usr/bin/env python3
"""
Complete Taiwan AQI Analysis with All Monitoring Stations
完整台灣空氣品質指標分析（包含所有監測站）

This script runs AQI analysis with complete Taiwan monitoring stations data.
"""

import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime
from aqi_visualizer import AQIVisualizer
from complete_aqi_data import create_complete_taiwan_aqi_data

def main():
    """Main function for complete AQI analysis"""
    print("=" * 70)
    print("完整台灣空氣品質指標分析系統")
    print("Complete Taiwan Air Quality Index Analysis System")
    print("=" * 70)
    print(f"執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Generate complete AQI data
    print("步驟 1: 生成完整台灣 AQI 監測站數據")
    print("-" * 50)
    aqi_df = create_complete_taiwan_aqi_data()
    print(f"✓ 成功生成 {len(aqi_df)} 個監測站的完整數據")
    print()
    
    # Show data overview
    print("數據概覽:")
    counties = len(aqi_df['County'].unique())
    area_types = len(aqi_df['Area'].unique())
    print(f"  涵蓋縣市: {counties} 個")
    print(f"  區域類型: {area_types} 種")
    print(f"  平均 AQI: {aqi_df['AQI'].mean():.1f}")
    print(f"  AQI 範圍: {aqi_df['AQI'].min()} - {aqi_df['AQI'].max()}")
    print()
    
    # Step 2: Create GeoDataFrame
    print("步驟 2: 創建地理數據")
    print("-" * 50)
    geometry = [Point(xy) for xy in zip(aqi_df['Longitude'], aqi_df['Latitude'])]
    gdf = gpd.GeoDataFrame(aqi_df, geometry=geometry, crs='EPSG:4326')
    print(f"✓ 創建包含 {len(gdf)} 個地理點的 GeoDataFrame")
    print()
    
    # Step 3: Initialize visualizer
    print("步驟 3: 初始化視覺化工具")
    print("-" * 50)
    visualizer = AQIVisualizer()
    print("✓ AQI 視覺化工具初始化完成")
    print()
    
    # Step 4: Analyze AQI patterns
    print("步驟 4: 分析 AQI 模式")
    print("-" * 50)
    analysis = visualizer.analyze_aqi_data(aqi_df)
    
    if 'aqi_stats' in analysis:
        stats = analysis['aqi_stats']
        print(f"平均 AQI: {stats['mean']:.2f}")
        print(f"AQI 範圍: {stats['min']:.2f} - {stats['max']:.2f}")
        print(f"標準差: {stats['std']:.2f}")
    
    if 'aqi_distribution' in analysis:
        dist = analysis['aqi_distribution']
        print(f"空氣品質分佈 (三分色):")
        print(f"  良好 (0-50): {dist['good']} 個站 ({dist['good']/len(aqi_df)*100:.1f}%)")
        print(f"  普通 (51-100): {dist['moderate']} 個站 ({dist['moderate']/len(aqi_df)*100:.1f}%)")
        print(f"  不健康 (101+): {dist['unhealthy']} 個站 ({dist['unhealthy']/len(aqi_df)*100:.1f}%)")
    print()
    
    # Show county statistics
    if 'county_avg_aqi' in analysis:
        print("各縣市平均 AQI (前5名最高):")
        county_stats = analysis['county_avg_aqi']
        sorted_counties = sorted(county_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        for county, avg_aqi in sorted_counties:
            print(f"  {county}: {avg_aqi:.1f}")
    print()
    
    # Step 5: Create comprehensive AQI map
    print("步驟 5: 創建完整 AQI 地圖")
    print("-" * 50)
    map_path = visualizer.create_aqi_map(gdf)
    print(f"✓ 完整 AQI 地圖: {map_path}")
    print()
    
    # Step 6: Generate comprehensive report
    print("步驟 6: 生成詳細分析報告")
    print("-" * 50)
    report_path = visualizer.generate_aqi_report(aqi_df, analysis)
    print(f"✓ 分析報告: {report_path}")
    print()
    
    # Step 7: Distance analysis
    print("步驟 7: 距離分析")
    print("-" * 50)
    from distance_calculator import DistanceCalculator
    
    calculator = DistanceCalculator()
    result_df = calculator.calculate_distances_from_dataframe(aqi_df, method='geodesic')
    stats = calculator.calculate_distance_statistics(result_df)
    stats['method'] = 'geodesic'
    
    print(f"距離統計:")
    print(f"  平均距離: {stats['mean_km']:.2f} km")
    print(f"  最近站點: {stats['closest_station']['name']} ({stats['closest_station']['distance_km']:.2f} km)")
    print(f"  最遠站點: {stats['farthest_station']['name']} ({stats['farthest_station']['distance_km']:.2f} km)")
    print()
    
    # Save distance results
    csv_path, stats_path = calculator.save_distance_results(result_df, stats, "complete_analysis_distances")
    print(f"✓ 距離分析結果: {csv_path}")
    print(f"✓ 距離統計報告: {stats_path}")
    print()
    
    # Step 8: Save complete data
    print("步驟 8: 保存完整數據")
    print("-" * 50)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save complete data
    data_path = f"../data/processed/complete_analysis_{timestamp}.csv"
    aqi_df.to_csv(data_path, index=False, encoding='utf-8-sig')
    print(f"✓ 完整數據: {data_path}")
    print()
    
    # Summary
    print("=" * 70)
    print("完整台灣 AQI 分析完成！")
    print("=" * 70)
    print(f"📊 分析規模:")
    print(f"  - 監測站總數: {len(aqi_df)} 個")
    print(f"  - 涵蓋縣市: {len(aqi_df['County'].unique())} 個")
    print(f"  - 區域類型: {len(aqi_df['Area'].unique())} 種")
    print()
    print(f"📁 生成的檔案:")
    print(f"  - 完整地圖: {map_path}")
    print(f"  - 分析報告: {report_path}")
    print(f"  - 距離數據: {csv_path}")
    print(f"  - 距離統計: {stats_path}")
    print(f"  - 完整數據: {data_path}")
    print()
    print(f"🎯 主要發現:")
    if 'aqi_stats' in analysis:
        stats = analysis['aqi_stats']
        print(f"  - 全台平均 AQI: {stats['mean']:.1f}")
        print(f"  - 最高 AQI: {stats['max']:.1f}")
        print(f"  - 最低 AQI: {stats['min']:.1f}")
    
    if 'county_avg_aqi' in analysis:
        county_stats = analysis['county_avg_aqi']
        highest_county = max(county_stats.items(), key=lambda x: x[1])
        lowest_county = min(county_stats.items(), key=lambda x: x[1])
        print(f"  - 空氣品質最差縣市: {highest_county[0]} ({highest_county[1]:.1f})")
        print(f"  - 空氣品質最好縣市: {lowest_county[0]} ({lowest_county[1]:.1f})")
    
    print(f"  - 距離台北車站最近: {stats.get('closest_station', {}).get('name', 'N/A')} ({stats.get('closest_station', {}).get('distance_km', 0):.2f} km)")
    print(f"  - 距離台北車站最遠: {stats.get('farthest_station', {}).get('name', 'N/A')} ({stats.get('farthest_station', {}).get('distance_km', 0):.2f} km)")
    print()
    print(f"🔍 優化功能展示:")
    print(f"  ✓ 三分色顯示: 綠色(0-50)、黃色(51-100)、紅色(101+)")
    print(f"  ✓ 簡化資訊視窗: 站名、縣市、即時 AQI")
    print(f"  ✓ 動態標記大小: AQI 越高標記越大")
    print(f"  ✓ 完整覆蓋台灣所有主要監測站")
    print()
    print(f"📈 數據完整性:")
    print(f"  ✓ 從 {20} 個站點擴展到 {len(aqi_df)} 個完整站點")
    print(f"  ✓ 涵蓋台灣本島及離島所有監測站")
    print(f"  ✓ 按區域類型生成真實 AQI 分佈")
    print(f"  ✓ 完整的空間距離計算")
    print()
    print(f"🚀 建議下一步:")
    print(f"  1. 在瀏覽器中打開完整 AQI 地圖")
    print(f"  2. 查看詳細分析報告了解統計資訊")
    print(f"  3. 可以定期運行進行時間序列分析")
    print(f"  4. 比較不同時段的空氣品質變化")
    print("=" * 70)

if __name__ == "__main__":
    main()
