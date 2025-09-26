import pygame
import math
import random
from constants import *

class Particle:
    def __init__(self, x, y, velocity_x, velocity_y, color, size=3, lifetime=30):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        self.size = size
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        self.gravity = 0.1
        self.fade = True
        
    def update(self):
        """Update particle position and lifetime"""
        # Move particle
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Apply gravity and friction
        self.velocity_y += self.gravity
        self.velocity_x *= 0.98  # Air resistance
        self.velocity_y *= 0.98
        
        # Decrease lifetime
        self.lifetime -= 1
        
    def is_alive(self):
        """Check if particle is still alive"""
        return self.lifetime > 0
        
    def draw(self, screen):
        """Draw the particle with fading effect"""
        if self.is_alive():
            # Calculate alpha for fading effect
            if self.fade:
                alpha = int(255 * (self.lifetime / self.max_lifetime))
                # Create a surface for alpha blending
                particle_surface = pygame.Surface((self.size * 2, self.size * 2))
                particle_surface.set_alpha(alpha)
                particle_surface.fill(self.color)
                screen.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))
            else:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def create_explosion(self, x, y, color, particle_count=15, intensity=1.0):
        """Create an explosion effect at given position"""
        for _ in range(particle_count):
            # Random direction
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8) * intensity
            
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            # Vary particle properties
            size = random.randint(2, 5)
            lifetime = random.randint(20, 40)
            
            # Create color variations
            particle_color = self._vary_color(color)
            
            particle = Particle(x, y, velocity_x, velocity_y, particle_color, size, lifetime)
            self.particles.append(particle)
    
    def create_enemy_death_effect(self, enemy):
        """Create specific death effect based on enemy type"""
        if enemy.enemy_type == 'tank':
            # Big explosion for tank
            self.create_explosion(enemy.x, enemy.y, enemy.color, particle_count=25, intensity=1.5)
            # Add some sparks
            self._create_sparks(enemy.x, enemy.y, YELLOW, 10)
        elif enemy.enemy_type == 'fast':
            # Quick burst for fast enemy
            self.create_explosion(enemy.x, enemy.y, enemy.color, particle_count=12, intensity=2.0)
        elif enemy.enemy_type == 'boss':
            # Huge explosion
            self.create_explosion(enemy.x, enemy.y, enemy.color, particle_count=120, intensity=4.0)
        elif enemy.enemy_type == 'mini':
            # Small pop for mini enemy
            self.create_explosion(enemy.x, enemy.y, enemy.color, particle_count=8, intensity=0.8)
        else:  # basic
            # Standard explosion
            self.create_explosion(enemy.x, enemy.y, enemy.color, particle_count=15, intensity=1.0)
    
    def _create_sparks(self, x, y, color, count):
        """Create spark-like particles"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 10)
            
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            particle = Particle(x, y, velocity_x, velocity_y, color, size=2, lifetime=20)
            particle.gravity = 0.05  # Less gravity for sparks
            self.particles.append(particle)
    
    def _vary_color(self, base_color):
        """Create color variations for more interesting effects"""
        r, g, b = base_color
        
        # Add some randomness to each channel
        r = max(0, min(255, r + random.randint(-30, 30)))
        g = max(0, min(255, g + random.randint(-30, 30)))
        b = max(0, min(255, b + random.randint(-30, 30)))
        
        return (r, g, b)
    
    def create_muzzle_flash(self, x, y, angle):
        """Create muzzle flash effect when shooting"""
        # Create a few particles in the shooting direction
        for i in range(3):
            # Slight angle variation
            flash_angle = angle + random.uniform(-0.3, 0.3)
            speed = random.uniform(3, 6)
            
            velocity_x = math.cos(flash_angle) * speed
            velocity_y = math.sin(flash_angle) * speed
            
            # Use yellow/orange colors for muzzle flash
            flash_colors = [YELLOW, ORANGE, WHITE]
            color = random.choice(flash_colors)
            
            particle = Particle(x, y, velocity_x, velocity_y, color, size=3, lifetime=10)
            particle.gravity = 0  # No gravity for muzzle flash
            self.particles.append(particle)
    
    def create_hit_effect(self, x, y, color):
        """Create small hit effect when bullet hits enemy"""
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            particle = Particle(x, y, velocity_x, velocity_y, color, size=2, lifetime=15)
            self.particles.append(particle)
    
    def update(self):
        """Update all particles and remove dead ones"""
        # Update all particles
        for particle in self.particles:
            particle.update()
        
        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]
    
    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)
    
    def get_particle_count(self):
        """Get current number of active particles"""
        return len(self.particles)