import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy, QFrame
from PyQt5.QtCore import Qt, QTimer
from techno_modbus_controller import TechnoModbusLiftController  # Import your Modbus controller class

class LMSdisplayApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Modbus controller instance
        self.controller = TechnoModbusLiftController()

        # Set the COM port and establish connection (replace 'COM3' with your actual COM port)
        if not self.controller.techno_set_com_port('COM2'):
            print("Failed to connect to Modbus device.")
            sys.exit(1)

        # Set the window properties
        self.setStyleSheet("background-color: #33a2ff;")
        self.setWindowTitle("Elevator Display App")
        self.resize(800, 600)

        # Company name label
        self.company_name_label = QLabel("<b>Technologics Global Private Limited</b>", self)
        self.company_name_label.setStyleSheet("font-size: 30px; font-family: 'Arial'; color: white;")

        # Arrow label to show up/down status
        self.arrow_label = QLabel("", self)  # Leave blank; set dynamically
        self.arrow_label.setStyleSheet("font-size: 200px; font-family: 'Arial'; color: white;")

        # Floor number label
        self.floor_label = QLabel("1", self)  # Default; will update dynamically
        self.floor_label.setStyleSheet("font-size: 200px; font-family: 'Arial'; color: white;")

        # Door Status Label
        self.door_status_label = QLabel("⬜", self)  # Default text
        self.door_status_label.setStyleSheet("font-size: 100px; font-family: 'Arial'; color: white;")

        # Borders for design
        self.top_border = QFrame(self)
        self.top_border.setFrameShape(QFrame.HLine)
        self.top_border.setFrameShadow(QFrame.Sunken)
        self.top_border.setLineWidth(15)
        self.bottom_border = QFrame(self)
        self.bottom_border.setFrameShape(QFrame.HLine)
        self.bottom_border.setFrameShadow(QFrame.Sunken)
        self.bottom_border.setLineWidth(10)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.company_name_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.top_border, alignment=Qt.AlignCenter)
        layout.addItem(QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.arrow_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.floor_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.door_status_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.bottom_border, alignment=Qt.AlignBottom)
        self.setLayout(layout)

        # Timer to update the display with real-time data
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(1000)  # Update every 1 second
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start()

        # Blink timer for arrow
        self.blink_timer = QTimer(self)
        self.blink_timer.setInterval(500)  # Blink every 500 ms
        self.blink_timer.timeout.connect(self.toggle_arrow_visibility)
        self.blink_timer.start()

        self.show()

    def toggle_arrow_visibility(self):
        """Toggle visibility of the arrow for blinking effect."""
        if self.arrow_label.isVisible():
            self.arrow_label.hide()
        else:
            self.arrow_label.show()

    def update_display(self):
        """Fetch real-time data and update the display."""
        # Update floor number
        floor_number = self.controller.techno_get_floor_number()
        if floor_number != -1:  # Ensure valid response
            self.floor_label.setText(str(floor_number))

        # Update movement direction arrow
        movement_status = self.controller.techno_get_movement_status()
        if movement_status == "up":
            self.arrow_label.setText("⮝")
        elif movement_status == "down":
            self.arrow_label.setText("⮟")
        else:
            self.arrow_label.setText("")  # Clear arrow if stationary
            
        # Fetch door status
        door_status = self.controller.techno_get_door_status()
        if door_status == "open":
            self.door_status_label.setText("⬜")
            self.door_status_label.setStyleSheet("font-size: 100px; font-family: 'Arial'; color: white; ")
        elif door_status == "closed":
            self.door_status_label.setText("")
        else:
            self.door_status_label.setText("")
            
            
        # Check additional lift details if needed
        faults = self.controller.techno_read_faults()
        board_status = self.controller.techno_get_board_status()
        
        # Optionally, log or display these details somewhere in the UI
        print(f"Door status: {door_status}, Faults: {faults}, Board online: {board_status}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LMSdisplayApp()
    sys.exit(app.exec_())
