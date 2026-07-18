# AI Video Intelligence System

AI Video Summarization and Quiz Generation - an offline AI pipeline that transforms any video into a written transcript, a concise summary, and an interactive multiple-choice quiz.

Built as a final year project by Amulya.

## Features

- Video Upload - supports MP4, AVI, MOV, MKV formats
- Speech-to-Text Transcription - powered by OpenAI Whisper (runs locally)
- AI Summarization - generates a concise summary using a local DistilBART model
- Automatic Quiz Generation - creates fill-in-the-blank multiple-choice questions using spaCy Named Entity Recognition
- Live Stats - video duration, transcript word count, and quiz score
- Downloadable Results - export transcript and summary as .txt files
- Polished UI - dark animated theme built with Streamlit and custom CSS
- 100% Offline - no paid APIs, no API keys required

## Tech Stack

- UI Framework: Streamlit
- Audio Extraction: MoviePy
- Speech-to-Text: OpenAI Whisper (base model)
- Summarization: Hugging Face Transformers - sshleifer/distilbart-cnn-12-6
- Quiz Generation: spaCy - en_core_web_sm (Named Entity Recognition)
- Language: Python 3

## Installation and Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: pip install -r requirements.txt
4. Download the spaCy model: python -m spacy download en_core_web_sm
5. Run the app: streamlit run app.py

## How It Works

1. Upload a video file
2. Click Generate Summary and Quiz
3. The pipeline extracts audio, transcribes speech, summarizes it, and generates a quiz
4. View results across three tabs: Transcript, Summary, and Quiz
5. Take the quiz and get an instant score
6. Download the transcript and summary as text files

## Developed By

Amulya - Final Year Project

AI Video Summarization and Quiz Generation
'@ | Out-File -FilePath README.md -Encoding utf8