import hmac
import hashlib
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import SessionLocal
from app.models import User
from app.payment import RAZORPAY_SECRET
from datetime import datetime
import pytz

router = APIRouter()

class PaymentData(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    user_id: int
    plan: str

@router.post("/verify-payment")
def verify_payment(data: PaymentData):

    from datetime import datetime
    import pytz

    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    if not (10 <= now.hour < 11):
        raise HTTPException(400, "Payments allowed only between 10–11 AM")


    try:
      
        generated_signature = hmac.new(
        RAZORPAY_SECRET.encode(),
        (data.razorpay_order_id + "|" + data.razorpay_payment_id).encode(),
        hashlib.sha256
        ).hexdigest()

        if generated_signature != data.razorpay_signature:
            raise HTTPException(400, "Invalid payment signature")

        db = SessionLocal()
        user = db.query(User).filter(User.id == data.user_id).first()

        if not user:
            raise HTTPException(404, "User not found")

        user.plan = data.plan
        db.commit()
        db.close()

        return {"message": "Payment verified & plan upgraded"}

    except Exception as e:
        raise HTTPException(400, f"Payment verification failed: {str(e)}")