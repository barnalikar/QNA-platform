import hmac
import hashlib
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import SessionLocal
from app.models import User
from app.payment import RAZORPAY_SECRET
from app.email_utils import send_email

router = APIRouter()

class PaymentData(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    user_id: int
    plan: str

@router.post("/verify-payment")
def verify_payment(data: PaymentData):

    try:

        generated_signature = hmac.new(
            RAZORPAY_SECRET.encode(),
            f"{data.razorpay_order_id}|{data.razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()

        if generated_signature != data.razorpay_signature:
            raise HTTPException(400, "Invalid payment")

        db = SessionLocal()
        user = db.query(User).filter(User.id == data.user_id).first()

        if not user:
            raise HTTPException(404, "User not found")

        user.plan = data.plan
        db.commit()

        send_email(
            user.email,
            "Subscription Activated",
            f"You have successfully subscribed to {data.plan} plan."
        )

        db.close()

        return {"message": "Payment verified & plan upgraded"}

    except Exception as e:
        raise HTTPException(400, f"Payment verification failed: {str(e)}")