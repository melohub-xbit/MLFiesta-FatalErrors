from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    Trainer, 
    TrainingArguments
)
import torch
from torch.utils.data import Dataset
import nltk
from nltk.tokenize import sent_tokenize
import os
from deep_translator import GoogleTranslator
import dotenv
from huggingface_hub import login

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

MODEL_DIR = "downloaded_models"
TRAINING_DIR = "training_data"
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(TRAINING_DIR, exist_ok=True)

login(token=os.getenv("HUGGINGFACE_TOKEN"))

class TextDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_length=512, chunk_size=3):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.chunk_size = chunk_size
        self.qa_pairs = self.process_text_file(file_path)

    def process_text_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        sentences = sent_tokenize(text)
        qa_pairs = []
        
        for i in range(0, len(sentences) - self.chunk_size + 1):
            question = sentences[i]
            answer = " ".join(sentences[i+1:i+self.chunk_size])
            qa_pairs.append((question, answer))
        
        return qa_pairs

    def __len__(self):
        return len(self.qa_pairs)

    def __getitem__(self, idx):
        question, answer = self.qa_pairs[idx]
        
        input_text = f"question: {question}"

        inputs = self.tokenizer(
            input_text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        targets = self.tokenizer(
            answer,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        return {
            "input_ids": inputs["input_ids"].squeeze(),
            "attention_mask": inputs["attention_mask"].squeeze(),
            "labels": targets["input_ids"].squeeze()
        }

class QASystem:
    def __init__(self):
        # Change this to use your fine-tuned model
        self.model_path = "./fine_tuned_gpt2"  # Path where you saved the fine-tuned model
        self.tokenizer = GPT2Tokenizer.from_pretrained(
            self.model_path,
            cache_dir=MODEL_DIR
        )
        self.model = GPT2LMHeadModel.from_pretrained(
            self.model_path,
            cache_dir=MODEL_DIR
        )
        
        # Add padding token for GPT2
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def generate_response(self, question):
        # Format prompt for GPT2
        prompt = f"Question: {question}\nAnswer:"
        
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True,
            padding=True
        ).to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_length=256,
            num_beams=4,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=self.tokenizer.eos_token_id,
            length_penalty=1.0,
            early_stopping=True,
            repetition_penalty=1.2
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Remove the original prompt from response
        response = response.replace(prompt, "").strip()
        return response

class TranslationSystem:
    def __init__(self):
        print("Loading translation system...")
        pass

    def translate(self, text, source_lang, target_lang):
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated_text = translator.translate(text)
        return translated_text

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    from_lang = data.get('from_lang')
    to_lang = data.get('to_lang')
    
    try:
        translated_text = translation_system.translate(text, from_lang, to_lang)
        return jsonify({'translatedText': translated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    question = data.get('question')
    
    try:
        response = qa_system.generate_response(question)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    nltk.download('punkt')
    nltk.download('punkt_tab')
    
    # Initialize systems
    qa_system = QASystem()
    translation_system = TranslationSystem()
    
    # Train the model with the text file
    training_file = "D:/forKrishna/Dell-ForKrishna-All/MLFiesta/sandalwood_data.txt"
    # if os.path.exists(training_file):
    #     # print("Starting training process...")
    #     # qa_system.train_on_text_file(training_file)
    #     # print("Training completed, model saved!")
    #     # qa_system.load_trained_model()
    # else:
    #     print(f"Training file not found at: {training_file}")
    
    # Start the Flask server
    app.run(debug=True, port=5000)