#!/usr/bin/env python3
"""
Simple script to run the FastAPI backend server
"""

import subprocess
import sys
import os

def main():
    """Run the FastAPI backend server"""
    print("🚀 Starting Vexere AI Customer Service Backend...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Change to the project root directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Start FastAPI server using uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start backend: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
        print("✅ Shutdown complete")

if __name__ == "__main__":
    main()
