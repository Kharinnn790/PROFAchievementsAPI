from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api import auth

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PROFAchievements API",
    description="API для мониторинга достижений выпускников",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры
app.include_router(auth.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to PROFAchievements API"}

@app.get("/health")
def health():
    return {"status": "healthy"}