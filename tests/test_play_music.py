import main


def test_play_music_parses_inline_song_for_spotify(monkeypatch):
    monkeypatch.setattr(main, "speak", lambda _text: None)
    monkeypatch.setattr(main, "listen_command", lambda: "believer")

    called = {}

    def fake_startfile(uri):
        called["uri"] = uri

    monkeypatch.setattr(main.os, "startfile", fake_startfile, raising=False)

    main.play_music("play believer on spotify")

    assert called["uri"] == "spotify:search:believer"


def test_play_music_prompts_when_song_not_in_query(monkeypatch):
    monkeypatch.setattr(main, "speak", lambda _text: None)
    monkeypatch.setattr(main, "listen_command", lambda: "Believer")

    called = {}

    def fake_playonyt(song):
        called["song"] = song

    monkeypatch.setattr(main.pywhatkit, "playonyt", fake_playonyt)

    main.play_music("play")

    assert called["song"] == "Believer"


# TODO: This test is a bit hacky, but it ensures that the inline song parsing is used when the song is in the query, and that listen_command is not called. A better way to test this would be to refactor play_music to separate the parsing logic from the command execution logic, but this will do for now.
def test_play_music_parses_inline_song_for_spotify_(monkeypatch):
    monkeypatch.setattr(main, "speak", lambda _text: None)
    monkeypatch.setattr(
        main,
        "listen_command",
        lambda: (_ for _ in ()).throw(
            AssertionError("listen_command should not be called")
        ),
    )

    called = {}

    def fake_startfile(uri):
        called["uri"] = uri

    monkeypatch.setattr(main.os, "startfile", fake_startfile, raising=False)

    main.play_music_("play believer on spotify")

    assert called["uri"] == "spotify:search:believer"
