#!/usr/bin/env python3
"""
Environmental Protection Agency AQI API Client
環境部空氣品質指標 API 客戶端

This script fetches real-time AQI data from EPA's open data API.
"""

import os
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EPAAQIClient:
    """Environmental Protection Agency AQI API Client"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize EPA AQI API Client
        
        Args:
            api_key: EPA API key. If not provided, will use environment variable.
        """
        self.api_key = api_key or os.getenv('EPA_API_KEY')
        if not self.api_key:
            raise ValueError("EPA API key is required. Set EPA_API_KEY environment variable.")
        
        self.base_url = "https://data.moenv.gov.tw/api/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GIS-Project-EPA-AQI-Client/1.0',
            'Accept': 'application/json'
        })
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make request to EPA API
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            API response data
        """
        url = f"{self.base_url}/{endpoint}"
        
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            raise
    
    def get_real_time_aqi(self) -> Dict[str, Any]:
        """
        Get real-time AQI data for all monitoring stations
        
        Returns:
            Real-time AQI data
        """
        endpoint = "aqx_p_432"
        params = {
            'format': 'JSON',
            'limit': 1000  # Get all stations
        }
        
        return self._make_request(endpoint, params)
    
    def get_aqi_by_site(self, site_name: str) -> Dict[str, Any]:
        """
        Get AQI data for specific monitoring site
        
        Args:
            site_name: Site name in Chinese
            
        Returns:
            AQI data for specific site
        """
        endpoint = "aqx_p_432"
        params = {
            'format': 'JSON',
            'filters': f'SiteName eq {site_name}'
        }
        
        return self._make_request(endpoint, params)
    
    def get_aqi_by_county(self, county: str) -> Dict[str, Any]:
        """
        Get AQI data for specific county
        
        Args:
            county: County name in Chinese
            
        Returns:
            AQI data for specific county
        """
        endpoint = "aqx_p_432"
        params = {
            'format': 'JSON',
            'filters': f'County eq {county}'
        }
        
        return self._make_request(endpoint, params)
    
    def save_to_csv(self, data: Dict[str, Any], filename: str, output_dir: str = "../data/processed"):
        """
        Save AQI data to CSV file
        
        Args:
            data: API response data
            filename: Output filename
            output_dir: Output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        # Extract records and convert to DataFrame
        if 'records' in data and data['records']:
            df = pd.DataFrame(data['records'])
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            print(f"AQI data saved to: {filepath}")
        else:
            # Save raw JSON as fallback
            with open(filepath.replace('.csv', '.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Raw JSON data saved to: {filepath.replace('.csv', '.json')}")


def main():
    """Main function to demonstrate EPA AQI API usage"""
    try:
        # Initialize client
        client = EPAAQIClient()
        
        print("=== 環境部空氣品質指標 API 客戶端 ===")
        print("EPA AQI API Client Demo")
        print("=" * 40)
        
        # Get real-time AQI data
        print("\n1. 獲取全台即時 AQI 數據...")
        aqi_data = client.get_real_time_aqi()
        
        if 'records' in aqi_data and aqi_data['records']:
            records = aqi_data['records']
            print(f"找到 {len(records)} 個監測站數據")
            
            # Display sample data
            print("\n前5個監測站數據:")
            for i, record in enumerate(records[:5]):
                print(f"{i+1}. {record.get('SiteName', '')} - AQI: {record.get('AQI', 'N/A')}")
                print(f"   縣市: {record.get('County', '')}")
                print(f"   狀態: {record.get('Status', '')}")
                print(f"   PM2.5: {record.get('PM2.5', 'N/A')}")
                print(f"   PM10: {record.get('PM10', 'N/A')}")
                print()
        else:
            print("未找到 AQI 數據")
        
        # Save data
        print("\n2. 保存 AQI 數據...")
        client.save_to_csv(aqi_data, "real_time_aqi.csv")
        
        # Get data for specific county
        print("\n3. 獲取特定縣市 AQI 數據 (台北市)...")
        taipei_aqi = client.get_aqi_by_county("臺北市")
        
        if 'records' in taipei_aqi and taipei_aqi['records']:
            print(f"台北市有 {len(taipei_aqi['records'])} 個監測站")
            for record in taipei_aqi['records']:
                print(f"- {record.get('SiteName', '')}: AQI {record.get('AQI', 'N/A')}")
        
        print("\n=== 數據獲取完成 ===")
        
    except Exception as e:
        print(f"錯誤: {e}")


if __name__ == "__main__":
    main()
