from app.services.rag_service import RAGService
from app.models.schemas import FAQRequest, FAQResponse
import time

class FAQService:
    def __init__(self):
        self.rag_service = RAGService()
        self.initialized = False
    
    def initialize(self):
        """
        Initialize the FAQ service
        """
        if not self.initialized:
            self.initialized = self.rag_service.initialize()
        return self.initialized
    
    def get_faq_answer(self, request: FAQRequest) -> FAQResponse:
        """
        Get FAQ answer for a user question
        """
        if not self.initialized:
            return FAQResponse(
                answer="Hệ thống đang khởi tạo, vui lòng thử lại sau.",
                confidence=0.0,
                processing_time=0.0
            )
        
        start_time = time.time()
        
        try:
            # Get answer from RAG service
            answer, confidence, source_question = self.rag_service.get_answer(request.question)
            
            processing_time = time.time() - start_time
            
            return FAQResponse(
                answer=answer,
                confidence=confidence,
                source_question=source_question,
                processing_time=processing_time
            )
        
        except Exception as e:
            processing_time = time.time() - start_time
            return FAQResponse(
                answer=f"Xin lỗi, đã xảy ra lỗi khi xử lý câu hỏi: {str(e)}",
                confidence=0.0,
                processing_time=processing_time
            )
    
    def get_all_faqs(self) -> list:
        """
        Get all FAQ questions for display
        """
        if not self.initialized or self.rag_service.faq_data is None:
            return []
        
        return self.rag_service.faq_data['question'].tolist()
    
    def search_faqs(self, keyword: str) -> list:
        """
        Search FAQs by keyword
        """
        if not self.initialized or self.rag_service.faq_data is None:
            return []
        
        # Simple keyword search
        faq_data = self.rag_service.faq_data
        matching_faqs = faq_data[
            faq_data['question'].str.contains(keyword, case=False, na=False)
        ]
        
        return matching_faqs.to_dict('records')
