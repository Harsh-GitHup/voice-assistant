def test_regression_engine_initialization():
    """
    Ensures the engine is initialized once
    globally (Performance Fix).
    If engine is local to the function, it
    will be a different object each time
    This test checks if we are using
    the optimized global engine.
    """

    from main import engine

    assert engine is not None
    assert hasattr(engine, "say"), "Engine should be pre-initialized"


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
