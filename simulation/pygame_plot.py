import matplotlib
matplotlib.use("Agg")
import pygame
from pygame.locals import *
import matplotlib.backends.backend_agg as agg

import pylab

def py_plot(y_values: list) -> pygame.Surface:
	fig: pylab.Figure = pylab.figure(figsize=[4, 4], # Inches
					dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
					)
	ax: pylab.Axes = fig.gca()
	ax.plot(y_values)

	canvas = agg.FigureCanvasAgg(fig)
	canvas.draw()
	renderer = canvas.get_renderer()
	raw_data = renderer.tostring_rgb()

	size: tuple[int, int] = canvas.get_width_height()

	surface: pygame.Surface = pygame.image.fromstring(raw_data, size, "RGB")
 
	return surface