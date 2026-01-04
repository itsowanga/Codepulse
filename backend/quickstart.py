#!/usr/bin/env python3
"""
CodePulse Quick Start Guide
Run this file to get everything set up and running
"""

import os
import subprocess
import sys
import time
from config import get_db_path

def run_command(cmd, description):
    """Run a shell command and report status"""
    print(f"\n📌 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            return True
        else:
            print(f"❌ {description} - Failed!")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 CodePulse - Live Dashboard Setup")
    print("=" * 60)
    
    # Check if data/activity.db exists
    db_path = get_db_path()
    if not os.path.exists(db_path):
        print("\n⚠️  Database not found! Initializing sample data...")
        run_command('python backend/init_sample_data.py', 'Initialize sample data')
    else:
        print(f"✅ Database found ({os.path.getsize(db_path)} bytes)")
    
    # Check Flask
    print("\n📦 Checking dependencies...")
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask not installed. Installing...")
        run_command('pip install flask flask-cors', 'Install Flask & CORS')
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SETUP COMPLETE!")
    print("=" * 60)
    
    print("""
To start the dashboard:
    1. Run: python backend/api_server.py
    2. Open: http://localhost:5000
    3. Charts update every 30 seconds

API Endpoints:
  GET /api/stats       - Last 7 days activity
  GET /api/languages   - Today's language breakdown
  GET /api/projects    - Top projects by activity
  GET /api/health      - API health check

Tips:
  - Leave the server running to keep data fresh
  - Auto-updates every 30 seconds
  - Green indicator = connected, Red = offline
  - Browser back button won't work (single page app)
  
Troubleshooting:
    - Port 5000 in use? Use: python -c "from backend.api_server import app; app.run(port=8000)"
    - No data? Run: python backend/init_sample_data.py
  - Check: http://localhost:5000/api/health
    """)

if __name__ == '__main__':
    main()
