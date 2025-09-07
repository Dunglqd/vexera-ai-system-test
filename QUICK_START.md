# 🚀 Hướng dẫn khởi động nhanh

## Cách chạy hệ thống

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy Backend API (chỉ API)
```bash
python run_backend.py
```
- API sẽ chạy tại: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 3. Chạy toàn bộ hệ thống (Backend + Frontend)
```bash
python start_system.py
```
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### 4. Chạy Backend thủ công (nếu cần)
```bash
python -m app.main
```
hoặc
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Lưu ý
- Đảm bảo bạn đang ở thư mục gốc của project (`E:\LearnIT\azure\vexera`)
- Nếu gặp lỗi import, hãy chạy từ thư mục gốc với lệnh `python -m app.main`
- File `faq_data.csv` phải có trong thư mục gốc để hệ thống hoạt động
