import pygame, random
from dataclasses import dataclass
from typing import Callable
from constants import *
from math import sqrt

@dataclass
class EnemyType:
    name: str
    color: tuple
    radius: int
    dmg: int
    health: int
    speed: float
    score_value: int
    weight_fn: Callable[[int], float]

# To add a new enemy type, append one entry here — nothing else changes.
ENEMY_TYPES: list[EnemyType] = [
    EnemyType("standard",  RED,    15, 10,   50, 2.5,  200, lambda lvl: lvl * 3),
    EnemyType("mini",      ORANGE, 10,  5,   25, 7.5,  250, lambda lvl: max(0, (lvl - 2) * 2)),
    EnemyType("tank",      PURPLE, 20, 20,  300, 1.5,  300, lambda lvl: max(0, (lvl - 5) * 3)),
    EnemyType("mini_boss", WHITE,  32, 85, 1350, 0.4, 1500, lambda lvl: max(0, (lvl - 10))),
]

class Enemy:
    def __init__(self, x, y, player_level):
        self.x = x
        self.y = y

        chosen = random.choices(
            ENEMY_TYPES,
            weights=[t.weight_fn(player_level) for t in ENEMY_TYPES],
            k=1,
        )[0]

        self.color = chosen.color
        self.radius = chosen.radius
        self.dmg = chosen.dmg
        self.start_health = chosen.health
        self.health = chosen.health
        self.speed = chosen.speed
        self.score_value = chosen.score_value

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

    def draw_health_bar(self, screen):
        if self.health != self.start_health:
            pygame.draw.rect(screen, RED,   (self.x - (self.radius * 2), self.y - (self.radius * 2), (self.radius * 4), 3))
            pygame.draw.rect(screen, GREEN, (self.x - (self.radius * 2), self.y - (self.radius * 2), ((self.radius * 4) * (self.health / self.start_health)), 3))
