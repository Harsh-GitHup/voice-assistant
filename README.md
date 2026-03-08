# Vision-Voice AI Assistant 🤖👁️🎤

![CI Status](https://github.com/Harsh-GitHup/voice-assistant/actions/workflows/python-tests.yml/badge.svg)

A Python 3.11 voice assistant with speech input/output, web utilities, weather lookup, Wikipedia search, and email support.

## ✨ Features (CLI: `main.py`)

- **Voice Interaction**:  
  - Speech-to-Text via `speech_recognition` (Google recognizer)  
  - Text-to-Speech via `pyttsx3`
- **Core Commands**:
  - Greetings (`hello`)
  - Time and date
  - Weather by city (OpenWeatherMap)
  - Open websites (YouTube, Google, GitHub, StackOverflow, Gmail)
  - Open Windows apps (Notepad, Calculator, Chrome, Explorer, Excel, Word, PowerPoint, Spotify)
  - Web search (Google)
  - Wikipedia summary search
  - Send email via Gmail SMTP
- **Resilience**:
  - Graceful handling when microphone/audio input is unavailable
  - Safe city query encoding for weather API calls

---

## 🚀 Quick Start

### 1. Prerequisites

- **OS**: Windows (app-launch commands in `main.py` are Windows-oriented)
- **Python**: 3.11
- **uv** package manager

### 2. Install dependencies

```bash
uv sync --dev
```

### 3. Configure environment

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=optional_for_other_modules
WEATHER_API_KEY=your_openweathermap_key
EMAIL_ADDRESS=your_gmail_address
EMAIL_PASSWORD=your_gmail_app_password
```

> For Gmail, use an App Password if 2FA is enabled.

### 4. Run the CLI assistant

```bash
uv run python main.py
```

---

## 🗣️ Example voice commands

- "hello"
- "what is the time"
- "what is the date"
- "weather"
- "open website github"
- "open app notepad"
- "search python decorators"
- "search quantum computing on wikipedia"
- "send email"
- "exit" / "stop"

---

## 🧪 Testing

```bash
uv run python generate_test_audio.py
uv run pytest -q
# or
uv run pytest --cov=main tests/
```

For deterministic tests, mock network, microphone, and TTS dependencies.

---

## 📁 Project Structure (relevant modules)

- `main.py` → primary CLI assistant (used by tests/CI)
- `app.py` → runtime flow with microphone checks + text fallback
- `src/memory.py` → long-term memory (Chroma + RetrievalQA)
- `src/vision.py`, `src/streamlit_ui.py` → vision and UI-specific flows

---

## ⚠️ Notes

- Keep secrets in `.env` only.
- On Linux CI, audio/vision system libraries may be required (`portaudio19-dev`, `libasound2-dev`, `libgl1-mesa-glx`).

[⚖️ LICENSE (MIT)](LICENSE)
