import pygame, random
from dataclasses import dataclass, field
from typing import Callable, Optional
from constants import *
from math import sqrt, cos, sin, pi

def _make_circle_mask(radius):
    size = radius * 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 255, 255), (radius, radius), radius)
    return pygame.mask.from_surface(surf)

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
    boss_round: Optional[int] = field(default=None)
    ability_fn: Optional[Callable] = field(default=None)
    ability_interval: int = field(default=25)

def _boss_spawner_ability(host, enemies, player_level):
    count = 7
    for i in range(count):
        angle = (2 * pi / count) * i
        sx = host.x + cos(angle) * (host.radius + 25)
        sy = host.y + sin(angle) * (host.radius + 25)
        mini = Enemy(sx, sy, player_level, forced_type="mini")
        mini.score_value = 0
        enemies.append(mini)

def _boss_tank_spawner_ability(host, enemies, player_level):
    count = 3
    for i in range(count):
        angle = (2 * pi / count) * i
        sx = host.x + cos(angle) * (host.radius + 60)
        sy = host.y + sin(angle) * (host.radius + 60)
        mini_boss = Enemy(sx, sy, player_level, forced_type="mini_boss")
        mini_boss.score_value = 0
        enemies.append(mini_boss)

# To add a new enemy type, append one entry here — nothing else changes.
# To add a new boss, set boss_round to the target round and define an ability_fn above.
ENEMY_TYPES: list[EnemyType] = [
    EnemyType("standard",  RED,    15, 10,   50, 2.5,  200, lambda lvl: lvl * 3),
    EnemyType("mini",      ORANGE, 10,  5,   25, 7.5,  250, lambda lvl: max(0, (lvl - 2) * 2)),
    EnemyType("tank",      PURPLE, 20, 20,  300, 1.5,  450, lambda lvl: max(0, (lvl - 5) * 3)),
    EnemyType("mini_boss", WHITE,  32, 85, 1350, 0.4, 3000, lambda lvl: max(0, (lvl - 10))),

    # Bosses — weight_fn always 0; spawned exclusively via boss_round logic
    EnemyType("boss_spawner", GREY, 50, 150, 25000, 4.5, 0, lambda lvl: 0, boss_round=10, ability_fn=_boss_spawner_ability, ability_interval=25),
    EnemyType("boss_tank_spawner", PURPLE, 20, 300, 40000, 3.5, 0, lambda lvl: 0, boss_round=20, ability_fn=_boss_tank_spawner_ability, ability_interval=180),
]

BOSS_ROUNDS: dict[int, EnemyType] = {
    t.boss_round: t for t in ENEMY_TYPES if t.boss_round is not None
}

class Enemy:
    def __init__(self, x, y, player_level, forced_type: Optional[str] = None):
        self.x = x
        self.y = y

        if forced_type is not None:
            chosen = next(t for t in ENEMY_TYPES if t.name == forced_type)
        else:
            chosen = random.choices(
                ENEMY_TYPES,
                weights=[t.weight_fn(player_level) for t in ENEMY_TYPES],
                k=1,
            )[0]

        self.type_name = chosen.name
        self.color = chosen.color
        self.radius = chosen.radius
        self.dmg = chosen.dmg
        self.start_health = chosen.health
        self.health = chosen.health
        self.speed = chosen.speed
        self.score_value = chosen.score_value
        self.ability_fn = chosen.ability_fn
        self.ability_interval = chosen.ability_interval
        self.ability_timer = 0
        self.contact_cooldown = 0
        self._mask = _make_circle_mask(self.radius)

    @property
    def rect(self):
        r = self.radius
        return pygame.Rect(int(self.x) - r, int(self.y) - r, r * 2, r * 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self, player, dt):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = sqrt(dx*dx + dy*dy)

        if distance > 0:
            scale = self.speed * dt * 60
            self.x += (dx / distance) * scale
            self.y += (dy / distance) * scale

    def check_collision_with_player(self, player):
        if player._mask is None:
            return sqrt((self.x - player.x)**2 + (self.y - player.y)**2) < self.radius + player.radius
        offset = (self.rect.x - player._rect.x, self.rect.y - player._rect.y)
        return player._mask.overlap(self._mask, offset) is not None

    def check_collision_with_bullet(self, bullet):
        offset = (bullet.rect.x - self.rect.x, bullet.rect.y - self.rect.y)
        return self._mask.overlap(bullet._mask, offset) is not None

    def draw_health_bar(self, screen):
        if self.health != self.start_health:
            pygame.draw.rect(screen, RED,   (self.x - (self.radius * 2), self.y - (self.radius * 2), (self.radius * 4), 3))
            pygame.draw.rect(screen, GREEN, (self.x - (self.radius * 2), self.y - (self.radius * 2), ((self.radius * 4) * (self.health / self.start_health)), 3))
