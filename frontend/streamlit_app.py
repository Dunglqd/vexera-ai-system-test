import streamlit as st
import requests
import json
from datetime import datetime
import time

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Vexere AI Customer Service",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .bot-message {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    .confidence-bar {
        height: 20px;
        background-color: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
    }
    .confidence-fill {
        height: 100%;
        background-color: #4caf50;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def ask_faq(question, user_id=None):
    """Send FAQ question to API"""
    try:
        payload = {
            "question": question,
            "user_id": user_id
        }
        response = requests.post(
            f"{API_BASE_URL}/api/faq/ask",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection Error: {str(e)}"}

def change_booking_time(booking_id, new_time, reason, user_id):
    """Send booking change request to API"""
    try:
        payload = {
            "booking_id": booking_id,
            "new_departure_time": new_time,
            "reason": reason,
            "user_id": user_id
        }
        response = requests.post(
            f"{API_BASE_URL}/api/booking/change-time",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection Error: {str(e)}"}

def get_booking_info(booking_id, user_id):
    """Get booking information"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/booking/{booking_id}",
            params={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection Error: {str(e)}"}

def main():
    # Header
    st.markdown('<h1 class="main-header">✈️ Vexere AI Customer Service</h1>', unsafe_allow_html=True)
    
    # Check API health
    if not check_api_health():
        st.error("⚠️ Không thể kết nối đến API. Vui lòng đảm bảo server đang chạy.")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Cài đặt")
        
        # User ID input
        user_id = st.text_input("User ID", value="user001", help="Nhập ID người dùng")
        
        # Service selection
        service = st.selectbox(
            "Chọn dịch vụ",
            ["FAQ - Hỏi đáp", "After-Service - Đổi giờ bay", "Thông tin đặt chỗ"]
        )
        
        st.markdown("---")
        st.markdown("### 📊 Thống kê")
        st.info("Hệ thống đang hoạt động bình thường")
    
    # Main content based on service selection
    if service == "FAQ - Hỏi đáp":
        st.header("🤖 FAQ - Hỏi đáp tự động")
        
        # Chat interface
        if "faq_messages" not in st.session_state:
            st.session_state.faq_messages = []
        
        # Display chat messages
        for message in st.session_state.faq_messages:
            if message["type"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>Bạn:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                confidence = message.get("confidence", 0)
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>AI Assistant:</strong> {message["content"]}
                    <br><br>
                    <small>Độ tin cậy: {confidence:.1f}%</small>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {confidence}%"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Input form
        with st.form("faq_form"):
            question = st.text_area("Nhập câu hỏi của bạn:", height=100)
            submit_button = st.form_submit_button("Gửi câu hỏi")
            
            if submit_button and question:
                # Add user message
                st.session_state.faq_messages.append({
                    "type": "user",
                    "content": question,
                    "timestamp": datetime.now()
                })
                
                # Get AI response
                with st.spinner("Đang xử lý câu hỏi..."):
                    response = ask_faq(question, user_id)
                
                if "error" not in response:
                    # Add bot response
                    st.session_state.faq_messages.append({
                        "type": "bot",
                        "content": response["answer"],
                        "confidence": response["confidence"],
                        "processing_time": response["processing_time"],
                        "timestamp": datetime.now()
                    })
                else:
                    st.error(f"Lỗi: {response['error']}")
                
                st.rerun()
        
        # Sample questions
        st.markdown("### 💡 Câu hỏi mẫu")
        sample_questions = [
            "Làm thế nào để đặt vé máy bay trên Vexere?",
            "Tôi có thể đặt tối đa bao nhiêu vé máy bay?",
            "Cách check-in online như thế nào?",
            "Quy định mang chất lỏng lên máy bay",
            "Thời gian hoàn tiền trong bao lâu?"
        ]
        
        for i, sample_q in enumerate(sample_questions):
            if st.button(f"Q{i+1}: {sample_q[:50]}...", key=f"sample_{i}"):
                st.session_state.faq_messages.append({
                    "type": "user",
                    "content": sample_q,
                    "timestamp": datetime.now()
                })
                
                with st.spinner("Đang xử lý..."):
                    response = ask_faq(sample_q, user_id)
                
                if "error" not in response:
                    st.session_state.faq_messages.append({
                        "type": "bot",
                        "content": response["answer"],
                        "confidence": response["confidence"],
                        "processing_time": response["processing_time"],
                        "timestamp": datetime.now()
                    })
                else:
                    st.error(f"Lỗi: {response['error']}")
                
                st.rerun()
    
    elif service == "After-Service - Đổi giờ bay":
        st.header("✈️ After-Service - Đổi giờ bay")
        
        with st.form("booking_change_form"):
            st.subheader("Thông tin đặt chỗ")
            
            col1, col2 = st.columns(2)
            with col1:
                booking_id = st.text_input("Mã đặt chỗ", value="VX001234", help="Nhập mã đặt chỗ 8 ký tự")
            with col2:
                new_time = st.text_input("Thời gian mới", value="2024-01-15 10:30", help="Định dạng: YYYY-MM-DD HH:MM")
            
            reason = st.text_area("Lý do thay đổi", placeholder="Vui lòng nêu lý do thay đổi giờ bay...")
            
            submit_button = st.form_submit_button("Gửi yêu cầu thay đổi")
            
            if submit_button:
                if not booking_id or not new_time or not reason:
                    st.error("Vui lòng điền đầy đủ thông tin")
                else:
                    with st.spinner("Đang xử lý yêu cầu..."):
                        response = change_booking_time(booking_id, new_time, reason, user_id)
                    
                    if "error" not in response:
                        if response["success"]:
                            st.success(f"✅ {response['message']}")
                            if response.get("new_booking_details"):
                                st.json(response["new_booking_details"])
                        else:
                            st.error(f"❌ {response['message']}")
                    else:
                        st.error(f"Lỗi: {response['error']}")
        
        # Sample booking IDs
        st.markdown("### 📋 Mã đặt chỗ mẫu")
        st.info("VX001234, VX001235")
    
    elif service == "Thông tin đặt chỗ":
        st.header("📋 Thông tin đặt chỗ")
        
        with st.form("booking_info_form"):
            booking_id = st.text_input("Mã đặt chỗ", value="VX001234")
            submit_button = st.form_submit_button("Tra cứu thông tin")
            
            if submit_button and booking_id:
                with st.spinner("Đang tra cứu..."):
                    response = get_booking_info(booking_id, user_id)
                
                if "error" not in response:
                    st.success("✅ Tìm thấy thông tin đặt chỗ")
                    st.json(response)
                else:
                    st.error(f"❌ {response['error']}")

if __name__ == "__main__":
    main()
