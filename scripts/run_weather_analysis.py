#!/usr/bin/env python3
"""
Weather Analysis Runner
天氣分析執行器

Main script to run complete weather data analysis workflow.
"""

import os
import sys
from datetime import datetime
from weather_data_processor import WeatherDataProcessor

def setup_environment():
    """Setup environment and check dependencies"""
    print("檢查環境設定...")
    
    # Check required directories
    required_dirs = [
        "../data/processed",
        "../output/maps", 
        "../output/reports",
        "../output/exports",
        "../logs"
    ]
    
    for dir_path in required_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ {dir_path}")
    
    # Check .env file
    if not os.path.exists("../.env"):
        print("❌ .env 檔案不存在，請先設定環境變數")
        return False
    
    print("✓ 環境設定完成")
    return True

def main():
    """Main execution function"""
    print("=" * 60)
    print("台灣中央氣象局天氣數據分析系統")
    print("Taiwan Central Weather Administration Data Analysis System")
    print("=" * 60)
    print(f"執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    try:
        # Initialize processor
        processor = WeatherDataProcessor()
        
        # Define major cities and counties for analysis
        locations = [
            # 主要城市
            "臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市",
            # 其他縣市
            "基隆市", "新竹市", "嘉義市",
            "新竹縣", "苗栗縣", "彰化縣", "南投縣", "雲林縣",
            "嘉義縣", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣",
            # 離島地區
            "澎湖縣", "金門縣", "連江縣"
        ]
        
        print(f"將從 {len(locations)} 個地點收集天氣數據...")
        print()
        
        # Step 1: Collect weather data
        print("步驟 1: 收集天氣數據")
        print("-" * 30)
        weather_df = processor.collect_weather_data(locations)
        
        if weather_df.empty:
            print("❌ 無法收集天氣數據，請檢查 API 連接和金鑰")
            sys.exit(1)
        
        print(f"✓ 成功收集 {len(weather_df)} 個地點的數據")
        print()
        
        # Step 2: Create GeoDataFrame
        print("步驟 2: 創建地理數據")
        print("-" * 30)
        gdf = processor.create_geodataframe(weather_df)
        print(f"✓ 創建包含 {len(gdf)} 個地理點的 GeoDataFrame")
        print()
        
        # Step 3: Analyze weather patterns
        print("步驟 3: 分析天氣模式")
        print("-" * 30)
        analysis = processor.analyze_weather_patterns(weather_df)
        
        print("分析結果:")
        for parameter, stats in analysis.items():
            print(f"  {parameter}:")
            for stat_name, stat_value in stats.items():
                print(f"    {stat_name}: {stat_value:.2f}")
        print()
        
        # Step 4: Create visualizations
        print("步驟 4: 創建視覺化")
        print("-" * 30)
        
        # Create temperature map
        map_path = processor.create_temperature_map(gdf)
        print(f"✓ 溫度地圖: {map_path}")
        
        # Create charts
        chart_paths = processor.create_weather_charts(weather_df)
        for i, chart_path in enumerate(chart_paths, 1):
            print(f"✓ 圖表 {i}: {chart_path}")
        print()
        
        # Step 5: Generate report
        print("步驟 5: 生成分析報告")
        print("-" * 30)
        report_path = processor.generate_weather_report(weather_df, analysis)
        print(f"✓ 分析報告: {report_path}")
        print()
        
        # Summary
        print("=" * 60)
        print("分析完成！")
        print("=" * 60)
        print(f"處理的地點數量: {len(weather_df)}")
        print(f"生成的檔案:")
        print(f"  - 溫度地圖: {map_path}")
        for chart_path in chart_paths:
            print(f"  - 分析圖表: {chart_path}")
        print(f"  - 分析報告: {report_path}")
        print()
        print("建議下一步:")
        print("1. 在瀏覽器中打開溫度地圖查看交互式地圖")
        print("2. 查看分析圖表了解天氣模式")
        print("3. 閱讀分析報告獲取詳細統計信息")
        print("4. 可以定期運行此腳本進行時間序列分析")
        
    except KeyboardInterrupt:
        print("\n用戶中斷執行")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 執行過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
