#!/usr/bin/env python3
"""
AQI Analysis Runner
空氣品質分析執行器

Main script to run complete AQI data analysis workflow.
"""

import os
import sys
from datetime import datetime
from aqi_visualizer import AQIVisualizer

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
    
    # Check EPA API key
    from dotenv import load_dotenv
    load_dotenv()
    if not os.getenv('EPA_API_KEY'):
        print("❌ EPA_API_KEY 環境變數未設定")
        print("請在 .env 檔案中添加: EPA_API_KEY=your_api_key_here")
        return False
    
    print("✓ 環境設定完成")
    return True

def main():
    """Main execution function"""
    print("=" * 60)
    print("台灣環境部空氣品質指標分析系統")
    print("Taiwan EPA Air Quality Index Analysis System")
    print("=" * 60)
    print(f"執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    try:
        # Initialize visualizer
        visualizer = AQIVisualizer()
        
        print("開始執行 AQI 分析流程...")
        print()
        
        # Step 1: Collect AQI data
        print("步驟 1: 收集空氣品質數據")
        print("-" * 30)
        aqi_df = visualizer.collect_aqi_data()
        
        if aqi_df.empty:
            print("❌ 無法收集 AQI 數據，請檢查 API 連接和金鑰")
            sys.exit(1)
        
        print(f"✓ 成功收集 {len(aqi_df)} 個監測站的數據")
        
        # Display sample data
        print("\n數據樣本:")
        sample = aqi_df[['SiteName', 'County', 'AQI', 'Status']].head()
        for _, row in sample.iterrows():
            print(f"  {row['SiteName']} ({row['County']}): AQI {row['AQI']} - {row['Status']}")
        print()
        
        # Step 2: Create GeoDataFrame
        print("步驟 2: 創建地理數據")
        print("-" * 30)
        gdf = visualizer.create_geodataframe(aqi_df)
        print(f"✓ 創建包含 {len(gdf)} 個地理點的 GeoDataFrame")
        print()
        
        # Step 3: Analyze AQI patterns
        print("步驟 3: 分析空氣品質模式")
        print("-" * 30)
        analysis = visualizer.analyze_aqi_data(aqi_df)
        
        if 'aqi_stats' in analysis:
            stats = analysis['aqi_stats']
            print(f"平均 AQI: {stats['mean']:.2f}")
            print(f"AQI 範圍: {stats['min']:.2f} - {stats['max']:.2f}")
        
        if 'aqi_distribution' in analysis:
            dist = analysis['aqi_distribution']
            print(f"空氣品質分佈 (三分色):")
            print(f"  良好 (0-50): {dist['good']} 個站")
            print(f"  普通 (51-100): {dist['moderate']} 個站")
            print(f"  不健康 (101+): {dist['unhealthy']} 個站")
        print()
        
        # Step 4: Create interactive map
        print("步驟 4: 創建交互式 AQI 地圖")
        print("-" * 30)
        map_path = visualizer.create_aqi_map(gdf)
        print(f"✓ AQI 地圖: {map_path}")
        print()
        
        # Step 5: Generate comprehensive report
        print("步驟 5: 生成詳細分析報告")
        print("-" * 30)
        report_path = visualizer.generate_aqi_report(aqi_df, analysis)
        print(f"✓ 分析報告: {report_path}")
        print()
        
        # Summary
        print("=" * 60)
        print("分析完成！")
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
            print(f"  - 最高 AQI: {stats['max']:.1f}")
            print(f"  - 最低 AQI: {stats['min']:.1f}")
        
        if 'top_polluted_stations' in analysis and analysis['top_polluted_stations']:
            top = analysis['top_polluted_stations'][0]
            print(f"  - 空氣品質最差地區: {top['SiteName']} ({top['County']})")
        
        print()
        print("建議下一步:")
        print("1. 在瀏覽器中打開 AQI 地圖查看即時空氣品質分佈")
        print("2. 查看分析報告了解詳細統計資訊")
        print("3. 可以定期運行此腳本進行時間序列分析")
        print("4. 比較不同時段的空氣品質變化趨勢")
        
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
