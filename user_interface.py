import pygame
from constants import *

def draw_stat_panel(screen, font, title, stats, x_center, y_start, width=170):
    line_h = 26
    pad = 8
    panel_h = (len(stats) + 1) * line_h + pad * 2 + 4

    rect = pygame.Rect(x_center - width // 2, y_start, width, panel_h)
    pygame.draw.rect(screen, WHITE, rect, 1)

    title_surf = font.render(title, True, WHITE)
    screen.blit(title_surf, (rect.centerx - title_surf.get_width() // 2, rect.y + pad))

    pygame.draw.line(screen, WHITE, (rect.x + 1, rect.y + line_h + pad), (rect.right - 1, rect.y + line_h + pad), 1)

    for i, (label, value) in enumerate(stats):
        text = font.render(f"{label}: {value}", True, WHITE)
        screen.blit(text, (rect.centerx - text.get_width() // 2, rect.y + pad + 4 + (i + 1) * line_h))


def pause_menu(screen, clock, joystick, score=0):
    font_title = pygame.font.SysFont(None, 80)
    font_btn = pygame.font.SysFont(None, 50)

    options = ["Resume", "Return to Menu"]
    selected = 0
    nav_cooldown = 0

    btn_w, btn_h = 280, 55
    btn_x = WIDTH // 2 - btn_w // 2
    rects = [
        pygame.Rect(btn_x, HEIGHT // 2, btn_w, btn_h),
        pygame.Rect(btn_x, HEIGHT // 2 + 80, btn_w, btn_h),
    ]

    snapshot = screen.copy()
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(130)
    overlay.fill((60, 60, 60))

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "resume" if selected == 0 else "menu"
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(mouse_pos):
                        return "resume" if i == 0 else "menu"
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # A / Cross — confirm
                    return "resume" if selected == 0 else "menu"
                if event.button == 1:  # B / Circle — resume
                    return "resume"

        if nav_cooldown > 0:
            nav_cooldown -= 1
        if joystick and nav_cooldown == 0:
            left_y = joystick.get_axis(1)
            hat = joystick.get_hat(0) if joystick.get_numhats() > 0 else (0, 0)
            if left_y < -0.5 or hat[1] == 1:
                selected = (selected - 1) % len(options)
                nav_cooldown = 15
            elif left_y > 0.5 or hat[1] == -1:
                selected = (selected + 1) % len(options)
                nav_cooldown = 15

        for i, rect in enumerate(rects):
            if rect.collidepoint(mouse_pos):
                selected = i

        screen.blit(snapshot, (0, 0))
        screen.blit(overlay, (0, 0))

        title = font_title.render("PAUSED", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 150))

        font_score = pygame.font.SysFont(None, 45)
        score_surf = font_score.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, HEIGHT // 2 - 70))

        for i, (label, rect) in enumerate(zip(options, rects)):
            color = WHITE if i == selected else GREY
            pygame.draw.rect(screen, color, rect, 2)
            text = font_btn.render(label, True, color)
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)


def main_menu(screen, clock, joystick, last_score=0):
    font_title = pygame.font.SysFont(None, 80)
    font_btn = pygame.font.SysFont(None, 50)

    options = ["Start", "Quit"]
    selected = 0
    nav_cooldown = 0

    btn_w, btn_h = 200, 55
    btn_x = WIDTH // 2 - btn_w // 2
    rects = [
        pygame.Rect(btn_x, HEIGHT // 2, btn_w, btn_h),
        pygame.Rect(btn_x, HEIGHT // 2 + 80, btn_w, btn_h),
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return options[selected].lower()
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_ESCAPE:
                    return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(mouse_pos):
                        return options[i].lower()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # A / Cross — confirm
                    return options[selected].lower()
                if event.button == 1:  # B / Circle — back/quit
                    return "quit"

        # Controller stick/d-pad navigation
        if nav_cooldown > 0:
            nav_cooldown -= 1
        if joystick and nav_cooldown == 0:
            left_y = joystick.get_axis(1)
            hat = joystick.get_hat(0) if joystick.get_numhats() > 0 else (0, 0)
            if left_y < -0.5 or hat[1] == 1:
                selected = (selected - 1) % len(options)
                nav_cooldown = 15
            elif left_y > 0.5 or hat[1] == -1:
                selected = (selected + 1) % len(options)
                nav_cooldown = 15

        # Mouse hover selects button
        for i, rect in enumerate(rects):
            if rect.collidepoint(mouse_pos):
                selected = i

        # Draw background
        screen.fill(BLACK)
        for i in range(0, HEIGHT, 50):
            pygame.draw.rect(screen, DARKBLUE, (0, i, WIDTH, 1))
        for i in range(25, HEIGHT, 50):
            pygame.draw.rect(screen, DARKERBLUE, (0, i, WIDTH, 1))
        for i in range(50, WIDTH, 50):
            pygame.draw.rect(screen, DARKBLUE, (i, 0, 1, HEIGHT))
        for i in range(25, WIDTH, 50):
            pygame.draw.rect(screen, DARKERBLUE, (i, 0, 1, HEIGHT))

        title = font_title.render("Ball Game", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 150))

        font_score = pygame.font.SysFont(None, 40)
        prev_surf = font_score.render(f"Previous Score: {last_score}", True, GREY)
        screen.blit(prev_surf, (WIDTH // 2 - prev_surf.get_width() // 2, HEIGHT // 2 - 80))

        for i, (label, rect) in enumerate(zip(options, rects)):
            color = WHITE if i == selected else GREY
            pygame.draw.rect(screen, color, rect, 2)
            text = font_btn.render(label, True, color)
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)
