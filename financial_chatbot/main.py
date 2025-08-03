from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Any
from core.router import Router
# uvicorn main:app --reload --port 8001
router_instance = Router()

app = FastAPI(
    title="Financial Analysis API",
    description="Ask questions about public companies' financials, risks, and relationships",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    intent: str
    company: str
    data: Any
    data_type: str
    success: bool

@app.post("/finance_chatbot", response_model=QueryResponse)
def analyze_query(request: QueryRequest):
    """Analyze a company question and return structured response."""
    result = router_instance.process_query(request.query)
    return result
