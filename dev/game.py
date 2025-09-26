import pygame
import random
from constants import *
from player import Player
from bullet import Bullet
from enemy import Enemy
from particles import ParticleSystem

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Twin-Stick Shooter")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize joystick
        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Controller connected: {self.joystick.get_name()}")
            print(f"Number of axes: {self.joystick.get_numaxes()}")
            print(f"Number of buttons: {self.joystick.get_numbuttons()}")
        else:
            print("No controller detected. Connect an Xbox controller and restart game.")

        # Game objects
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.bullets = []
        self.enemies = []
        self.particle_system = ParticleSystem()
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 60  # frames
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.bombs = 3

        # Shooting
        self.shoot_timer = 0
        self.shoot_delay = 10  # frames between shots

    def _draw_background_grid(self):
        grid_size = 20
        for x in range(0, SCREEN_WIDTH, grid_size):
            pygame.draw.line(self.screen, BACKGROUND_GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(self.screen, BACKGROUND_GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    def spawn_enemy(self, boss = False):
        # Spawn enemy at random edge of screen
        side = random.randint(0, 3)
        if side == 0:    # Top
            x, y = random.randint(0, SCREEN_WIDTH), 0
        elif side == 1:  # Right
            x, y = SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # Bottom
            x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT
        else:            # Left
            x, y = 0, random.randint(0, SCREEN_HEIGHT)

        self.enemies.append(Enemy(x, y, boss))

    def update(self):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Button Pressed: {event.button}")
                if event.button == 7:                       # Start button (pause/quit)
                    self.running = False
                elif event.button == 5 and self.bombs > 0:  # Right bumper button (giga bomb)
                    self.bombs -= 1
                    for enemy in self.enemies[:]:
                        self.kill_enemy(enemy)
                elif event.button == 4:                     # Left Bumper (debugging)
                    self.spawn_enemy(True)
                elif event.button == 3:                     # Y button (debugging)
                    self.score += 500

        if not self.joystick:
            return

        # Update player
        self.player.update(self.joystick)

        # Handle shooting
        if self.shoot_timer > 0:
            self.shoot_timer -= 1       

        aim_direction = self.player.get_aim_direction(self.joystick)
        if aim_direction is not None and self.shoot_timer <= 0:
            # Create bullet
            bullet = Bullet(self.player.x, self.player.y, aim_direction)
            self.bullets.append(bullet)
            self.shoot_timer = self.shoot_delay

            # Create muzzle flash effect
            self.particle_system.create_muzzle_flash(self.player.x, self.player.y, aim_direction)

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.particle_system.create_hit_effect(bullet.x, bullet.y, YELLOW)
                self.bullets.remove(bullet)
                

        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
            # Gradually increase spawn rate
            if self.enemy_spawn_delay > 10:
                self.enemy_spawn_delay -= 0.10

        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.player)

        # Update particle system
        self.particle_system.update()

        # Check bullet-enemy collisions
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if enemy.check_collision_with_bullet(bullet):
                    self.bullets.remove(bullet)

                    # Create hit effect
                    self.particle_system.create_hit_effect(bullet.x, bullet.y, enemy.color)

                    enemy.health -= 25
                    if enemy.health <= 0:
                        self.kill_enemy(enemy)
                    break

        # Check player-enemy collisions
        for enemy in self.enemies[:]:
            if enemy.check_collision_with_player(self.player):
                self.player.health -= 1
                if self.player.health <= 0:
                    print(f"Game Over! Final Score: {self.score}")
                    self.running = False

        # Check for player leveling up
        if self.score > 1000 and self.player.level == 1:
            self.shoot_delay -= 2
            self.player.level += 1
            self.bombs += 1
        elif self.score > 2000 and self.player.level == 2:
            self.shoot_delay -= 2
            self.player.level += 1
            self.bombs += 1
            self.spawn_enemy(True)
        elif self.score > 3000 and self.player.level == 3:
            self.shoot_delay -= 2
            self.player.level += 1
            self.bombs += 1
        elif self.score > 4000 and self.player.level == 4:
            self.shoot_delay -= 1
            self.player.level += 1
            self.bombs += 1
            self.spawn_enemy(True)

    def kill_enemy(self, enemy):
        self.particle_system.create_enemy_death_effect(enemy)
        self.enemies.remove(enemy)
        self.score += 10
        if enemy.enemy_type == "boss":
            for enemy in self.enemies[:]:
                self.kill_enemy(enemy)

    def draw(self):
        self.screen.fill(BLACK)
        self._draw_background_grid()

        # Draw game objects
        self.player.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw particle effects
        self.particle_system.draw(self.screen)

        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, GREY)
        self.screen.blit(score_text, (10, 10))

        score_text = self.font.render(f"Level: {self.player.level}", True, GREY)
        self.screen.blit(score_text, (250, 10))

        enemies_text = self.font.render(f"Enemies: {len(self.enemies)}", True, GREY)
        self.screen.blit(enemies_text, (10, 40))

        enemies_text = self.font.render(f"GIGA Bombs: {self.bombs}", True, GREY)
        self.screen.blit(enemies_text, (10, 70))

        # Draw controller instructions
        if not self.joystick:
            no_controller_text = self.font.render("No Controller Detected!", True, RED)
            text_rect = no_controller_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(no_controller_text, text_rect)
        else:
            instructions = [
                "Left Stick: Move",
                "Right Stick: Aim & Shoot", 
                "Start: Quit"
            ]
            for i, instruction in enumerate(instructions):
                text = pygame.font.Font(None, 24).render(instruction, True, WHITE)
                self.screen.blit(text, (SCREEN_WIDTH - 200, 10 + i * 25))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
