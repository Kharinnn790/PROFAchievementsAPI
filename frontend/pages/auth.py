import streamlit as st
from utils.auth import register_user, login_user, is_authenticated

def show_auth_page():   
    st.set_page_config(
        page_title="PROFAchievements - Вход",
        page_icon="🎓",
        layout="centered"
    )
    #   css
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
            }
            .auth-container {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            }
            .auth-container h2 {
                color: #333333;
                text-align: center;
                margin-bottom: 1.5rem;
            }
            .stTextInput label, .stButton button {
                color: #333333;
            }
            .demo-link {
                text-align: center;
                margin-top: 1rem;
                font-size: 0.9rem;
                color: #555555;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    
    # Логотип и заголовок
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🎓 PROFAchievements")
        st.markdown("### Система мониторинга достижений выпускников")
    
    st.markdown("---")
    
    # Вкладки для входа и регистрации
    tab1, tab2 = st.tabs(["🔐 Вход", "📝 Регистрация"])
    
    with tab1:
        st.markdown("### Войдите в свой аккаунт")
        
        with st.form("login_form"):
            username = st.text_input("Email или имя пользователя")
            password = st.text_input("Пароль", type="password")
            submitted = st.form_submit_button("Войти", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("Пожалуйста, заполните все поля")
                else:
                    success, result = login_user(username, password)
                    if success:
                        st.success("Успешный вход!")
                        st.rerun()
                    else:
                        st.error(f"Ошибка: {result}")
        
        # Демо-аккаунты
        with st.expander("ℹ️ Демо-аккаунты"):
            st.markdown("""
            **Студент:**  
            - Логин: `student`  
            - Пароль: `student123`
            
            **Администратор:**  
            - Логин: `admin`  
            - Пароль: `admin123`
            """)
    
    with tab2:
        st.markdown("### Создайте новый аккаунт")
        
        with st.form("register_form"):
            email = st.text_input("Email *")
            username = st.text_input("Имя пользователя *")
            full_name = st.text_input("Полное имя")
            password = st.text_input("Пароль *", type="password")
            confirm_password = st.text_input("Подтвердите пароль *", type="password")
            
            submitted = st.form_submit_button("Зарегистрироваться", use_container_width=True)
            
            if submitted:
                if not email or not username or not password:
                    st.error("Пожалуйста, заполните обязательные поля")
                elif password != confirm_password:
                    st.error("Пароли не совпадают")
                elif len(password) < 6:
                    st.error("Пароль должен содержать минимум 6 символов")
                else:
                    success, result = register_user(email, username, password, full_name)
                    if success:
                        st.success("Регистрация успешна! Теперь вы можете войти.")
                    else:
                        st.error(f"Ошибка: {result}")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_logout_button():
    """Отображение кнопки выхода"""
    
    if is_authenticated():
        from utils.auth import get_current_user, logout
        
        user = get_current_user()
        if user:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**👤 {user.get('full_name', user.get('username'))}**")
            with col2:
                if st.button("🚪 Выйти", use_container_width=True):
                    logout()