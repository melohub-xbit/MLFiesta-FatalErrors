# Chandana - AI-Powered Translation and Q&A System

Chandana is a powerful application that combines translation capabilities with an intelligent question-answering system. It features a Flask backend API and a React frontend interface.


[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.0+-61DAFB.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/flask-2.0+-black.svg)](https://flask.palletsprojects.com/)
[![NLTK](https://img.shields.io/badge/NLTK-3.0+-yellow.svg)](https://www.nltk.org/)
[![Groq](https://img.shields.io/badge/Groq-LLaMA3-orange.svg)](https://groq.com/)
[![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-2.0+-red.svg)](https://www.sbert.net/)
[![Material UI](https://img.shields.io/badge/Material_UI-5.0+-0081CB.svg)](https://mui.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-success)](https://ml-fiesta-fatal-errors.vercel.app/)

## Deployment
Chandana is live and accessible at: [Chandana](https://ml-fiesta-fatal-errors.vercel.app/)


## Team Details
- **Team Name**: ramyaparsania4
- **Team Members**:
  - [Krishna Sai](https://github.com/melohub-xbit)
  - [Ramya Parsania](https://github.com/RAMYA-PARSANIA)
  - [Sarthak Maheshwari](https://github.com/SartMa)

## Features

- **Translation Service**: Supports multiple language translation using Google Translator
- **Smart Q&A System**: Context-aware question answering using LLaMA 3 model via Groq
- **Semantic Search**: Utilizes sentence transformers for intelligent context matching
- **Modern Frontend**: React-based user interface for seamless interaction
- **Responsive Design**: Optimized for various screen sizes
- **Retrieving relevant information**: Utilizes semantic search to retrieve the most relevant information from the context and return the most relevant audio

## Tech Stack

### Backend
- Flask (Python web framework)
- NLTK for natural language processing
- SentenceTransformer for text embeddings
- Groq API for LLM integration
- deep-translator for translation services

### Frontend
- React
- Material UI components
- Axios for API calls

## Setup

### Prerequisites
- Python 3.8+
- Node.js and npm
- Groq API key
- Environment variables set up

### Installation (to run locally or use the deployed frontend link to use our application)
#### Please make sure to run the backend locally before running the frontend, and enter the API keys in the .env file

1. Clone the repository:
```bash
git clone https://github.com/melohub-xbit/MLFiesta-FatalErrors
```
#### Navigate to the folder named MLFiesta-FatalErrors and continuee with the steps below
2. Install backend dependencies:
```bash
pip install -r requirements.txt
```
3. Setup environment variables in a .env file like this:
```bash
GROQ_API_KEY=your_groq_api_key
HUGGINGFACE_TOKEN=your_huggingface_token
```

4. Install frontend dependencies (or use the deployed frontend link to use our application):
```bash
cd frontend
npm install
```

### Running the Application
1. Start the backend server:
```bash
python main.py
```
2. Start the frontend server (no need to do this if using the deployed frontend link):
```bash
cd frontend
npm start
```
And you can run our application from the frontend page that opens up
## Youtube Video Link

Find the Youtube link at: [MLFiesta Demo](https://drive.google.com/drive/folders/1781WXkVwYn90hG3D54W1N0pk3swaEU2V?usp=drive_link)

