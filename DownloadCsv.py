import firebase_admin
from firebase_admin import credentials, db
import csv
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Initialize Firebase app
cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-fb1fd-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendacerealtime-fb1fd.appspot.com"
})

def download_and_save_data_as_csv():
    # Assume we're fetching data from a specific Firebase path
    ref = db.reference('Students')
    data = ref.get()

    if data:
        # Get the current date in the format YYYYMMDD
        current_date = datetime.now().strftime('%Y-%m-%d')
        csv_file_path = f'DBdownload/Attendance_{current_date}.csv'

        # Write data to CSV
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['major','filename','name','intake','section','total_Attendance', 'last_attendance_time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write CSV header
            writer.writeheader()

            # Assuming the data is a dictionary
            for key, value in data.items():
                writer.writerow({
                    'filename': key,
                    'major': value.get('major', ''),
                    'name': value.get('name', ''),
                    'intake': value.get('intake', ''),
                    'section': value.get('section', ''),
                    'total_Attendance': value.get('total_attendance', ''),
                    'last_attendance_time': value.get('last_attendance_time', '')
                })

        print(f'Data downloaded and saved as CSV successfully. File name: {csv_file_path}')
    else:
        print('No data available.')

def send_email(csv_file_path):
    sender_email = 'adrisshobalok@gmail.com'
    receiver_email = 'lonetamim66@gmail.com'
    subject = 'Student Attendance Data'
    body = 'Attached is the Student attendance data from Firebase.'

    # Create a MIME message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEBase('application', 'octet-stream'))
    
    # Attach the CSV file
    with open(csv_file_path, 'rb') as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{csv_file_path}"')
        message.attach(part)
    
    # Connect to SMTP server and send email
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_username = 'adrisshobalok@gmail.com'
    smtp_password = 'bkru kcly zssm ifmz'
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print('Email sent successfully.')

if __name__ == "__main__":
    csv_file_path = download_and_save_data_as_csv()
    if csv_file_path:
        send_email(csv_file_path)


