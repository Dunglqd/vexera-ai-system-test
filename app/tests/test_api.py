import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

class TestAPI:
    """Test cases for FastAPI endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "faq_service" in data
        assert "booking_service" in data
    
    @patch('app.main.faq_service.get_faq_answer')
    def test_ask_faq_success(self, mock_get_faq_answer, client):
        """Test successful FAQ question"""
        # Mock FAQ service response
        mock_response = Mock()
        mock_response.answer = "Đây là câu trả lời mẫu"
        mock_response.confidence = 85.5
        mock_response.source_question = "Câu hỏi gốc"
        mock_response.processing_time = 0.5
        mock_get_faq_answer.return_value = mock_response
        
        # Test request
        request_data = {
            "question": "Làm thế nào để đặt vé?",
            "user_id": "user001"
        }
        
        response = client.post("/api/faq/ask", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Đây là câu trả lời mẫu"
        assert data["confidence"] == 85.5
        assert data["source_question"] == "Câu hỏi gốc"
        assert data["processing_time"] == 0.5
    
    @patch('app.main.faq_service.get_faq_answer')
    def test_ask_faq_exception(self, mock_get_faq_answer, client):
        """Test FAQ question with exception"""
        # Mock service to raise exception
        mock_get_faq_answer.side_effect = Exception("Test error")
        
        request_data = {
            "question": "Test question",
            "user_id": "user001"
        }
        
        response = client.post("/api/faq/ask", json=request_data)
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
    
    @patch('app.main.faq_service.get_all_faqs')
    def test_list_faqs_success(self, mock_get_all_faqs, client):
        """Test successful FAQ list retrieval"""
        # Mock FAQ service response
        mock_faqs = ["Question 1", "Question 2", "Question 3"]
        mock_get_all_faqs.return_value = mock_faqs
        
        response = client.get("/api/faq/list")
        
        assert response.status_code == 200
        data = response.json()
        assert "faqs" in data
        assert "count" in data
        assert data["count"] == 3
        assert data["faqs"] == mock_faqs
    
    @patch('app.main.faq_service.search_faqs')
    def test_search_faqs_success(self, mock_search_faqs, client):
        """Test successful FAQ search"""
        # Mock search results
        mock_results = [
            {"question": "How to book?", "answer": "Answer 1"},
            {"question": "Booking process", "answer": "Answer 2"}
        ]
        mock_search_faqs.return_value = mock_results
        
        response = client.get("/api/faq/search?keyword=book")
        
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "count" in data
        assert data["count"] == 2
        assert data["results"] == mock_results
    
    @patch('app.main.booking_service.change_booking_time')
    def test_change_booking_time_success(self, mock_change_booking_time, client):
        """Test successful booking time change"""
        # Mock booking service response
        mock_response = Mock()
        mock_response.success = True
        mock_response.message = "Thay đổi thành công"
        mock_response.new_booking_details = {
            "booking_id": "VX001234",
            "new_departure_time": "2024-01-20 10:30",
            "change_fee": 50000
        }
        mock_change_booking_time.return_value = mock_response
        
        # Test request
        request_data = {
            "booking_id": "VX001234",
            "new_departure_time": "2024-01-20 10:30",
            "reason": "Personal emergency",
            "user_id": "user001"
        }
        
        response = client.post("/api/booking/change-time", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "thành công" in data["message"]
        assert data["new_booking_details"] is not None
    
    @patch('app.main.booking_service.change_booking_time')
    def test_change_booking_time_failure(self, mock_change_booking_time, client):
        """Test booking time change failure"""
        # Mock booking service response
        mock_response = Mock()
        mock_response.success = False
        mock_response.message = "Mã đặt chỗ không hợp lệ"
        mock_response.new_booking_details = None
        mock_change_booking_time.return_value = mock_response
        
        request_data = {
            "booking_id": "INVALID",
            "new_departure_time": "2024-01-20 10:30",
            "reason": "Test reason",
            "user_id": "user001"
        }
        
        response = client.post("/api/booking/change-time", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "không hợp lệ" in data["message"]
    
    @patch('app.main.booking_service.get_booking_info')
    def test_get_booking_info_success(self, mock_get_booking_info, client):
        """Test successful booking info retrieval"""
        # Mock booking service response
        mock_booking_info = {
            "booking_id": "VX001234",
            "user_id": "user001",
            "flight_number": "VJ123",
            "departure_time": "2024-01-15 08:30",
            "status": "confirmed"
        }
        mock_get_booking_info.return_value = mock_booking_info
        
        response = client.get("/api/booking/VX001234?user_id=user001")
        
        assert response.status_code == 200
        data = response.json()
        assert data["booking_id"] == "VX001234"
        assert data["user_id"] == "user001"
        assert data["flight_number"] == "VJ123"
    
    @patch('app.main.booking_service.get_booking_info')
    def test_get_booking_info_error(self, mock_get_booking_info, client):
        """Test booking info retrieval with error"""
        # Mock booking service to return error
        mock_get_booking_info.return_value = {"error": "Không tìm thấy thông tin đặt chỗ"}
        
        response = client.get("/api/booking/VX999999?user_id=user001")
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "không tìm thấy" in data["detail"].lower()
    
    def test_process_image_message(self, client):
        """Test image processing endpoint (architecture ready)"""
        response = client.post("/api/chat/image")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data
        assert data["status"] == "architecture_ready"
        assert "Image processing" in data["message"]
    
    def test_process_voice_message(self, client):
        """Test voice processing endpoint (architecture ready)"""
        response = client.post("/api/chat/voice")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data
        assert data["status"] == "architecture_ready"
        assert "Voice processing" in data["message"]
    
    def test_ask_faq_invalid_request(self, client):
        """Test FAQ endpoint with invalid request"""
        # Missing required field
        request_data = {
            "user_id": "user001"
            # Missing "question" field
        }
        
        response = client.post("/api/faq/ask", json=request_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_change_booking_time_invalid_request(self, client):
        """Test booking change endpoint with invalid request"""
        # Missing required fields
        request_data = {
            "booking_id": "VX001234"
            # Missing other required fields
        }
        
        response = client.post("/api/booking/change-time", json=request_data)
        
        assert response.status_code == 422  # Validation error
