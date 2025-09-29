import pygame, sys, math, random
from constants import *
from bullet import Bullet
from player import Player
from enemy import Enemy

def spawn_enemy():
    x_spawn_points = [0, WIDTH, random.randint(0, WIDTH), random.randint(0, WIDTH)]
    y_spawn_points = [random.randint(0, HEIGHT), random.randint(0, HEIGHT), 0, HEIGHT]
    choice = random.randint(0, 3)
    enemies.append(Enemy(x_spawn_points[choice], y_spawn_points[choice], player.level))

pygame.init()

# Screen and colors
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Game")
font = pygame.font.SysFont(None, 30)

# Entities
player = Player(WIDTH / 2, HEIGHT / 2)
score = 0
og_score = 0
level_up = 1999

bullets = []
bullet_delay = 10
shoot_timer = 0

enemies = []
enemy_spawn_timer = 0
enemy_spawn_delay = 175

# Settup
last_tick = pygame.time.get_ticks()
clock = pygame.time.Clock()

joystick = None
pygame.joystick.init()

# Initialize controller if available
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controller detected: {joystick.get_name()}")
else:
    print("No controller detected. Using keyboard (WASD) and mouse controls.")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False
    
    # Time keeping
    now = pygame.time.get_ticks()
    dt_ms = now - last_tick
    last_tick = now

    # Movement
    player.handle_movement(joystick)

    # Create bullets
    if shoot_timer > 0:
        shoot_timer -= 1  
    
    aim_direction = player.get_aim_direction(joystick)
    if aim_direction is not None and shoot_timer <= 0:
        if player.level == 1 or player.level == 2:
            bullet = Bullet(player, aim_direction)
            bullets.append(bullet)
        elif player.level == 3 or player.level == 4:
            bullet = Bullet(player, aim_direction - 0.08)
            bullets.append(bullet)
            bullet = Bullet(player, aim_direction + 0.08)
            bullets.append(bullet)
        elif player.level >= 5:
            bullet = Bullet(player, aim_direction - 0.1)
            bullets.append(bullet)
            bullet = Bullet(player, aim_direction + 0.1)
            bullets.append(bullet)
            bullet = Bullet(player, aim_direction)
            bullets.append(bullet)
        shoot_timer = bullet_delay

    # Handle enemies
    for enemy in enemies:
        enemy.update(player)
        if enemy.check_collision_with_player(player):
            enemies.remove(enemy)
            player.health -= enemy.dmg
            if player.health <= 0:
                player.alive = False
    
    # Handle bullets
    for bullet in bullets:
        for enemy in enemies:
            if enemy.check_collision_with_bullet(bullet):
                bullets.remove(bullet)
                enemy.health -= 25
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    score += enemy.score_value
                break
        # Remove bullets off screen
        if bullet.x > WIDTH or bullet.x < 0 or bullet.y > HEIGHT or bullet.y < 0:
            try:
                bullets.remove(bullet)
            except ValueError:
                print("Tried to remove bullet that was already removed.")
        bullet.update()

    # Create enemies
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_delay:
        for i in range(0, player.level):
            spawn_enemy()
        enemy_spawn_timer = 0

    # Handle level up (increase difficulty, increase weapon power)
    if score > og_score + level_up:
        player.level += 1
        og_score += level_up + 1
        level_up += 3000
        enemy_spawn_delay -= enemy_spawn_delay * 0.10
        bullet_delay -= bullet_delay * 0.20

    # Draw screen
    screen.fill(BLACK) 

    # Grid lines
    for i in range(0, HEIGHT, 50):
        pygame.draw.rect(screen, DARKBLUE, (0, i, WIDTH, 1))
    for i in range(25, HEIGHT, 50):
        pygame.draw.rect(screen, DARKERBLUE, (0, i, WIDTH, 1))

    for i in range(50, WIDTH, 50):
        pygame.draw.rect(screen, DARKBLUE, (i, 0, 1, HEIGHT))
    for i in range(25, WIDTH, 50):
        pygame.draw.rect(screen, DARKERBLUE, (i, 0, 1, HEIGHT))

    # Draw enemies
    for enemy in enemies:
        enemy.draw_health_bar(screen)
        enemy.draw(screen)

    # Draw player
    player.draw(screen)
    player.draw_health_bar(screen)

    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen)
    
    # Draw ui elements (score, level, time)
    score_display = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_display, (25, 25))
    level_display = font.render(f"Level: {player.level}", True, (255, 255, 255))
    screen.blit(level_display, (25, 50))

    # Print death screen
    if not player.alive:
        break

    # Update screen and advance time
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()