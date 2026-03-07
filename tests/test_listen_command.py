import time
from unittest.mock import MagicMock, patch

from main import listen_command


def test_latency_threshold() -> None:
    """Voice assistant should respond in under 2 seconds for good UX."""
    with patch("main.sr.Recognizer") as mock_recognizer:
        mock_instance = MagicMock()
        mock_recognizer.return_value = mock_instance
        mock_instance.listen.return_value = MagicMock()
        mock_instance.recognize_google.return_value = "test command"

        start = time.time()
        listen_command()
        duration = time.time() - start
        assert duration < 2.0
