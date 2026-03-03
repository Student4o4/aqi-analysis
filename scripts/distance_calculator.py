#!/usr/bin/env python3
"""
Distance Calculator for AQI Monitoring Stations
AQI 監測站距離計算器

This script calculates distances from each monitoring station to Taipei Main Station.
"""

import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
from geopy.distance import geodesic
import os
from datetime import datetime

class DistanceCalculator:
    """Distance calculator for AQI monitoring stations"""
    
    def __init__(self):
        """Initialize calculator with Taipei Main Station coordinates"""
        self.taipei_main_station = (25.0478, 121.5170)  # (latitude, longitude)
        self.output_dir = "../output"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
    
    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
            
        Returns:
            Distance in kilometers
        """
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        # Earth's radius in kilometers
        r = 6371.0
        return c * r
    
    def geodesic_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance using geopy's geodesic method (more accurate)
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
            
        Returns:
            Distance in kilometers
        """
        point1 = (lat1, lon1)
        point2 = (lat2, lon2)
        
        return geodesic(point1, point2).kilometers
    
    def calculate_distances_from_dataframe(self, df: pd.DataFrame, method: str = 'geodesic') -> pd.DataFrame:
        """
        Calculate distances from all stations to Taipei Main Station
        
        Args:
            df: DataFrame with station coordinates
            method: 'haversine' or 'geodesic'
            
        Returns:
            DataFrame with distance calculations
        """
        result_df = df.copy()
        
        distances = []
        
        for _, row in df.iterrows():
            station_lat = float(row['Latitude'])
            station_lon = float(row['Longitude'])
            
            if method == 'haversine':
                distance = self.haversine_distance(
                    station_lat, station_lon,
                    self.taipei_main_station[0], self.taipei_main_station[1]
                )
            else:  # geodesic
                distance = self.geodesic_distance(
                    station_lat, station_lon,
                    self.taipei_main_station[0], self.taipei_main_station[1]
                )
            
            distances.append(distance)
        
        result_df['Distance_to_Taipei_Main_km'] = distances
        result_df['Distance_Calculation_Method'] = method
        
        return result_df
    
    def calculate_distance_statistics(self, df: pd.DataFrame) -> dict:
        """
        Calculate distance statistics
        
        Args:
            df: DataFrame with distance column
            
        Returns:
            Dictionary with statistics
        """
        if 'Distance_to_Taipei_Main_km' not in df.columns:
            return {}
        
        distances = df['Distance_to_Taipei_Main_km']
        
        stats = {
            'count': len(distances),
            'mean_km': distances.mean(),
            'min_km': distances.min(),
            'max_km': distances.max(),
            'std_km': distances.std(),
            'median_km': distances.median()
        }
        
        # Find closest and farthest stations
        closest_idx = distances.idxmin()
        farthest_idx = distances.idxmax()
        
        stats['closest_station'] = {
            'name': df.loc[closest_idx, 'SiteName'],
            'county': df.loc[closest_idx, 'County'],
            'distance_km': distances.min(),
            'coordinates': (df.loc[closest_idx, 'Latitude'], df.loc[closest_idx, 'Longitude'])
        }
        
        stats['farthest_station'] = {
            'name': df.loc[farthest_idx, 'SiteName'],
            'county': df.loc[farthest_idx, 'County'],
            'distance_km': distances.max(),
            'coordinates': (df.loc[farthest_idx, 'Latitude'], df.loc[farthest_idx, 'Longitude'])
        }
        
        return stats
    
    def save_distance_results(self, df: pd.DataFrame, stats: dict, filename_prefix: str = "station_distances"):
        """
        Save distance calculation results to CSV
        
        Args:
            df: DataFrame with distance calculations
            stats: Distance statistics
            filename_prefix: Prefix for output files
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save detailed results
        csv_filename = f"{filename_prefix}_{timestamp}.csv"
        csv_path = os.path.join(self.output_dir, csv_filename)
        
        # Reorder columns for better readability
        columns_order = [
            'SiteName', 'County', 'AQI', 'Status', 'Latitude', 'Longitude',
            'Distance_to_Taipei_Main_km', 'Distance_Calculation_Method',
            'PublishTime', 'PM2.5', 'PM10', 'O3'
        ]
        
        # Only include columns that exist
        available_columns = [col for col in columns_order if col in df.columns]
        result_df = df[available_columns]
        
        # Sort by distance
        result_df = result_df.sort_values('Distance_to_Taipei_Main_km')
        
        result_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"距離計算結果已保存到: {csv_path}")
        
        # Save statistics summary
        stats_filename = f"{filename_prefix}_statistics_{timestamp}.txt"
        stats_path = os.path.join(self.output_dir, stats_filename)
        
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write("AQI 監測站到台北車站距離統計\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"計算時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"台北車站座標: {self.taipei_main_station}\n")
            f.write(f"計算方法: {stats.get('method', 'geodesic')}\n\n")
            
            f.write("統計摘要:\n")
            f.write("-" * 30 + "\n")
            f.write(f"監測站總數: {stats['count']}\n")
            f.write(f"平均距離: {stats['mean_km']:.2f} km\n")
            f.write(f"最短距離: {stats['min_km']:.2f} km\n")
            f.write(f"最長距離: {stats['max_km']:.2f} km\n")
            f.write(f"距離標準差: {stats['std_km']:.2f} km\n")
            f.write(f"距離中位數: {stats['median_km']:.2f} km\n\n")
            
            f.write("最近的監測站:\n")
            f.write("-" * 30 + "\n")
            closest = stats['closest_station']
            f.write(f"站名: {closest['name']}\n")
            f.write(f"縣市: {closest['county']}\n")
            f.write(f"距離: {closest['distance_km']:.2f} km\n")
            f.write(f"座標: {closest['coordinates']}\n\n")
            
            f.write("最遠的監測站:\n")
            f.write("-" * 30 + "\n")
            farthest = stats['farthest_station']
            f.write(f"站名: {farthest['name']}\n")
            f.write(f"縣市: {farthest['county']}\n")
            f.write(f"距離: {farthest['distance_km']:.2f} km\n")
            f.write(f"座標: {farthest['coordinates']}\n\n")
            
            # Distance distribution
            distances = df['Distance_to_Taipei_Main_km']
            f.write("距離分佈:\n")
            f.write("-" * 30 + "\n")
            f.write(f"0-25 km: {len(distances[distances <= 25])} 個站\n")
            f.write(f"25-50 km: {len(distances[(distances > 25) & (distances <= 50)])} 個站\n")
            f.write(f"50-100 km: {len(distances[(distances > 50) & (distances <= 100)])} 個站\n")
            f.write(f"100+ km: {len(distances[distances > 100])} 個站\n")
        
        print(f"統計報告已保存到: {stats_path}")
        
        return csv_path, stats_path


def create_sample_aqi_data():
    """Create sample AQI data with Taiwan monitoring stations"""
    sample_data = [
        {'SiteName': '台北', 'County': '臺北市', 'AQI': 45, 'Latitude': 25.0320, 'Longitude': 121.5654, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 12, 'PM10': 18, 'O3': 35, 'Status': '良好'},
        {'SiteName': '松山', 'County': '臺北市', 'AQI': 52, 'Latitude': 25.0500, 'Longitude': 121.5770, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 15, 'PM10': 22, 'O3': 42, 'Status': '普通'},
        {'SiteName': '板橋', 'County': '新北市', 'AQI': 68, 'Latitude': 25.0150, 'Longitude': 121.4630, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 18, 'PM10': 25, 'O3': 45, 'Status': '普通'},
        {'SiteName': '桃園', 'County': '桃園市', 'AQI': 85, 'Latitude': 24.9936, 'Longitude': 121.3010, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 25, 'PM10': 35, 'O3': 58, 'Status': '普通'},
        {'SiteName': '台中', 'County': '臺中市', 'AQI': 78, 'Latitude': 24.1477, 'Longitude': 120.6736, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 22, 'PM10': 30, 'O3': 52, 'Status': '普通'},
        {'SiteName': '台南', 'County': '臺南市', 'AQI': 105, 'Latitude': 22.9999, 'Longitude': 120.2269, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 35, 'PM10': 45, 'O3': 75, 'Status': '對敏感族群不健康'},
        {'SiteName': '高雄', 'County': '高雄市', 'AQI': 98, 'Latitude': 22.6273, 'Longitude': 120.3014, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 32, 'PM10': 42, 'O3': 68, 'Status': '普通'},
        {'SiteName': '基隆', 'County': '基隆市', 'AQI': 42, 'Latitude': 25.1276, 'Longitude': 121.7392, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 11, 'PM10': 16, 'O3': 32, 'Status': '良好'},
        {'SiteName': '宜蘭', 'County': '宜蘭縣', 'AQI': 35, 'Latitude': 24.7700, 'Longitude': 121.7326, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 9, 'PM10': 14, 'O3': 26, 'Status': '良好'},
        {'SiteName': '花蓮', 'County': '花蓮縣', 'AQI': 38, 'Latitude': 23.8228, 'Longitude': 121.6090, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 10, 'PM10': 15, 'O3': 29, 'Status': '良好'},
        {'SiteName': '台東', 'County': '臺東縣', 'AQI': 32, 'Latitude': 22.7580, 'Longitude': 121.1500, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 8, 'PM10': 13, 'O3': 24, 'Status': '良好'},
        {'SiteName': '新竹', 'County': '新竹市', 'AQI': 58, 'Latitude': 24.8138, 'Longitude': 120.9675, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 16, 'PM10': 22, 'O3': 40, 'Status': '普通'},
        {'SiteName': '嘉義', 'County': '嘉義市', 'AQI': 72, 'Latitude': 23.4801, 'Longitude': 120.4491, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 20, 'PM10': 28, 'O3': 48, 'Status': '普通'},
        {'SiteName': '屏東', 'County': '屏東縣', 'AQI': 88, 'Latitude': 22.6756, 'Longitude': 120.4884, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 26, 'PM10': 36, 'O3': 60, 'Status': '普通'},
        {'SiteName': '苗栗', 'County': '苗栗縣', 'AQI': 65, 'Latitude': 24.5660, 'Longitude': 120.8220, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 19, 'PM10': 26, 'O3': 46, 'Status': '普通'},
        {'SiteName': '彰化', 'County': '彰化縣', 'AQI': 76, 'Latitude': 24.0815, 'Longitude': 120.5450, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 21, 'PM10': 29, 'O3': 51, 'Status': '普通'},
        {'SiteName': '南投', 'County': '南投縣', 'AQI': 48, 'Latitude': 23.9096, 'Longitude': 120.6870, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 13, 'PM10': 18, 'O3': 36, 'Status': '良好'},
        {'SiteName': '雲林', 'County': '雲林縣', 'AQI': 82, 'Latitude': 23.7080, 'Longitude': 120.4300, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 24, 'PM10': 33, 'O3': 55, 'Status': '普通'},
        {'SiteName': '澎湖', 'County': '澎湖縣', 'AQI': 55, 'Latitude': 23.5640, 'Longitude': 119.5780, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 15, 'PM10': 20, 'O3': 38, 'Status': '普通'},
        {'SiteName': '金門', 'County': '金門縣', 'AQI': 41, 'Latitude': 24.4320, 'Longitude': 118.3220, 'PublishTime': '2024-03-03 14:00', 'PM2.5': 11, 'PM10': 15, 'O3': 30, 'Status': '良好'},
    ]
    
    return pd.DataFrame(sample_data)


def main():
    """Main function to demonstrate distance calculation"""
    print("=" * 60)
    print("AQI 監測站距離計算系統")
    print("AQI Station Distance Calculator")
    print("=" * 60)
    print(f"執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize calculator
    calculator = DistanceCalculator()
    print(f"台北車站座標: {calculator.taipei_main_station}")
    print()
    
    # Create sample data
    print("步驟 1: 創建範例 AQI 數據")
    print("-" * 30)
    aqi_df = create_sample_aqi_data()
    print(f"✓ 創建了 {len(aqi_df)} 個監測站的數據")
    print()
    
    # Calculate distances
    print("步驟 2: 計算到台北車站的距離")
    print("-" * 30)
    result_df = calculator.calculate_distances_from_dataframe(aqi_df, method='geodesic')
    print(f"✓ 使用 geodesic 方法計算距離")
    print()
    
    # Calculate statistics
    print("步驟 3: 計算距離統計")
    print("-" * 30)
    stats = calculator.calculate_distance_statistics(result_df)
    stats['method'] = 'geodesic'
    
    print(f"監測站總數: {stats['count']}")
    print(f"平均距離: {stats['mean_km']:.2f} km")
    print(f"最短距離: {stats['min_km']:.2f} km")
    print(f"最長距離: {stats['max_km']:.2f} km")
    print()
    
    # Show closest and farthest stations
    print("最近的監測站:")
    closest = stats['closest_station']
    print(f"  {closest['name']} ({closest['county']}): {closest['distance_km']:.2f} km")
    print()
    
    print("最遠的監測站:")
    farthest = stats['farthest_station']
    print(f"  {farthest['name']} ({farthest['county']}): {farthest['distance_km']:.2f} km")
    print()
    
    # Save results
    print("步驟 4: 保存計算結果")
    print("-" * 30)
    csv_path, stats_path = calculator.save_distance_results(result_df, stats)
    print()
    
    # Show sample of results
    print("距離計算結果預覽 (前10個最近的監測站):")
    print("-" * 50)
    closest_stations = result_df.nsmallest(10, 'Distance_to_Taipei_Main_km')
    for _, row in closest_stations.iterrows():
        print(f"{row['SiteName']:8s} ({row['County']:4s}): {row['Distance_to_Taipei_Main_km']:6.2f} km | AQI: {row['AQI']:3d}")
    print()
    
    print("=" * 60)
    print("距離計算完成！")
    print("=" * 60)
    print(f"輸出檔案:")
    print(f"  - 詳細結果: {csv_path}")
    print(f"  - 統計報告: {stats_path}")
    print()
    print("計算方法說明:")
    print("✓ 使用 geodesic 演算法 (WGS84 椭球體)")
    print("✓ 考慮地球曲率的精確計算")
    print("✓ 適合中距離地理計算")
    print("=" * 60)


if __name__ == "__main__":
    main()
