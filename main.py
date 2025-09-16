import pygame
from robot import RobotState
from map import MapVisualizer
from sensors import simulated_ultrasonic
from utils import deg_to_rad

def main():
    running = True
    robot = RobotState(0, 0, 0)
    visualizer = MapVisualizer()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            robot.move_forward(5)
        if keys[pygame.K_a]:
            robot.rotate(deg_to_rad(-5))
        if keys[pygame.K_d]:
            robot.rotate(deg_to_rad(5))
        if keys[pygame.K_SPACE]:
            point = simulated_ultrasonic(robot, 120)
            visualizer.points.append(point)

        visualizer.update(robot)

    pygame.quit()

if __name__ == "__main__":
    main()
