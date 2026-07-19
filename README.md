# 🎥 AI Video Intelligence System

### AI Video Summarization & Quiz Generation

An offline AI pipeline that transforms any video into a written transcript, a concise summary, and an interactive multiple-choice quiz — no paid APIs, no API keys, runs entirely on your own machine.

**Developed by Amulya — Final Year Project**

---

## 📖 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#️-installation--setup)
- [How It Works](#-how-it-works)
- [Future Improvements](#-future-improvements)
- [Author](#-developed-by)

---

## ✨ Features

| | |
|---|---|
| 📤 | **Video Upload** — supports MP4, AVI, MOV, MKV formats |
| 🎙️ | **Speech-to-Text Transcription** — powered by OpenAI Whisper (runs locally) |
| 📌 | **AI Summarization** — concise summaries via a local DistilBART model (map-reduce chunking for long transcripts) |
| ❓ | **Automatic Quiz Generation** — fill-in-the-blank multiple-choice questions using spaCy Named Entity Recognition |
| 📊 | **Live Stats** — video duration, transcript word count, quiz score |
| 📄 | **Downloadable Results** — export transcript and summary as `.txt` files |
| 🎨 | **Polished UI** — dark animated theme built with Streamlit and custom CSS |
| 🔒 | **100% Offline** — no paid APIs, no API keys required |

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | [Streamlit](https://streamlit.io/) |
| Audio Extraction | [MoviePy](https://zulko.github.io/moviepy/) |
| Speech-to-Text | [OpenAI Whisper](https://github.com/openai/whisper) (`base` model) |
| Summarization | [Hugging Face Transformers](https://huggingface.co/) — `sshleifer/distilbart-cnn-12-6` |
| Quiz Generation | [spaCy](https://spacy.io/) — `en_core_web_sm` (Named Entity Recognition) |
| Language | Python 3 |

---

## 📁 Project Structure

```
AI_Video_Summarizer/
├── app.py                  # Main Streamlit application
├── summarizer.py            # Summarization logic (DistilBART, chunking)
├── quiz_generator.py        # Quiz generation logic (spaCy NER-based MCQs)
├── requirements.txt         # Python dependencies
├── .streamlit/
│   └── config.toml          # Theme configuration
├── uploads/                 # Uploaded videos (gitignored)
├── audio/                   # Extracted audio files (gitignored)
└── transcript/               # Generated transcripts (gitignored)
```

---

## ⚙️ Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/Amulya014/AI_Video_Summarizer.git
cd AI_Video_Summarizer
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Download the spaCy language model**
```bash
python -m spacy download en_core_web_sm
```

**5. Run the app**
```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

> 💡 **Note:** On first run, Whisper and DistilBART models download automatically (a few hundred MB total). This happens once — subsequent runs use cached models.

---

## 🚀 How It Works

1. **Upload** a video file
2. Click **Generate Summary & Quiz**
3. The pipeline runs through:
   - 🎧 Audio extraction (MoviePy)
   - 📝 Speech-to-text transcription (Whisper)
   - 📌 Summarization (DistilBART, chunked for long transcripts)
   - ❓ Quiz generation (spaCy NER → fill-in-the-blank MCQs)
4. View results across three tabs: **Transcript**, **Summary**, **Quiz**
5. Take the quiz and get an instant score
6. Download the transcript/summary as text files

---

## 🔮 Future Improvements

- 🌍 Support for multiple languages
- 🎚️ Adjustable quiz difficulty levels
- 📑 Export quiz results as PDF
- 🔗 Support for YouTube video URLs (not just local uploads)
- 🎯 Larger Whisper models (`small`/`medium`) for improved transcription accuracy

---

## 👩‍💻 Developed By

**Amulya** — Final Year Project

*AI Video Summarization & Quiz Generation*

`Python` · `Streamlit` · `Whisper` · `NLP`

⭐ If you found this project interesting, consider giving it a star!
