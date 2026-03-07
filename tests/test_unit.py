import unittest
from unittest.mock import patch

from main import wish_user


class TestVoiceAssistant(unittest.TestCase):
    @patch("main.speak")
    @patch("datetime.datetime")
    def test_wish_user_morning(self, mock_datetime, mock_speak):
        # Mock time to 9 AM
        mock_datetime.now.return_value.hour = 9
        wish_user()
        mock_speak.assert_called_with("Good morning! How can I assist you?")
