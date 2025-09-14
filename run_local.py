<<<<<<< HEAD
#!/usr/bin/env python3
"""
Local development server for Chartink Backtesting Dashboard.
This script helps you run the app locally for testing.
"""

import os
import sys
import subprocess
import webbrowser
from time import sleep

def check_requirements():
    """Check if requirements are installed"""
    try:
        import flask
        import pandas
        import numpy
        import plotly
        import requests
        return True
    except ImportError:
        return False

def install_requirements():
    """Install requirements if not present"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_uploads_directory():
    """Create uploads directory if it doesn't exist"""
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        print("📁 Created uploads directory")

def run_app():
    """Run the Flask application"""
    print("🚀 Starting Chartink Backtesting Dashboard...")
    print("📍 Local URL: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Import and run the app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")

def main():
    """Main function"""
    print("🎯 Chartink Backtesting Dashboard - Local Development")
    print("=" * 60)
    
    # Check if requirements are installed
    if not check_requirements():
        print("⚠️  Requirements not found. Installing...")
        if not install_requirements():
            print("❌ Failed to install requirements. Please install manually:")
            print("   pip install -r requirements.txt")
            return False
    
    # Create necessary directories
    create_uploads_directory()
    
    # Run the app
    run_app()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
=======
#!/usr/bin/env python3
"""
Local development server for Chartink Backtesting Dashboard.
This script helps you run the app locally for testing.
"""

import os
import sys
import subprocess
import webbrowser
from time import sleep

def check_requirements():
    """Check if requirements are installed"""
    try:
        import flask
        import pandas
        import numpy
        import plotly
        import requests
        return True
    except ImportError:
        return False

def install_requirements():
    """Install requirements if not present"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_uploads_directory():
    """Create uploads directory if it doesn't exist"""
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        print("📁 Created uploads directory")

def run_app():
    """Run the Flask application"""
    print("🚀 Starting Chartink Backtesting Dashboard...")
    print("📍 Local URL: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Import and run the app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")

def main():
    """Main function"""
    print("🎯 Chartink Backtesting Dashboard - Local Development")
    print("=" * 60)
    
    # Check if requirements are installed
    if not check_requirements():
        print("⚠️  Requirements not found. Installing...")
        if not install_requirements():
            print("❌ Failed to install requirements. Please install manually:")
            print("   pip install -r requirements.txt")
            return False
    
    # Create necessary directories
    create_uploads_directory()
    
    # Run the app
    run_app()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
>>>>>>> 1abbab347fd49b3876b85f07a1608ddf2868e824
