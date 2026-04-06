
from fastapi import FastAPI

app = FastAPI(title="PROFAchievements API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to PROFAchievements API!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}