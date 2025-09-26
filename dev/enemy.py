import pygame
import math
import random
from constants import *

class Enemy:
    def __init__(self, x, y, boss = False):
        self.x = x
        self.y = y
        self.radius = 12

        # Randomly select enemy type
        self.enemy_type = random.choice(['basic', 'fast', 'tank', 'mini'])
        if (boss):
            self.enemy_type = "boss"

         # Set properties based on enemy type
        if self.enemy_type == 'basic':
            self.color = RED
            self.speed = 2
            self.health = 50
            self.radius = 12
            self.points = 10
        elif self.enemy_type == 'fast':
            self.color = ORANGE
            self.speed = 4
            self.health = 25
            self.radius = 10
            self.points = 15
        elif self.enemy_type == 'tank':
            self.color = PURPLE
            self.speed = 1
            self.health = 100
            self.radius = 18
            self.points = 25
        elif self.enemy_type == 'mini':
            self.color = CYAN
            self.speed = 3.5
            self.health = 15
            self.radius = 8
            self.points = 8
        elif self.enemy_type == 'boss':
            self.color = GREEN
            self.speed = 1
            self.health = 1500
            self.radius = 40
            self.points = 250

        self.max_health = self.health
        self._prev_health = self.health
        self._last_damage_time = None
        self._health_bar_visible = False

    def update(self, player):
        # Move toward player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)

        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def check_collision_with_bullet(self, bullet):
        distance = math.sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)
        return distance < self.radius + bullet.radius

    def check_collision_with_player(self, player):
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        return distance < self.radius + player.radius 

    def draw_health(self, screen):
        current_time = pygame.time.get_ticks()

        if self.health < self._prev_health:
            self._last_damage_time = current_time
            self._health_bar_visible = True

        self._prev_health = self.health

        if not self._health_bar_visible or self._last_damage_time is None:
            return

        elapsed = current_time - self._last_damage_time
        if elapsed >= 2000:
            self._health_bar_visible = False
            return

        fade_ratio = 1 - (elapsed / 2000)
        alpha = max(0, min(255, int(255 * fade_ratio)))

        if alpha <= 0:
            self._health_bar_visible = False
            return

        bar_width = self.radius * 2
        bar_height = 4
        bar_x = int(self.x - bar_width / 2)
        bar_y = int(self.y - self.radius - 8)

        if self.max_health > 0:
            health_ratio = max(self.health, 0) / self.max_health
        else:
            health_ratio = 0
        health_width = int(bar_width * health_ratio)

        bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        pygame.draw.rect(bar_surface, (60, 60, 60, alpha), bar_surface.get_rect())

        if health_width > 0:
            health_rect = pygame.Rect(0, 0, health_width, bar_height)
            pygame.draw.rect(bar_surface, (0, 255, 0, alpha), health_rect)

        pygame.draw.rect(bar_surface, (0, 0, 0, alpha), bar_surface.get_rect(), 1)
        screen.blit(bar_surface, (bar_x, bar_y))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        self.draw_health(screen)
