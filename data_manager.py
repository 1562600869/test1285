import json
import os
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.legal_aid.json")

LEGAL_TYPES = ["民事", "刑事", "劳动", "家事", "商事"]
TIME_SLOTS = ["上午", "下午"]
LAWYER_STATUSES = ["在职", "停职"]

EMPTY_DATA = {
    "lawyers": {},
    "schedules": [],
    "consults": []
}


def load_data():
    if not os.path.exists(DATA_FILE):
        return json.loads(json.dumps(EMPTY_DATA))
    try:
        with open(DATA_FILE,
                  encoding="utf-8") as f:
            data = json.load(f)
        for key in EMPTY_DATA:
            if key not in data:
                data[key] = EMPTY_DATA[key]
        return data
    except (json.JSONDecodeError, IOError):
        return json.loads(json.dumps(EMPTY_DATA))


def save_data(data):
    with open(DATA_FILE,
              "w",
              encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_month(month_str):
    try:
        datetime.strptime(month_str, "%Y-%m")
        return True
    except ValueError:
        return False


def validate_legal_type(lt):
    return lt in LEGAL_TYPES


def validate_time_slot(slot):
    return slot in TIME_SLOTS


def validate_status(status):
    return status in LAWYER_STATUSES


def lawyer_exists(data, lawyer_id):
    return lawyer_id in data["lawyers"]


def get_lawyer(data, lawyer_id):
    return data["lawyers"].get(lawyer_id)


def lawyer_is_active(data, lawyer_id):
    lawyer = get_lawyer(data, lawyer_id)
    return lawyer and lawyer["status"] == "在职"


def has_duplicate_schedule(data, lawyer_id, date, slot):
    for s in data["schedules"]:
        if s["lawyer_id"] == lawyer_id and s["date"] == date and s["slot"] == slot:
            return True
    return False


def count_same_slot_count(data, date, slot):
    count = 0
    for s in data["schedules"]:
        if s["date"] == date and s["slot"] == slot:
            count += 1
    return count


def has_schedule(data, lawyer_id, date, slot):
    for s in data["schedules"]:
        if s["lawyer_id"] == lawyer_id and s["date"] == date and s["slot"] == slot:
            return True
    return False
