import pygame
from pygame_extensions.pyui_elements import PyScrollView, PyButton

# Create a new pygame window
pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)

# Create a PyButton object
button = PyButton("Click me!", 100, 100, 200, 50, pygame.Color("blue"), pygame.Color("blue"), pygame.Color("blue"), pygame.font.SysFont("arial", 20))

# Create a ScrollView object
scroll_view = PyScrollView(0, 0, 600, 400, [button])

# Add some content to the ScrollView
content = pygame.Surface((800, 800))
content.fill((255, 255, 255))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scroll_view.handle_event(event)
        
    # Update the ScrollView
    scroll_view.draw(window)

    # Draw the ScrollView and its content
    window.fill((0, 0, 0))
    scroll_view.draw(window)
    pygame.display.flip()

# Quit pygame
pygame.quit()