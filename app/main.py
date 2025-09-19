from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import QueryRequest, QueryResponse
from .assistant import MiniAssistant
from .model_utils import load_model
from .db import log_interaction
import uvicorn
from .config import HOST, PORT

app = FastAPI(title="Mini Assistant API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
try:
    model = load_model()
except FileNotFoundError:
    model = None

assistant = MiniAssistant(model=model, name="RafciuAssistant") if model else None

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    if not req.text:
        raise HTTPException(status_code=400, detail="Empty text")
    if assistant is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Run training first.")
    res = await assistant.handle(req.text, user_id=req.user_id)
    log_interaction(req.user_id, req.text, res["answer"], res.get("intent"), res.get("confidence", 0.0))
    return res

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, log_level="info")
