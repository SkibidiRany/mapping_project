import numpy as np
from geometry import project_point

def simulated_ultrasonic(robot, distance=100):
    """Simulate a sensor reading in front of the robot."""
    origin = robot.position
    direction = robot.get_direction()
    return project_point(origin, direction, distance)
