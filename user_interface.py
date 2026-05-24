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


def upgrade_selection_menu(screen, clock, joystick, player=None):
    font_title = pygame.font.SysFont(None, 80)
    font_card_title = pygame.font.SysFont(None, 54)
    font_desc = pygame.font.SysFont(None, 32)

    health_gain = player.health_upgrade_strength if player else 0
    upgrades = [
        {
            "key": "health",
            "label": "HEALTH",
            "desc": [f"+{health_gain} Max HP", "Full Heal"],
            "color": GREEN,
            "icon": "circle",
        },
        {
            "key": "weapon",
            "label": "WEAPON",
            "desc": ["+1 Weapon Level"],
            "color": CYAN,
            "icon": "bullet",
        },
        {
            "key": "speed",
            "label": "SPEED",
            "desc": ["+1 Speed Level"],
            "color": YELLOW,
            "icon": "arrow",
        },
    ]

    card_w, card_h = 280, 340
    gap = 60
    total_w = len(upgrades) * card_w + (len(upgrades) - 1) * gap

    selected = 0
    nav_cooldown = 0

    snapshot = screen.copy()
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.set_alpha(160)
    overlay.fill((20, 20, 40))

    while True:
        sw, sh = screen.get_width(), screen.get_height()
        start_x = (sw - total_w) // 2
        card_y = sh // 2 - card_h // 2
        rects = [
            pygame.Rect(start_x + i * (card_w + gap), card_y, card_w, card_h)
            for i in range(len(upgrades))
        ]

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return upgrades[selected]["key"]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(upgrades)
                if event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(upgrades)
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return upgrades[selected]["key"]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(mouse_pos):
                        return upgrades[i]["key"]
            if event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(mouse_pos):
                        selected = i
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # A / Cross — confirm
                    return upgrades[selected]["key"]

        if nav_cooldown > 0:
            nav_cooldown -= 1
        if joystick and nav_cooldown == 0:
            left_x = joystick.get_axis(0)
            hat = joystick.get_hat(0) if joystick.get_numhats() > 0 else (0, 0)
            if left_x < -0.5 or hat[0] == -1:
                selected = (selected - 1) % len(upgrades)
                nav_cooldown = 15
            elif left_x > 0.5 or hat[0] == 1:
                selected = (selected + 1) % len(upgrades)
                nav_cooldown = 15

        screen.blit(snapshot, (0, 0))
        screen.blit(overlay, (0, 0))

        title_surf = font_title.render("SELECT UPGRADE", True, WHITE)
        screen.blit(title_surf, (sw // 2 - title_surf.get_width() // 2, card_y - 100))

        for i, (upgrade, rect) in enumerate(zip(upgrades, rects)):
            is_selected = i == selected
            color = upgrade["color"]
            border_color = color if is_selected else tuple(max(0, c // 3) for c in color)
            border_w = 3 if is_selected else 1

            bg_color = (50, 50, 80) if is_selected else (30, 30, 50)
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, border_color, rect, border_w)

            icon_cx = rect.centerx
            icon_cy = rect.y + 100

            if upgrade["icon"] == "circle":
                pygame.draw.circle(screen, color, (icon_cx, icon_cy), 36)
                pygame.draw.circle(screen, WHITE, (icon_cx, icon_cy), 36, 2)
            elif upgrade["icon"] == "bullet":
                pygame.draw.circle(screen, color, (icon_cx, icon_cy), 14)
                pygame.draw.line(screen, color, (icon_cx - 40, icon_cy), (icon_cx - 16, icon_cy), 5)
                pygame.draw.line(screen, color, (icon_cx + 40, icon_cy), (icon_cx + 16, icon_cy), 5)
            elif upgrade["icon"] == "arrow":
                pts = [
                    (icon_cx + 44, icon_cy),
                    (icon_cx + 18, icon_cy - 22),
                    (icon_cx + 18, icon_cy - 10),
                    (icon_cx - 44, icon_cy - 10),
                    (icon_cx - 44, icon_cy + 10),
                    (icon_cx + 18, icon_cy + 10),
                    (icon_cx + 18, icon_cy + 22),
                ]
                pygame.draw.polygon(screen, color, pts)

            label_surf = font_card_title.render(upgrade["label"], True, color)
            screen.blit(label_surf, (rect.centerx - label_surf.get_width() // 2, rect.y + 170))

            for j, line in enumerate(upgrade["desc"]):
                desc_surf = font_desc.render(line, True, WHITE)
                screen.blit(desc_surf, (rect.centerx - desc_surf.get_width() // 2, rect.y + 240 + j * 36))

        pygame.display.flip()
        clock.tick(60)


def pause_menu(screen, clock, joystick, score=0, show_stats=True):
    font_title = pygame.font.SysFont(None, 80)
    font_btn = pygame.font.SysFont(None, 50)

    # 0=Resume, 1=Toggle Stats, 2=Toggle Fullscreen, 3=Return to Menu
    NUM_OPTIONS = 4
    selected = 0
    nav_cooldown = 0

    btn_w, btn_h = 280, 55

    snapshot = screen.copy()
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.set_alpha(130)
    overlay.fill((60, 60, 60))

    while True:
        sw, sh = screen.get_width(), screen.get_height()
        btn_x = sw // 2 - btn_w // 2
        rects = [
            pygame.Rect(btn_x, sh // 2,       btn_w, btn_h),
            pygame.Rect(btn_x, sh // 2 + 80,  btn_w, btn_h),
            pygame.Rect(btn_x, sh // 2 + 160, btn_w, btn_h),
            pygame.Rect(btn_x, sh // 2 + 240, btn_w, btn_h),
        ]

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", show_stats
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume", show_stats
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected == 0:
                        return "resume", show_stats
                    elif selected == 1:
                        show_stats = not show_stats
                    elif selected == 2:
                        pygame.display.toggle_fullscreen()
                    else:
                        return "menu", show_stats
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % NUM_OPTIONS
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % NUM_OPTIONS
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(mouse_pos):
                        if i == 0:
                            return "resume", show_stats
                        elif i == 1:
                            show_stats = not show_stats
                        elif i == 2:
                            pygame.display.toggle_fullscreen()
                        else:
                            return "menu", show_stats
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # A / Cross — confirm
                    if selected == 0:
                        return "resume", show_stats
                    elif selected == 1:
                        show_stats = not show_stats
                    elif selected == 2:
                        pygame.display.toggle_fullscreen()
                    else:
                        return "menu", show_stats
                if event.button == 1:  # B / Circle — resume
                    return "resume", show_stats

        if nav_cooldown > 0:
            nav_cooldown -= 1
        if joystick and nav_cooldown == 0:
            left_y = joystick.get_axis(1)
            hat = joystick.get_hat(0) if joystick.get_numhats() > 0 else (0, 0)
            if left_y < -0.5 or hat[1] == 1:
                selected = (selected - 1) % NUM_OPTIONS
                nav_cooldown = 15
            elif left_y > 0.5 or hat[1] == -1:
                selected = (selected + 1) % NUM_OPTIONS
                nav_cooldown = 15

        for i, rect in enumerate(rects):
            if rect.collidepoint(mouse_pos):
                selected = i

        screen.blit(snapshot, (0, 0))
        screen.blit(overlay, (0, 0))

        title = font_title.render("PAUSED", True, WHITE)
        screen.blit(title, (sw // 2 - title.get_width() // 2, sh // 2 - 150))

        font_score = pygame.font.SysFont(None, 45)
        score_surf = font_score.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (sw // 2 - score_surf.get_width() // 2, sh // 2 - 70))

        is_fullscreen = bool(screen.get_flags() & pygame.FULLSCREEN)
        labels = ["Resume", "Hide Stats" if show_stats else "Show Stats", "Windowed" if is_fullscreen else "Fullscreen", "Return to Menu"]
        for i, (label, rect) in enumerate(zip(labels, rects)):
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

    while True:
        sw, sh = screen.get_width(), screen.get_height()
        btn_x = sw // 2 - btn_w // 2
        rects = [
            pygame.Rect(btn_x, sh // 2,      btn_w, btn_h),
            pygame.Rect(btn_x, sh // 2 + 80, btn_w, btn_h),
        ]

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
        for i in range(0, sh, 50):
            pygame.draw.rect(screen, DARKBLUE,   (0, i, sw, 1))
        for i in range(25, sh, 50):
            pygame.draw.rect(screen, DARKERBLUE, (0, i, sw, 1))
        for i in range(50, sw, 50):
            pygame.draw.rect(screen, DARKBLUE,   (i, 0, 1, sh))
        for i in range(25, sw, 50):
            pygame.draw.rect(screen, DARKERBLUE, (i, 0, 1, sh))

        title = font_title.render("Ball Game", True, WHITE)
        screen.blit(title, (sw // 2 - title.get_width() // 2, sh // 2 - 150))

        font_score = pygame.font.SysFont(None, 40)
        prev_surf = font_score.render(f"Previous Score: {last_score}", True, GREY)
        screen.blit(prev_surf, (sw // 2 - prev_surf.get_width() // 2, sh // 2 - 80))

        for i, (label, rect) in enumerate(zip(options, rects)):
            color = WHITE if i == selected else GREY
            pygame.draw.rect(screen, color, rect, 2)
            text = font_btn.render(label, True, color)
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)
