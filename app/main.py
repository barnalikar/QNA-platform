from fastapi import FastAPI
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
# Import routers
from app.routes import auth, questions, payment

# Import scheduler
from app.scheduler import scheduler

# Create tables
Base.metadata.create_all(bind=engine)

# Create app
app = FastAPI()

# Include routers
app.include_router(auth.router, prefix="/auth")
app.include_router(questions.router, prefix="/questions")
app.include_router(payment.router, prefix="/payment")

# Start scheduler
scheduler.start()

# Home route
@app.get("/")
def home():
    return {"message": "Welcome to QA Platform 🚀"}
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)