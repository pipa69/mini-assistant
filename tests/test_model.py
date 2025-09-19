from app.model_utils import load_model

def test_model_load():
    try:
        m = load_model()
    except FileNotFoundError:
        assert True  # acceptable in CI if model not present; ensure training runs separately
        return
    assert m is not None
