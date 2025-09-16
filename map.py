import pygame
import numpy as np

WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)

class MapVisualizer:
    def __init__(self, width=800, height=600, scale=1):
        pygame.init()
        self.width, self.height, self.scale = width, height, scale
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("2D Robot Mapping")
        self.clock = pygame.time.Clock()
        self.points = []

    def world_to_screen(self, pos, robot_pos):
        offset = pos - robot_pos
        x = int(self.width // 2 + offset[0] * self.scale)
        y = int(self.height // 2 - offset[1] * self.scale)
        return (x, y)

    def draw_robot(self, robot_pos, robot_dir):
        pos = self.world_to_screen(robot_pos, robot_pos)
        tip = self.world_to_screen(robot_pos + robot_dir * 20, robot_pos)
        pygame.draw.circle(self.screen, BLUE, pos, 8)
        pygame.draw.line(self.screen, GREEN, pos, tip, 2)

    def draw_points(self, robot_pos):
        for p in self.points:
            screen_pos = self.world_to_screen(p, robot_pos)
            pygame.draw.circle(self.screen, RED, screen_pos, 3)

    def update(self, robot_pos, robot_dir):
        self.screen.fill(WHITE)
        self.draw_points(robot_pos)
        self.draw_robot(robot_pos, robot_dir)
        pygame.display.flip()
        self.clock.tick(30)
