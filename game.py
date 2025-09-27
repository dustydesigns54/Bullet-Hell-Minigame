import pygame, sys, math, random
from player import Player
from constants import *

pygame.init()

#screen and colors
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Game")
font = pygame.font.SysFont(None, 48)

joystick = None

#entities
player = Player(WIDTH / 2, HEIGHT / 2)
enemies = []

#settup
last_tick = pygame.time.get_ticks()
clock = pygame.time.Clock()
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


    # handle enemies, remove enemies that are off screen



    #if alive, check for collision, indicate death
    
    #disables movement while waiting for respawn


    # spawn enemies, increase difficulty


    #create enemies


    #increase difficulty

    #draw screen
    screen.fill(BLACK) 

    #draw player
    player.draw(screen)

    #draw enemies

    if not player.alive:
        break

    #update screen and advance time
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()