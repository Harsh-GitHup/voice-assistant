import main as assist_main


def test_check_email_routes_to_send(monkeypatch):
    called = {"send": 0}

    monkeypatch.setattr(
        assist_main,
        "send_email",
        lambda: called.__setitem__("send", called["send"] + 1),
    )

    assist_main.process_command("send email")

    assert called["send"] == 1


def test_search_routes_to_generic_web_search(monkeypatch):
    called = {"search": 0}

    monkeypatch.setattr(
        assist_main,
        "search_web",
        lambda _query: called.__setitem__("search", called["search"] + 1),
    )

    assist_main.process_command("search python pytest")

    assert called["search"] == 1
