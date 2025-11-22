from fastapi import APIRouter
from models import GenerateRequest

from prompt import build_prompt

router = APIRouter()

@router.post("/generate")
async def generate_text(req: GenerateRequest):
    prompt = build_prompt(req.query, req.contexts)