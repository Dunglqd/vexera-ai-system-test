# Vexere AI Customer Service System

Hệ thống AI Customer Service cho Vexere với khả năng RAG-FAQ và After-Service tự động.

## 📊 Demo 

### 1. Link Demo & Test
[Link Demo](https://drive.google.com/drive/folders/1Hqxj9jrsPU171Vd3JrtAfkIfNZtkoPMq?usp=sharing)

## ⚡ Quick Start

```bash
# 1. Cài đặt dependencies
pip install -r requirements.txt

# 2. Chạy hệ thống (Backend + Frontend)
python start_system.py

# 3. Truy cập:
# - Web Interface: http://localhost:8501
# - API Docs: http://localhost:8000/docs
```

> 💡 **Lưu ý**: Đảm bảo file `faq_data.csv` có trong thư mục gốc của project.

## 🚀 Tính năng chính

- **RAG-FAQ System**: Trả lời câu hỏi tự động sử dụng Retrieval-Augmented Generation
- **After-Service Flow**: Xử lý yêu cầu đổi giờ bay
- **Text Channel**: Giao diện chat đơn giản và thân thiện
- **Architecture Ready**: Sẵn sàng mở rộng cho Image & Voice processing

## 📋 Yêu cầu hệ thống

- Python 3.8+

## 🛠️ Cài đặt

### 1. Clone repository
```bash
git clone https://github.com/Dunglqd/vexera-ai-system-test.git
cd vexera-ai-system
```

### 2. Tạo virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Chuẩn bị dữ liệu
Đảm bảo file `faq_data.csv` có trong thư mục gốc của project.

## 🏃‍♂️ Chạy hệ thống

### 🚀 Cách 1: Chạy nhanh (Khuyến nghị)

#### Chạy toàn bộ hệ thống (Backend + Frontend)
```bash
python start_system.py
```
- ✅ Tự động khởi động cả Backend và Frontend
- ✅ Tự động mở trình duyệt
- ✅ Frontend: http://localhost:8501
- ✅ Backend API: http://localhost:8000
- ✅ API Documentation: http://localhost:8000/docs

#### Chạy chỉ Backend API
```bash
python run_backend.py
```
- ✅ Chỉ khởi động Backend API
- ✅ API: http://localhost:8000
- ✅ API Documentation: http://localhost:8000/docs
- ✅ Health Check: http://localhost:8000/health

### 🔧 Cách 2: Chạy thủ công

#### 1. Khởi động Backend API
```bash
# Sử dụng module syntax (khuyến nghị)
python -m app.main

# Hoặc sử dụng uvicorn trực tiếp
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Khởi động Frontend (Streamlit)
```bash
# Trong terminal mới
streamlit run frontend/streamlit_app.py
```

### 📱 Truy cập hệ thống
- **Web Interface**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Root API**: http://localhost:8000

## 🧪 Chạy tests

### Chạy tất cả tests
```bash
python run_tests.py
```

### Chạy test cụ thể
```bash
python run_tests.py test_rag_service.py
python run_tests.py test_faq_service.py
python run_tests.py test_booking_service.py
python run_tests.py test_api.py
```

### Chạy với pytest trực tiếp
```bash
pytest app/tests/ -v
```

## 📖 Hướng dẫn sử dụng

### 1. FAQ - Hỏi đáp tự động

1. Truy cập giao diện web tại `http://localhost:8501`
2. Chọn "FAQ - Hỏi đáp" từ sidebar
3. Nhập câu hỏi vào ô text
4. Nhấn "Gửi câu hỏi"
5. Hệ thống sẽ trả lời với độ tin cậy

**Ví dụ câu hỏi:**
- "Làm thế nào để đặt vé máy bay trên Vexere?"
- "Cách check-in online như thế nào?"
- "Thời gian hoàn tiền trong bao lâu?"

### 2. After-Service - Đổi giờ bay

1. Chọn "After-Service - Đổi giờ bay" từ sidebar
2. Nhập thông tin:
   - Mã đặt chỗ (ví dụ: VX001234)
   - Thời gian mới (định dạng: YYYY-MM-DD HH:MM)
   - Lý do thay đổi
3. Nhấn "Gửi yêu cầu thay đổi"
4. Hệ thống sẽ xử lý và thông báo kết quả

**Mã đặt chỗ mẫu:**
- VX001234 (user001)
- VX001235 (user002)

### 3. API Endpoints

#### FAQ Endpoints
```bash
# Hỏi câu hỏi FAQ
curl -X POST "http://localhost:8000/api/faq/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Làm thế nào để đặt vé?", "user_id": "user001"}'

# Lấy danh sách FAQ
curl -X GET "http://localhost:8000/api/faq/list"

# Tìm kiếm FAQ
curl -X GET "http://localhost:8000/api/faq/search?keyword=đặt vé"
```

#### After-Service Endpoints
```bash
# Đổi giờ bay
curl -X POST "http://localhost:8000/api/booking/change-time" \
     -H "Content-Type: application/json" \
     -d '{
       "booking_id": "VX001234",
       "new_departure_time": "2024-01-20 10:30",
       "reason": "Personal emergency",
       "user_id": "user001"
     }'

# Lấy thông tin đặt chỗ
curl -X GET "http://localhost:8000/api/booking/VX001234?user_id=user001"
```

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   AI Services   │
│   (Streamlit)   │◄──►│   (FastAPI)     │◄──►│   (RAG/LLM)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Data Layer    │
                       │   (CSV/FAISS)   │
                       └─────────────────┘
```

### Components chính:

1. **RAG Service**: Xử lý câu hỏi FAQ sử dụng vector similarity
2. **FAQ Service**: Quản lý logic FAQ và trả lời
3. **Booking Service**: Xử lý yêu cầu After-Service
4. **Image/Voice Services**: Kiến trúc sẵn sàng cho xử lý đa phương tiện


## 🔧 Cấu hình

### Environment Variables
Tạo file `.env` trong thư mục gốc:
```env
# OpenAI API (nếu sử dụng)
OPENAI_API_KEY=your_api_key_here

# Database
DATABASE_URL=sqlite:///./vexera.db

# Logging
LOG_LEVEL=INFO
```

### Model Configuration
Chỉnh sửa trong `app/services/rag_service.py`:
```python
# Thay đổi embedding model
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Thay đổi số lượng kết quả tìm kiếm
top_k = 3
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
docker build -t vexera-ai-system .

# Run container
docker run -p 8000:8000 -p 8501:8501 vexera-ai-system
```

### Production Setup
1. Sử dụng Gunicorn cho FastAPI
2. Nginx làm reverse proxy
3. Redis cho caching
4. PostgreSQL cho production database

## 🐛 Troubleshooting

### Lỗi thường gặp:

1. **"ModuleNotFoundError: No module named 'app'"**
   ```bash
   # Sử dụng script có sẵn (khuyến nghị)
   python run_backend.py
   
   # Hoặc chạy với module syntax
   python -m app.main
   
   # Hoặc đảm bảo đang ở thư mục gốc
   cd folder
   python -m app.main
   ```

2. **"No matching distribution found for sqlite3"**
   ```bash
   # sqlite3 đã được xóa khỏi requirements.txt
   # Chỉ cần chạy lại:
   pip install -r requirements.txt
   ```

3. **"Port already in use"**
   ```bash
   # Thay đổi port
   uvicorn app.main:app --port 8001
   ```

4. **"FAQ data not loaded"**
   - Kiểm tra file `faq_data.csv` có tồn tại trong thư mục gốc
   - Kiểm tra quyền đọc file

5. **"Embeddings not found"**
   - Hệ thống sẽ tự tạo embeddings lần đầu
   - Đợi quá trình tạo embeddings hoàn tất (có thể mất 1-2 phút)

## 📈 Performance

- **Response Time**: < 2 giây cho FAQ
- **Accuracy**: > 85% cho câu hỏi phù hợp
- **Throughput**: 100+ requests/phút
- **Memory Usage**: ~500MB RAM

## 🔮 Roadmap

- [ ] Tích hợp OpenAI GPT-4
- [ ] Hỗ trợ đa ngôn ngữ
- [ ] Voice processing
- [ ] Image processing
- [ ] Mobile app
- [ ] Analytics dashboard

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra logs trong console
2. Chạy tests để xác định lỗi
3. Tạo issue trên repository

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

---

**Lưu ý**: Đây là phiên bản POC (Proof of Concept) cho mục đích demo. Không sử dụng trong production mà không có testing và security review đầy đủ.
