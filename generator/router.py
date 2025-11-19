from fastapi import APIRouter
from models import GenerateRequest

router = APIRouter()

@router.post("/generate")
async def generate_text(prompt: GenerateRequest):
    return {"generated_text": f"Generated text based on prompt: {prompt}"}