#!/usr/bin/env python3
"""
Simple test script to verify the application works correctly.
Run this before deploying to ensure everything is working.
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import flask
        import pandas
        import numpy
        import plotly
        import requests
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_csv_parsing():
    """Test CSV parsing functionality"""
    try:
        # Create a test CSV
        test_data = {
            'entry_datetime': ['06-08-2025 10:15 am', '06-08-2025 11:15 am'],
            'symbol': ['YATHARTH', 'KAMATHOTEL'],
            'market_cap': ['Midcap', 'Smallcap'],
            'sector': ['Pharmaceuticals', 'Services']
        }
        
        df = pd.DataFrame(test_data)
        df['entry_datetime'] = pd.to_datetime(df['entry_datetime'])
        
        print("✅ CSV parsing test passed")
        return True
    except Exception as e:
        print(f"❌ CSV parsing error: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'templates/index.html',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_flask_app():
    """Test if Flask app can be created"""
    try:
        from app import app
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Flask app test passed")
                return True
            else:
                print(f"❌ Flask app returned status code: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Chartink Backtesting Dashboard Tests\n")
    
    tests = [
        ("Import Test", test_imports),
        ("File Structure Test", test_file_structure),
        ("CSV Parsing Test", test_csv_parsing),
        ("Flask App Test", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your app is ready for deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Please fix the issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
