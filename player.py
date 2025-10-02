import pygame
from constants import *
from math import atan2, sqrt
from particle import spawn_explosion

class Player:
    def __init__(self, x, y):
        self.alive = True
        self.death_time = None
        self.radius = 10
        self.color = GREEN
        self.speed = 8
        self.x = x
        self.y = y
        self.start_health = 100
        self.health = 100
        self.level = 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def handle_movement(self, joystick):
        if self.alive:
            if joystick:
                # Controller input
                left_x = joystick.get_axis(0)
                left_y = joystick.get_axis(1)

                # Apply deadzone
                deadzone = 0.15
                if abs(left_x) > deadzone:
                    self.x += left_x * self.speed
                if abs(left_y) > deadzone:
                    self.y += left_y * self.speed
            else:
                # Keyboard input (WASD)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    self.x -= self.speed
                if keys[pygame.K_d]:
                    self.x += self.speed
                if keys[pygame.K_w]:
                    self.y -= self.speed
                if keys[pygame.K_s]:
                    self.y += self.speed

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
            # Controller input - Get right stick input
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
        else:
            # Mouse input - aim towards mouse cursor
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Calculate direction from player to mouse
            dx = mouse_x - self.x
            dy = mouse_y - self.y

            # Only aim if mouse is far enough from player (acts like deadzone)
            distance = sqrt(dx*dx + dy*dy)
            if distance > 30:  # Minimum distance threshold
                return atan2(dy, dx)

        return None
    
    def draw_health_bar(self, screen):
        if self.health != self.start_health:
            pygame.draw.rect(screen, RED, (self.x - (self.radius * 2), self.y - (self.radius * 2), (self.radius * 4), 3))
            pygame.draw.rect(screen, GREEN, (self.x - (self.radius * 2), self.y - (self.radius * 2), ((self.radius * 4) * (self.health / self.start_health)), 3))

    def level_up(self, explosions):
        self.level += 1
        self.start_health += 10
        self.health = self.start_health
        self.radius += 1
        self.speed += 0.3
        spawn_explosion(explosions, self.x, self.y, 10, self.color, 15, 50)