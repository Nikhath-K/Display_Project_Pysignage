# Import the ModbusLiftController class
from modbus_controller import ModbusLiftController

# Step 1: Initialize the lift controller object
lift_controller = ModbusLiftController()

# Step 2: Set the COM port
com_port = "COM2"
connection_success = lift_controller.techno_set_com_port(com_port)

if connection_success:
    print(f"Connected successfully to {com_port}")
else:
    print(f"Failed to connect to {com_port}")
    # If connection fails, you may stop here or retry with a different COM port

# Step 3: Check if the board is online
if lift_controller.techno_get_board_status():
    print("Lift control board is online.")
else:
    print("Lift control board is offline or not responding.")
    # If the board is offline, you may need to troubleshoot the connection


# Get current floor number
current_floor = lift_controller.techno_get_floor_number()
print(f"Current Floor: {current_floor}")

# Get door status
door_status = lift_controller.techno_get_door_status()
print(f"Door Open: {door_status}")

# Get movement status
movement_status = lift_controller.techno_get_movement_status()
print(f"Lift Movement: {movement_status}")

# Get any faults
faults = lift_controller.techno_read_faults()
print("Detected Faults: ", end='')
for label, value in faults:
    print(f"{value}", end=' ')
print()


# Get all lift details at once
lift_details = lift_controller.techno_get_lift_details()
print("Lift Details:", lift_details)
