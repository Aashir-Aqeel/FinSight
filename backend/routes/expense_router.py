# routers/expense_router.py
from fastapi import APIRouter, Depends, HTTPException
from models.expense import Expense
from core.database import db
from bson import ObjectId
from core.auth import get_current_user

router = APIRouter(prefix="/expense", tags=["Expense"])

# -------------------------
# Add Expense
# -------------------------
@router.post("/")
def add_expense(expense: Expense, user_email: str = Depends(get_current_user)):
    data = expense.dict()
    data["user_email"] = user_email  # attach logged-in user
    result = db.expense.insert_one(data)
    saved_expense = db.expense.find_one({"_id": result.inserted_id})
    saved_expense["_id"] = str(saved_expense["_id"])
    return {"message": "Expense added successfully", "expense": saved_expense}

# -------------------------
# Get All Expenses for User
# -------------------------
@router.get("/")
def get_expenses(user_email: str = Depends(get_current_user)):
    data = list(db.expense.find({"user_email": user_email}))
    expenses = []
    for item in data:
        item["_id"] = str(item["_id"])
        expenses.append(item)
    return expenses

# -------------------------
# Delete Expense
# -------------------------
@router.delete("/{expense_id}")
def delete_expense(expense_id: str, user_email: str = Depends(get_current_user)):
    try:
        oid = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense ID")

    result = db.expense.delete_one({"_id": oid, "user_email": user_email})
    if result.deleted_count == 1:
        return {"message": "Expense deleted successfully"}
    return {"error": "Expense not found or unauthorized"}

# -------------------------
# Update Expense
# -------------------------
@router.put("/{expense_id}")
def update_expense(expense_id: str, expense: Expense, user_email: str = Depends(get_current_user)):
    try:
        oid = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense ID")

    update_result = db.expense.update_one(
        {"_id": oid, "user_email": user_email},
        {"$set": expense.dict(exclude_unset=True)}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found or no changes made")

    updated_expense = db.expense.find_one({"_id": oid})
    updated_expense["_id"] = str(updated_expense["_id"])
    return {"message": "Expense updated successfully", "expense": updated_expense}

# -------------------------
# Get Categories for User
# -------------------------
@router.get("/categories")
def get_categories(user_email: str = Depends(get_current_user)):
    categories = db.expense.distinct("category", {"user_email": user_email})
    return {"categories": categories}

# -------------------------
# Expense Summary for Dashboard
# -------------------------
@router.get("/summary")
def get_expense_summary(user_email: str = Depends(get_current_user)):
    total = 0
    for exp in db.expense.find({"user_email": user_email}):
        try:
            total += float(exp.get("amount", 0))
        except (TypeError, ValueError):
            continue
    return {"total_expense": total}
