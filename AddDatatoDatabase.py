import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "your firebase db url"
})

ref = db.reference('Students')

data = {
    "109":
        {
            "name": "Tamim Iqbal",
            "major": "CSE",
            "starting_year": 2020,
            "total_attendance": 7,
            "intake": "47",
            "section": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "106":
        {
            "name": "Sheikh Rabby",
            "major": "CSE",
            "starting_year": 2022,
            "total_attendance": 0,
            "intake": "47",
            "section": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
}

for key, value in data.items():
    ref.child(key).set(value)