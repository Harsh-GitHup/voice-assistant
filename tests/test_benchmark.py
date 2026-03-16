import datetime as real_datetime
import importlib
import sys
import types

import pytest


class _FakeEngine:
    def __init__(self):
        self._voices = [types.SimpleNamespace(id="fake-voice")]

    def getProperty(self, name):
        if name == "voices":
            return self._voices
        return None

    def setProperty(self, name, value):
        return None

    def say(self, text):
        return None

    def runAndWait(self):
        return None


def _install_stub_modules(monkeypatch):
    # pyttsx3 stub
    pyttsx3_mod = types.ModuleType("pyttsx3")
    pyttsx3_mod.init = lambda: _FakeEngine()
    monkeypatch.setitem(sys.modules, "pyttsx3", pyttsx3_mod)

    # speech_recognition stub
    sr_mod = types.ModuleType("speech_recognition")

    class UnknownValueError(Exception):
        pass

    class RequestError(Exception):
        pass

    class Recognizer:
        def adjust_for_ambient_noise(self, source, duration=1):
            return None

        def listen(self, source):
            return b"audio"

        def recognize_google(self, audio, language="en-US"):
            return "test command"

    class Microphone:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    sr_mod.UnknownValueError = UnknownValueError
    sr_mod.RequestError = RequestError
    sr_mod.Recognizer = Recognizer
    sr_mod.Microphone = Microphone
    monkeypatch.setitem(sys.modules, "speech_recognition", sr_mod)

    # wikipedia stub
    wiki_mod = types.ModuleType("wikipedia")

    class DisambiguationError(Exception):
        pass

    class PageError(Exception):
        pass

    wiki_mod.exceptions = types.SimpleNamespace(
        DisambiguationError=DisambiguationError,
        PageError=PageError,
    )
    wiki_mod.summary = lambda query, sentences=2: "Stub Wikipedia summary"
    monkeypatch.setitem(sys.modules, "wikipedia", wiki_mod)

    # dotenv stub
    dotenv_mod = types.ModuleType("dotenv")
    dotenv_mod.load_dotenv = lambda: None
    monkeypatch.setitem(sys.modules, "dotenv", dotenv_mod)


@pytest.fixture
def assistant_module(monkeypatch):
    _install_stub_modules(monkeypatch)
    sys.modules.pop("main", None)
    return importlib.import_module("main")


def test_process_command_hello_speaks_greeting(assistant_module, monkeypatch):
    spoken = []
    monkeypatch.setattr(assistant_module, "speak", lambda text: spoken.append(text))

    assistant_module.process_command("hello assistant")

    assert "Hello there!" in spoken


def test_open_site_github_opens_browser(assistant_module, monkeypatch):
    opened = []
    spoken = []
    monkeypatch.setattr(assistant_module, "speak", lambda text: spoken.append(text))
    monkeypatch.setattr(
        assistant_module.webbrowser, "open", lambda url: opened.append(url)
    )

    assistant_module.open_site("github")

    assert opened == ["https://www.github.com"]
    assert spoken[0] == "Opening github..."


def test_open_app_notepad_calls_os_system(assistant_module, monkeypatch):
    commands = []
    monkeypatch.setattr(assistant_module, "speak", lambda _: None)
    monkeypatch.setattr(assistant_module.os, "system", lambda cmd: commands.append(cmd))

    assistant_module.open_app("notepad")

    assert commands == ["notepad.exe"]


def test_search_wikipedia_success(assistant_module, monkeypatch, capsys):
    spoken = []
    monkeypatch.setattr(assistant_module, "speak", lambda text: spoken.append(text))
    monkeypatch.setattr(
        assistant_module.wikipedia,
        "summary",
        lambda query, sentences=2: "Python is a programming language.",
    )

    assistant_module.search_wikipedia("Python")

    captured = capsys.readouterr()
    assert "According to Wikipedia" in spoken
    assert "Python is a programming language." in spoken
    assert "Python is a programming language." in captured.out


def test_search_wikipedia_disambiguation_error(assistant_module, monkeypatch):
    spoken = []
    monkeypatch.setattr(assistant_module, "speak", lambda text: spoken.append(text))

    def _raise_disambiguation(*args, **kwargs):
        raise assistant_module.wikipedia.exceptions.DisambiguationError("Ambiguous")

    monkeypatch.setattr(assistant_module.wikipedia, "summary", _raise_disambiguation)

    assistant_module.search_wikipedia("Mercury")

    assert "Multiple Wikipedia results found. Please be more specific." in spoken


def test_get_weather_success(assistant_module, monkeypatch):
    spoken = []
    monkeypatch.setattr(assistant_module, "speak", lambda text: spoken.append(text))
    monkeypatch.setattr(
        assistant_module.os,
        "getenv",
        lambda key: "dummy-key" if key == "WEATHER_API_KEY" else None,
    )
    monkeypatch.setattr(assistant_module, "listen_command", lambda: "Delhi")

    class _Resp:
        def json(self):
            return {
                "weather": [{"description": "clear sky"}],
                "main": {"temp": 300.15},  # 27.0 C
            }

    monkeypatch.setattr(
        assistant_module.requests, "get", lambda *args, **kwargs: _Resp()
    )

    assistant_module.get_weather()

    assert any("temperature in Delhi is 27.0 degrees Celsius" in s for s in spoken)


def test_get_weather_missing_api_key(assistant_module, monkeypatch):
    spoken = []
    monkeypatch.setattr(assistant_module, "speak", lambda text: spoken.append(text))
    monkeypatch.setattr(assistant_module.os, "getenv", lambda key: None)

    result = assistant_module.get_weather()

    assert result is None
    assert "Weather API key is missing." in spoken


def test_send_email_success(assistant_module, monkeypatch):
    spoken = []
    monkeypatch.setattr(assistant_module, "speak", lambda text: spoken.append(text))

    env = {
        "EMAIL_ADDRESS": "sender@example.com",
        "EMAIL_PASSWORD": "password123",
    }
    monkeypatch.setattr(assistant_module.os, "getenv", lambda key: env.get(key))

    answers = iter(["to@example.com", "Subject", "Body"])
    monkeypatch.setattr(assistant_module, "listen_command", lambda: next(answers))

    calls = {"login": None, "send_message": None, "closed": 0}

    class _FakeSMTPSSL:
        def __init__(self, host, port, context=None):
            self.host = host
            self.port = port
            self.context = context

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            calls["closed"] += 1
            return False

        def login(self, email, pwd):
            calls["login"] = (email, pwd)

        def send_message(self, msg):
            calls["send_message"] = msg

    monkeypatch.setattr(assistant_module.smtplib, "SMTP_SSL", _FakeSMTPSSL)

    assistant_module.send_email()

    assert calls["login"] == ("sender@example.com", "password123")
    assert calls["send_message"]["To"] == "to@example.com"
    assert calls["send_message"]["Subject"] == "Subject"
    assert "Email has been sent successfully!" in spoken


def test_process_command_exit_daytime_says_goodbye_and_exits(
    assistant_module, monkeypatch
):
    import builtins

    spoken = []

    class _FakeDateTime(real_datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2025, 1, 1, 14, 0, 0)

    monkeypatch.setattr(assistant_module, "speak", lambda text: spoken.append(text))
    monkeypatch.setattr(assistant_module.datetime, "datetime", _FakeDateTime)
    monkeypatch.setattr(builtins, "exit", lambda: (_ for _ in ()).throw(SystemExit))

    with pytest.raises(SystemExit):
        assistant_module.process_command("exit")

    assert "Goodbye!" in spoken
