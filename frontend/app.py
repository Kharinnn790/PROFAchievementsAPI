
import streamlit as st
from pages.auth import show_auth_page, show_logout_button
from utils.auth import is_authenticated, get_current_user

# Настройка страницы
st.set_page_config(
    page_title="PROFAchievements",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Проверка аутентификации
if not is_authenticated():
    show_auth_page()
else:
    # Пользователь авторизован — показываем основной интерфейс
    user = get_current_user()
    
    # Sidebar с информацией о пользователе
    with st.sidebar:
        st.image("https://via.placeholder.com/150?text=Logo", width=100)
        st.markdown(f"### 🎓 PROFAchievements")
        st.markdown("---")
        
        # Информация о пользователе
        st.markdown(f"**👤 {user.get('full_name', user.get('username'))}**")
        st.markdown(f"📧 {user.get('email')}")
        st.markdown("---")
        
        # Кнопка выхода
        show_logout_button()
        
        st.markdown("---")
        st.caption("© 2024 PROFAchievements")
    
    # Основной контент
    st.title("📊 Панель управления")
    st.markdown("Добро пожаловать в систему мониторинга достижений выпускников!")
    
    # Здесь будет ваш основной дашборд
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📈 Всего выпускников", "1,234", "+12%")
    with col2:
        st.metric("💼 Трудоустроены", "987", "+8%")
    with col3:
        st.metric("🏆 Достижений", "5,678", "+23%")
    
    st.markdown("---")
    st.info("🚀 Здесь будет основной дашборд с визуализацией данных")