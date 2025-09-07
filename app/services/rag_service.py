import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os
from typing import List, Tuple
import time

class RAGService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize RAG service with sentence transformer model
        """
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.faq_data = None
        self.embeddings = None
        self.embeddings_path = "data/embeddings/faq_embeddings.pkl"
        self.index_path = "data/embeddings/faq_index.faiss"
        
    def load_faq_data(self, csv_path: str = "faq_data.csv"):
        """
        Load FAQ data from CSV file
        """
        try:
            self.faq_data = pd.read_csv(csv_path)
            print(f"Loaded {len(self.faq_data)} FAQ entries")
            return True
        except Exception as e:
            print(f"Error loading FAQ data: {e}")
            return False
    
    def create_embeddings(self):
        """
        Create embeddings for FAQ questions and save to disk
        """
        if self.faq_data is None:
            print("No FAQ data loaded")
            return False
            
        print("Creating embeddings...")
        questions = self.faq_data['question'].tolist()
        
        # Create embeddings
        self.embeddings = self.model.encode(questions, show_progress_bar=True)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        embeddings_f32 = self.embeddings.astype('float32')
        # Manual L2 normalization to avoid FAISS issues
        norms = np.linalg.norm(embeddings_f32, axis=1, keepdims=True)
        embeddings_f32 = embeddings_f32 / norms
        self.index.add(embeddings_f32)
        
        # Save embeddings and index
        os.makedirs("data/embeddings", exist_ok=True)
        with open(self.embeddings_path, 'wb') as f:
            pickle.dump(self.embeddings, f)
        faiss.write_index(self.index, self.index_path)
        
        print(f"Created and saved embeddings for {len(questions)} questions")
        return True
    
    def load_embeddings(self):
        """
        Load pre-computed embeddings and FAISS index
        """
        try:
            if os.path.exists(self.embeddings_path) and os.path.exists(self.index_path):
                with open(self.embeddings_path, 'rb') as f:
                    self.embeddings = pickle.load(f)
                self.index = faiss.read_index(self.index_path)
                print("Loaded pre-computed embeddings")
                return True
            else:
                print("No pre-computed embeddings found")
                return False
        except Exception as e:
            print(f"Error loading embeddings: {e}")
            return False
    
    def search_similar_questions(self, query: str, top_k: int = 3) -> List[Tuple[int, float]]:
        """
        Search for similar questions using vector similarity
        """
        if self.index is None:
            print("No index available")
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        query_embedding_f32 = query_embedding.astype('float32')
        # Manual L2 normalization to avoid FAISS issues
        query_norm = np.linalg.norm(query_embedding_f32, axis=1, keepdims=True)
        query_embedding_f32 = query_embedding_f32 / query_norm
        
        # Search
        scores, indices = self.index.search(query_embedding_f32, top_k)
        
        # Return results as list of (index, score) tuples
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx != -1:  # Valid index
                results.append((int(idx), float(score)))
        
        return results
    
    def get_answer(self, query: str, top_k: int = 3) -> Tuple[str, float, str]:
        """
        Get answer for a query using RAG approach
        """
        start_time = time.time()
        
        # Search for similar questions
        similar_questions = self.search_similar_questions(query, top_k)
        
        if not similar_questions:
            return "Xin lỗi, tôi không tìm thấy câu trả lời phù hợp cho câu hỏi của bạn.", 0.0, ""
        
        # Get the best match
        best_idx, best_score = similar_questions[0]
        best_question = self.faq_data.iloc[best_idx]['question']
        best_answer = self.faq_data.iloc[best_idx]['answer']
        
        # Calculate confidence based on similarity score
        confidence = min(best_score * 100, 100.0)  # Convert to percentage
        
        processing_time = time.time() - start_time
        
        # If confidence is too low, provide a generic response
        if confidence < 30:
            return "Xin lỗi, tôi không hiểu rõ câu hỏi của bạn. Bạn có thể hỏi lại một cách cụ thể hơn không?", confidence, best_question
        
        return best_answer, confidence, best_question
    
    def initialize(self):
        """
        Initialize the RAG service - load data and embeddings
        """
        # Load FAQ data
        if not self.load_faq_data():
            return False
        
        # Try to load existing embeddings, if not available, create new ones
        if not self.load_embeddings():
            print("Creating new embeddings...")
            if not self.create_embeddings():
                return False
        
        print("RAG service initialized successfully")
        return True
