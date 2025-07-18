import streamlit as st
import calendar
from datetime import datetime
import json
import re
import os
from twilio.rest import Client
from dotenv import load_dotenv

<<<<<<< HEAD
# === Load environment variables or use your real credentials ===
TWILIO_SID = "A******************"
TWILIO_AUTH_TOKEN = "******************"
TWILIO_PHONE_NUMBER = "************"
=======
load_dotenv("/Users/euniceokeke/Birthday Reminder App/twilio.env")  # Loads values from .env file into environment variables

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
>>>>>>> 25cf074 (New changes)

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

st.page_link("Dashboard.py", label="⬅️ Back to Dashboard")
st.set_page_config(page_title="Birthday Calendar - Birthday Reminder App", page_icon="📅", layout="wide")

BIRTHDAY_FILE = "/Birthday Reminder App/birthdays.json"
NUMBER_FILE = "/Birthday Reminder App/numbers.json"

def load_birthdays():
    try:
        with open(BIRTHDAY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

birthdays = load_birthdays()

birthday_lookup = {}
for name, info in birthdays.items():
    key = (int(info["month"]), int(info["day"]))
    birthday_lookup.setdefault(key, []).append(name)

st.title("📅 Birthday Calendar")

year = datetime.now().year
month = st.selectbox("Select Month", list(calendar.month_name)[1:], index=datetime.now().month - 1)

month_number = list(calendar.month_name).index(month)
cal = calendar.monthcalendar(year, month_number)

st.write(f"### {month} {year}")

selected_day = None

for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day == 0:
            cols[i].write(" ")
        else:
            label = f"{day}"
            if (month_number, day) in birthday_lookup:
                label = f"🎂 {day}"
            if cols[i].button(label, key=f"{month_number}-{day}"):
                selected_day = day


if selected_day:
    st.write(f"## Birthdays on {month} {selected_day}:")
    names = birthday_lookup.get((month_number, selected_day), [])
    if names:
        for n in names:
            st.write(f"- {n}'s birthday")
    else:
        st.write("No birthdays on this day.")

st.markdown("---")

def is_valid_phone(phone):
    phone_pattern = r"^\+1\d{10}$"
    return re.match(phone_pattern, phone) is not None

# Load numbers from JSON file
def load_numbers():
    if os.path.exists(NUMBER_FILE):
        try:
            with open(NUMBER_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# Save phone if it doesn't already exist
def save_number(phone):
    numbers = load_numbers()
    if phone in numbers:
        return False  # Already registered
    numbers.append(phone)
    with open(NUMBER_FILE, "w") as f:
        json.dump(numbers, f, indent=4)
    return True  # Successfully registered

def is_verified_number(phone_number):
    try:
        verified_numbers = client.outgoing_caller_ids.list()
        verified_list = [n.phone_number for n in verified_numbers]
        return phone_number in verified_list
    except Exception as e:
        print(f"Error checking verified numbers: {e}")
        return False
    
# Streamlit UI
with st.expander("📱 Receive SMS reminders?"):
    phone = st.text_input("Enter your phone number", placeholder="e.g. +12345678910")
    if st.button("Submit"):
        if not phone or not is_valid_phone(phone):
            st.error("Please enter a valid phone number. Must begin with +1 followed by 10 digits.")
        elif not is_verified_number(phone):
            st.error("Phone number must be verified before you can receive messages, contact support (Kelly).")
        else:
            if save_number(phone):
                st.success(f"You have successfully registered phone number {phone} for SMS reminders!")
            else:
                st.warning(f"This phone number {phone} is already registered.")
