from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models import User
from datetime import datetime
import pytz

def reset_questions():
    db = SessionLocal()
    users = db.query(User).all()

    for user in users:
        user.questions_today = 0

    db.commit()
    db.close()

    print("Daily limits reset at", datetime.now())

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

scheduler.add_job(reset_questions, "cron", hour=0, minute=0)