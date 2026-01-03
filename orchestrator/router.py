from fastapi import APIRouter, HTTPException
from models import QueryRequest
from services.orchestrator_service import OrchestratorService

router = APIRouter()

orchestrator_service = OrchestratorService()

@router.post("/query")
async def handle_query(req: QueryRequest):
    """
    Handle a query request by delegating to the orchestrator service.
    
    This is a thin route handler that:
    1. Validates the request (handled by Pydantic)
    2. Delegates business logic to OrchestratorService
    3. Handles HTTP exceptions and converts service errors to HTTP responses
    """
    try:
        # Delegate to service layer
        result = orchestrator_service.process_query(
            query_text=req.query_text,
            top_k=req.top_k
        )
        return result
        
    except Exception as e:
        print(f"Unexpected error processing query: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )