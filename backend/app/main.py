from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from .database import engine, Base
from .api import auth

# Загрузка переменных окружения
load_dotenv()

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PROFAchievements API",
    description="API для мониторинга и визуализации достижений выпускников",
    version="1.0.0"
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Регистрация роутеров
app.include_router(auth.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to PROFAchievements API"}

@app.get("/health")
def health():
    return {"status": "healthy"}