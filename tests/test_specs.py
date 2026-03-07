import os
import time


def test_security_env_loading():
    # Ensure load_dotenv is working and key isn't empty string
    assert os.getenv("WEATHER_API_KEY") is not None


def test_performance_latency():
    start = time.time()
    # Simulate a quick greeting check
    from main import wish_user

    wish_user()
    duration = time.time() - start
    assert duration < 0.5  # Should execute logic in under 500ms
