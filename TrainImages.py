import cv2
import os
import numpy as np
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-fb1fd-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendacerealtime-fb1fd.appspot.com"
})

# Firebase Storage bucket
bucket = storage.bucket()

def capture_and_upload_face(output_directory, output_filename):
    # Load pre-trained Haar Cascade face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open a connection to the default camera (usually the built-in webcam)
    camera = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    frame_count = 0
    face_detected_count = 0

    while True:
        # Capture a frame from the camera
        ret, frame = camera.read()
        
        if not ret:
            print("Error: Could not capture frame.")
            break

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Increment the frame count
        frame_count += 1

        # Check if a face is detected
        if len(faces) > 0:
            face_detected_count += 1

            for (x, y, w, h) in faces:
                # Crop the face to 216x216 pixels
                cropped_face = frame[y:y+h, x:x+w]
                cropped_face = cv2.resize(cropped_face, (216, 216))

                # Create the output directory if it doesn't exist
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)

                # Save the captured face to the output directory with the provided filename
                output_path = os.path.join(output_directory, f"{output_filename}.png")
                cv2.imwrite(output_path, cropped_face)
                print("Face image saved to", output_path)

                # Upload the face image to Firebase Storage
                image_url = upload_to_firebase(output_path, output_filename)

                # Capture additional data
                person_data = {
                    'name': input("Enter the person's name: "),
                    'major': input("Enter the person's major: "),
                    'starting_year': input("Enter the starting year: "),
                    'total_attendance': 0,
                    'intake': input("Enter the intake: "),
                    'section': input("Enter the section: "),
                    'last_attendance_time': datetime.now().strftime("%Y-%m-%d %I:%M:%S"),
                }

                # Upload data to Firebase Realtime Database
                upload_data_to_firebase(output_filename, person_data)

                # Break the loop and stop capturing frames
                break

        # Check if a face has been detected in more than 10 frames
        if face_detected_count > 2:
            break

        # Check for user input to exit
        key = cv2.waitKey(1)
        if key == 27:  # ESC key
            break

    # Release the camera
    camera.release()

    # Destroy OpenCV windows
    cv2.destroyAllWindows()

def upload_to_firebase(image_path, output_filename):
    try:
        # Upload the image to Firebase Storage
        folderPath = 'Images'
        pathList = os.listdir(folderPath)
        print(pathList)
        imgList = []
        studentIds = []
        for path in pathList:
            imgList.append(cv2.imread(os.path.join(folderPath, path)))
            studentIds.append(os.path.splitext(path)[0])
            fileName = f'{folderPath}/{path}'
            bucket = storage.bucket()
            blob = bucket.blob(fileName)
            blob.upload_from_filename(fileName)
        print("Image uploaded to Firebase Storage.")
        return blob.public_url
    except Exception as e:
        print("Error uploading image to Firebase Storage:", str(e))
        return None

def upload_data_to_firebase(filename, data):
    try:
        # Initialize Firebase Realtime Database
        ref = db.reference('Students')
        ref.child(filename).set(data)
        print("Data uploaded to Firebase Realtime Database.")
    except Exception as e:
        print("Error uploading data to Firebase Realtime Database:", str(e))

if __name__ == "__main__":
    output_directory = 'Images'  # Change this to your desired output directory
    output_filename = input("Enter Student ID: ")
    capture_and_upload_face(output_directory, output_filename)
