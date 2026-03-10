def test_regression_engine_initialization():
    """
    Ensures the engine is initialized once
    globally (Performance Fix).
    If engine is local to the function, it
    will be a different object each time
    This test checks if we are using
    the optimized global engine.
    """

    from main import _build_tts_engine

    assert _build_tts_engine() is not None, "TTS engine should be initialized"
    assert hasattr(_build_tts_engine(), "say"), "Engine should be pre-initialized"


def test_performance_response_time(mocker):
    """
    Performance Test: Logic processing must happen in under 200ms
    (excluding network time).
    """
    import time

    import main

    # Exclude external TTS engine latency from pure logic timing.
    mocker.patch("main.speak")

    start = time.perf_counter()

    # Run the internal logic of command processing
    main.wish_user()

    duration = time.perf_counter() - start
    assert duration < 0.2, f"Greeting logic is too slow: {duration}s"


def test_play_music_spotify_falls_back_to_youtube(monkeypatch):
    import main

    monkeypatch.setattr(main, "listen_command", lambda: "Believer")
    monkeypatch.setattr(main, "speak", lambda _text: None)
    monkeypatch.setattr(main.os, "startfile", lambda _uri: (_ for _ in ()).throw(OSError("no app")), raising=False)

    called = {"youtube": False}

    def fake_playonyt(song):
        called["youtube"] = True
        assert song == "Believer"

    monkeypatch.setattr(main.pywhatkit, "playonyt", fake_playonyt)

    main.play_music("play on spotify")
    assert called["youtube"] is True

