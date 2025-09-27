import pygame
from constants import *

class Player:
    def __init__(self, x, y):
        self.alive = True
        self.death_time = None
        self.ball_radius = 10
        self.speed = 8
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.ball_radius)

    def handle_movement(self, joystick):
        if self.alive:
            left_x = joystick.get_axis(0)
            left_y = joystick.get_axis(1)
            
            # Apply deadzone
            deadzone = 0.15
            if abs(left_x) > deadzone:
                self.x += left_x * self.speed
            if abs(left_y) > deadzone:
                self.y += left_y * self.speed

        #set border restrictions
        if self.x - self.ball_radius < 0:
            self.x = self.ball_radius
        if self.x + self.ball_radius > WIDTH:
            self.x = WIDTH - self.ball_radius
        if self.y - self.ball_radius < 0:
            self.y = self.ball_radius
        if self.y + self.ball_radius > HEIGHT:
            self.y = HEIGHT - self.ball_radius