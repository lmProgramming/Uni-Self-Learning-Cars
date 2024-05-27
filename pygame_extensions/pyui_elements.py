import pygame as pg
from pygame.surface import Surface
from typing import Callable
from abc import ABC, abstractmethod
from pygame.font import Font
from simulation.pygame_plot import py_plot

pg.font.init()

COLOR_INACTIVE = pg.Color(200, 200, 200)
COLOR_ACTIVE = pg.Color(255, 255, 255)
FONT = pg.font.Font(None, 32)
TOOLTIP_COLOR = pg.Color(150, 150, 150)

BORDER_SIZE = 2

class PyUiElement(ABC):    
    @abstractmethod    
    def draw(self, screen) -> None:
        ...
        
    @abstractmethod
    def handle_event(self, event) -> bool:
        '''
        Returns True if the event was handled, False otherwise.
        '''
        ...

class PyInputBox(PyUiElement):
    def __init__(self, x, y, w, h, tooltip='') -> None:
        self.rect = pg.Rect(x, y, w, h)
        self.default_width = w
        self.color: pg.Color = COLOR_INACTIVE
        self.tooltip: str = tooltip
        self.text: str = ""
        self.txt_surface: pg.Surface = FONT.render(tooltip, True, self.color)
        self.active: bool = False
        self.update_width()        

    def handle_event(self, event) -> bool:
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.mouse_over(event.pos):
                self.set_active(not self.active)
            else:
                self.set_active(False)
            return True
                
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.set_active(False)
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()
                self.update_width()
                return True
        
        return False
    
    def mouse_over(self, pos) -> bool:
        return self.rect.collidepoint(pos)
    
    @property
    def showing_tooltip(self) -> bool:
        return self.text == ""
    
    def render_text(self):
        if not self.showing_tooltip:
            self.txt_surface = FONT.render(self.text, True, self.color)
        else:
            self.txt_surface = FONT.render(self.tooltip, True, TOOLTIP_COLOR)
                
    def set_active(self, active: bool) -> None:
        self.active = active
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        self.txt_surface = FONT.render(self.text, True, self.color)

    def update_width(self) -> None:
        width: int = max(self.default_width, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen) -> None:
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)
        
class PyButton(PyUiElement):
    def __init__(self, text: str, x: float, y: float, width: float, height: float, color, hover_color, font_color, font: Font) -> None:
        self.text = text
        self.rect = pg.Rect(x, y, width, height)
        self.rect_border = pg.Rect(x - BORDER_SIZE, y - BORDER_SIZE, width + 2 * BORDER_SIZE, height + 2 * BORDER_SIZE)
        self.color = color
        self.hover_color = hover_color
        self.font_color = font_color
        self.font: Font = font
        self.action: Callable[[], None]
        self.is_button_hovering = False
    
    def draw(self, surface) -> None:
        pg.draw.rect(surface, self.color, self.rect_border, 2)
        if self.is_button_hovering:
            pg.draw.rect(surface, self.hover_color, self.rect)
        else:
            pg.draw.rect(surface, self.color, self.rect)
            
        if self.text:        
            text_surface: pg.Surface = self.font.render(self.text, True, self.font_color)
            text_rect: pg.Rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
        
    def connect(self, action) -> None:
        self.action = action
        
    def handle_event(self, event) -> bool:
        if self.is_clicked(event):            
            self.action()
            return True
        return False
                
    def is_clicked(self, event) -> bool:
        self.is_button_hovering = False        
        if hasattr(event, 'pos'):
            if not self.rect.collidepoint(event.pos):
                return False
            self.is_button_hovering = True
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                return True
        return False
       
class PyImage(PyUiElement):
    def __init__(self, win: Surface, left_x: float, bottom_y: float, filename: str) -> None:
        self.win: Surface = win
        self.bottom_x: float = left_x
        self.bottom_y: float = bottom_y
        self.image: Surface = pg.image.load(filename)   
        
    def load_image(self, filename) -> None:
        self.image = pg.image.load(filename)            
        
    def handle_event(self, _) -> bool:
        return False
        
    def draw(self, screen) -> None:      
        y: float = self.bottom_y - self.image.get_height()     
        screen.blit(self.image, (self.bottom_x, y))
    
class PyPlot(PyUiElement):
    def __init__(self, x_right: float, y_bottom: float, width: float, height: float, *values_to_plot: list[float]):
        self.x_right: float = x_right
        self.y_bottom: float = y_bottom
        self.plot: Surface = py_plot(width, height, *values_to_plot)
        
    def draw(self, screen):
        screen.blit(self.plot, (self.x_right - self.plot.get_width(), self.y_bottom - self.plot.get_height()))
        
    def handle_event(self, _) -> bool:
        return False
        
class PyScrollView(PyUiElement):
    SCROLL_STRENGTH = 10
    def __init__(self, x: float, y: float, width: float, visible_height: float) -> None:
        self.rect = pg.Rect(x, y, width, visible_height)
        self.elements: list[PyUiElement] = []
        self.scroll_offset: float = 0
        self.scrollable_area = pg.Surface((width, visible_height))   
        self.visible_height: float = visible_height     
        self.needed_height: float = 0

    def handle_event(self, event: pg.event.Event) -> bool:
        self.handle_scrolling(event)         

        for element in self.elements:            
            if hasattr(event, 'pos'):
                prev_event_pos = event.pos
                event.pos -= pg.Vector2(0, self.rect.y - self.scroll_offset)
                                
                element.handle_event(event)
                
                event.pos = prev_event_pos

        return False

    def handle_scrolling(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scroll_offset -= self.SCROLL_STRENGTH
            elif event.button == 5:
                self.scroll_offset += self.SCROLL_STRENGTH
            self.scroll_offset = max(0, min(self.scroll_offset, self.scrollable_area.get_height() - self.rect.height))
    
    def add_element(self, element: PyUiElement, element_height: float) -> None:
        self.elements.append(element)
        self.needed_height += element_height
        self.scrollable_area = pg.Surface((self.rect.width, max(self.needed_height, self.rect.height)))

    def draw(self, screen) -> None:
        self.scrollable_area.fill((255, 255, 255))

        for element in self.elements:
            element.draw(self.scrollable_area)            

        visible_area: Surface = self.scrollable_area.subsurface(pg.Rect(0, self.scroll_offset, self.rect.width, self.rect.height))

        screen.blit(visible_area, (self.rect.x, self.rect.y))
        pg.draw.rect(screen, (0, 0, 0), self.rect, 2)