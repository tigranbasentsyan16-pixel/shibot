import json
import os

FILE = "reminders.json"


def load_data():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_reminder(user_id, time, mode):
    data = load_data()

    if str(user_id) not in data:
        data[str(user_id)] = []

    data[str(user_id)].append({
        "time": time,
        "mode": mode
    })

    save_data(data)


def get_all_reminders():
    return load_data()