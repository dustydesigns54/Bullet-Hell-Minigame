import pygame, random

class Particle:
    def __init__(self, x, y, color, size, distance):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.size = float(size)
        self.vx = random.uniform(-distance, distance)
        self.vy = random.uniform(-distance, distance)
        self.lifetime = random.randint(30, 50) # Frames

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        if self.size > 0:
            self.size -= 0.1 

    def alive(self):
        return self.lifetime > 0 and self.size > 0

    def draw(self, surface):
        if self.alive():
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), max(1, int(self.size)))

def spawn_explosion(explosions, x, y, size, color, distance, count=30):
    explosions.append([Particle(x, y, color, size, distance) for _ in range(count)])
