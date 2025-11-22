from fastapi import APIRouter
from models import GenerateRequest, GenerateResponse
from llm import generate_answer
import config

from prompt import build_prompt

router = APIRouter()

@router.post("/generate")
async def generate_text(req: GenerateRequest):
    prompt = build_prompt(req.prompt, [doc.dict() for doc in req.contexts])

    answer, latency = generate_answer(prompt)
    return GenerateResponse(
        answer=answer,
        model=config.MODEL_NAME,
        latency_ms=latency
    )