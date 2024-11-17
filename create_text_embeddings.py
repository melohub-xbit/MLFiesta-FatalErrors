from sentence_transformers import SentenceTransformer
import numpy as np
from nltk.tokenize import sent_tokenize
import os
import pickle

def create_and_save_embeddings(text_files_directory, output_directory):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    text_chunks = []
    
    # Process texts
    for filename in os.listdir(text_files_directory):
        if filename.endswith('.txt'):
            with open(os.path.join(text_files_directory, filename), 'r', encoding='utf-8') as f:
                text = f.read()
                sentences = sent_tokenize(text)
                for i in range(len(sentences) - 2):
                    chunk = ' '.join(sentences[i:i+3])
                    text_chunks.append(chunk)
    
    # Create embeddings
    embeddings = model.encode(text_chunks)
    
    # Save both embeddings and chunks
    os.makedirs(output_directory, exist_ok=True)
    np.save(os.path.join(output_directory, 'embeddings.npy'), embeddings)
    with open(os.path.join(output_directory, 'text_chunks.pkl'), 'wb') as f:
        pickle.dump(text_chunks, f)

if __name__ == "__main__":
    create_and_save_embeddings('text_files', 'text_embeddings')
