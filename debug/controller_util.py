import pygame

def debug_controller():
    pygame.init()
    pygame.joystick.init()
    
    # Create a small window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Controller Debug Tool")
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    
    if pygame.joystick.get_count() == 0:
        print("No controller detected!")
        return
    
    # Initialize the first controller
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    print(f"Controller: {joystick.get_name()}")
    print(f"Axes: {joystick.get_numaxes()}")
    print(f"Buttons: {joystick.get_numbuttons()}")
    print(f"Hats: {joystick.get_numhats()}")
    print("\nMove your sticks and press buttons to see the values...")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill((0, 0, 0))
        
        # Display controller info
        y_offset = 20
        
        # Controller name
        text = font.render(f"Controller: {joystick.get_name()}", True, (255, 255, 255))
        screen.blit(text, (10, y_offset))
        y_offset += 30
        
        # Axes (sticks and triggers)
        text = font.render("AXES (Sticks & Triggers):", True, (255, 255, 0))
        screen.blit(text, (10, y_offset))
        y_offset += 25
        
        for i in range(joystick.get_numaxes()):
            value = joystick.get_axis(i)
            color = (255, 255, 255)
            if abs(value) > 0.1:  # Highlight active axes
                color = (0, 255, 0)
            
            text = font.render(f"  Axis {i}: {value:.3f}", True, color)
            screen.blit(text, (20, y_offset))
            y_offset += 20
        
        y_offset += 20
        
        # Buttons
        text = font.render("BUTTONS:", True, (255, 255, 0))
        screen.blit(text, (10, y_offset))
        y_offset += 25
        
        pressed_buttons = []
        for i in range(joystick.get_numbuttons()):
            if joystick.get_button(i):
                pressed_buttons.append(str(i))
        
        if pressed_buttons:
            text = font.render(f"  Pressed: {', '.join(pressed_buttons)}", True, (0, 255, 0))
        else:
            text = font.render("  None pressed", True, (255, 255, 255))
        screen.blit(text, (20, y_offset))
        y_offset += 40
        
        # Hats (D-pad)
        if joystick.get_numhats() > 0:
            text = font.render("D-PAD (Hat):", True, (255, 255, 0))
            screen.blit(text, (10, y_offset))
            y_offset += 25
            
            hat = joystick.get_hat(0)
            text = font.render(f"  Hat 0: {hat}", True, (255, 255, 255))
            screen.blit(text, (20, y_offset))
        
        # Instructions
        instruction_text = font.render("Move sticks, press buttons, then press ESC to exit", True, (200, 200, 200))
        screen.blit(instruction_text, (10, 550))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    debug_controller()