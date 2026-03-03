#!/usr/bin/env python3
"""
AQI Project Setup Script
空氣品質分析專案設定腳本

This script automatically installs dependencies and sets up the environment.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ 需要 Python 3.8 或更高版本")
        print(f"當前版本: {sys.version}")
        return False
    print(f"✓ Python 版本: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n安裝專案依賴...")
    
    try:
        # Upgrade pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("✓ pip 已更新")
        
        # Install requirements
        requirements_path = Path(__file__).parent / "requirements.txt"
        if requirements_path.exists():
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)], 
                          check=True)
            print("✓ 所有依賴已安裝")
        else:
            print("❌ requirements.txt 檔案不存在")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 安裝依賴時發生錯誤: {e}")
        return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    print("\n創建專案目錄...")
    
    directories = [
        "data/processed",
        "data/raw", 
        "output/maps",
        "output/reports",
        "output/exports",
        "logs"
    ]
    
    for directory in directories:
        dir_path = Path(__file__).parent / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ {directory}")

def check_env_file():
    """Check and guide environment setup"""
    print("\n檢查環境設定...")
    
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        print("✓ .env 檔案存在")
        
        # Check if EPA_API_KEY is set
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'EPA_API_KEY=your_epa_api_key_here' in content:
                print("⚠️  請在 .env 檔案中設定您的 EPA API 金鑰")
                print("   1. 前往 https://data.epa.gov.tw/api/v1/")
                print("   2. 註冊並獲取 API 金鑰")
                print("   3. 將 .env 檔案中的 'your_epa_api_key_here' 替換為您的金鑰")
                return False
            else:
                print("✓ EPA API 金鑰已設定")
    else:
        print("❌ .env 檔案不存在")
        return False
    
    return True

def test_imports():
    """Test if all required modules can be imported"""
    print("\n測試模組導入...")
    
    required_modules = [
        'pandas',
        'geopandas', 
        'folium',
        'requests',
        'dotenv',
        'numpy',
        'matplotlib'
    ]
    
    failed_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_modules.append(module)
    
    if failed_modules:
        print(f"\n❌ 以下模組導入失敗: {', '.join(failed_modules)}")
        print("請重新安裝依賴")
        return False
    
    return True

def run_sample_test():
    """Run a sample test to verify the setup"""
    print("\n執行範例測試...")
    
    try:
        # Test AQI client import
        from aqi_api_client import EPAAQIClient
        print("✓ AQI 客戶端導入成功")
        
        # Test visualizer import
        from aqi_visualizer import AQIVisualizer
        print("✓ AQI 視覺化工具導入成功")
        
        print("✓ 所有組件測試通過")
        return True
        
    except ImportError as e:
        print(f"❌ 模組導入失敗: {e}")
        return False
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("空氣品質分析專案自動設定")
    print("AQI Analysis Project Auto Setup")
    print("=" * 60)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    steps = [
        ("檢查 Python 版本", check_python_version),
        ("安裝依賴", install_dependencies),
        ("創建目錄", setup_directories),
        ("檢查環境設定", check_env_file),
        ("測試模組導入", test_imports),
        ("執行範例測試", run_sample_test)
    ]
    
    all_passed = True
    
    for step_name, step_func in steps:
        print(f"\n{step_name}:")
        print("-" * 30)
        
        if not step_func():
            all_passed = False
            if step_name in ["檢查 Python 版本", "安裝依賴"]:
                print("❌ 必要步驟失敗，設定中止")
                break
            else:
                print("⚠️  非必要步驟失敗，繼續執行")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 設定完成！")
        print("\n下一步:")
        print("1. 確保已在 .env 檔案中設定 EPA_API_KEY")
        print("2. 運行: python scripts/run_aqi_analysis.py")
        print("3. 在瀏覽器中打開生成的地圖檔案")
    else:
        print("❌ 設定未完成，請解決上述問題")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
