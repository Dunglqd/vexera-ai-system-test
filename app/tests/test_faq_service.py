import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.faq_service import FAQService
from app.models.schemas import FAQRequest, FAQResponse

class TestFAQService:
    """Test cases for FAQ Service"""
    
    @pytest.fixture
    def faq_service(self):
        """Create FAQ service instance for testing"""
        return FAQService()
    
    def test_initialize_success(self, faq_service):
        """Test successful service initialization"""
        with patch.object(faq_service.rag_service, 'initialize', return_value=True):
            result = faq_service.initialize()
            
            assert result is True
            assert faq_service.initialized is True
    
    def test_initialize_failure(self, faq_service):
        """Test initialization failure"""
        with patch.object(faq_service.rag_service, 'initialize', return_value=False):
            result = faq_service.initialize()
            
            assert result is False
            assert faq_service.initialized is False
    
    def test_get_faq_answer_not_initialized(self, faq_service):
        """Test getting FAQ answer when service not initialized"""
        request = FAQRequest(question="Test question")
        
        response = faq_service.get_faq_answer(request)
        
        assert isinstance(response, FAQResponse)
        assert "khởi tạo" in response.answer
        assert response.confidence == 0.0
        assert response.processing_time == 0.0
    
    def test_get_faq_answer_success(self, faq_service):
        """Test successful FAQ answer retrieval"""
        # Mock initialized service
        faq_service.initialized = True
        
        # Mock RAG service response
        mock_answer = "Đây là câu trả lời mẫu"
        mock_confidence = 85.5
        mock_source = "Câu hỏi gốc"
        
        with patch.object(faq_service.rag_service, 'get_answer', 
                         return_value=(mock_answer, mock_confidence, mock_source)):
            
            request = FAQRequest(question="Test question")
            response = faq_service.get_faq_answer(request)
            
            assert isinstance(response, FAQResponse)
            assert response.answer == mock_answer
            assert response.confidence == mock_confidence
            assert response.source_question == mock_source
            assert response.processing_time >= 0
    
    def test_get_faq_answer_exception(self, faq_service):
        """Test FAQ answer retrieval with exception"""
        # Mock initialized service
        faq_service.initialized = True
        
        # Mock RAG service to raise exception
        with patch.object(faq_service.rag_service, 'get_answer', 
                         side_effect=Exception("Test error")):
            
            request = FAQRequest(question="Test question")
            response = faq_service.get_faq_answer(request)
            
            assert isinstance(response, FAQResponse)
            assert "lỗi" in response.answer.lower()
            assert response.confidence == 0.0
            assert response.processing_time >= 0
    
    def test_get_all_faqs_not_initialized(self, faq_service):
        """Test getting all FAQs when service not initialized"""
        faqs = faq_service.get_all_faqs()
        
        assert faqs == []
    
    def test_get_all_faqs_success(self, faq_service):
        """Test successful retrieval of all FAQs"""
        # Mock initialized service with FAQ data
        faq_service.initialized = True
        import pandas as pd
        mock_faq_data = pd.DataFrame({
            'question': ["Question 1", "Question 2", "Question 3"],
            'answer': ["Answer 1", "Answer 2", "Answer 3"]
        })
        faq_service.rag_service.faq_data = mock_faq_data
        
        faqs = faq_service.get_all_faqs()
        
        assert len(faqs) == 3
        assert "Question 1" in faqs
        assert "Question 2" in faqs
        assert "Question 3" in faqs
    
    def test_search_faqs_not_initialized(self, faq_service):
        """Test searching FAQs when service not initialized"""
        results = faq_service.search_faqs("test")
        
        assert results == []
    
    def test_search_faqs_success(self, faq_service):
        """Test successful FAQ search"""
        # Mock initialized service with FAQ data
        faq_service.initialized = True
        
        # Create mock DataFrame
        import pandas as pd
        mock_data = pd.DataFrame({
            'question': ['How to book?', 'How to check-in?', 'How to cancel?'],
            'answer': ['Answer 1', 'Answer 2', 'Answer 3']
        })
        
        # Mock the search functionality
        faq_service.rag_service.faq_data = mock_data
        
        # Mock the contains method on the Series
        with patch.object(mock_data['question'], 'str') as mock_str:
            mock_str.contains.return_value = pd.Series([True, False, False])
            results = faq_service.search_faqs("book")
            
            assert len(results) == 1
            assert results[0]['question'] == 'How to book?'
    
    def test_search_faqs_no_matches(self, faq_service):
        """Test FAQ search with no matches"""
        # Mock initialized service with FAQ data
        faq_service.initialized = True
        
        import pandas as pd
        mock_data = pd.DataFrame({
            'question': ['How to book?', 'How to check-in?'],
            'answer': ['Answer 1', 'Answer 2']
        })
        
        # Mock no matches
        faq_service.rag_service.faq_data = mock_data
        
        with patch.object(mock_data['question'], 'str') as mock_str:
            mock_str.contains.return_value = pd.Series([False, False])
            results = faq_service.search_faqs("nonexistent")
            
            assert len(results) == 0
