import streamlit as st
import requests
import time

API_URL = "http://localhost:8000/api/v1"

def register_user(email: str, username: str, password: str, full_name: str = None):

    response = requests.post(
        f"{API_URL}/auth/register",
        json={
            "email":        email,
            "username":     username,
            "password":     password,
            "full_name":    full_name
        }
    )
    
    if response.status_code == 200:
        return True, response.json()
    else:
        error = response.json().get("detail", "Ошибка регистрации")
        return False, error

def login_user(username: str, password: str):

    response = requests.post(
        f"{API_URL}/auth/login",
        data={
            "username":     username,
            "password":     password
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        st.session_state["access_token"] = data["access_token"]
        st.session_state["token_type"] = data["token_type"]
        st.session_state["is_authenticated"] = True
        
        # Сохранение времени истечения
        st.session_state["expires_at"] = time.time() + data["expires_in"]
        
        return True, data
    else:
        error = response.json().get("detail", "Ошибка авторизации")
        return False, error

def get_current_user():
    """Получение информации о текущем пользователе"""
    
    if not is_authenticated():
        return None
    
    headers = {
        "Authorization": f"{st.session_state['token_type']} {st.session_state['access_token']}"
    }
    
    response = requests.get(
        f"{API_URL}/auth/me",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        # Токен истек или недействителен
        logout()
        return None

def is_authenticated():
  
    if "is_authenticated" not in st.session_state:
        return False
    
    # Проверка истечения токена
    if "expires_at" in st.session_state:
        if time.time() > st.session_state["expires_at"]:
            logout()
            return False
    
    return st.session_state["is_authenticated"]

def logout():    
    st.session_state["is_authenticated"] = False
    st.session_state.pop("access_token", None)
    st.session_state.pop("token_type", None)
    st.session_state.pop("expires_at", None)
    st.rerun()