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


def test_latency_threshold_() -> None:
    """listen_command should complete quickly when audio stack is mocked."""
    with (
        patch("main.sr.Recognizer") as mock_recognizer,
        patch("main.sr.Microphone") as mock_mic,
    ):
        mock_instance = MagicMock()
        mock_recognizer.return_value = mock_instance
        mock_instance.listen.return_value = MagicMock()
        mock_instance.recognize_google.return_value = "test command"
        mock_instance.adjust_for_ambient_noise.return_value = None

        mic_ctx = MagicMock()
        mock_mic.return_value.__enter__.return_value = mic_ctx
        mock_mic.return_value.__exit__.return_value = False

        start = time.time()
        listen_command()
        duration = time.time() - start
        assert duration < 2.0  # 2 seconds is a reasonable threshold for responsiveness
