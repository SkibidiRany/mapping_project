import serial
import time

class ArduinoRobot:
    def __init__(self, port="COM3", baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # wait for Arduino to reset

    def send_command(self, cmd):
        """Send movement command to Arduino"""
        if self.ser:
            self.ser.write((cmd + "\n").encode())

    def get_distance_cm(self):
        """Request ultrasonic reading from Arduino"""
        self.send_command("distance")  # Arduino should handle this
        line = self.ser.readline().decode().strip()
        try:
            return float(line)
        except:
            return 0.0

    def read_sensors(self):
        """Requests sensor readings from Arduino."""
        self.send_command("read_sensors")
        try:
            # read a line, ignore undecodable bytes
            line = self.ser.readline()
            line = line.decode(errors="ignore").strip()
        except Exception:
            return {"ultra": 0, "ir1": 0, "ir2": 0}

        if not line:
            return {"ultra": 0, "ir1": 0, "ir2": 0}

        parts = line.split(",")
        if len(parts) != 3:
            return {"ultra": 0, "ir1": 0, "ir2": 0}

        try:
            return {
                "ultra": float(parts[0]),
                "ir1": int(parts[1]),
                "ir2": int(parts[2])
            }
        except ValueError:
            return {"ultra": 0, "ir1": 0, "ir2": 0}

    def close(self):
        if self.ser:
            self.ser.close()
