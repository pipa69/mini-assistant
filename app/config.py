import os
SERVICE_NAME = os.getenv("SERVICE_NAME", "mini-assistant")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
MODEL_PATH = os.getenv("MODEL_PATH", "")
