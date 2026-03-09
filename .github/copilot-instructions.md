# Project Guidelines

## Code Style
- Follow PEP 8 for Python code.
- Keep changes targeted; avoid broad refactors unless requested.
- Add docstrings for new public functions and classes.
- Add or update tests with every behavior change.

## Architecture
- `main.py` is the primary CLI assistant module used by tests and CI.
- `app.py` handles alternate runtime flow (including microphone checks and text fallback).
- `src/` contains UI/vision and supporting modules.
- Preserve module boundaries:
  - Core CLI assistant behavior in `main.py`
  - UI/vision/runtime-specific behavior in `app.py` and `src/`

## Build and Test
- Python version: `3.11`
- Install dependencies: `uv sync --dev`
- Generate audio test fixtures: `uv run python generate_test_audio.py`
- Run tests:
  - `uv run pytest -q`
  - or `uv run pytest --cov=main tests/`
- Run CLI app: `uv run python main.py`
- Run Streamlit app: `uv run streamlit run app.py`

## Conventions
- Use `.env` for secrets/keys (`WEATHER_API_KEY`, `OPENAI_API_KEY`, email credentials).
- Keep assistant flows resilient to missing microphone/audio hardware; fail gracefully.
- Sanitize/encode city input before weather API URL composition.
- Prefer deterministic tests by mocking network, microphone, and TTS dependencies.
- Preserve existing TTS lifecycle behavior in edited modules (for `main.py`, keep per-utterance engine recreation if present).

## Documentation
- Keep `README.md`, `CONTRIBUTING.md`, and examples aligned with current `main.py` commands and behavior.
- Do not document features as stable unless implemented in code and covered by tests.

## Pitfalls
- Do not introduce conflicting OpenCV variants (`opencv-python` vs `opencv-python-headless`) unless explicitly required.
- Keep BDD assets aligned with tests (for example, `tests/features/weather.feature`).
- Linux CI may require system libraries:
  - `portaudio19-dev`
  - `libasound2-dev`
  - `libgl1-mesa-glx`
