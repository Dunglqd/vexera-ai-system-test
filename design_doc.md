# Design Document - Vexere AI Customer Service System

## 1. Tổng quan kiến trúc hệ thống

### 1.1 Mục tiêu
Xây dựng hệ thống AI Customer Service cho Vexere với khả năng:
- Trả lời câu hỏi FAQ tự động (RAG-FAQ)
- Xử lý yêu cầu After-Service (đổi giờ bay)
- Sẵn sàng mở rộng cho Image & Voice processing

### 1.2 Kiến trúc tổng thể
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   AI Services   │
│   (Web/Mobile)  │◄──►│   (FastAPI)     │◄──►│   (RAG/LLM)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (SQLite/CSV)  │
                       └─────────────────┘
```

## 2. Lựa chọn công nghệ và lý do

### 2.1 Backend Framework: FastAPI
**Lý do:**
- Hiệu suất cao, async support
- Tự động generate API documentation
- Type hints và validation tích hợp
- Dễ dàng tích hợp với AI services

### 2.2 AI/ML Stack
**RAG System:**
- **Embedding Model**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS (local, lightweight)
- **LLM**: OpenAI GPT-3.5-turbo hoặc local model (Ollama)

**Lý do:**
- sentence-transformers: nhẹ, hiệu quả cho tiếng Việt
- FAISS: nhanh, không cần server riêng
- GPT-3.5: chất lượng tốt, cost-effective

### 2.3 Database: SQLite + CSV
**Lý do:**
- Đơn giản, không cần setup server
- CSV cho FAQ data (dễ maintain)
- SQLite cho user sessions và logs

### 2.4 Frontend: Streamlit
**Lý do:**
- Rapid prototyping
- Tích hợp tốt với Python backend
- UI đơn giản nhưng đầy đủ chức năng

## 3. Sơ đồ hệ thống chi tiết

### 3.1 RAG-FAQ Flow
```
User Question → Text Preprocessing → Embedding → Vector Search → 
Context Retrieval → LLM Generation → Response
```

### 3.2 After-Service Flow
```
User Request → Intent Classification → Data Validation → 
Business Logic → Confirmation → Database Update
```

### 3.3 Image & Voice Architecture (Future)
```
Image: Upload → OCR/Image Analysis → Text Extraction → RAG Processing
Voice: Audio → Speech-to-Text → Text Processing → RAG Processing
```

## 4. Cấu trúc dự án
```
vexera-ai-system/
├── app/
│   ├── main.py                 # FastAPI app
│   ├── models/                 # Data models
│   ├── services/               # Business logic
│   │   ├── rag_service.py      # RAG implementation
│   │   ├── faq_service.py      # FAQ handling
│   │   └── booking_service.py  # After-service logic
│   ├── utils/                  # Utilities
│   └── tests/                  # Test files
├── data/
│   ├── faq_data.csv           # FAQ database
│   └── embeddings/            # Vector embeddings
├── frontend/
│   └── streamlit_app.py       # UI interface
├── requirements.txt
├── README.md
└── CODE_REVIEW.md
```

## 5. Pipeline Testing & CI/CD

### 5.1 Testing Strategy
- **Unit Tests**: pytest cho business logic
- **Integration Tests**: API endpoints testing
- **RAG Tests**: Accuracy testing với sample questions
- **Performance Tests**: Response time benchmarks

### 5.2 CI/CD Pipeline
```yaml
# GitHub Actions
- Code Quality: flake8, black
- Testing: pytest với coverage
- Security: bandit
- Deployment: Docker container
```

## 6. Continuous Improvement

### 6.1 Monitoring
- Response accuracy tracking
- User satisfaction metrics
- Performance monitoring
- Error logging và analysis

### 6.2 Model Updates
- Regular retraining với new FAQ data
- A/B testing cho different models
- Feedback loop từ user interactions

## 7. Security & Privacy
- Input validation và sanitization
- Rate limiting cho API calls
- Data encryption cho sensitive info
- GDPR compliance cho user data

## 8. Scalability Considerations
- Horizontal scaling với load balancer
- Caching cho frequent queries
- Database optimization
- CDN cho static assets

## 9. Deployment Architecture
```
Production:
- Docker containers
- Nginx reverse proxy
- SSL/TLS encryption
- Environment variables cho config
```

## 10. Future Enhancements
- Multi-language support
- Advanced NLP features
- Integration với existing Vexere systems
- Mobile app integration
- Real-time chat capabilities
