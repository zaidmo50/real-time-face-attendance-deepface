import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QDialog
)
from PyQt5.QtCore import Qt, QTimer
from threading import Thread


# Define the main window
class FacialAttendanceSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Facial Attendance System")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Header label
        header_label = QLabel("Facial Attendance System")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 32px; font-weight: bold;padding:50px")
        layout.addWidget(header_label)

        layout.addStretch()
        # Buttons
        register_button = QPushButton("Register New User")
        register_button.setStyleSheet("font-size: 20px; padding: 10px;")
        register_button.clicked.connect(self.register_user)
        layout.addWidget(register_button)

        mark_attendance_button = QPushButton("Mark Attendance")
        mark_attendance_button.setStyleSheet("font-size: 20px; padding: 10px;")
        mark_attendance_button.clicked.connect(self.mark_attendance)
        layout.addWidget(mark_attendance_button)

        log_button = QPushButton("Attendance Log")
        log_button.setStyleSheet("font-size: 20px; padding: 10px;")
        log_button.clicked.connect(self.show_attendance_log)
        layout.addWidget(log_button)

        layout.addStretch()
        # Finalize layout
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def register_user(self):
        self.run_script_with_dialog("System is initiating Registration for new user", 8000, ["python", "scripts/register.py"])

    def mark_attendance(self):
        self.run_script_with_dialog("Attendance Marking System is Opening. Please Wait...", 12000, ["python", "scripts/recog.py"])

    def show_attendance_log(self):
        self.run_script_with_dialog("Fetching Attendance Log...", 4000, ["python", "scripts/attendance_log.py"])

    def run_script_with_dialog(self, message, duration, script):
        dialog = ProcessingDialog(message, duration)
        dialog.show()  # Show the dialog without blocking
        Thread(target=lambda: self.run_script(script, dialog)).start()

    def run_script(self, script, dialog):
        subprocess.run(script) 
        dialog.close()  


# Define the processing dialog
class ProcessingDialog(QDialog):
    def __init__(self, message, duration):
        super().__init__()
        self.setWindowTitle("Processing Your Request")
        self.setFixedSize(700, 200)

        # Layout and message
        layout = QVBoxLayout()
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px;")
        layout.addWidget(label)
        self.setLayout(layout)

        # Auto-close the dialog after the specified duration
        QTimer.singleShot(duration, self.close)


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = FacialAttendanceSystem()
    main_window.show()
    sys.exit(app.exec_())