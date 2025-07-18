import streamlit as st
from streamlit.components.v1 import html
import re
import json

st.set_page_config(page_title="Add Birthday - Birthday Reminder App", page_icon="🎂", layout="wide")
st.page_link("Dashboard.py", label="⬅️ Back to Dashboard")

BIRTHDAY_FILE = "/Birthday Reminder App/birthdays.json"

# ---- Function to validate name ----
def is_valid_name(name):
    name_pattern = r"^[a-zA-Z\s]+$"
    return re.match(name_pattern, name) is not None

# ---- Save birthday to JSON ----
def save_birthday(name, month, day):
    try:
        with open(BIRTHDAY_FILE, "r") as f:
            birthdays = json.load(f)
            if not isinstance(birthdays, dict):
                birthdays = {}
    except (FileNotFoundError, json.JSONDecodeError):
        birthdays = {}

    birthdays[name] = {"month": month, "day": day}

    with open(BIRTHDAY_FILE, "w") as f:
        json.dump(birthdays, f, indent=4)

# ---- Birthday input form ----
def add_form():
    st.header("🎂 Add A Birthday")

    months = ["--"] + list(range(1, 13))
    days = ["--"] + list(range(1, 32))

    with st.form("add_form"):
        name = st.text_input("What's your name?")
        month = st.selectbox("Select birth month", months)
        day = st.selectbox("Select day", days)
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if not name or not is_valid_name(name):
            st.error("Please enter a valid name (letters and spaces only).")
            return
        
        if month == "--" or day == "--":
            st.error("Please select both month and day.")
            return
        
        save_birthday(name.strip(), month, day)
        st.success(f"{name}'s birthday ({month}/{day}) has been saved! 🎉")

add_form()


