import pygame, sys, math, random
from constants import *
from bullet import Bullet
from player import Player
from enemy import Enemy

def spawn_enemy():
    spawn_points = [] #enhance spawning
    enemies.append(Enemy(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

pygame.init()

#screen and colors
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Game")
font = pygame.font.SysFont(None, 48)

#entities
player = Player(WIDTH / 2, HEIGHT / 2)
score = 0

bullets = []
bullet_delay = 10
shoot_timer = 0

enemies = []
enemy_spawn_timer = 0
enemy_spawn_delay = 100

#settup
last_tick = pygame.time.get_ticks()
clock = pygame.time.Clock()

joystick = None
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False
    
    #time keeping
    now = pygame.time.get_ticks()
    dt_ms = now - last_tick
    last_tick = now

     # Movement
    player.handle_movement(joystick)

    if shoot_timer > 0:
        shoot_timer -= 1       

    aim_direction = player.get_aim_direction(joystick)
    if aim_direction is not None and shoot_timer <= 0:
        # Create bullet
        bullet = Bullet(player, aim_direction)
        bullets.append(bullet)
        shoot_timer = bullet_delay

    #handle enemies
    for enemy in enemies:
        enemy.update(player)
        if enemy.check_collision_with_player(player):
            player.alive = False
    
    for bullet in bullets:
        for enemy in enemies:
            if enemy.check_collision_with_bullet(bullet):
                bullets.remove(bullet)
                enemies.remove(enemy)

    #create enemies
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_delay:
        spawn_enemy()
        enemy_spawn_timer = 0

    #handle bullets
    for bullet in bullets:
        bullet.update()

    #increase difficulty

    #disables movement while waiting for respawn

    #draw screen
    screen.fill(BLACK) 

    #draw enemies
    for enemy in enemies:
        enemy.draw(screen)

    #draw player
    player.draw(screen)

    #draw bullets
    for bullet in bullets:
        bullet.draw(screen)

    #print death screen
    if not player.alive:
        break

    #update screen and advance time
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()