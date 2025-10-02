import pygame, random
from constants import *
from math import sqrt

class Enemy:
    def __init__(self, x, y, player_level):
        self.x = x
        self.y = y
        self.color = RED
        self.radius = 15
        self.score_value = 200
        self.dmg = 10
        self.start_health = 50
        self.health = 50
        self.speed = 2.5

        def make_mini(self):
            self.color = ORANGE
            self.radius = 10
            self.score_value = 250
            self.dmg = 5
            self.start_health = 25
            self.health = 25
            self.speed = 7.5
        
        def make_tank(self):
            self.color = PURPLE
            self.radius = 20
            self.score_value = 300
            self.dmg = 20
            self.start_health = 300
            self.health = 300
            self.speed = 1.5

        def make_mini_boss(self):
            self.color = WHITE
            self.radius = 30
            self.score_value = 1500
            self.dmg = 75
            self.start_health = 1200
            self. health = 1200
            self.speed = 0.33

        if player_level == 3 or player_level == 4:
            if random.randint(0, 3) == 0:
                make_mini(self)
        elif player_level == 5 or player_level == 6 or player_level == 7:
            if random.randint(0, 5) == 0:
                make_mini(self)
            elif random.randint(0, 4) == 0:
                make_tank(self)
        elif player_level >= 8:
            if random.randint(0, 100) == 0:
                make_mini_boss(self)
            elif random.randint(0, 4) == 0:
                make_mini(self)
            elif random.randint(0, 3) == 0:
                make_tank(self)

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
            pygame.draw.rect(screen, RED, (self.x - (self.radius * 2), self.y - (self.radius * 2), (self.radius * 4), 3))
            pygame.draw.rect(screen, GREEN, (self.x - (self.radius * 2), self.y - (self.radius * 2), ((self.radius * 4) * (self.health / self.start_health)), 3))