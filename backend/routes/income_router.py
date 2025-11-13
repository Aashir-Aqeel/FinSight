# routers/income_router.py
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import datetime
from core.database import async_db 
from core.auth import get_current_user

router = APIRouter(prefix="/income", tags=["Income"])

income_collection = async_db["income"]


# -------------------------
# Add Income
# -------------------------
@router.post("/")
async def add_income(income: dict, user_email: str = Depends(get_current_user)):
    income["date"] = income.get("date", datetime.utcnow())
    income["user_email"] = user_email
    result = await income_collection.insert_one(income)
    saved_income = await income_collection.find_one({"_id": result.inserted_id})
    saved_income["_id"] = str(saved_income["_id"])
    return {"message": "Income added successfully", "income": saved_income}


# -------------------------
# Get All Incomes for User
# -------------------------
@router.get("/")
async def get_incomes(user_email: str = Depends(get_current_user)):
    cursor = income_collection.find({"user_email": user_email})
    incomes = []
    async for item in cursor:
        item["_id"] = str(item["_id"])
        incomes.append(item)
    return incomes


# -------------------------
# Get Unique Categories for User
# -------------------------
@router.get("/categories")
async def get_income_categories(user_email: str = Depends(get_current_user)):
    categories = await income_collection.distinct("category", {"user_email": user_email})
    return {"categories": categories}


# -------------------------
# Update Income
# -------------------------
@router.put("/{income_id}")
async def update_income(income_id: str, updated_income: dict, user_email: str = Depends(get_current_user)):
    try:
        oid = ObjectId(income_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid income ID")

    result = await income_collection.update_one(
        {"_id": oid, "user_email": user_email},
        {"$set": updated_income}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Income not found or no changes made")

    updated_obj = await income_collection.find_one({"_id": oid})
    updated_obj["_id"] = str(updated_obj["_id"])
    return {"message": "Income updated successfully", "income": updated_obj}


# -------------------------
# Delete Income
# -------------------------
@router.delete("/{income_id}")
async def delete_income(income_id: str, user_email: str = Depends(get_current_user)):
    try:
        oid = ObjectId(income_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid income ID")

    result = await income_collection.delete_one({"_id": oid, "user_email": user_email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Income not found or unauthorized")
    return {"message": "Income deleted successfully"}


# -------------------------
# Income Summary for Dashboard
# -------------------------
@router.get("/summary")
async def get_income_summary(user_email: str = Depends(get_current_user)):
    total = 0
    cursor = income_collection.find({"user_email": user_email})
    async for inc in cursor:
        try:
            total += float(inc.get("amount", 0))
        except (TypeError, ValueError):
            continue
    return {"total_income": total}
