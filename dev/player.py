import pygame
import math
from constants import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = PLAYER_RADIUS
        self.speed = PLAYER_SPEED
        self.color = BLUE
        self.health = 100
        self.max_health = 100
        self.level = 1
        self._right_trigger_pressed = False
        
    def update(self, joystick):
        # Movement with left stick
        if joystick:
            # Get left stick input (axis 0 = X, axis 1 = Y)
            left_x = joystick.get_axis(0)
            left_y = joystick.get_axis(1)
            
            # Apply deadzone
            deadzone = 0.15
            if abs(left_x) > deadzone:
                self.x += left_x * self.speed
            if abs(left_y) > deadzone:
                self.y += left_y * self.speed
                
        # Keep player on screen
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))

    def get_aim_direction(self, joystick):
        """Get aiming direction from right stick"""
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
                return math.atan2(right_y, right_x)
        return None
    
    def draw(self, screen):
        # Draw player
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw health bar
        bar_width = 40
        bar_height = 2
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.radius - 15
        
        # Background
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # Health
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
