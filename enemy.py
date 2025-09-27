import pygame
from constants import *
from math import sqrt

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = RED
        self.radius = 15
        self.score_value = 100
        self.health = 50
        self.speed = 2.5
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = sqrt(dx*dx + dy*dy)

        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def check_collision_with_player(self, player):
        distance = sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        return distance < self.radius + player.radius 
    
    def check_collision_with_bullet(self, bullet):
        distance = sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)
        return distance < self.radius + bullet.radius