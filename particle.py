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

    def update(self, width, height, dt):
        scale = dt * 60
        self.x += self.vx * scale
        self.y += self.vy * scale
        self.lifetime -= scale
        if self.size > 0:
            self.size -= 0.1 * scale

        if self.x - self.size < 0:
            self.x = self.size
            self.vx = abs(self.vx)
        elif self.x + self.size > width:
            self.x = width - self.size
            self.vx = -abs(self.vx)

        if self.y - self.size < 0:
            self.y = self.size
            self.vy = abs(self.vy)
        elif self.y + self.size > height:
            self.y = height - self.size
            self.vy = -abs(self.vy)

    def alive(self):
        return self.lifetime > 0 and self.size > 0

    def draw(self, surface):
        if self.alive():
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), max(1, int(self.size)))

def spawn_explosion(explosions, x, y, size, color, distance, count=30):
    explosions.append([Particle(x, y, color, size, distance) for _ in range(count)])
