from unittest.mock import patch

import main


def test_e2e_weather_flow(mocker):
    """Weather flow from mocked voice input to spoken weather response."""
    mocker.patch("main.os.getenv", return_value="dummy-api-key")
    mocker.patch("main.listen_command", return_value="London")

    mock_get = mocker.patch("main.requests.get")
    mock_get.return_value.json.return_value = {
        "main": {"temp": 298.15},  # 25 Celsius
        "weather": [{"description": "sunny"}],
        "name": "London",
    }
    spy_speak = mocker.patch("main.speak")

    main.get_weather()

    spy_speak.assert_any_call(
        "The temperature in London is 25.0 degrees Celsius. "
        "And the weather is sunny."
    )


def test_security_input_sanitization():
    """Security Test: city query should be URL-encoded."""
    with patch("main.os.getenv", return_value="dummy-api-key"):
        with patch("main.listen_command", return_value="London&units=metric"):
            with patch("main.speak"):
                with patch("main.requests.get") as mock_requests:
                    mock_requests.return_value.json.return_value = {
                        "main": {"temp": 298.15},
                        "weather": [{"description": "clear sky"}],
                        "name": "London",
                    }
                    main.get_weather()
                    # URL currently uses direct interpolation;
                    # this guards against regressions.
                    args, _ = mock_requests.call_args
                    assert "q=London%26units%3Dmetric" in args[0]
                    assert (
                        "London%26units%3Dmetric" in args[0]
                        or "London&units=metric" in args[0]
                    )
