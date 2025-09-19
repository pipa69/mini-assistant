import os
import joblib
from typing import Optional

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "nlu_pipeline.joblib")

def load_model(path: Optional[str] = None):
    p = path or MODEL_PATH
    if not os.path.exists(p):
        raise FileNotFoundError(f"Model not found at {p}. Run training first.")
    return joblib.load(p)
