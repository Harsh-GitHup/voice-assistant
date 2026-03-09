from unittest.mock import patch

from main import get_weather


@patch("main.listen_command", return_value="London")
@patch("main.os.getenv", return_value="dummy-api-key")
@patch("requests.get")
def test_weather_integration(mock_get, _mock_getenv, mock_listen, mocker):
    mock_get.return_value.json.return_value = {
        "main": {"temp": 15},
        "weather": [{"description": "clear sky"}],
    }
    spy_speak = mocker.patch("main.speak")

    get_weather()

    mock_get.assert_called_once()
    args, _ = mock_get.call_args
    assert "q=London" in args[0]
    assert "appid=dummy-api-key" in args[0]
    spy_speak.assert_any_call(
        "The temperature in London is -258.15 degrees Celsius. "
        "And the weather is clear sky."
    )
