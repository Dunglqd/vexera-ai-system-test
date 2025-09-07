from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import FAQRequest, FAQResponse, BookingChangeRequest, BookingChangeResponse
from app.services.faq_service import FAQService
from app.services.booking_service import BookingService
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Vexere AI Customer Service API",
    description="API for Vexere AI Customer Service System with RAG-FAQ and After-Service capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
faq_service = FAQService()
booking_service = BookingService()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("Initializing Vexere AI Customer Service...")
    faq_service.initialize()
    print("Services initialized successfully!")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Vexere AI Customer Service API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "faq_service": "initialized" if faq_service.initialized else "not_initialized",
        "booking_service": "ready"
    }

# FAQ Endpoints
@app.post("/api/faq/ask", response_model=FAQResponse)
async def ask_faq(request: FAQRequest):
    """
    Ask a question to the FAQ system
    """
    try:
        response = faq_service.get_faq_answer(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/faq/list")
async def list_faqs():
    """
    Get list of all FAQ questions
    """
    try:
        faqs = faq_service.get_all_faqs()
        return {"faqs": faqs, "count": len(faqs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/faq/search")
async def search_faqs(keyword: str):
    """
    Search FAQs by keyword
    """
    try:
        results = faq_service.search_faqs(keyword)
        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# After-Service Endpoints
@app.post("/api/booking/change-time", response_model=BookingChangeResponse)
async def change_booking_time(request: BookingChangeRequest):
    """
    Change booking departure time
    """
    try:
        response = booking_service.change_booking_time(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/booking/{booking_id}")
async def get_booking_info(booking_id: str, user_id: str):
    """
    Get booking information
    """
    try:
        booking_info = booking_service.get_booking_info(booking_id, user_id)
        if "error" in booking_info:
            raise HTTPException(status_code=400, detail=booking_info["error"])
        return booking_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Image & Voice Processing Endpoints (Architecture Ready)
@app.post("/api/chat/image")
async def process_image_message():
    """
    Process image message (Architecture ready - not implemented)
    """
    return {
        "message": "Image processing endpoint ready for implementation",
        "status": "architecture_ready",
        "note": "This endpoint is designed to handle image uploads, OCR processing, and RAG integration"
    }

@app.post("/api/chat/voice")
async def process_voice_message():
    """
    Process voice message (Architecture ready - not implemented)
    """
    return {
        "message": "Voice processing endpoint ready for implementation", 
        "status": "architecture_ready",
        "note": "This endpoint is designed to handle voice uploads, speech-to-text, and RAG integration"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
