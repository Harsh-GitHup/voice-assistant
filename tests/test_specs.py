import os
import time
from pathlib import Path

from dotenv import load_dotenv


def test_security_env_loading():
    """
    Ensure .env is loaded and
    WEATHER_API_KEY is not an empty string when present."""
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=env_path, override=False)

    key = os.getenv("WEATHER_API_KEY")
    assert key is None or key.strip() != ""


def test_performance_latency(monkeypatch):
    """Ensure greeting logic runs quickly without external TTS overhead."""
    from main import wish_user

    # Avoid audio/TTS latency in performance test
    monkeypatch.setattr("main.speak", lambda *_args, **_kwargs: None, raising=False)

    start = time.perf_counter()
    wish_user()
    duration = time.perf_counter() - start

    assert duration < 0.5
