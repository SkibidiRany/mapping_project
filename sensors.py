import numpy as np

def simulated_ultrasonic(robot_pos, robot_dir, distance=100):
    return robot_pos + robot_dir * distance

def simulated_ir(robot_pos, robot_dir):
    x, y = robot_pos
    left_edge = x < -500
    right_edge = x > 500
    return left_edge, right_edge
