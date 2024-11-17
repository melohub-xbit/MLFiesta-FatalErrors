from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from deep_translator import GoogleTranslator
import dotenv
from qa_system_v2 import EnhancedQASystem
import os
import datetime

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

class TranslationSystem:
    def __init__(self):
        print("Loading translation system...")
        pass

    def translate(self, text, source_lang, target_lang):
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated_text = translator.translate(text)
        return translated_text

# Initialize systems once at module level
qa_system = EnhancedQASystem('text_embeddings')
translation_system = TranslationSystem()
    
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/translate', methods=['POST'])
def translate():
    global translation_system
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
    global qa_system
    data = request.json
    question = data.get('question')
    
    try:
        response = qa_system.generate_response(question)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    nltk.download('punkt')
        
    # Start the Flask server
    app.run(debug=True, port=5000, use_reloader=False)
