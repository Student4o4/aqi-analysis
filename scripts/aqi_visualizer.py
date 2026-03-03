#!/usr/bin/env python3
"""
AQI Data Visualizer
空氣品質指標視覺化工具

This script processes AQI data and creates interactive maps with folium.
"""

import os
import pandas as pd
import geopandas as gpd
import folium
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np
from shapely.geometry import Point
from aqi_api_client import EPAAQIClient

class AQIVisualizer:
    """AQI data visualizer for GIS analysis"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize visualizer with EPA AQI client"""
        self.client = EPAAQIClient(api_key)
        self.data_dir = "../data/processed"
        self.output_dir = "../output/maps"
        
        # Create directories
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_aqi_color(self, aqi_value: float) -> str:
        """
        Get color based on AQI value (simplified 3-color scheme)
        
        Args:
            aqi_value: AQI value
            
        Returns:
            Color code
        """
        if aqi_value <= 50:
            return '#00E400'    # Green (Good)
        elif aqi_value <= 100:
            return '#FFFF00'    # Yellow (Moderate)
        else:
            return '#FF0000'    # Red (Unhealthy)
    
    def get_aqi_status_text(self, aqi_value: float) -> str:
        """
        Get status text based on AQI value (simplified)
        
        Args:
            aqi_value: AQI value
            
        Returns:
            Status description
        """
        if aqi_value <= 50:
            return '良好'
        elif aqi_value <= 100:
            return '普通'
        else:
            return '不健康'
    
    def collect_aqi_data(self) -> pd.DataFrame:
        """
        Collect AQI data from EPA API
        
        Returns:
            AQI data DataFrame
        """
        try:
            print("獲取全台 AQI 數據...")
            aqi_data = self.client.get_real_time_aqi()
            
            if 'records' not in aqi_data or not aqi_data['records']:
                print("未找到 AQI 數據")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(aqi_data['records'])
            
            # Filter out records with missing coordinates
            df = df.dropna(subset=['Latitude', 'Longitude'])
            
            # Convert coordinates to numeric
            df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
            df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
            df['AQI'] = pd.to_numeric(df['AQI'], errors='coerce')
            
            # Remove invalid coordinates
            df = df[(df['Latitude'] != 0) & (df['Longitude'] != 0)]
            df = df.dropna(subset=['Latitude', 'Longitude'])
            
            # Save to CSV
            csv_path = os.path.join(self.data_dir, f"aqi_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"AQI 數據已保存到: {csv_path}")
            
            return df
            
        except Exception as e:
            print(f"獲取 AQI 數據時出錯: {e}")
            return pd.DataFrame()
    
    def create_geodataframe(self, df: pd.DataFrame) -> gpd.GeoDataFrame:
        """
        Convert AQI DataFrame to GeoDataFrame
        
        Args:
            df: AQI data DataFrame
            
        Returns:
            GeoDataFrame with point geometries
        """
        # Create geometry points
        geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
        
        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
        
        return gdf
    
    def create_aqi_map(self, gdf: gpd.GeoDataFrame) -> str:
        """
        Create interactive AQI map using Folium with optimized display
        
        Args:
            gdf: GeoDataFrame with AQI data
            
        Returns:
            Path to saved HTML map
        """
        # Calculate center of map (Taiwan center)
        center_lat = 23.8
        center_lon = 120.9
        
        # Create map with better tiles
        m = folium.Map(
            location=[center_lat, center_lon], 
            zoom_start=8,
            tiles='OpenStreetMap'
        )
        
        # Add AQI markers with optimized popup
        for idx, row in gdf.iterrows():
            if pd.notna(row['AQI']):
                aqi = float(row['AQI'])
                color = self.get_aqi_color(aqi)
                status = self.get_aqi_status_text(aqi)
                
                # Create simplified popup content (station name, county, AQI)
                popup_content = f"""
                <div style="font-family: Arial, sans-serif; width: 200px;">
                    <h4 style="margin: 5px 0; color: {color};">{row.get('SiteName', 'N/A')}</h4>
                    <p style="margin: 3px 0;"><strong>所在地:</strong> {row.get('County', 'N/A')}</p>
                    <p style="margin: 3px 0;"><strong>即時 AQI:</strong> <span style="color: {color}; font-weight: bold;">{aqi}</span></p>
                    <p style="margin: 3px 0;"><strong>狀態:</strong> {status}</p>
                    <p style="margin: 3px 0; font-size: 12px; color: #666;">更新: {row.get('PublishTime', 'N/A')}</p>
                </div>
                """
                
                # Create tooltip
                tooltip_content = f"{row.get('SiteName', 'N/A')} ({row.get('County', 'N/A')})<br>AQI: {aqi}"
                
                # Adjust marker size based on AQI value
                if aqi <= 50:
                    radius = 6
                elif aqi <= 100:
                    radius = 8
                else:
                    radius = 10
                
                folium.CircleMarker(
                    location=[row['Latitude'], row['Longitude']],
                    radius=radius,
                    popup=folium.Popup(popup_content, max_width=250),
                    tooltip=tooltip_content,
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.8,
                    weight=2,
                    opacity=0.9
                ).add_to(m)
        
        # Add simplified legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 180px; height: 120px; 
                    background-color:rgba(255,255,255,0.9); border:2px solid #666; z-index:9999; 
                    font-size:12px; padding: 8px; border-radius: 5px;
                    font-family: Arial, sans-serif;">
        <h4 style="margin: 0 0 8px 0; font-size: 14px;">AQI 指標</h4>
        <div style="display: flex; align-items: center; margin: 4px 0;">
            <div style="width: 20px; height: 20px; background-color: #00E400; border-radius: 50%; margin-right: 8px;"></div>
            <span>0-50: 良好</span>
        </div>
        <div style="display: flex; align-items: center; margin: 4px 0;">
            <div style="width: 20px; height: 20px; background-color: #FFFF00; border-radius: 50%; margin-right: 8px;"></div>
            <span>51-100: 普通</span>
        </div>
        <div style="display: flex; align-items: center; margin: 4px 0;">
            <div style="width: 20px; height: 20px; background-color: #FF0000; border-radius: 50%; margin-right: 8px;"></div>
            <span>101+: 不健康</span>
        </div>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Add title
        title_html = '''
        <div style="position: fixed; 
                    top: 10px; left: 50%; transform: translateX(-50%); 
                    background-color:rgba(255,255,255,0.9); border:2px solid #666; z-index:9999; 
                    font-size:16px; padding: 8px 15px; border-radius: 5px;
                    font-family: Arial, sans-serif; font-weight: bold;">
        台灣空氣品質指標即時地圖
        </div>
        '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Save map
        map_path = os.path.join(self.output_dir, f"aqi_map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        m.save(map_path)
        
        print(f"優化的 AQI 地圖已保存到: {map_path}")
        return map_path
    
    def analyze_aqi_data(self, df: pd.DataFrame) -> Dict:
        """
        Analyze AQI data and generate statistics
        
        Args:
            df: AQI data DataFrame
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {}
        
        # Basic statistics
        if 'AQI' in df.columns:
            aqi_data = pd.to_numeric(df['AQI'], errors='coerce').dropna()
            if not aqi_data.empty:
                analysis['aqi_stats'] = {
                    'count': len(aqi_data),
                    'mean': aqi_data.mean(),
                    'min': aqi_data.min(),
                    'max': aqi_data.max(),
                    'std': aqi_data.std()
                }
        
        # AQI distribution (simplified 3-color scheme)
        if 'AQI' in df.columns:
            aqi_data = pd.to_numeric(df['AQI'], errors='coerce').dropna()
            if not aqi_data.empty:
                analysis['aqi_distribution'] = {
                    'good': len(aqi_data[aqi_data <= 50]),
                    'moderate': len(aqi_data[(aqi_data > 50) & (aqi_data <= 100)]),
                    'unhealthy': len(aqi_data[aqi_data > 100])
                }
        
        # County statistics
        if 'County' in df.columns and 'AQI' in df.columns:
            county_stats = df.groupby('County')['AQI'].apply(
                lambda x: pd.to_numeric(x, errors='coerce').mean()
            ).dropna().to_dict()
            analysis['county_avg_aqi'] = county_stats
        
        # Top polluted stations
        if 'AQI' in df.columns and 'SiteName' in df.columns:
            top_stations = df.nlargest(5, 'AQI')[['SiteName', 'County', 'AQI']].to_dict('records')
            analysis['top_polluted_stations'] = top_stations
        
        return analysis
    
    def generate_aqi_report(self, df: pd.DataFrame, analysis: Dict) -> str:
        """
        Generate AQI analysis report
        
        Args:
            df: AQI data DataFrame
            analysis: Analysis results
            
        Returns:
            Path to saved report
        """
        report_path = os.path.join("../output/reports", f"aqi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        os.makedirs("../output/reports", exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("空氣品質指標分析報告\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"監測站數量: {len(df)}\n\n")
            
            # AQI statistics
            if 'aqi_stats' in analysis:
                stats = analysis['aqi_stats']
                f.write("AQI 統計分析:\n")
                f.write("-" * 30 + "\n")
                f.write(f"平均 AQI: {stats['mean']:.2f}\n")
                f.write(f"最低 AQI: {stats['min']:.2f}\n")
                f.write(f"最高 AQI: {stats['max']:.2f}\n")
                f.write(f"標準差: {stats['std']:.2f}\n\n")
            
            # AQI distribution
            if 'aqi_distribution' in analysis:
                dist = analysis['aqi_distribution']
                f.write("AQI 分佈 (簡化三分色):")
                f.write("-" * 30 + "\n")
                f.write(f"良好 (0-50): {dist['good']} 個站\n")
                f.write(f"普通 (51-100): {dist['moderate']} 個站\n")
                f.write(f"不健康 (101+): {dist['unhealthy']} 個站\n\n")
            
            # County statistics
            if 'county_avg_aqi' in analysis:
                f.write("各縣市平均 AQI:\n")
                f.write("-" * 30 + "\n")
                for county, avg_aqi in sorted(analysis['county_avg_aqi'].items(), key=lambda x: x[1], reverse=True):
                    f.write(f"{county}: {avg_aqi:.2f}\n")
                f.write("\n")
            
            # Top polluted stations
            if 'top_polluted_stations' in analysis:
                f.write("AQI 最高的前5個監測站:\n")
                f.write("-" * 30 + "\n")
                for i, station in enumerate(analysis['top_polluted_stations'], 1):
                    f.write(f"{i}. {station['SiteName']} ({station['County']}): AQI {station['AQI']}\n")
                f.write("\n")
            
            # Data quality
            f.write(f"數據品質:\n")
            f.write(f"完整數據行數: {df.dropna().shape[0]}\n")
            f.write(f"缺失值比例: {(df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100:.1f}%\n")
        
        print(f"分析報告已保存到: {report_path}")
        return report_path


def main():
    """Main function to demonstrate AQI visualization"""
    try:
        # Initialize visualizer
        visualizer = AQIVisualizer()
        
        print("=== 空氣品質指標視覺化系統 ===")
        print("AQI Visualization System")
        print("=" * 40)
        
        # Step 1: Collect AQI data
        print("\n1. 收集 AQI 數據...")
        aqi_df = visualizer.collect_aqi_data()
        
        if aqi_df.empty:
            print("沒有收集到 AQI 數據，請檢查 API 連接")
            return
        
        print(f"✓ 成功收集 {len(aqi_df)} 個監測站的數據")
        
        # Step 2: Create GeoDataFrame
        print("\n2. 創建地理數據...")
        gdf = visualizer.create_geodataframe(aqi_df)
        
        # Step 3: Analyze AQI patterns
        print("\n3. 分析 AQI 模式...")
        analysis = visualizer.analyze_aqi_data(aqi_df)
        
        # Step 4: Create AQI map
        print("\n4. 創建 AQI 地圖...")
        map_path = visualizer.create_aqi_map(gdf)
        
        # Step 5: Generate report
        print("\n5. 生成分析報告...")
        report_path = visualizer.generate_aqi_report(aqi_df, analysis)
        
        print("\n=== 處理完成 ===")
        print(f"地圖: {map_path}")
        print(f"報告: {report_path}")
        print("\n建議下一步:")
        print("1. 在瀏覽器中打開 AQI 地圖查看即時空氣品質")
        print("2. 查看分析報告了解詳細統計信息")
        print("3. 可以定期運行此腳本進行時間序列分析")
        
    except Exception as e:
        print(f"錯誤: {e}")


if __name__ == "__main__":
    main()
