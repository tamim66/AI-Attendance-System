# AI-Attendance-System
- Credit goes to [Murtaza's Workshop - Robotics and AI](https://www.youtube.com/watch?v=iBomaK2ARyI&t=7424s) I just modified and added some features.
- A simple python project. 
- Automatic attendance using AI.
- Realtime Database.

![](https://i.postimg.cc/g2DS38XT/image-2023-10-17-191558836.png)

## How it works

![](https://i.postimg.cc/jdqZtCk6/image-2023-10-17-191911969.png)

### 1. Recognize and Attendance 

- OpenCV uses a Haar Cascade Classifier, a machine learning-based approach, to detect objects in images or video. A Haar Cascade is a classifier that is trained to recognize specific features (e.g., facial features) by using a set of positive and negative images.
- If face is Detected AI will update attendance count data in server.

### 2. Download Attendance

- Downloads Attendance Data as .CSV format.
- saved file can be found in "DBdownload" folder.

### 3. Train Images

- Captures your face using OpenCV
- Saves the captured image in 'Images' folder 
- After entering Student ID & Student Data Captured Image gets uploaded in Firebase storage & Database

# Installation

- Install Python.
- Install PIP.
- Install Microsoft Visual Studio [Community](https://visualstudio.microsoft.com/downloads/) & c++ libraries for windows

  ![](https://i.postimg.cc/QxhDkgYQ/image-2023-10-17-193926142.png)

- Open terminal/Cmd & run
  ```
  pip install -r requirements.txt
  ```
- Make a firebase project & build Storage `Images` and Databse `Students`
- Go to project settings > Service Account > Generate a private key > Download the JSON file in project dir and Rename it `ServiceAccountKey.json`
- Copy the Reference url from database and storage and place them inside :
  ```
  cred = credentials.Certificate("ServiceAccountKey.json")
  firebase_admin.initialize_app(cred, {
    'databaseURL': "database url",
    'storageBucket': "storage url"
  })
  ```
> [!IMPORTANT]
> Replace credential urls from every .py file.


> [!NOTE]
> Run App.py to start :D


 
