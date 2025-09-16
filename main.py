import pygame
import numpy as np
from map import MapVisualizer
from arduino_serial import ArduinoRobot
from utils import deg_to_rad
import time

MIN_COMMAND_DURATION = 0.1  # seconds, minimal time to hold a command on Arduino

def main():
    pygame.init()
    visualizer = MapVisualizer(width=800, height=600, scale=1.0)

    robot_pos = np.array([0.0, 0.0])
    robot_dir = np.array([1.0, 0.0])

    arduino = ArduinoRobot(port="COM3")  # Change COM port
    running = True
    last_command = "stop"
    last_sent_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Determine command in real-time based on current keys
        if keys[pygame.K_w]:
            move_cmd = "forward"
        elif keys[pygame.K_s]:
            move_cmd = "back"
        elif keys[pygame.K_a]:
            move_cmd = "left"
        elif keys[pygame.K_d]:
            move_cmd = "right"
        else:
            move_cmd = "stop"

        # Send command immediately if changed or minimal duration passed
        current_time = time.time()
        if move_cmd != last_command or (current_time - last_sent_time) > MIN_COMMAND_DURATION:
            arduino.send_command(move_cmd)
            last_command = move_cmd
            last_sent_time = current_time

        # Update robot position/direction locally
        if move_cmd == "forward":
            robot_pos += robot_dir * 1.0
        elif move_cmd == "back":
            robot_pos -= robot_dir * 1.0
        elif move_cmd == "left":
            angle = deg_to_rad(-5)
            rot_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                   [np.sin(angle),  np.cos(angle)]])
            robot_dir = rot_matrix @ robot_dir
        elif move_cmd == "right":
            angle = deg_to_rad(5)
            rot_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                   [np.sin(angle),  np.cos(angle)]])
            robot_dir = rot_matrix @ robot_dir

        # Optional: read Arduino sensors
        try:
            sensors = arduino.read_sensors()
            distance = sensors.get("ultra", 50)
        except Exception:
            distance = 50

        # Update map
        point = robot_pos + robot_dir * distance
        visualizer.points.append(point)
        visualizer.update(robot_pos, robot_dir)

        pygame.time.delay(30)  # small delay to avoid overloading CPU

    arduino.close()
    pygame.quit()


if __name__ == "__main__":
    main()
