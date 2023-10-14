import os

def execute_file(file_number):
    files = ["main.py", "DownloadCsv.py","TrainImages.py","AddDatatoDatabase.py","EncodeGenerator.py",]

    if 1 <= file_number <= len(files):
        file_to_execute = files[file_number - 1]
        os.system(f"python {file_to_execute}")
    else:
        print("Invalid input. Please choose a valid option.")

if __name__ == "__main__":
    while True:
        print("\t")
        print("\t")
        print("\t----------------------------------------------")
        print("\t----- Face Recognition Attendance System -----")
        print("\t----------------------------------------------")
        print("\t------- By Tamim, Rabby, Shorna, Rafi --------")
        print("\t----------------------------------------------")
        print("\t")
        print("Choose a file to execute:")
        print("1. Recognize & Attendance")
        print("2. Download")
        print("3. Train Images")
        print("4. Import Student Data Manually")
        print("5. Import Student Images Manually")
        print("6. Quit")

        user_input = input("Enter your choice (1-6): ")

        if user_input.lower() == 'q' or user_input == '6':
            break
        elif user_input.isdigit():
            execute_file(int(user_input))
        else:
            print("Invalid input. Please enter a number (1-6).")
