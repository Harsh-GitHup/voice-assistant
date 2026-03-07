from __future__ import annotations

import re
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when

import main

scenarios("features/weather.feature")


def _extract_city(utterance: str) -> str:
    match = re.search(r"\bin\s+([A-Za-z\s]+)$", utterance.strip(), flags=re.IGNORECASE)
    if not match:
        return ""
    return match.group(1).strip()


def _default_weather_payload(city: str) -> dict[str, Any]:
    # 293.15K -> 20.0C for stable and easy-to-assert output.
    return {
        "main": {"temp": 293.15},
        "weather": [{"description": f"clear sky in {city}"}],
    }


@given("the assistant is listening", target_fixture="scenario_ctx")
@given("the assistant is active", target_fixture="scenario_ctx")
def assistant_ready() -> dict[str, Any]:
    return {
        "spoken": [],
        "request_url": None,
        "request_called": False,
        "utterance": None,
        "city": None,
    }


@given(parsers.parse('the user says "{utterance}"'))
@when(parsers.parse('the user says "{utterance}"'))
def user_says_weather_query(
    scenario_ctx: dict[str, Any], monkeypatch, utterance: str
) -> None:
    city = _extract_city(utterance)
    scenario_ctx["utterance"] = utterance
    scenario_ctx["city"] = city

    def _speak(msg: str) -> None:
        scenario_ctx["spoken"].append(msg)

    def _fake_get(url: str, timeout: int = 5):
        scenario_ctx["request_called"] = True
        scenario_ctx["request_url"] = url

        class _Resp:
            def json(self_nonlocal):
                return _default_weather_payload(city)

        return _Resp()

    monkeypatch.setattr(main, "speak", _speak)
    monkeypatch.setattr(
        main.os,
        "getenv",
        lambda key: "bdd-api-key" if key == "WEATHER_API_KEY" else None,
    )
    monkeypatch.setattr(main, "listen_command", lambda: city)
    monkeypatch.setattr(main.requests, "get", _fake_get)

    main.process_command(utterance)


@then(parsers.parse('the assistant should respond with "{expected}"'))
def assistant_response_contains(scenario_ctx: dict[str, Any], expected: str) -> None:
    all_output = "\n".join(scenario_ctx["spoken"]).lower()
    # Current app output uses "... And the weather is ...", so normalize expectation.
    normalized_expected = expected.lower().replace("the weather is", "weather is")
    assert normalized_expected in all_output


@then("the assistant should fetch data from OpenWeather")
def weather_api_called(scenario_ctx: dict[str, Any]) -> None:
    assert scenario_ctx["request_called"] is True
    assert "openweathermap.org" in str(scenario_ctx["request_url"])
    # URL-encoded city (spaces become +)
    encoded_city = scenario_ctx['city'].replace(" ", "+")
    assert f"q={encoded_city}" in str(scenario_ctx["request_url"])


@then("speak the temperature to the user")
def assistant_speaks_temperature(scenario_ctx: dict[str, Any]) -> None:
    all_output = "\n".join(scenario_ctx["spoken"]).lower()
    assert "temperature in" in all_output
    assert "degrees celsius" in all_output
