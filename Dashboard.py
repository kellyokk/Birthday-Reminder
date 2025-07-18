import streamlit as st

st.set_page_config(
    page_title="Birthday Reminder App",
    page_icon="🎊",
    layout="wide"
)


st.title("Dashboard")

st.markdown("""
    <style>
    .card-link {
        flex: 1;
        padding: 40px 20px;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        background-color: #ffffff;
        text-align: center;
        font-size: 22px;
        font-weight: 600;
        color: #2d3748;
        transition: all 0.25s ease;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        text-decoration: none;
        display: block;
    }

    .card-link:hover {
        background-color: #f7fafc;
        transform: scale(1.02);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
        border-color: #cbd5e0;
    }
            
    a {
            text-decoration: none !important;
            color: inherit !important;
        }
    </style>
""", unsafe_allow_html=True)

# Columns for page links
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <a href="/Add_Birthday" target="_self" class="card-link">
            🎂 Add a Birthday
        </a>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <a href="/View_Birthday_Calendar" target="_self" class="card-link">
            📅 View Birthdays
        </a>
        """,
        unsafe_allow_html=True
    )
