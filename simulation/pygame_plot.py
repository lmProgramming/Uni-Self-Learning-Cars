import matplotlib
matplotlib.use("Agg")
import pygame
from pygame.locals import *
import matplotlib.backends.backend_agg as agg

import pylab

def py_plot(width, height, *y_values_packed) -> pygame.Surface:
    if len(y_values_packed) == 0:
        raise ValueError("No values to plot")
    
    dpi = 100

    fig: pylab.Figure = pylab.figure(figsize=[width // dpi, height // dpi], dpi=dpi)
    ax: pylab.Axes = fig.gca()

    for y_values in y_values_packed:
        ax.plot(y_values)

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data: bytes = renderer.tostring_rgb()

    size: tuple[int, int] = canvas.get_width_height()

    surface: pygame.Surface = pygame.image.fromstring(raw_data, size, "RGB")
 
    return surface

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 400))

    surface = py_plot(400, 400, [1, 2, 3], [4, 5, 6], [7, 8, 9])
    screen.blit(surface, (0, 0))

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()