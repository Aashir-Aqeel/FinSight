from fastapi import FastAPI
from routes.income_router import router as income_router
from routes.expense_router import router as expense_router
from routes.auth_routes import router as auth_router
from routes.ai_routes import router as ai_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Expense Tracker API", description="API for managing expenses")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(income_router)
app.include_router(expense_router)
app.include_router(ai_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running 🚀"}