import numpy as np
from geometry import rotate

class RobotState:
    def __init__(self, x=0, y=0, theta=0):
        self.position = np.array([x, y], dtype=float)  # (x, y)
        self.theta = theta  # orientation in radians

    def move_forward(self, step=5):
        dx = np.cos(self.theta) * step
        dy = np.sin(self.theta) * step
        self.position += np.array([dx, dy])

    def rotate(self, angle_rad):
        self.theta += angle_rad

    def get_direction(self):
        return np.array([np.cos(self.theta), np.sin(self.theta)])
