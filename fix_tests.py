#!/usr/bin/env python3
"""
Script để sửa lỗi tests
"""

import subprocess
import sys
import os

def main():
    """Sửa lỗi tests"""
    print("🔧 Đang sửa lỗi tests...")
    print("=" * 50)
    
    # 1. Cài đặt FAISS version cũ
    print("📦 Cài đặt FAISS version tương thích...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "uninstall", "-y", "faiss-cpu"
        ], check=True)
        
        subprocess.run([
            sys.executable, "-m", "pip", "install", "faiss-cpu==1.7.4"
        ], check=True)
        print("✅ FAISS đã được cài đặt lại")
    except Exception as e:
        print(f"❌ Lỗi cài đặt FAISS: {e}")
    
    # 2. Cài đặt dependencies
    print("\n📦 Cài đặt dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ Dependencies đã được cài đặt")
    except Exception as e:
        print(f"❌ Lỗi cài đặt dependencies: {e}")
    
    # 3. Chạy tests
    print("\n🧪 Chạy tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "app/tests/", "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print("📊 Kết quả tests:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Tất cả tests đã pass!")
        else:
            print(f"❌ Còn {result.returncode} test failed")
            
    except Exception as e:
        print(f"❌ Lỗi chạy tests: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Hoàn tất sửa lỗi tests!")

if __name__ == "__main__":
    main()
