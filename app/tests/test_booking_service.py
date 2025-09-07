import pytest
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.booking_service import BookingService
from app.models.schemas import BookingChangeRequest, BookingChangeResponse

class TestBookingService:
    """Test cases for Booking Service"""
    
    @pytest.fixture
    def booking_service(self):
        """Create booking service instance for testing"""
        return BookingService()
    
    def test_validate_booking_id_valid(self, booking_service):
        """Test valid booking ID validation"""
        valid_ids = ["VX001234", "VX999999", "VX000001"]
        
        for booking_id in valid_ids:
            assert booking_service.validate_booking_id(booking_id) is True
    
    def test_validate_booking_id_invalid(self, booking_service):
        """Test invalid booking ID validation"""
        invalid_ids = ["VX123", "VX1234567", "ABC12345", "12345678", ""]
        
        for booking_id in invalid_ids:
            assert booking_service.validate_booking_id(booking_id) is False
    
    def test_validate_time_format_valid(self, booking_service):
        """Test valid time format validation"""
        valid_times = [
            "2024-01-15 08:30",
            "2024-12-31 23:59",
            "2024-06-01 00:00"
        ]
        
        for time_str in valid_times:
            assert booking_service.validate_time_format(time_str) is True
    
    def test_validate_time_format_invalid(self, booking_service):
        """Test invalid time format validation"""
        invalid_times = [
            "2024-01-15",
            "08:30",
            "2024/01/15 08:30",
            "15-01-2024 08:30",
            "2024-01-15 8:30",
            "invalid"
        ]
        
        for time_str in invalid_times:
            result = booking_service.validate_time_format(time_str)
            assert result is False, f"Expected False for '{time_str}', got {result}"
    
    def test_check_time_availability_valid(self, booking_service):
        """Test valid time availability"""
        # Future time (more than 2 hours from now, within business hours 5-23h)
        future_time = (datetime.now() + timedelta(days=1)).replace(hour=10, minute=0).strftime("%Y-%m-%d %H:%M")
        
        assert booking_service.check_time_availability(future_time) is True
    
    def test_check_time_availability_too_close(self, booking_service):
        """Test time availability - too close to current time"""
        # Time too close (less than 2 hours from now)
        close_time = (datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
        
        assert booking_service.check_time_availability(close_time) is False
    
    def test_check_time_availability_past_time(self, booking_service):
        """Test time availability - past time"""
        # Past time
        past_time = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
        
        assert booking_service.check_time_availability(past_time) is False
    
    def test_check_time_availability_outside_hours(self, booking_service):
        """Test time availability - outside business hours"""
        # Very early morning (before 5 AM)
        early_time = (datetime.now() + timedelta(days=1)).replace(hour=3, minute=0).strftime("%Y-%m-%d %H:%M")
        
        assert booking_service.check_time_availability(early_time) is False
        
        # Very late night (after 11 PM)
        late_time = (datetime.now() + timedelta(days=1)).replace(hour=23, minute=30).strftime("%Y-%m-%d %H:%M")
        
        assert booking_service.check_time_availability(late_time) is False
    
    def test_calculate_change_fee_within_24h(self, booking_service):
        """Test change fee calculation - within 24 hours"""
        booking_id = "VX001234"
        new_time = "2024-01-15 10:30"  # Same day, different time
        
        fee = booking_service.calculate_change_fee(booking_id, new_time)
        
        assert fee == 50000  # 50k VND for changes within 24h
    
    def test_calculate_change_fee_beyond_24h(self, booking_service):
        """Test change fee calculation - beyond 24 hours"""
        booking_id = "VX001234"
        new_time = "2024-01-20 10:30"  # Different day
        
        fee = booking_service.calculate_change_fee(booking_id, new_time)
        
        assert fee == 100000  # 100k VND for changes beyond 24h
    
    def test_calculate_change_fee_nonexistent_booking(self, booking_service):
        """Test change fee calculation - nonexistent booking"""
        booking_id = "VX999999"
        new_time = "2024-01-15 10:30"
        
        fee = booking_service.calculate_change_fee(booking_id, new_time)
        
        assert fee == 0.0
    
    def test_change_booking_time_success(self, booking_service):
        """Test successful booking time change"""
        # Use future time that's definitely available (within business hours 5-23h)
        future_time = (datetime.now() + timedelta(days=1)).replace(hour=10, minute=0).strftime("%Y-%m-%d %H:%M")
        
        request = BookingChangeRequest(
            booking_id="VX001234",
            new_departure_time=future_time,
            reason="Personal emergency",
            user_id="user001"
        )
        
        response = booking_service.change_booking_time(request)
        
        assert isinstance(response, BookingChangeResponse)
        assert response.success is True
        assert "thành công" in response.message
        assert response.new_booking_details is not None
        assert response.new_booking_details["booking_id"] == "VX001234"
        assert response.new_booking_details["new_departure_time"] == future_time
    
    def test_change_booking_time_invalid_booking_id(self, booking_service):
        """Test booking time change with invalid booking ID"""
        request = BookingChangeRequest(
            booking_id="INVALID",
            new_departure_time="2024-01-20 10:30",
            reason="Test reason",
            user_id="user001"
        )
        
        response = booking_service.change_booking_time(request)
        
        assert response.success is False
        assert "không hợp lệ" in response.message
    
    def test_change_booking_time_nonexistent_booking(self, booking_service):
        """Test booking time change with nonexistent booking"""
        request = BookingChangeRequest(
            booking_id="VX999999",
            new_departure_time="2024-01-20 10:30",
            reason="Test reason",
            user_id="user001"
        )
        
        response = booking_service.change_booking_time(request)
        
        assert response.success is False
        assert "không tìm thấy" in response.message.lower()
    
    def test_change_booking_time_unauthorized_user(self, booking_service):
        """Test booking time change with unauthorized user"""
        request = BookingChangeRequest(
            booking_id="VX001234",
            new_departure_time="2024-01-20 10:30",
            reason="Test reason",
            user_id="unauthorized_user"
        )
        
        response = booking_service.change_booking_time(request)
        
        assert response.success is False
        assert "không có quyền" in response.message
    
    def test_change_booking_time_invalid_time_format(self, booking_service):
        """Test booking time change with invalid time format"""
        request = BookingChangeRequest(
            booking_id="VX001234",
            new_departure_time="invalid_time",
            reason="Test reason",
            user_id="user001"
        )
        
        response = booking_service.change_booking_time(request)
        
        assert response.success is False
        assert "định dạng thời gian" in response.message.lower()
    
    def test_change_booking_time_unavailable_time(self, booking_service):
        """Test booking time change with unavailable time"""
        # Time too close to current time
        close_time = (datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
        
        request = BookingChangeRequest(
            booking_id="VX001234",
            new_departure_time=close_time,
            reason="Test reason",
            user_id="user001"
        )
        
        response = booking_service.change_booking_time(request)
        
        assert response.success is False
        assert "không khả dụng" in response.message
    
    def test_get_booking_info_success(self, booking_service):
        """Test successful booking info retrieval"""
        booking_id = "VX001234"
        user_id = "user001"
        
        result = booking_service.get_booking_info(booking_id, user_id)
        
        assert "error" not in result
        assert result["booking_id"] == booking_id
        assert result["user_id"] == user_id
        assert "flight_number" in result
        assert "departure_time" in result
    
    def test_get_booking_info_invalid_booking_id(self, booking_service):
        """Test booking info retrieval with invalid booking ID"""
        booking_id = "INVALID"
        user_id = "user001"
        
        result = booking_service.get_booking_info(booking_id, user_id)
        
        assert "error" in result
        assert "không hợp lệ" in result["error"]
    
    def test_get_booking_info_nonexistent_booking(self, booking_service):
        """Test booking info retrieval with nonexistent booking"""
        booking_id = "VX999999"
        user_id = "user001"
        
        result = booking_service.get_booking_info(booking_id, user_id)
        
        assert "error" in result
        assert "không tìm thấy" in result["error"].lower()
    
    def test_get_booking_info_unauthorized_user(self, booking_service):
        """Test booking info retrieval with unauthorized user"""
        booking_id = "VX001234"
        user_id = "unauthorized_user"
        
        result = booking_service.get_booking_info(booking_id, user_id)
        
        assert "error" in result
        assert "không có quyền" in result["error"]
    
    def test_generate_confirmation_code(self, booking_service):
        """Test confirmation code generation"""
        code = booking_service.generate_confirmation_code()
        
        assert isinstance(code, str)
        assert len(code) == 6
        assert code.isalnum()
        assert code.isupper()
