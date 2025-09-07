import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.rag_service import RAGService

class TestRAGService:
    """Test cases for RAG Service"""
    
    @pytest.fixture
    def sample_faq_data(self):
        """Create sample FAQ data for testing"""
        return pd.DataFrame({
            'question': [
                'Làm thế nào để đặt vé máy bay?',
                'Cách check-in online như thế nào?',
                'Thời gian hoàn tiền trong bao lâu?'
            ],
            'answer': [
                'Bạn có thể đặt vé qua website hoặc app Vexere...',
                'Check-in online từ 24h trước giờ bay...',
                'Thời gian hoàn tiền từ 1-14 ngày...'
            ]
        })
    
    @pytest.fixture
    def rag_service(self):
        """Create RAG service instance for testing"""
        return RAGService()
    
    def test_load_faq_data_success(self, rag_service, sample_faq_data, tmp_path):
        """Test successful FAQ data loading"""
        # Create temporary CSV file
        csv_file = tmp_path / "test_faq.csv"
        sample_faq_data.to_csv(csv_file, index=False)
        
        # Test loading
        result = rag_service.load_faq_data(str(csv_file))
        
        assert result is True
        assert rag_service.faq_data is not None
        assert len(rag_service.faq_data) == 3
        assert 'question' in rag_service.faq_data.columns
        assert 'answer' in rag_service.faq_data.columns
    
    def test_load_faq_data_file_not_found(self, rag_service):
        """Test FAQ data loading with non-existent file"""
        result = rag_service.load_faq_data("non_existent_file.csv")
        
        assert result is False
        assert rag_service.faq_data is None
    
    @patch('app.services.rag_service.SentenceTransformer')
    def test_create_embeddings_success(self, mock_transformer, rag_service, sample_faq_data, tmp_path):
        """Test successful embeddings creation"""
        # Mock the transformer
        mock_model = Mock()
        mock_embeddings = np.random.rand(3, 384)  # Mock embeddings
        mock_model.encode.return_value = mock_embeddings
        mock_transformer.return_value = mock_model
        
        # Setup service
        rag_service.faq_data = sample_faq_data
        rag_service.model = mock_model
        
        # Create embeddings directory
        embeddings_dir = tmp_path / "embeddings"
        embeddings_dir.mkdir()
        rag_service.embeddings_path = str(embeddings_dir / "test_embeddings.pkl")
        rag_service.index_path = str(embeddings_dir / "test_index.faiss")
        
        # Test creation
        result = rag_service.create_embeddings()
        
        assert result is True
        assert rag_service.embeddings is not None
        assert rag_service.index is not None
        assert os.path.exists(rag_service.embeddings_path)
        assert os.path.exists(rag_service.index_path)
    
    def test_create_embeddings_no_data(self, rag_service):
        """Test embeddings creation without FAQ data"""
        result = rag_service.create_embeddings()
        
        assert result is False
    
    @patch('app.services.rag_service.SentenceTransformer')
    def test_search_similar_questions(self, mock_transformer, rag_service, sample_faq_data):
        """Test similar questions search"""
        # Mock the transformer
        mock_model = Mock()
        mock_embeddings = np.random.rand(3, 384)
        mock_query_embedding = np.random.rand(1, 384)
        mock_model.encode.return_value = mock_query_embedding
        mock_transformer.return_value = mock_model
        
        # Setup service with mock index
        rag_service.faq_data = sample_faq_data
        rag_service.model = mock_model
        rag_service.embeddings = mock_embeddings
        
        # Mock FAISS index
        mock_index = Mock()
        mock_index.search.return_value = (np.array([[0.9, 0.8]]), np.array([[0, 1]]))
        rag_service.index = mock_index
        
        # Test search
        results = rag_service.search_similar_questions("Làm sao để đặt vé?", top_k=2)
        
        assert len(results) == 2
        assert all(isinstance(result, tuple) for result in results)
        assert all(len(result) == 2 for result in results)
    
    def test_search_similar_questions_no_index(self, rag_service):
        """Test search without index"""
        results = rag_service.search_similar_questions("Test question")
        
        assert results == []
    
    @patch('app.services.rag_service.SentenceTransformer')
    def test_get_answer_high_confidence(self, mock_transformer, rag_service, sample_faq_data):
        """Test getting answer with high confidence"""
        # Mock the transformer
        mock_model = Mock()
        mock_model.encode.return_value = np.random.rand(1, 384)
        mock_transformer.return_value = mock_model
        
        # Setup service
        rag_service.faq_data = sample_faq_data
        rag_service.model = mock_model
        
        # Mock search results with high confidence
        mock_index = Mock()
        mock_index.search.return_value = (np.array([[0.9]]), np.array([[0]]))
        rag_service.index = mock_index
        
        # Test get answer
        answer, confidence, source_question = rag_service.get_answer("Làm sao để đặt vé?")
        
        assert isinstance(answer, str)
        assert len(answer) > 0
        assert 0 <= confidence <= 100
        assert isinstance(source_question, str)
    
    @patch('app.services.rag_service.SentenceTransformer')
    def test_get_answer_low_confidence(self, mock_transformer, rag_service, sample_faq_data):
        """Test getting answer with low confidence"""
        # Mock the transformer
        mock_model = Mock()
        mock_model.encode.return_value = np.random.rand(1, 384)
        mock_transformer.return_value = mock_model
        
        # Setup service
        rag_service.faq_data = sample_faq_data
        rag_service.model = mock_model
        
        # Mock search results with low confidence
        mock_index = Mock()
        mock_index.search.return_value = (np.array([[0.2]]), np.array([[0]]))
        rag_service.index = mock_index
        
        # Test get answer
        answer, confidence, source_question = rag_service.get_answer("Random question")
        
        assert "Xin lỗi" in answer
        assert confidence < 30
    
    def test_get_answer_no_results(self, rag_service):
        """Test getting answer with no search results"""
        # Mock empty search results
        mock_index = Mock()
        mock_index.search.return_value = (np.array([[]]), np.array([[]]))
        rag_service.index = mock_index
        
        # Test get answer
        answer, confidence, source_question = rag_service.get_answer("Test question")
        
        assert "Xin lỗi" in answer
        assert confidence == 0.0
        assert source_question == ""
    
    def test_initialize_success(self, rag_service, sample_faq_data, tmp_path):
        """Test successful service initialization"""
        # Create temporary CSV file
        csv_file = tmp_path / "test_faq.csv"
        sample_faq_data.to_csv(csv_file, index=False)
        
        with patch.object(rag_service, 'load_embeddings', return_value=False), \
             patch.object(rag_service, 'create_embeddings', return_value=True), \
             patch.object(rag_service, 'load_faq_data', return_value=True):
            
            result = rag_service.initialize()
            
            assert result is True
    
    def test_initialize_load_data_failure(self, rag_service):
        """Test initialization with data loading failure"""
        with patch.object(rag_service, 'load_faq_data', return_value=False):
            result = rag_service.initialize()
            
            assert result is False
