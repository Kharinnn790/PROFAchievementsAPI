import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

# ============================================
# НАСТРОЙКИ СТРАНИЦЫ
# ============================================
st.set_page_config(
    page_title="PROFAchievements - Мониторинг выпускников",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ПОДКЛЮЧЕНИЕ К БЭКЕНД API
# ============================================
API_URL = "http://localhost:8000/api/v1"

# Функция для запросов к API
def fetch_data(endpoint):
    """Получение данных из бэкенда"""
    try:
        response = requests.get(f"{API_URL}/{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка подключения к API: {e}")
        return None

# ============================================
# БОКОВАЯ ПАНЕЛЬ (ФИЛЬТРЫ)
# ============================================
with st.sidebar:
    st.image("https://via.placeholder.com/300x100?text=PROFAchievements", use_container_width=True)
    st.title("🎓 Фильтры")
    
    # Год выпуска
    year_filter = st.selectbox(
        "Год выпуска",
        options=["Все годы", 2020, 2021, 2022, 2023, 2024, 2025],
        index=0
    )
    
    # Специальность
    specialty_filter = st.selectbox(
        "Специальность",
        options=["Все специальности", "Информационные системы", "Гостиничное дело", "Экономика", "Дизайн"],
        index=0
    )
    
    st.divider()
    
    # Статистика в боковой панели
    st.subheader("📊 Быстрая статистика")
    
    # Здесь будут подгружаться данные
    if st.button("🔄 Обновить данные"):
        st.cache_data.clear()
        st.rerun()

# ============================================
# ЗАГОЛОВОК ГЛАВНОЙ СТРАНИЦЫ
# ============================================
st.title("🎓 Мониторинг профессиональных достижений выпускников")
st.markdown("---")

# ============================================
# КЛЮЧЕВЫЕ МЕТРИКИ (KPI)
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Всего выпускников",
        value="1,247",
        delta="+12% за год",
        help="Общее количество выпускников за все годы"
    )

with col2:
    st.metric(
        label="Трудоустроены",
        value="86%",
        delta="+5%",
        help="Процент трудоустроенных выпускников"
    )

with col3:
    st.metric(
        label="Средняя зарплата",
        value="85,000 ₽",
        delta="+8,000 ₽",
        help="Средняя заработная плата выпускников"
    )

with col4:
    st.metric(
        label="Работодателей",
        value="342",
        delta="+28",
        help="Количество компаний, нанимающих выпускников"
    )

st.markdown("---")

# ============================================
# ГРАФИКИ И ВИЗУАЛИЗАЦИЯ
# ============================================

# Создание двух колонок для графиков
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Трудоустройство по годам выпуска")
    
    # Пример данных (позже заменить на реальные из API)
    employment_data = pd.DataFrame({
        'Год выпуска': [2020, 2021, 2022, 2023, 2024],
        'Трудоустроены (%)': [92, 88, 85, 84, 89],
        'Продолжают обучение (%)': [5, 7, 9, 10, 8],
        'Не трудоустроены (%)': [3, 5, 6, 6, 3]
    })
    
    fig1 = px.bar(
        employment_data,
        x='Год выпуска',
        y='Трудоустроены (%)',
        title='Динамика трудоустройства выпускников',
        color_discrete_sequence=['#2E86C1'],
        text_auto=True
    )
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("💰 Средняя зарплата по специальностям")
    
    # Пример данных
    salary_data = pd.DataFrame({
        'Специальность': ['Информационные системы', 'Гостиничное дело', 'Экономика', 'Дизайн'],
        'Средняя зарплата (тыс. руб.)': [120, 65, 85, 70],
        'Количество выпускников': [450, 320, 280, 197]
    })
    
    fig2 = px.bar(
        salary_data,
        x='Специальность',
        y='Средняя зарплата (тыс. руб.)',
        title='Средняя зарплата по специальностям',
        color='Специальность',
        text_auto=True
    )
    fig2.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# Второй ряд графиков
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏢 Топ-5 работодателей")
    
    employers_data = pd.DataFrame({
        'Работодатель': ['Яндекс', 'Сбербанк', 'Ozon', 'Тинькофф', 'Wildberries'],
        'Выпускников': [45, 38, 32, 28, 25]
    })
    
    fig3 = px.bar(
        employers_data,
        x='Выпускников',
        y='Работодатель',
        orientation='h',
        title='Количество выпускников по работодателям',
        color='Выпускников',
        color_continuous_scale='Blues'
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("⭐ Востребованные навыки")
    
    skills_data = pd.DataFrame({
        'Навык': ['Python', 'SQL', 'JavaScript', 'Управление проектами', 'Английский язык'],
        'Востребованность (%)': [78, 72, 65, 58, 55]
    })
    
    fig4 = px.pie(
        skills_data,
        values='Востребованность (%)',
        names='Навык',
        title='Топ-5 востребованных навыков',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

# ============================================
# ТАБЛИЦА ПОСЛЕДНИХ ДОСТИЖЕНИЙ
# ============================================
st.markdown("---")
st.subheader("🏆 Последние достижения выпускников")

# Пример данных о достижениях
achievements_data = pd.DataFrame({
    'Выпускник': [
        'Иванов Иван',
        'Петрова Мария',
        'Сидоров Алексей',
        'Кузнецова Анна',
        'Смирнов Дмитрий'
    ],
    'Специальность': [
        'Информационные системы',
        'Дизайн',
        'Информационные системы',
        'Гостиничное дело',
        'Экономика'
    ],
    'Достижение': [
        'Повышение до Senior Developer в Яндексе',
        'Победа в конкурсе молодых дизайнеров',
        'Сертификат AWS Solutions Architect',
        'Назначение управляющим отелем 5*',
        'Защита кандидатской диссертации'
    ],
    'Дата': [
        '2026-02-15',
        '2026-02-10',
        '2026-02-05',
        '2026-01-28',
        '2026-01-20'
    ]
})

st.dataframe(
    achievements_data,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Дата": st.column_config.DateColumn("Дата", format="DD.MM.YYYY")
    }
)

# ============================================
# ФУТЕР
# ============================================
st.markdown("---")
st.caption(f"© PROFAchievements | Последнее обновление: {datetime.now().strftime('%d.%m.%Y %H:%M')}")