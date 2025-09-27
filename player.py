import pygame
from constants import *
from math import atan2

class Player:
    def __init__(self, x, y):
        self.alive = True
        self.death_time = None
        self.radius = 10
        self.speed = 8
        self.x = x
        self.y = y
        self.health = 100
        self.level = 1

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.radius)

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
        if self.x - self.radius < 0:
            self.x = self.radius
        if self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
        if self.y - self.radius < 0:
            self.y = self.radius
        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
    
    def get_aim_direction(self, joystick):
        if joystick:
            # Get right stick input (axis 2 = X, axis 3 = Y on most Xbox controllers)
            # Note: Some controllers may use different axis numbers
            try:
                right_x = joystick.get_axis(2)  # Right stick X
                right_y = joystick.get_axis(3)  # Right stick Y
            except:
                # Fallback for controllers with different axis mapping
                right_x = joystick.get_axis(4) if joystick.get_numaxes() > 4 else 0
                right_y = joystick.get_axis(5) if joystick.get_numaxes() > 5 else 0
            
            # Apply deadzone
            deadzone = 0.3
            if abs(right_x) > deadzone or abs(right_y) > deadzone:
                return atan2(right_y, right_x)
        return None