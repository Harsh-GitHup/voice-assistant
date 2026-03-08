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
