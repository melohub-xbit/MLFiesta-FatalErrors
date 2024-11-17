from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
from groq import Groq
import dotenv
import pickle

dotenv.load_dotenv()

class EnhancedQASystem:
    def __init__(self, embeddings_directory):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.load_saved_embeddings(embeddings_directory)
        
    def load_saved_embeddings(self, directory):
        # Load pre-computed embeddings
        embeddings_path = os.path.join(directory, 'embeddings.npy')
        chunks_path = os.path.join(directory, 'text_chunks.pkl')
        
        self.embeddings = np.load(embeddings_path)
        with open(chunks_path, 'rb') as f:
            self.text_chunks = pickle.load(f)
    
    def generate_response(self, question, max_context_chunks=5):
        question_embedding = self.model.encode(question)
        
        # Calculate similarities for all chunks
        similarities = cosine_similarity(
            [question_embedding],
            self.embeddings
        )[0]
        
        # Sort all indices by similarity
        sorted_indices = np.argsort(similarities)[::-1]
        
        # Take top chunks with highest similarity
        top_chunks = [self.text_chunks[i] for i in sorted_indices[:max_context_chunks]]
        top_similarities = similarities[sorted_indices[:max_context_chunks]]
        
        # Check if we have any relevant context
        has_relevant_context = any(sim > 0.4 for sim in top_similarities)
        
        if has_relevant_context:
            context = "\n".join(top_chunks)
            prompt = f"""Based on the following context, please provide a clear and concise answer to the question.
            
    Question: {question}

    Context: {context}

    Please provide a well-structured answer using the information from the context. Also refine the answer based on your knowledge on the query, answer very briefly, don't use any irrelevant details and answer only the asked question concisely, but properly."""
        else:
            prompt = f"""Please answer this question based on your general knowledge, answer very briefly, don't use any irrelevant details and answer only the asked question concisely, but properly.:

    Question: {question}"""

        completion = self.groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides clear and accurate answers. When given context, you use it. When no context is available, you answer based on your general knowledge."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        return completion.choices[0].message.content
