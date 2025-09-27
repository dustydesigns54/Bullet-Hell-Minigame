import pygame
from constants import *
from math import cos, sin

class Bullet:
    def __init__(self, player, angle):
        self.x = player.x
        self.y = player.y
        self.color = YELLOW
        self.speed = 20
        self.radius = 5
        self.angle = angle
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def update(self):
        self.x += cos(self.angle) * self.speed
        self.y += sin(self.angle) * self.speed