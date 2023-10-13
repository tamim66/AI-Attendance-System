import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-fb1fd-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "20215103109":
        {
            "name": "Tamim Iqbal",
            "major": "CSE",
            "starting_year": 2020,
            "total_attendance": 7,
            "intake": "47",
            "section": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
}

for key, value in data.items():
    ref.child(key).set(value)