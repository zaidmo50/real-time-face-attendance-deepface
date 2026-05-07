from tkinter import *
import csv
import os

def show_attendance_log():
    root = Tk()
    root.title("Attendance Log")
    root.geometry("1920x1080")
    
    Label(root, text="Attendance Log", font=("Arial", 20)).pack(pady=10)
    
    text = Text(root, height=36, width=100)
    text.pack(pady=5)

    # Check if the attendance log file exists; if not, create it
    log_file_path = 'data/attendance_log.csv'
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as file:
            file.write('User Name,Date and Time\n') 
    
    # Read and display the attendance log
    with open(log_file_path, newline='') as file:
        reader = csv.reader(file)
        lines = list(reader)
        
        if len(lines) <= 1:  # Check if there's any attendance logged
            text.insert(END, "No attendance logged yet.\n")
        else:
            for row in lines[1:]:  # Skip the header row
                # Ensure the row is not empty and has enough columns
                if len(row) >= 2:  
                    text.insert(END, f"{row[0]} - {row[1]}\n")  # Display user and timestamp
                else:
                    text.insert(END, "Error: Incomplete log entry.\n")

    root.mainloop()


show_attendance_log()
