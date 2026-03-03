#!/usr/bin/env python3
"""
Central Weather Administration AQI API Client
中央氣象局空氣品質指標 API 客戶端

This script fetches AQI data using CWA API.
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

class CWAAQIClient:
    """Central Weather Administration AQI API Client"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize CWA AQI API Client
        
        Args:
            api_key: CWA API key. If not provided, will use environment variable.
        """
        self.api_key = api_key or os.getenv('CWA_API_KEY')
        if not self.api_key:
            raise ValueError("CWA API key is required. Set CWA_API_KEY environment variable.")
        
        self.base_url = "https://opendata.cwa.gov.tw/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GIS-Project-CWA-AQI-Client/1.0',
            'Accept': 'application/json'
        })
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make request to CWA API
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            API response data
        """
        url = f"{self.base_url}/{endpoint}"
        
        if params is None:
            params = {}
        
        params['Authorization'] = self.api_key
        params['format'] = 'JSON'
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            raise
    
    def get_aqi_data(self) -> Dict[str, Any]:
        """
        Get AQI data from CWA
        
        Returns:
            AQI data
        """
        # Note: CWA might not have direct AQI API, so we'll try to get related data
        # This is a placeholder - you may need to adjust based on actual CWA API structure
        endpoint = "rest/datastore/F-A0012-001"  # This is an example endpoint
        
        params = {
            'limit': 1000
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
    """Main function to demonstrate CWA AQI API usage"""
    try:
        # Initialize client
        client = CWAAQIClient()
        
        print("=== 中央氣象局空氣品質指標 API 客戶端 ===")
        print("CWA AQI API Client Demo")
        print("=" * 40)
        
        # Get AQI data
        print("\n1. 獲取空氣品質數據...")
        aqi_data = client.get_aqi_data()
        
        if 'records' in aqi_data and aqi_data['records']:
            records = aqi_data['records']
            print(f"找到 {len(records)} 條記錄")
            
            # Display sample data
            print("\n前5條記錄:")
            for i, record in enumerate(records[:5]):
                print(f"{i+1}. {record}")
        else:
            print("未找到 AQI 數據")
            print("API 返回:", aqi_data)
        
        # Save data
        print("\n2. 保存 AQI 數據...")
        client.save_to_csv(aqi_data, "cwa_aqi_data.csv")
        
        print("\n=== 數據獲取完成 ===")
        
    except Exception as e:
        print(f"錯誤: {e}")


if __name__ == "__main__":
    main()
