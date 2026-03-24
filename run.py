import subprocess
import sys
import os

def run_backend():
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"],
        cwd=os.path.join(os.path.dirname(__file__), "backend")
    )

def run_frontend():
    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py"],
        cwd=os.path.join(os.path.dirname(__file__), "frontend")
    )

if __name__ == "__main__":
    print(" Запуск бэкенда (FastAPI)...")
    backend = run_backend()
    
    print(" Запуск фронтенда (Streamlit)...")
    frontend = run_frontend()
    
    print("Приложения запущены!")
    print(" Бэкенд: http://localhost:8000")
    print(" Документация: http://localhost:8000/docs")
    print(" Фронтенд: http://localhost:8501")

    print("\nНажмите Ctrl+C для остановки...")
    
    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\n Остановка приложений...")
        backend.terminate()
        frontend.terminate()