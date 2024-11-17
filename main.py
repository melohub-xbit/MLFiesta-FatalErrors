from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import nltk
from deep_translator import GoogleTranslator
import dotenv
from qa_system_v2 import EnhancedQASystem
import os
import torch
import os
import json
import torch
import soundfile as sf
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Tuple
import logging
import warnings

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

class AudioProcessor:
    # [Previous methods remain the same until generate_embeddings]
    def __init__(self, 
                 input_folder: str = "./audio_files",
                 output_folder: str = "./audio_chunks",
                 processed_dir: str = "./processed_chunks",
                 language_id: str = 'kn',
                 chunk_duration: int = 30,
                 device: str = None):
        """
        Initialize the AudioProcessor with configuration parameters.
        """
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.processed_dir = processed_dir
        self.language_id = language_id
        self.chunk_duration = chunk_duration
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        # Initialize the embedding model
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    

        # Create necessary directories
        for folder in [input_folder, output_folder, processed_dir]:
            os.makedirs(folder, exist_ok=True)
        
        logging.info(f"Initialized AudioProcessor. Using device: {self.device}")
        
    
    def find_similar_segments(self, query: str, metadata_df: pd.DataFrame, 
                            top_k: int = 5) -> List[Dict[str, Any]]:
        """Find audio segments similar to the query text."""
        try:
            # Get embedding columns
            embedding_cols = [col for col in metadata_df.columns if col.startswith('embedding_')]
            if not embedding_cols:
                logging.error("No embedding columns found in metadata")
                return []
            
            # Get valid rows (those with embeddings)
            valid_rows = metadata_df.dropna(subset=[embedding_cols[0]])
            if len(valid_rows) == 0:
                logging.error("No valid embeddings found in metadata")
                return []
            
            logging.info(f"Searching through {len(valid_rows)} segments")
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query)
            
            # Get embeddings matrix
            embeddings_matrix = valid_rows[embedding_cols].values
            
            # Calculate similarities
            similarities = cosine_similarity([query_embedding], embeddings_matrix)[0]
            
            # Get top k results
            top_indices = similarities.argsort()[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                row = valid_rows.iloc[idx]
                results.append({
                    'chunk_id': row['chunk_id'],
                    'original_file': row['original_file'],
                    'start_time': row['start_time'],
                    'end_time': row['end_time'],
                    'transcription': row['transcription'],
                    'similarity_score': similarities[idx]
                })
            
            logging.info(f"Found {len(results)} similar segments")
            return results
            
        except Exception as e:
            logging.error(f"Error in similarity search: {str(e)}")
            return []

    
class TranslationSystem:
    def __init__(self):
        #print("Loading translation system...")
        pass

    def translate(self, text, source_lang, target_lang):
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated_text = translator.translate(text)
        return translated_text

def get_best_matching_chunk_path(segment_info: dict, output_folder: str) -> str:
    """Get the file path of the matching audio chunk"""
    # Extract filename without extension from original file
    original_filename = os.path.splitext(segment_info['original_file'])[0]
    
    # Create unique chunk identifier using original filename and chunk_id
    chunk_filename = f"{original_filename}_chunk_{segment_info['chunk_id']}.wav"
    
    # Join with output folder to get full path
    chunk_path = os.path.join(output_folder, chunk_filename)
    
    # Verify file exists
    if not os.path.exists(chunk_path):
        raise FileNotFoundError(f"Audio chunk not found at {chunk_path}")
        
    return chunk_path


# Initialize systems once at module level
qa_system = EnhancedQASystem('text_embeddings')
translation_system = TranslationSystem()
    
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy"
    }), 200

@app.route('/translate', methods=['POST'])
def translate():
    #print("Received translation request")
    global translation_system
    data = request.json
    text = data.get('text')
    from_lang = data.get('from_lang')
    to_lang = data.get('to_lang')
    #print(f"Received text: {text}, from_lang: {from_lang}, to_lang: {to_lang}")
    
    try:
        translated_text = translation_system.translate(text, from_lang, to_lang)
        #print("Translation successful")
        return jsonify({'translatedText': translated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    #print("Received generate request")
    global qa_system
    data = request.json
    question = data.get('question')
    #print(f"Received question: {question}")
    
    try:
        response = qa_system.generate_response(question)
        #print("Response generated successfully")
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/retrieve', methods=['POST'])
def retrieve():
    #print("Received retrieve request")
    data = request.json
    kannada_query = data.get('text')
    #print(f"Received Kannada query: {kannada_query}")
    
    if not kannada_query:
        return jsonify({'error': 'Kannada query text is required'}), 400
        
    processor = AudioProcessor(
        input_folder="./Dataset",
        output_folder="./audio_chunks",
        processed_dir="./processed_chunks",
        language_id="kn",
        chunk_duration=30
        )
    try:
        metadata_df = pd.read_csv("embeddings.csv")
        similar_segments = processor.find_similar_segments(kannada_query, metadata_df, top_k=5)
        
        #print(similar_segments)
        # Get the segment with highest similarity score
        best_segment = max(similar_segments, key=lambda x: x['similarity_score'])
        #print(f"Best segment: {best_segment}")
        best_match_path = get_best_matching_chunk_path(best_segment, "./audio_chunks")
        #print(f"Retrieval successful: {best_match_path}")
        return jsonify({
            'best_match_path': best_match_path,
            'similarity_score': best_segment['similarity_score'],
            'transcription': best_segment['transcription']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    audio_path = os.path.join('audio_chunks', filename)
    #print(f"Serving audio: {audio_path}")
    return send_file(audio_path, mimetype='audio/wav')

if __name__ == '__main__':
    nltk.download('punkt')
        
    # Start the Flask server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
