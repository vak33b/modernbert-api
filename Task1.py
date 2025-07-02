from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import psutil

app = FastAPI()

# Загрузка модели и токенайзера
model_name = "answerdotai/ModernBERT-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
pipe = pipeline("fill-mask", model = model_name)

# Входные данные и эндпоинты
class TextRequest(BaseModel):
    text: str
@app.get("/status")
async def status():
    return {"status": "OK"}

@app.get("/metrics")
async def metrics():
    ram_used_mb = psutil.Process().memory_info().rss / 1024 * 1024
    return {"ram_usage_mb": round(ram_used_mb, 2)}

@app.get("/examples")
def examples():
    return {
        "examples": [
            "The capital of France is [MASK].",
            "He went to the [MASK] to buy some bread.",
            "Artificial intelligence will [MASK] the world."
        ]
    }


# POST-запрос формата " ... [MASK] ...
# [MASK] заполняется приоритетными вариантами
@app.post("/predict")
async def predict(request: TextRequest):
    try:
        result = pipe(request.text)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


