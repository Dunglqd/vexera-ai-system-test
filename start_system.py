#!/usr/bin/env python3
"""
Startup script for Vexere AI Customer Service System
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import streamlit
        import sentence_transformers
        import faiss
        import pandas
        import numpy
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_data_files():
    """Check if required data files exist"""
    print("📁 Checking data files...")
    
    faq_file = Path("faq_data.csv")
    if not faq_file.exists():
        print("❌ faq_data.csv not found")
        return False
    
    print("✅ Data files found")
    return True

def start_backend():
    """Start FastAPI backend server"""
    print("🚀 Starting backend server...")
    
    try:
        # Start FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
        return True

def start_frontend():
    """Start Streamlit frontend"""
    print("🎨 Starting frontend...")
    
    try:
        # Start Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", 
            "run", "frontend/streamlit_app.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start frontend: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")
        return True

def open_browser():
    """Open browser to the application"""
    time.sleep(3)  # Wait for servers to start
    print("🌐 Opening browser...")
    
    try:
        webbrowser.open("http://localhost:8501")
        webbrowser.open("http://localhost:8000/docs")
    except Exception as e:
        print(f"⚠️ Could not open browser: {e}")
        print("Please manually open: http://localhost:8501")

def main():
    """Main startup function"""
    print("=" * 60)
    print("✈️  Vexere AI Customer Service System")
    print("=" * 60)
    
    # Check prerequisites
    if not check_dependencies():
        sys.exit(1)
    
    if not check_data_files():
        sys.exit(1)
    
    print("\n🎯 Starting system components...")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a bit for backend to start
    time.sleep(2)
    
    # Start frontend in a separate thread
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("\n" + "=" * 60)
    print("🎉 System started successfully!")
    print("=" * 60)
    print("📱 Frontend: http://localhost:8501")
    print("🔧 API Docs: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    print("\n💡 Press Ctrl+C to stop the system")
    print("=" * 60)
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down system...")
        print("✅ System stopped successfully")

if __name__ == "__main__":
    main()

