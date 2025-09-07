from app.models.schemas import BookingChangeRequest, BookingChangeResponse
from datetime import datetime, timedelta
import re
import random
import string

class BookingService:
    def __init__(self):
        # Mock database for demonstration
        self.bookings = {}
        self.generate_sample_bookings()
    
    def generate_sample_bookings(self):
        """
        Generate some sample bookings for demonstration
        """
        sample_bookings = [
            {
                "booking_id": "VX001234",
                "user_id": "user001",
                "flight_number": "VJ123",
                "departure_time": "2024-01-15 08:30",
                "arrival_time": "2024-01-15 10:30",
                "route": "Hà Nội - TP.HCM",
                "passenger_name": "Nguyễn Văn A",
                "status": "confirmed"
            },
            {
                "booking_id": "VX001235",
                "user_id": "user002", 
                "flight_number": "VN456",
                "departure_time": "2024-01-16 14:00",
                "arrival_time": "2024-01-16 16:00",
                "route": "TP.HCM - Đà Nẵng",
                "passenger_name": "Trần Thị B",
                "status": "confirmed"
            }
        ]
        
        for booking in sample_bookings:
            self.bookings[booking["booking_id"]] = booking
    
    def validate_booking_id(self, booking_id: str) -> bool:
        """
        Validate booking ID format
        """
        # Simple validation - booking ID should be 8 characters
        return len(booking_id) == 8 and booking_id.startswith("VX")
    
    def validate_time_format(self, time_str: str) -> bool:
        """
        Validate time format (YYYY-MM-DD HH:MM) - strict format
        """
        try:
            # Check if format matches exactly YYYY-MM-DD HH:MM
            if not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$', time_str):
                return False
            datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False
    
    def check_time_availability(self, new_time: str) -> bool:
        """
        Check if new time is available (mock implementation)
        """
        try:
            new_datetime = datetime.strptime(new_time, "%Y-%m-%d %H:%M")
            current_time = datetime.now()
            
            # Check if new time is at least 2 hours in the future
            if new_datetime <= current_time + timedelta(hours=2):
                return False
            
            # Check if new time is within business hours (6 AM - 10 PM)
            # But allow some flexibility for testing
            hour = new_datetime.hour
            if hour < 5 or hour > 23:  # More flexible hours
                return False
            
            return True
        except:
            return False
    
    def calculate_change_fee(self, booking_id: str, new_time: str) -> float:
        """
        Calculate change fee (mock implementation)
        """
        # Simple fee calculation based on time difference
        try:
            booking = self.bookings.get(booking_id)
            if not booking:
                return 0.0
            
            original_time = datetime.strptime(booking["departure_time"], "%Y-%m-%d %H:%M")
            new_datetime = datetime.strptime(new_time, "%Y-%m-%d %H:%M")
            
            time_diff = abs((new_datetime - original_time).total_seconds() / 3600)  # hours
            
            # Fee structure: 50k VND for changes within 24h, 100k for others
            if time_diff <= 24:
                return 50000
            else:
                return 100000
        except:
            return 100000
    
    def change_booking_time(self, request: BookingChangeRequest) -> BookingChangeResponse:
        """
        Process booking time change request
        """
        try:
            # Validate booking ID
            if not self.validate_booking_id(request.booking_id):
                return BookingChangeResponse(
                    success=False,
                    message="Mã đặt chỗ không hợp lệ. Vui lòng kiểm tra lại."
                )
            
            # Check if booking exists
            if request.booking_id not in self.bookings:
                return BookingChangeResponse(
                    success=False,
                    message="Không tìm thấy thông tin đặt chỗ. Vui lòng kiểm tra lại mã đặt chỗ."
                )
            
            booking = self.bookings[request.booking_id]
            
            # Check user authorization
            if booking["user_id"] != request.user_id:
                return BookingChangeResponse(
                    success=False,
                    message="Bạn không có quyền thay đổi đặt chỗ này."
                )
            
            # Validate new time format
            if not self.validate_time_format(request.new_departure_time):
                return BookingChangeResponse(
                    success=False,
                    message="Định dạng thời gian không đúng. Vui lòng sử dụng định dạng YYYY-MM-DD HH:MM"
                )
            
            # Check time availability
            if not self.check_time_availability(request.new_departure_time):
                return BookingChangeResponse(
                    success=False,
                    message="Thời gian mới không khả dụng hoặc quá gần thời gian hiện tại. Vui lòng chọn thời gian khác."
                )
            
            # Calculate change fee
            change_fee = self.calculate_change_fee(request.booking_id, request.new_departure_time)
            
            # Update booking
            original_time = booking["departure_time"]
            booking["departure_time"] = request.new_departure_time
            booking["change_reason"] = request.reason
            booking["change_fee"] = change_fee
            booking["last_modified"] = datetime.now().isoformat()
            
            # Generate new booking details
            new_booking_details = {
                "booking_id": request.booking_id,
                "original_departure_time": original_time,
                "new_departure_time": request.new_departure_time,
                "change_fee": change_fee,
                "status": "modified",
                "confirmation_code": self.generate_confirmation_code()
            }
            
            return BookingChangeResponse(
                success=True,
                message=f"Đã thay đổi thời gian bay thành công. Phí thay đổi: {change_fee:,} VND",
                new_booking_details=new_booking_details
            )
        
        except Exception as e:
            return BookingChangeResponse(
                success=False,
                message=f"Đã xảy ra lỗi khi xử lý yêu cầu: {str(e)}"
            )
    
    def generate_confirmation_code(self) -> str:
        """
        Generate confirmation code for booking change
        """
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def get_booking_info(self, booking_id: str, user_id: str) -> dict:
        """
        Get booking information
        """
        if not self.validate_booking_id(booking_id):
            return {"error": "Mã đặt chỗ không hợp lệ"}
        
        booking = self.bookings.get(booking_id)
        if not booking:
            return {"error": "Không tìm thấy thông tin đặt chỗ"}
        
        if booking["user_id"] != user_id:
            return {"error": "Bạn không có quyền xem thông tin đặt chỗ này"}
        
        return booking
