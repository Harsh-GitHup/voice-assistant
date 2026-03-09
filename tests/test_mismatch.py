import main


def test_hi_not_matched_inside_word(monkeypatch):
    spoken = []

    monkeypatch.setattr(main, "speak", lambda msg: spoken.append(msg))
    main.process_command("this should not trigger greeting")

    assert "Hello there!" not in spoken


def test_search_routes_to_web_search(monkeypatch):
    called = {"web": 0}

    monkeypatch.setattr(
        main,
        "search_web",
        lambda _q: called.__setitem__("web", called["web"] + 1),
    )

    main.process_command("search python testing")

    assert called["web"] == 1
