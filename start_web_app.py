#!/usr/bin/env python3
"""
Infinity Stones Search Engine - Web Application Startup Script
This script starts the Flask web server for the Infinity Stones Search Engine
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_cors
        print("✅ Flask and Flask-CORS are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Installing required packages...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Required packages installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install required packages")
            return False

def check_data_file():
    """Check if the dataset file exists"""
    data_file = Path("data-set.json")
    if data_file.exists():
        print(f"✅ Dataset file found: {data_file}")
        return True
    else:
        print(f"❌ Dataset file not found: {data_file}")
        print("Please ensure data-set.json is in the current directory")
        return False

def start_server():
    """Start the Flask development server"""
    print("🚀 Starting Infinity Stones Search Engine Web Server...")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Check data file
    if not check_data_file():
        return False
    
    print("🔮 Initializing the Infinity Stones...")
    print("🌐 Web interface will be available at: http://localhost:5000")
    print("🔧 API endpoints available at: http://localhost:5000/api/")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start the Flask app
    try:
        from app import app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main function"""
    print("🔮 INFINITY STONES SEARCH ENGINE - WEB INTERFACE 🔮")
    print("=" * 60)
    print("Starting the cosmic web application...")
    print()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Start the server
    success = start_server()
    
    if success:
        print("✨ Thank you for using the Infinity Stones Search Engine!")
    else:
        print("❌ Failed to start the web server")
        sys.exit(1)

if __name__ == "__main__":
    main()
