#!/usr/bin/env python3
"""
Weather Data Processor
天氣數據處理器

This script processes weather data from CWA API and performs GIS analysis.
"""

import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np
from shapely.geometry import Point
import folium
from cwa_api_client import CWAClient

class WeatherDataProcessor:
    """Weather data processor for GIS analysis"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize processor with CWA client"""
        self.client = CWAClient(api_key)
        self.data_dir = "../data/processed"
        self.output_dir = "../output/maps"
        
        # Create directories
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def collect_weather_data(self, locations: List[str]) -> pd.DataFrame:
        """
        Collect weather data from multiple locations
        
        Args:
            locations: List of location names
            
        Returns:
            Combined weather data DataFrame
        """
        all_data = []
        
        for location in locations:
            try:
                print(f"獲取 {location} 的天氣數據...")
                weather_data = self.client.get_current_weather(location)
                
                if 'records' in weather_data and 'Station' in weather_data['records']:
                    stations = weather_data['records']['Station']
                    
                    for station in stations:
                        # Extract coordinates (WGS84)
                        lat = 0.0
                        lon = 0.0
                        coordinates = station.get('GeoInfo', {}).get('Coordinates', [])
                        for coord in coordinates:
                            if coord.get('CoordinateName') == 'WGS84':
                                lat = float(coord.get('StationLatitude', 0))
                                lon = float(coord.get('StationLongitude', 0))
                                break
                        
                        # Extract basic info
                        row = {
                            'location': station.get('StationName', ''),
                            'latitude': lat,
                            'longitude': lon,
                            'station_id': station.get('StationId', ''),
                            'observation_time': station.get('ObsTime', {}).get('DateTime', ''),
                            'county': station.get('GeoInfo', {}).get('CountyName', ''),
                            'town': station.get('GeoInfo', {}).get('TownName', ''),
                            'timestamp': datetime.now()
                        }
                        
                        # Extract weather elements
                        weather_elements = station.get('WeatherElement', {})
                        for element_name, element_value in weather_elements.items():
                            if isinstance(element_value, (str, int, float)):
                                row[element_name] = element_value
                            elif isinstance(element_value, dict):
                                # Handle nested weather data
                                for sub_key, sub_value in element_value.items():
                                    if isinstance(sub_value, (str, int, float)):
                                        row[f"{element_name}_{sub_key}"] = sub_value
                        
                        all_data.append(row)
                    
            except Exception as e:
                print(f"獲取 {location} 數據時出錯: {e}")
                continue
        
        df = pd.DataFrame(all_data)
        
        # Save to CSV
        if not df.empty:
            csv_path = os.path.join(self.data_dir, f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"天氣數據已保存到: {csv_path}")
        
        return df
    
    def create_geodataframe(self, df: pd.DataFrame) -> gpd.GeoDataFrame:
        """
        Convert weather DataFrame to GeoDataFrame
        
        Args:
            df: Weather data DataFrame
            
        Returns:
            GeoDataFrame with point geometries
        """
        # Create geometry points
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
        
        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
        
        return gdf
    
    def create_temperature_map(self, gdf: gpd.GeoDataFrame) -> str:
        """
        Create temperature map using Folium
        
        Args:
            gdf: GeoDataFrame with weather data
            
        Returns:
            Path to saved HTML map
        """
        # Calculate center of map
        center_lat = gdf['latitude'].mean()
        center_lon = gdf['longitude'].mean()
        
        # Create map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=7)
        
        # Add temperature markers
        for idx, row in gdf.iterrows():
            if 'AirTemperature' in row and pd.notna(row['AirTemperature']):
                temp = float(row['AirTemperature'])
                
                # Color based on temperature
                if temp < 10:
                    color = 'blue'
                elif temp < 20:
                    color = 'green'
                elif temp < 30:
                    color = 'orange'
                else:
                    color = 'red'
                
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=8,
                    popup=f"{row['location']}<br>溫度: {temp}°C<br>濕度: {row.get('RelativeHumidity', 'N/A')}%",
                    tooltip=f"{row['location']}: {temp}°C",
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7
                ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Save map
        map_path = os.path.join(self.output_dir, f"temperature_map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        m.save(map_path)
        
        print(f"溫度地圖已保存到: {map_path}")
        return map_path
    
    def analyze_weather_patterns(self, df: pd.DataFrame) -> Dict:
        """
        Analyze weather patterns and statistics
        
        Args:
            df: Weather data DataFrame
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {}
        
        # Temperature analysis
        if 'AirTemperature' in df.columns:
            temp_data = pd.to_numeric(df['AirTemperature'], errors='coerce').dropna()
            if not temp_data.empty:
                analysis['temperature'] = {
                    'mean': temp_data.mean(),
                    'min': temp_data.min(),
                    'max': temp_data.max(),
                    'std': temp_data.std()
                }
        
        # Humidity analysis
        if 'RelativeHumidity' in df.columns:
            humidity_data = pd.to_numeric(df['RelativeHumidity'], errors='coerce').dropna()
            if not humidity_data.empty:
                analysis['humidity'] = {
                    'mean': humidity_data.mean(),
                    'min': humidity_data.min(),
                    'max': humidity_data.max(),
                    'std': humidity_data.std()
                }
        
        # Pressure analysis
        if 'AirPressure' in df.columns:
            pressure_data = pd.to_numeric(df['AirPressure'], errors='coerce').dropna()
            if not pressure_data.empty:
                analysis['pressure'] = {
                    'mean': pressure_data.mean(),
                    'min': pressure_data.min(),
                    'max': pressure_data.max(),
                    'std': pressure_data.std()
                }
        
        # Wind Speed analysis
        if 'WindSpeed' in df.columns:
            wind_data = pd.to_numeric(df['WindSpeed'], errors='coerce').dropna()
            if not wind_data.empty:
                analysis['wind_speed'] = {
                    'mean': wind_data.mean(),
                    'min': wind_data.min(),
                    'max': wind_data.max(),
                    'std': wind_data.std()
                }
        
        # UV Index analysis
        if 'UVIndex' in df.columns:
            uv_data = pd.to_numeric(df['UVIndex'], errors='coerce').dropna()
            if not uv_data.empty:
                analysis['uv_index'] = {
                    'mean': uv_data.mean(),
                    'min': uv_data.min(),
                    'max': uv_data.max(),
                    'std': uv_data.std()
                }
        
        return analysis
    
    def create_weather_charts(self, df: pd.DataFrame) -> List[str]:
        """
        Create weather analysis charts
        
        Args:
            df: Weather data DataFrame
            
        Returns:
            List of paths to saved chart files
        """
        chart_paths = []
        
        # Set style
        plt.style.use('seaborn-v0_8')
        
        # Temperature distribution
        if 'AirTemperature' in df.columns:
            plt.figure(figsize=(10, 6))
            temp_data = pd.to_numeric(df['AirTemperature'], errors='coerce').dropna()
            
            plt.subplot(1, 2, 1)
            plt.hist(temp_data, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            plt.xlabel('溫度 (°C)')
            plt.ylabel('頻率')
            plt.title('溫度分佈')
            plt.grid(True, alpha=0.3)
            
            plt.subplot(1, 2, 2)
            plt.boxplot(temp_data)
            plt.ylabel('溫度 (°C)')
            plt.title('溫度箱線圖')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            temp_chart_path = os.path.join(self.output_dir, f"temperature_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            plt.savefig(temp_chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            chart_paths.append(temp_chart_path)
        
        # Humidity vs Temperature scatter plot
        if 'AirTemperature' in df.columns and 'RelativeHumidity' in df.columns:
            plt.figure(figsize=(8, 6))
            temp_data = pd.to_numeric(df['AirTemperature'], errors='coerce')
            humidity_data = pd.to_numeric(df['RelativeHumidity'], errors='coerce')
            
            plt.scatter(temp_data, humidity_data, alpha=0.6, s=50)
            plt.xlabel('溫度 (°C)')
            plt.ylabel('濕度 (%)')
            plt.title('溫度 vs 濕度散佈圖')
            plt.grid(True, alpha=0.3)
            
            # Add trend line
            z = np.polyfit(temp_data.dropna(), humidity_data.dropna(), 1)
            p = np.poly1d(z)
            plt.plot(temp_data, p(temp_data), "r--", alpha=0.8)
            
            scatter_chart_path = os.path.join(self.output_dir, f"temp_humidity_scatter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            plt.savefig(scatter_chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            chart_paths.append(scatter_chart_path)
        
        return chart_paths
    
    def generate_weather_report(self, df: pd.DataFrame, analysis: Dict) -> str:
        """
        Generate weather analysis report
        
        Args:
            df: Weather data DataFrame
            analysis: Analysis results
            
        Returns:
            Path to saved report
        """
        report_path = os.path.join("../output/reports", f"weather_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        os.makedirs("../output/reports", exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("天氣數據分析報告\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"數據點數量: {len(df)}\n\n")
            
            # Location summary
            f.write("地點列表:\n")
            for location in df['location'].unique():
                f.write(f"- {location}\n")
            f.write("\n")
            
            # Analysis results
            f.write("統計分析:\n")
            f.write("-" * 30 + "\n")
            
            for parameter, stats in analysis.items():
                f.write(f"\n{parameter.upper()}:\n")
                for stat_name, stat_value in stats.items():
                    f.write(f"  {stat_name}: {stat_value:.2f}\n")
            
            # Data quality
            f.write(f"\n數據品質:\n")
            f.write(f"完整數據行數: {df.dropna().shape[0]}\n")
            f.write(f"缺失值比例: {(df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100:.1f}%\n")
        
        print(f"分析報告已保存到: {report_path}")
        return report_path


def main():
    """Main function to demonstrate weather data processing"""
    try:
        # Initialize processor
        processor = WeatherDataProcessor()
        
        print("=== 天氣數據處理器 ===")
        print("Weather Data Processor")
        print("=" * 40)
        
        # Define locations to collect data from
        locations = [
            "臺北市", "新北市", "桃園市", "臺中市", 
            "臺南市", "高雄市", "基隆市", "新竹市",
            "嘉義市", "宜蘭縣", "花蓮縣", "臺東縣"
        ]
        
        # Collect weather data
        print("\n1. 收集天氣數據...")
        weather_df = processor.collect_weather_data(locations)
        
        if weather_df.empty:
            print("沒有收集到天氣數據，請檢查 API 連接")
            return
        
        # Create GeoDataFrame
        print("\n2. 創建地理數據框...")
        gdf = processor.create_geodataframe(weather_df)
        
        # Analyze weather patterns
        print("\n3. 分析天氣模式...")
        analysis = processor.analyze_weather_patterns(weather_df)
        
        # Create temperature map
        print("\n4. 創建溫度地圖...")
        map_path = processor.create_temperature_map(gdf)
        
        # Create charts
        print("\n5. 創建分析圖表...")
        chart_paths = processor.create_weather_charts(weather_df)
        
        # Generate report
        print("\n6. 生成分析報告...")
        report_path = processor.generate_weather_report(weather_df, analysis)
        
        print("\n=== 處理完成 ===")
        print(f"地圖: {map_path}")
        print(f"圖表: {chart_paths}")
        print(f"報告: {report_path}")
        
    except Exception as e:
        print(f"錯誤: {e}")


if __name__ == "__main__":
    main()
