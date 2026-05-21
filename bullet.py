import pygame
from constants import *
from math import cos, sin

def _make_circle_mask(radius):
    size = radius * 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 255, 255), (radius, radius), radius)
    return pygame.mask.from_surface(surf)

class Bullet:
    def __init__(self, player, angle, speed):
        self.x = player.x
        self.y = player.y
        self.color = YELLOW
        self.speed = speed
        self.radius = 5
        self.angle = angle
        self._mask = _make_circle_mask(self.radius)

    @property
    def rect(self):
        r = self.radius
        return pygame.Rect(int(self.x) - r, int(self.y) - r, r * 2, r * 2)
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def update(self):
        self.x += cos(self.angle) * self.speed
        self.y += sin(self.angle) * self.speed