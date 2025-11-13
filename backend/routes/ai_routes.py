from fastapi import APIRouter
from core.openai_client import ask_openai
from models.ai import AIQuery

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/query")
async def ai_query(data: AIQuery):
    """
    AI endpoint for Financial Insights and Natural Language Queries
    """
    try:
        response = ask_openai(data.prompt)
        return {"response": response}
    except Exception as e:
        return {"response": f"❌ Error: {str(e)}"}


