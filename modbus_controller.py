from pymodbus.client.sync import ModbusSerialClient
from typing import Optional, List

class ModbusLiftController:
    def __init__(self):
        self.client = None
        self.com_port = None
        self.floor_count = 23

    # 1. Sets the RS485 USB COM port
    def techno_set_com_port(self, port: str) -> bool:
        self.client = ModbusSerialClient(method="rtu", port=port, baudrate=9600, timeout=1)
        if self.client.connect():
            self.com_port = port
            return True
        return False

    # 2. Retrieves the current RS485 USB COM port
    def techno_get_com_port(self) -> Optional[str]:
        return self.com_port

    # 3. Checks if the board is online
    def techno_get_board_status(self) -> bool:
        if not self.client or not self.client.connect():
            return False
        try:
            response = self.client.read_coils(0, 1, unit=1)  # Example coil address
            return response.isError() is False
        finally:
            self.client.close()

    # 4. Retrieves the current floor number
    def techno_get_floor_number(self) -> int:
        if not self.client or not self.client.connect():
            return -1
        try:
            response = self.client.read_holding_registers(0x00021, 1, unit=1)  # Example register for floor number
            return response.registers[0] if response.isError() is False else -1
        finally:
            self.client.close()
 
    # 5. Stores the lift's maximum floor count
    def techno_set_floor_count(self, floor_count: int) -> bool:
        self.floor_count = floor_count
        # You may choose to store this in a register for the device if necessary
        return True

    # 6. Indicates whether the door is open
    def techno_get_door_status(self) -> str:
        if not self.client or not self.client.connect():
            return "unknown"  # Return an "unknown" status if not connected

        try:
            # Read the registers at address 0x00018 and 0x00019
            response = self.client.read_holding_registers(address=0x00017, count=2, unit=1)

            # Check if there's an error
            if response.isError():
                return "unknown"

            # Assuming register 0x00018 is for "door open" status and 0x00019 for "door close" status
            door_open = response.registers[0]  # Value at address 0x00018
            door_close = response.registers[1]  # Value at address 0x00019

            # Interpret the values
            if door_open == 1 and door_close == 0:
                return "open"
            elif door_open == 0 and door_close == 1:
                return "closed"
            elif door_open == 0 and door_close == 0:
                return "unknown"  # Both registers indicate neither open nor close
            else:
                return "error"  # Invalid state or conflicting values

        finally:
            self.client.close()


    # 7. Shows if the lift is moving up, down, or stationary
    def techno_get_movement_status(self) -> str:
        if not self.client or not self.client.connect():
            return "unknown"  # Return an "unknown" status if not connected

        try:
            # Read the registers at addresses 0x00019 and 0x00020 for "up" and "down" movement status
            response = self.client.read_holding_registers(address=0x00019, count=2, unit=1)

            # Check if there's an error
            if response.isError():
                return "unknown"

            # Assuming register 0x00019 is for "up" status and 0x00020 for "down" status
            up_status = response.registers[0]   # Value at address 0x00019
            down_status = response.registers[1] # Value at address 0x00020

            # Interpret the values
            if up_status == 1 and down_status == 0:
                return "up"
            elif up_status == 0 and down_status == 1:
                return "down"
            elif up_status == 0 and down_status == 0:
                return "stationary"  # Lift is stationary if both are 0
            else:
                return "error"  # Invalid state or conflicting values

        finally:
            self.client.close()

    # 8. Provides an array of any detected faults
    def techno_read_faults(self) -> List[tuple[str, int]]:
        if not self.client or not self.client.connect():
            return []

        # Define the fault labels with their corresponding addresses
        fault_labels = [
            'MIMO', 'FAULT(ALARM MESSAGE)', 'FM RETURN', 'FM EMERGENCY',
            'FIREMAN OPERATION', 'MAINTENANCE', 'OVERLOAD', 'INDEPENDENT',
            'ATTENDANT', 'MANUAL', 'STOP/RUN'
        ]

        try:
            # Read registers from address 0x00006 to 0x00016 (17 registers)
            response = self.client.read_holding_registers(address=0x00006, count=17, unit=1)

            # Check if there was an error in the response
            if response.isError():
                return []

            # Map each register value to its corresponding fault label
            faults = [(fault_labels[i], response.registers[i]) for i in range(len(fault_labels))]

            return faults

        finally:
            self.client.close()

    # 9. Returns an array containing all lift details
    def techno_get_lift_details(self) -> dict:
        return {
            "com_port": self.techno_get_com_port(),
            "board_status": self.techno_get_board_status(),
            "floor_number": self.techno_get_floor_number(),
            "floor_count": self.floor_count,
            "door_status": self.techno_get_door_status(),
            "movement_status": self.techno_get_movement_status(),
            "faults": self.techno_read_faults(),
        }
