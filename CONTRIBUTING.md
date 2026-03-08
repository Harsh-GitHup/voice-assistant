# Contributing to Vision-Voice AI Assistant

Thanks for contributing.

## 📜 Code of Conduct

Be respectful and professional in all interactions.

## 🛠️ How to Contribute

### Report Bugs

- Open a GitHub issue.
- Include OS, Python version, and steps to reproduce.

### Suggest Enhancements

- Open an issue with the `enhancement` label.
- Explain the use case and expected behavior.

### Submit Pull Requests

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-change`).
3. Make targeted changes (avoid broad refactors unless requested).
4. Add/update tests for behavior changes.
5. Run checks locally.
6. Push and open a Pull Request.

## 🧪 Development Setup

```bash
uv sync --dev
uv run python generate_test_audio.py
uv run pytest -q
```

## ✅ Project Guidelines

- Follow **PEP 8**.
- Add docstrings for new public functions/classes.
- Preserve module boundaries:
  - `main.py`: core CLI assistant behavior
  - `app.py` and `src/`: UI/vision/runtime-specific behavior
- Use `.env` for keys/credentials (`WEATHER_API_KEY`, `OPENAI_API_KEY`, email creds).
- Keep flows resilient when microphone/audio hardware is missing.
- Sanitize city input before weather URL composition.
- Prefer deterministic tests by mocking network, microphone, and TTS.

## ⚠️ Common Pitfalls

- Do not add conflicting OpenCV variants (`opencv-python` vs `opencv-python-headless`) unless explicitly required.
- Keep BDD assets aligned with tests (e.g., `tests/features/weather.feature`).
- Linux CI may need:
  - `portaudio19-dev`
  - `libasound2-dev`
  - `libgl1-mesa-glx`
