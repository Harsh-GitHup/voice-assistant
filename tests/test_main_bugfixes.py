import main


def test_play_music_spotify_falls_back_to_web_when_app_missing(monkeypatch):
    monkeypatch.setattr(main, "speak", lambda _text: None)
    monkeypatch.setattr(main, "listen_command", lambda: "test song")
    monkeypatch.setattr(main.os.path, "exists", lambda _path: False)

    opened_urls = []
    monkeypatch.setattr(main.webbrowser, "open", lambda url: opened_urls.append(url))
    monkeypatch.setattr(
        main.pywhatkit,
        "playonyt",
        lambda _music: (_ for _ in ()).throw(AssertionError("YouTube should not be called")),
    )

    main.play_music("play music on spotify")

    assert opened_urls == ["https://open.spotify.com/search/test+song"]


def test_play_music_spotify_web_failure_falls_back_to_youtube(monkeypatch):
    monkeypatch.setattr(main, "speak", lambda _text: None)
    monkeypatch.setattr(main, "listen_command", lambda: "test song")
    monkeypatch.setattr(main.os.path, "exists", lambda _path: False)

    def raise_web_error(_url):
        raise RuntimeError("browser failure")

    monkeypatch.setattr(main.webbrowser, "open", raise_web_error)

    yt_calls = []
    monkeypatch.setattr(main.pywhatkit, "playonyt", lambda music: yt_calls.append(music))

    main.play_music("play music on spotify")

    assert yt_calls == ["test song"]


def test_send_email_does_not_send_when_subject_or_body_missing(monkeypatch):
    monkeypatch.setenv("EMAIL_ADDRESS", "sender@example.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "password")

    prompts = []
    monkeypatch.setattr(main, "speak", lambda text: prompts.append(text))

    inputs = iter(["receiver@example.com", None, "body"])
    monkeypatch.setattr(main, "listen_command", lambda: next(inputs))

    class FailIfCalledSMTP:
        def __init__(self, *args, **kwargs):
            raise AssertionError("SMTP should not be called when details are incomplete")

    monkeypatch.setattr(main.smtplib, "SMTP_SSL", FailIfCalledSMTP)

    main.send_email()

    assert any("subject or body" in msg.lower() for msg in prompts)


def test_process_command_wikipedia_query_is_cleaned(monkeypatch):
    monkeypatch.setattr(main, "speak", lambda _text: None)

    captured = {}
    monkeypatch.setattr(
        main, "search_wikipedia", lambda query: captured.setdefault("query", query)
    )

    main.process_command("search Python decorators on wikipedia")

    assert captured["query"] == "python decorators"