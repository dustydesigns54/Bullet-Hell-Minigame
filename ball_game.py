import pygame, sys, math, random

def circle_bullet_collide(cx, cy, r, rect):
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    dx = cx - closest_x
    dy = cy - closest_y
    return dx*dx + dy*dy <= r*r

pygame.init()

#-------------------------------------------------------------------
# initiate properties
#-------------------------------------------------------------------

#screen and colors
width, height = 1200, 700
black, green, red = (0, 0, 0), (0, 255, 0), (255, 0, 0)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball Game")
font = pygame.font.SysFont(None, 48)

joystick = None

#gameplay status
alive = True
death_time = None
respawn_delay = 1500

#ball properties
ball_radius, speed = 10, 8
ball_x, ball_y = width / 2, height / 2

#bullet properties
bullets = []
BULLET_W, BULLET_H = 20, 10
bullet_speed = 10
spawn_interval = 1000
starting_spawn_interval = spawn_interval
min_spawn_interval = 5
ramp_every = 3500
ramp_factor = 0.75

#bullet time accumulator 
accum_ms = 0
last_tick = pygame.time.get_ticks()
next_ramp_time = last_tick + ramp_every
clock = pygame.time.Clock()

#-------------------------------------------------------------------
# begin game loop, handle quit event, track time
#-------------------------------------------------------------------

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False
    
    now = pygame.time.get_ticks()
    dt_ms = now - last_tick
    last_tick = now

     # Initialize joystick
    pygame.joystick.init()
    
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Controller connected: {joystick.get_name()}")
        print(f"Number of axes: {joystick.get_numaxes()}")
        print(f"Number of buttons: {joystick.get_numbuttons()}")

    #-------------------------------------------------------------------
    # if alive, allow movement with either wasd or arrow keys
    #-------------------------------------------------------------------

    if alive:
        left_x = joystick.get_axis(0)
        left_y = joystick.get_axis(1)
        
        # Apply deadzone
        deadzone = 0.15
        if abs(left_x) > deadzone:
            ball_x += left_x * speed
        if abs(left_y) > deadzone:
            ball_y += left_y * speed

    #set border restrictions
    if ball_x - ball_radius < 0:
        ball_x = ball_radius
    if ball_x + ball_radius > width:
        ball_x = width - ball_radius
    if ball_y - ball_radius < 0:
        ball_y = ball_radius
    if ball_y + ball_radius > height:
        ball_y = height - ball_radius

    #-------------------------------------------------------------------
    # handle bullets, remove bullets that are off screen
    #-------------------------------------------------------------------

    for bullet in bullets:
        bullet.x += bullet_speed

    #update visible bullets
    new_bullets = []
    for b in bullets:
        if b.x < width:
            new_bullets.append(b)
    bullets = new_bullets

    #-------------------------------------------------------------------
    # handle state based actions
    #-------------------------------------------------------------------

    #if alive, check for collision, indicate death
    if alive:
        for b in bullets:
            if circle_bullet_collide(ball_x, ball_y, ball_radius, b):
                alive = False
                death_time = now
                break
    
    #disables movement while waiting for respawn
    if not alive and now - death_time >= respawn_delay:
        ball_x, ball_y = width / 2, height /2 
        bullets.clear()
        spawn_interval = starting_spawn_interval
        accum_ms = 0
        next_ramp_time = now + ramp_every
        alive = True
        death_time = None

    #-------------------------------------------------------------------
    # spawn bullets, increase difficulty
    #-------------------------------------------------------------------

    #create bullets
    accum_ms += dt_ms
    while accum_ms >= spawn_interval:
        bullets.append(pygame.Rect(0, random.randint(0, height - BULLET_H), BULLET_W, BULLET_H))
        accum_ms -= spawn_interval

    #increase difficulty
    if now >= next_ramp_time:
        spawn_interval = max(int(spawn_interval * ramp_factor), min_spawn_interval)
        accum_ms = min(accum_ms, spawn_interval)
        next_ramp_time += ramp_every

    #-------------------------------------------------------------------
    # create and update screen, handle death message
    #-------------------------------------------------------------------

    #draw screen and circle
    screen.fill(black) 
    pygame.draw.circle(screen, green, (int(ball_x), int(ball_y)), ball_radius)

    #draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, red, bullet)

    #if not alive, print death screen
    if not alive:
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, 120))
        screen.blit(overlay, (0, 0))
        msg = font.render("You died!", True, (255, 255, 255))
        screen.blit(msg, msg.get_rect(center=(width//2, height//2)))

    #update screen and advance time
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()