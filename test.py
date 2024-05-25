import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_width = 400
window_height = 300

def run_game():
    # Create the window
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Pygame Window")

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the window with white background
        window.fill((255, 255, 255))
        
        text = STAT_FONT.render("Score: {:.2f}".format(self.score), True, (255, 255, 255))
        window.win.blit(text, (WIDTH - 10 - text.get_width(), 10))

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    print("quit")

# Run the game
run_game()
run_game()
run_game()
run_game()