#!/usr/bin/env python3
"""
Central Weather Administration (CWA) API Client
台灣中央氣象局 API 客戶端

This script provides functions to fetch weather data from the CWA API.
"""

import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CWAClient:
    """Central Weather Administration API Client"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize CWA API Client
        
        Args:
            api_key: CWA API key. If not provided, will use environment variable.
        """
        self.api_key = api_key or os.getenv('CWA_API_KEY')
        if not self.api_key:
            raise ValueError("CWA API key is required. Set CWA_API_KEY environment variable.")
        
        self.base_url = "https://opendata.cwa.gov.tw/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GIS-Project-CWA-Client/1.0',
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
    
    def get_current_weather(self, location_name: str = "臺北市") -> Dict[str, Any]:
        """
        Get current weather observation
        
        Args:
            location_name: Location name in Chinese
            
        Returns:
            Current weather data
        """
        endpoint = "rest/datastore/O-A0003-001"
        params = {
            'locationName': location_name,
            'elementName': 'TEMP,HUMD,PRES,WD,WDSD,Weather'
        }
        
        return self._make_request(endpoint, params)
    
    def get_weather_forecast(self, location_name: str = "臺北市") -> Dict[str, Any]:
        """
        Get weather forecast
        
        Args:
            location_name: Location name in Chinese
            
        Returns:
            Weather forecast data
        """
        endpoint = "rest/datastore/F-C0032-001"
        params = {
            'locationName': location_name,
            'elementName': 'Wx,PoP,MinT,MaxT,CI'
        }
        
        return self._make_request(endpoint, params)
    
    def get_weather_forecast_36hr(self, location_name: str = "臺北市") -> Dict[str, Any]:
        """
        Get 36-hour weather forecast
        
        Args:
            location_name: Location name in Chinese
            
        Returns:
            36-hour weather forecast data
        """
        endpoint = "rest/datastore/F-C0032-001"
        params = {
            'locationName': location_name,
            'elementName': 'Wx,PoP6h,Td,CI'
        }
        
        return self._make_request(endpoint, params)
    
    def get_earthquake_info(self) -> Dict[str, Any]:
        """
        Get recent earthquake information
        
        Returns:
            Earthquake data
        """
        endpoint = "rest/datastore/E-A0016-001"
        
        return self._make_request(endpoint)
    
    def get_typhoon_info(self) -> Dict[str, Any]:
        """
        Get typhoon information
        
        Returns:
            Typhoon data
        """
        endpoint = "rest/datastore/W-C0033-001"
        
        return self._make_request(endpoint)
    
    def get_radar_image(self, time: Optional[str] = None) -> Dict[str, Any]:
        """
        Get radar image information
        
        Args:
            time: Time in format YYYYMMDDHHmm, defaults to latest
            
        Returns:
            Radar image data
        """
        endpoint = "rest/datastore/O-A0059-001"
        params = {}
        
        if time:
            params['time'] = time
        
        return self._make_request(endpoint, params)
    
    def get_available_locations(self) -> List[str]:
        """
        Get list of available location names
        
        Returns:
            List of location names
        """
        # Get a sample forecast to extract locations
        forecast_data = self.get_weather_forecast("臺北市")
        locations = []
        
        if 'records' in forecast_data and 'location' in forecast_data['records']:
            for location in forecast_data['records']['location']:
                locations.append(location['locationName'])
        
        return sorted(locations)
    
    def save_to_csv(self, data: Dict[str, Any], filename: str, output_dir: str = "../output/exports"):
        """
        Save API data to CSV file
        
        Args:
            data: API response data
            filename: Output filename
            output_dir: Output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        # Extract location data and convert to DataFrame
        if 'records' in data and 'location' in data['records']:
            locations = data['records']['location']
            
            # Flatten the data structure
            flattened_data = []
            for location in locations:
                base_info = {
                    'locationName': location.get('locationName', ''),
                    'lat': location.get('lat', ''),
                    'lon': location.get('lon', ''),
                    'stationId': location.get('stationId', ''),
                    'time': location.get('time', {}).get('obsTime', '')
                }
                
                # Add weather elements
                if 'weatherElement' in location:
                    for element in location['weatherElement']:
                        element_name = element.get('elementName', '')
                        element_value = element.get('elementValue', {})
                        
                        if isinstance(element_value, dict):
                            base_info[element_name] = element_value.get('value', '')
                        else:
                            base_info[element_name] = element_value
                
                flattened_data.append(base_info)
            
            df = pd.DataFrame(flattened_data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            print(f"Data saved to: {filepath}")
        else:
            # Save raw JSON as fallback
            with open(filepath.replace('.csv', '.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Raw JSON data saved to: {filepath.replace('.csv', '.json')}")


def main():
    """Main function to demonstrate CWA API usage"""
    try:
        # Initialize client
        client = CWAClient()
        
        print("=== 中央氣象局 API 客戶端 ===")
        print("CWA API Client Demo")
        print("=" * 40)
        
        # Get available locations
        print("\n1. 獲取可用地點列表...")
        locations = client.get_available_locations()
        print(f"找到 {len(locations)} 個地點")
        print("前10個地點:", locations[:10])
        
        # Get current weather for Taipei
        print("\n2. 獲取臺北市當前天氣...")
        current_weather = client.get_current_weather("臺北市")
        
        if 'records' in current_weather and 'location' in current_weather['records']:
            location_data = current_weather['records']['location'][0]
            print(f"地點: {location_data.get('locationName', '')}")
            print(f"觀測時間: {location_data.get('time', {}).get('obsTime', '')}")
            
            # Display weather elements
            if 'weatherElement' in location_data:
                for element in location_data['weatherElement']:
                    name = element.get('elementName', '')
                    value = element.get('elementValue', {})
                    if isinstance(value, dict):
                        print(f"{name}: {value.get('value', '')} {value.get('measure', '')}")
                    else:
                        print(f"{name}: {value}")
        
        # Save current weather data
        print("\n3. 保存當前天氣數據...")
        client.save_to_csv(current_weather, "current_weather_taipei.csv")
        
        # Get weather forecast
        print("\n4. 獲取天氣預報...")
        forecast = client.get_weather_forecast("臺北市")
        client.save_to_csv(forecast, "weather_forecast_taipei.csv")
        
        # Get earthquake info
        print("\n5. 獲取地震資訊...")
        earthquake_data = client.get_earthquake_info()
        if 'records' in earthquake_data and 'Earthquake' in earthquake_data['records']:
            earthquakes = earthquake_data['records']['Earthquake']
            print(f"最近 {len(earthquakes)} 筆地震記錄")
            
            for eq in earthquakes[:3]:  # Show first 3
                print(f"- {eq.get('reportContent', '')}")
                print(f"  時間: {eq.get('earthquakeNo', '')}")
                print(f"  規模: {eq.get('magnitude', {}).get('magnitudeValue', '')}")
        
        print("\n=== 資料獲取完成 ===")
        
    except Exception as e:
        print(f"錯誤: {e}")


if __name__ == "__main__":
    main()
