import json
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv("/Users/euniceokeke/Birthday Reminder App/twilio.env")  # Loads values from .env file into environment variables

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

<<<<<<< HEAD
# === Load environment variables or use your real credentials ===
TWILIO_SID = "A******************"
TWILIO_AUTH_TOKEN = "******************"
TWILIO_PHONE_NUMBER = "************"
=======
>>>>>>> 25cf074 (New changes)

# === File paths ===
BIRTHDAY_FILE = "/Birthday Reminder App/birthdays.json"
NUMBER_FILE = "/Birthday Reminder App/numbers.json"
LOG_FILE = "/Birthday Reminder App/log.txt"

# === Log Function ===
def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_message)

# === Twilio setup ===
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# === Load numbers ===
def load_numbers():
    try:
        with open(NUMBER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# === Load birthdays ===
def load_birthdays():
    try:
        with open(BIRTHDAY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# === Check for today's birthdays ===
def get_today_birthdays(birthdays):
    today = datetime.now()
    month = today.month
    day = today.day
    celebrants = [name for name, info in birthdays.items()
                  if info["month"] == month and info["day"] == day]
    return celebrants

# === Send SMS ===
def send_sms(to, message):
    try:
        msg = client.messages.create(
            to=to,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )
        success_message = f"✅ Message sent to {to}, SID: {msg.sid}"
        print(success_message)
        write_log(success_message)
        return True
    except Exception as e:
        error_message = f"❌ Failed to send message to {to}: {e}"
        print(error_message)
        write_log(error_message)
        return False


# === Main script ===
if __name__ == "__main__":
    numbers = load_numbers()
    birthdays = load_birthdays()
    celebrants = get_today_birthdays(birthdays)

    if celebrants:
        if len(celebrants) == 1:
            message = f"Today is {celebrants[0]}'s birthday! Wish them a happy birthday!"
        else:
            names = ", ".join(celebrants)
            message = f"Today is {names}'s birthdays! Wish them a happy birthday!"

        for number in numbers:
            send_sms(number, message)
    else:
        print("📭 No birthdays today.")
