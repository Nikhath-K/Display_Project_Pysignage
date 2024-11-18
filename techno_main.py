import sys
import random  # Simulating real-time data
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
from techno_modbus_controller import TechnoModbusLiftController  # Import your Modbus controller class
from PyQt5.QtGui import QTransform


class LMSdisplayApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Modbus controller instance
        self.controller = TechnoModbusLiftController()

        # Set the COM port and establish connection (replace 'COM3' with your actual COM port)
        if not self.controller.techno_set_com_port('COM4'):
            print("Failed to connect to Modbus device.")
            sys.exit(1)

        # Set the window properties
        self.setStyleSheet("background-color: #33a2ff;")
        self.setWindowTitle("Elevator Display App")
        # Get screen size
        screen = QApplication.primaryScreen()  # Get the primary screen
        screen_geometry = screen.geometry()  # Get the geometry of the screen
        screen_width = screen_geometry.width()  # Width of the screen
        screen_height = screen_geometry.height()  # Height of the screen
        # Resize the window to take up 30% of the screen's width and height
        self.resize(int(screen_width * 0.3), int(screen_height * 0.3))

        # Company name label
        self.company_name_label = QLabel("<b>Technologics Global Private Limited</b>", self)
        # Set the font for the company name
        self.company_name_label.setStyleSheet("font-size: 30px; font-family: 'Arial'; color: white;")


        # Door Status Label
        self.door_status_label = QLabel(self)  # Default text
        self.door_status_label.setStyleSheet("background-color: white; border: none;")
        self.door_status_label.setFixedSize(50, 50)  # Width: 50px, Height: 50px
        self.door_status_label.move(175, 400)  # Position the door status label (adjust coordinates)
        
        
        
        # Create a QLabel to display the arrow (GIF)
        self.arrow_label = QLabel(self)
        
        # Load the up arrow GIF and set it as the current movie
        self.up_arrow_movie = QMovie("up_arrow.gif")  # Load your up arrow GIF file
        self.down_arrow_movie = QMovie("down_arrow.gif")  
        self.arrow_label.setMovie(self.up_arrow_movie)
        self.arrow_label.setStyleSheet("border: 3px solid white;")  # Add a white border
        self.arrow_label.setFixedSize(350, 450)  # Width: 150px, Height: 150px
        self.arrow_label.setAlignment(Qt.AlignCenter)  # Center the arrow
        self.arrow_label.move(100, 50)  # Position the arrow (adjust coordinates)

        
        
        # Create a QLabel to display the floor number
        self.floor_label = QLabel("0", self)  # Default; will update dynamically
        # Set the font for the floor number
        self.floor_label.setStyleSheet("font-size: 300px; font-family: 'Nothing Font (5x7)'; color: white; border: 3px solid white; ")
        self.floor_label.setFixedSize(350, 350)  # Width: 200px, Height: 150px
        self.floor_label.move(100, 220)  # Position the floor label (adjust coordinates)
        
        
        # Create a frame for the border below the company name
        self.top_border = QFrame(self)
        self.top_border.setFrameShape(QFrame.HLine)
        self.top_border.setFrameShadow(QFrame.Sunken)
        self.top_border.setLineWidth(15) # Set the thickness of the border line
        
        # Create a frame for the border below the arrow
        self.bottom_border = QFrame(self)
        self.bottom_border.setFrameShape(QFrame.HLine)
        self.bottom_border.setFrameShadow(QFrame.Sunken)
        self.bottom_border.setLineWidth(10) # Set the thickness of the border line

        # Layout setup
        # Create a layout to position the company name, top border, arrow, floor, and bottom border
        layout = QVBoxLayout()
        
        # Add the company name label to the layout
        layout.addWidget(self.company_name_label, alignment=Qt.AlignCenter)
        
        # Add the top border line below the company name
        layout.addWidget(self.top_border, alignment=Qt.AlignCenter)
        
        # Add a spacer to keep the arrow at the top and avoid affecting the floor label
        layout.addItem(QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Add the door status label below the arrow
        layout.addWidget(self.door_status_label, alignment=Qt.AlignCenter)
        
        # Add the arrow label to the layout
        layout.addWidget(self.arrow_label, alignment=Qt.AlignCenter)
        
        # Add the floor number label below the arrow
        layout.addWidget(self.floor_label, alignment=Qt.AlignCenter)
        
        
        # Add the bottom border line
        layout.addWidget(self.bottom_border, alignment=Qt.AlignBottom)
        
        # Set the layout for the window
        self.setLayout(layout)

        # Initialize the floor number, arrow visibility, and direction state
        self.floor_number = 0
        self.movement_status = True  # Arrow starts by pointing up 
        self.current_movement_status = None

        # Set up a QTimer to make the arrow change and update the floor number
        self.animation_timer = QTimer(self)
        self.animation_timer.setInterval(1000)  # Update every 1000 milliseconds
        self.animation_timer.timeout.connect(self.update_display)
        self.animation_timer.start()  # Start the animation timer

        self.show()

    def update_display(self):
        """Fetch real-time data and update the display."""
        
        # Update floor number
        self.floor_number = self.controller.techno_get_floor_number()
        if self.floor_number != -1:  # Ensure valid response
            self.floor_label.setText(str(self.floor_number))

        # Update movement direction arrow
        self.movement_status = self.controller.techno_get_movement_status()
        # self.movement_status = "down"
        
        # movement_status = random.choice(['up', 'down', 'stationary'])  # Simulate movement status
        # if movement_status != self.current_movement_status:
        #     self.current_movement_status = movement_status

        if self.movement_status == "up":
            self.arrow_label.setMovie(self.up_arrow_movie)  # Reset rotation for "up"
            # Start the movie to show the animation
            self.arrow_label.movie().start()
        elif self.movement_status == "down":
            self.arrow_label.setMovie(self.down_arrow_movie)  # Reset rotation for "down"
            # Start the movie to show the animation
            self.arrow_label.movie().start()
        else:
            self.arrow_label.clear()
            
        
            
        # Fetch door status
        door_status = self.controller.techno_get_door_status()
        if door_status == "open":
            self.door_status_label.setText("")  # Clear any text
            self.door_status_label.setFixedSize(50, 50)  # Set a fixed size for the label (square)
            self.door_status_label.setStyleSheet("background-color: white; border: none;")  # Display a white box
        elif door_status == "closed":
            self.door_status_label.clear()  # Clear both text and styles
            self.door_status_label.setFixedSize(0, 0)  # Hide the label completely
        else:
            self.door_status_label.clear()  # Clear both text and styles
            self.door_status_label.setFixedSize(0, 0)  # Hide the label completely

    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LMSdisplayApp()
    # window.show()
    sys.exit(app.exec_())
