import ast
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlparse


def _mock_weather_response() -> MagicMock:
    """Create a stable mocked weather API response."""
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 25},
        "name": "London",
    }
    return response


def test_no_secrets_in_logs(monkeypatch, capsys, caplog):
    """Ensure API keys are not printed to stdout/stderr or logs."""
    import main

    secret_key = "super-secret-weather-key"
    monkeypatch.setenv("WEATHER_API_KEY", secret_key)
    monkeypatch.setattr(
        main, "speak", lambda *_args,
        **_kwargs: None, raising=False
    )

    with patch("main.requests.get", return_value=_mock_weather_response()):
        main.get_weather("London")

    captured = capsys.readouterr()
    logged = " ".join(record.getMessage() for record in caplog.records)
    combined_output = f"{captured.out}\n{captured.err}\n{logged}"

    assert secret_key not in combined_output


def test_input_sanitization(monkeypatch):
    """
    Ensure user-provided city input is safely transmitted and cannot
    override query parameters like appid.
    """
    import main

    monkeypatch.setenv("WEATHER_API_KEY", "expected-real-key")
    monkeypatch.setattr(main, "speak", lambda *_args,
                        **_kwargs: None, raising=False)

    bad_input = "London&units=imperial&appid=HACKED"
    captured_request = {}

    def _fake_get(url, *args, **kwargs):
        captured_request["url"] = url
        captured_request["kwargs"] = kwargs
        return _mock_weather_response()

    with patch("main.requests.get", side_effect=_fake_get):
        main.get_weather(bad_input)

    params = captured_request["kwargs"].get("params")

    if params is not None:
        # Preferred safe pattern: requests handles encoding via params dict
        assert params.get("q") == bad_input
        assert params.get("appid") == "expected-real-key"
    else:
        # If URL is manually built,
        # ensure query parsing still preserves full city string
        # without allowing appid override through user input.
        parsed = parse_qs(
            urlparse(captured_request["url"]).query, keep_blank_values=True
        )
        assert parsed.get("appid", [None])[0] != "HACKED"
        assert parsed.get("q", [None])[0] == bad_input


def test_env_file_protection():
    """Ensure WEATHER_API_KEY is
    not provided via non-empty hardcoded default.
    """
    main_path = Path(__file__).resolve().parents[1] / "main.py"
    source = main_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    violations = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        # os.getenv("WEATHER_API_KEY", <default>)
        if isinstance(node.func, ast.Attribute) and node.func.attr == "getenv":
            if node.args and isinstance(node.args[0], ast.Constant):
                if node.args[0].value == "WEATHER_API_KEY":
                    default_node = None
                    if len(node.args) >= 2:
                        default_node = node.args[1]
                    else:
                        for kw in node.keywords:
                            if kw.arg == "default":
                                default_node = kw.value
                                break

                    if isinstance(default_node, ast.Constant):
                        if (
                            isinstance(default_node.value, str)
                            and default_node.value.strip()
                        ):
                            violations.append(
                                "os.getenv has non-empty default "
                                "string for WEATHER_API_KEY"
                            )

    assert not violations, "; ".join(violations)
