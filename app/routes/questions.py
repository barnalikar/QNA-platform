from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import SessionLocal
from app.models import User, Question
from app.auth_utils import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class QuestionData(BaseModel):
    content: str

def get_limit(plan):
    limits = {
        "free": 1,
        "bronze": 5,
        "silver": 10,
        "gold": float("inf")
    }
    return limits.get(plan, 1)  # default fallback

@router.post("/ask")
def ask_question(
    data: QuestionData,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print("USER_ID:", user_id)
    user = db.query(User).filter(User.id == user_id ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    limit = get_limit(user.plan)

    if user.questions_today >= limit:
        raise HTTPException(status_code=400, detail="Daily question limit reached")

    q = Question(user_id=user.id, content=data.content)
    db.add(q)

    user.questions_today += 1
    db.commit()

    return {"message": "Question posted successfully"}