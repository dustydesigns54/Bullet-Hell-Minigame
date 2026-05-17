import pygame, sys, random
from constants import *
from bullet import Bullet
from player import Player
from enemy import Enemy, BOSS_ROUNDS
from particle import spawn_explosion
from user_interface import main_menu, pause_menu, draw_stat_panel, upgrade_selection_menu

def fire_spread(player, aim_direction, n, spread=0.15):
    speed = 15 + player.weapon_bullet_speed
    return [
        Bullet(player, aim_direction + (i - (n - 1) / 2) * spread, speed)
        for i in range(n)
    ]

def run_game(screen, clock, joystick):
    panel_font = pygame.font.SysFont(None, 24)
    player = Player(WIDTH / 2, HEIGHT / 2)
    score = 0
    kills = 0
    og_score = 0
    level_up = 1999

    bullets = []
    bullet_delay = 12
    shoot_timer = 0

    explosions = []

    damage_flash_timer = 0

    enemies = []
    enemy_spawn_timer = 0
    enemy_spawn_delay = 175

    force_level_up = False
    pending_boss_spawn = False
    ABILITY_INTERVAL = 30

    alternator = 0

    def spawn_enemy(forced_type=None):
        x_spawns = [0, WIDTH, random.randint(0, WIDTH), random.randint(0, WIDTH)]
        y_spawns = [random.randint(0, HEIGHT), random.randint(0, HEIGHT), 0, HEIGHT]
        choice = random.randint(0, 3)
        enemies.append(Enemy(x_spawns[choice], y_spawns[choice], player.level, forced_type=forced_type))

    paused = False
    upgrade_delay = 0
    show_stats = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:  # B / Circle
                    paused = True

        player.handle_movement(joystick)

        if shoot_timer > 0:
            shoot_timer -= 1

        aim_direction = player.get_aim_direction(joystick)
        if aim_direction is not None and shoot_timer <= 0:
            level = player.weapon_level
            if level % 2 == 1:
                bullets.extend(fire_spread(player, aim_direction, (level + 1) // 2))
            else:
                lo, hi = level // 2, level // 2 + 1
                n = hi if alternator % 2 == 0 else lo
                bullets.extend(fire_spread(player, aim_direction, n))
                alternator += 1
            shoot_timer = bullet_delay

        for enemy in enemies:
            enemy.update(player)

            if enemy.ability_fn is not None:
                enemy.ability_timer += 1
                if enemy.ability_timer >= ABILITY_INTERVAL:
                    enemy.ability_fn(enemy, enemies, player.level)
                    enemy.ability_timer = 0
                # Boss: survives contact, damage gated by cooldown
                if enemy.contact_cooldown > 0:
                    enemy.contact_cooldown -= 1
                elif enemy.check_collision_with_player(player):
                    player.health -= enemy.dmg
                    damage_flash_timer = 40
                    enemy.contact_cooldown = 90  # 1.5 seconds at 60fps
                    if player.health <= 0:
                        player.alive = False
            else:
                if enemy.check_collision_with_player(player):
                    spawn_explosion(explosions, enemy.x, enemy.y, enemy.radius * 0.33, enemy.color, enemy.radius * 0.3, 45)
                    enemies.remove(enemy)
                    player.health -= enemy.dmg
                    damage_flash_timer = 40
                    if player.health <= 0:
                        player.alive = False

        for bullet in bullets:
            for enemy in enemies:
                if enemy.check_collision_with_bullet(bullet):
                    spawn_explosion(explosions, bullet.x, bullet.y, 3, bullet.color, 2.5)
                    bullets.remove(bullet)
                    enemy.health -= 25
                    if enemy.health <= 0:
                        spawn_explosion(explosions, enemy.x, enemy.y, enemy.radius * 0.33, enemy.color, enemy.radius * 0.3, 45)
                        enemies.remove(enemy)
                        score += enemy.score_value
                        kills += 1
                        if any(t.name == enemy.type_name for t in BOSS_ROUNDS.values()):
                            force_level_up = True
                    break
            if bullet.x > WIDTH or bullet.x < 0 or bullet.y > HEIGHT or bullet.y < 0:
                try:
                    spawn_explosion(explosions, bullet.x, bullet.y, 3, bullet.color, 2.5)
                    bullets.remove(bullet)
                except ValueError:
                    pass
            bullet.update()

        enemy_spawn_timer += 1
        in_boss_round = (
            player.level in BOSS_ROUNDS
            and any(e.type_name == BOSS_ROUNDS[player.level].name for e in enemies)
        )
        if not in_boss_round and upgrade_delay == 0 and not force_level_up:
            if enemy_spawn_timer >= enemy_spawn_delay:
                for _ in range(player.level):
                    spawn_enemy()
                enemy_spawn_timer = 0

        if score > og_score + level_up or force_level_up:
            was_forced = force_level_up
            force_level_up = False
            player.level_up(explosions)
            for enemy in enemies:
                spawn_explosion(explosions, enemy.x, enemy.y, enemy.radius * 0.33, enemy.color, enemy.radius * 0.3, 45)
            enemies.clear()
            bullets.clear()
            og_score = score if was_forced else og_score + level_up + 1
            level_up += 2500
            enemy_spawn_delay -= enemy_spawn_delay * 0.09
            upgrade_delay = 60

            if player.level in BOSS_ROUNDS:
                pending_boss_spawn = True

        screen.fill(BLACK)

        if damage_flash_timer > 0:
            t = damage_flash_timer / 60
            damage_flash_timer -= 1
            grid_primary   = (int(t * 255), 0, int(DARKBLUE[2]   * (1 - t)))
            grid_secondary = (int(t * 255), 0, int(DARKERBLUE[2] * (1 - t)))
        else:
            grid_primary, grid_secondary = DARKBLUE, DARKERBLUE

        for i in range(0, HEIGHT, 50):
            pygame.draw.rect(screen, grid_primary, (0, i, WIDTH, 1))
        for i in range(25, HEIGHT, 50):
            pygame.draw.rect(screen, grid_secondary, (0, i, WIDTH, 1))
        for i in range(50, WIDTH, 50):
            pygame.draw.rect(screen, grid_primary, (i, 0, 1, HEIGHT))
        for i in range(25, WIDTH, 50):
            pygame.draw.rect(screen, grid_secondary, (i, 0, 1, HEIGHT))

        for enemy in enemies:
            enemy.draw_health_bar(screen)
            enemy.draw(screen)

        for particles in explosions:
            for p in particles:
                p.update(WIDTH, HEIGHT)
                p.draw(screen)
                if not p.alive():
                    particles.remove(p)
            if not particles:
                explosions.remove(particles)

        player.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)

        if show_stats:
            player_stats = [
                ("Player", f"Lv {player.level}"),
                ("Health", f"Lv {player.health_level}"),
                ("Weapon", f"Lv {player.weapon_level}"),
                ("Speed",  f"Lv {player.speed_level}"),
                ("Score",  str(score)),
            ]
            draw_stat_panel(screen, panel_font, "PLAYER", player_stats, 95, 20)

            actual_stats = [
                ("HP", f"{player.health} / {player.start_health}"),
                ("Speed", str(player.speed)),
            ]
            draw_stat_panel(screen, panel_font, "STATS", actual_stats, 95, 202)

            wave_in = max(0, (enemy_spawn_delay - enemy_spawn_timer) / 60)
            enemy_stats = [
                ("On Screen", str(len(enemies))),
                ("Killed",    str(kills)),
                ("Wave In",   f"{wave_in:.1f}s"),
            ]
            draw_stat_panel(screen, panel_font, "ENEMIES", enemy_stats, WIDTH - 95, 20)

        # Top health bar — spans between the two stat panels
        bar_x, bar_y, bar_w, bar_h = 200, 30, 1100, 18
        fill_w = int(bar_w * (player.health / player.start_health))
        pygame.draw.rect(screen, RED,   (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, fill_w, bar_h))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 1)

        # XP bar — tracks progress to next level
        xp_bar_h = 10
        xp_bar_y = bar_y + bar_h + 4
        xp_fill_w = int(bar_w * min((score - og_score) / level_up, 1.0))
        pygame.draw.rect(screen, (20, 20, 80),   (bar_x, xp_bar_y, bar_w, xp_bar_h))
        pygame.draw.rect(screen, (30, 144, 255), (bar_x, xp_bar_y, xp_fill_w, xp_bar_h))
        pygame.draw.rect(screen, WHITE,          (bar_x, xp_bar_y, bar_w, xp_bar_h), 1)

        if not player.alive:
            return "menu", score

        if paused:
            paused = False
            result, show_stats = pause_menu(screen, clock, joystick, score, show_stats)
            if result in ("menu", "quit"):
                return result, score

        if upgrade_delay > 0:
            upgrade_delay -= 1
            if upgrade_delay == 0:
                choice = upgrade_selection_menu(screen, clock, joystick, player)
                if choice == "health":
                    player.upgrade_health()
                elif choice == "weapon":
                    player.upgrade_weapon()
                    bullet_delay = max(3, bullet_delay - 1)
                elif choice == "speed":
                    player.upgrade_speed()
                if pending_boss_spawn:
                    boss_type = BOSS_ROUNDS[player.level]
                    bx = random.randint(boss_type.radius, WIDTH - boss_type.radius)
                    enemies.append(Enemy(bx, -boss_type.radius, player.level,
                                        forced_type=boss_type.name))
                    pending_boss_spawn = False

        pygame.display.flip()
        clock.tick(60)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Game")
clock = pygame.time.Clock()

joystick = None
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controller detected: {joystick.get_name()}")
else:
    print("No controller detected. Using keyboard (WASD) and mouse controls.")

state = "menu"
last_score = 0
while state != "quit":
    if state == "menu":
        state = main_menu(screen, clock, joystick, last_score)
    elif state == "start":
        state, last_score = run_game(screen, clock, joystick)

pygame.quit()
sys.exit()
