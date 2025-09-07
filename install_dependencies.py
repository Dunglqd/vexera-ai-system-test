#!/usr/bin/env python3
"""
Script để cài đặt dependencies một cách an toàn
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Chạy command và hiển thị kết quả"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} thành công")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} thất bại: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Cài đặt dependencies theo thứ tự ưu tiên"""
    print("=" * 60)
    print("🔧 Cài đặt Dependencies cho Vexere AI System")
    print("=" * 60)
    
    # Danh sách commands theo thứ tự ưu tiên
    commands = [
        ("pip install --upgrade pip", "Cập nhật pip"),
        ("pip uninstall -y huggingface-hub", "Gỡ bỏ huggingface-hub cũ"),
        ("pip install huggingface-hub==0.19.4", "Cài đặt huggingface-hub tương thích"),
        ("pip install sentence-transformers==2.2.2", "Cài đặt sentence-transformers"),
        ("pip install faiss-cpu==1.7.4", "Cài đặt faiss-cpu"),
        ("pip install -r requirements.txt", "Cài đặt các dependencies còn lại"),
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
        else:
            print(f"⚠️ Bỏ qua lỗi và tiếp tục...")
    
    print("\n" + "=" * 60)
    print(f"📊 Kết quả: {success_count}/{len(commands)} commands thành công")
    
    if success_count >= len(commands) - 1:  # Cho phép 1 lỗi nhỏ
        print("✅ Cài đặt dependencies hoàn tất!")
        print("\n🚀 Bây giờ bạn có thể chạy:")
        print("   python start_system.py")
    else:
        print("❌ Có lỗi trong quá trình cài đặt")
        print("💡 Thử chạy lại script này hoặc cài đặt thủ công")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
