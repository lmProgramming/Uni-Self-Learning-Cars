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
        self.update()        

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
                self.update()
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

    def update(self) -> None:
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
    
    def draw(self, surface) -> None:
        mouse_pos = pg.mouse.get_pos()
        pg.draw.rect(surface, self.color, self.rect_border, 2)
        if self.rect.collidepoint(mouse_pos):
            pg.draw.rect(surface, self.hover_color, self.rect)
        else:
            pg.draw.rect(surface, self.color, self.rect)
        
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
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
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
        print(*values_to_plot)
        self.plot: Surface = py_plot(width, height, *values_to_plot)
        
    def draw(self, screen):
        screen.blit(self.plot, (self.x_right - self.plot.get_width(), self.y_bottom - self.plot.get_height()))
        
    def handle_event(self, _) -> bool:
        return False
        
#class HidableUi:
#    def __init__(self, win: Surface, element_inside: PyUiElement, show_animation_duration: int = 500, hide_animation_duration: int = 500) -> None:
#        self.show_animation_duration: int = show_animation_duration
#        self.hide_animation_duration: int = hide_animation_duration
#        
#        self.is_visible = False
#        self.animation_start_time = 0
#        self.animation_end_time = 0
#        
#        self.win: Surface = win
#        
#        self.show_hide_button: PyButton = self.create_button(10, 10, 200, DEFAULT_BUTTON_HEIGHT, "Show")
#        self.show_hide_button.action = self.show_hide_ui
#        
#        self.element_inside: PyUiElement = element_inside
#        
#        self.ui_elements: list[PyUiElement] = [self.show_hide_button, self.element_inside]
#        
#    def handle_event(self, event) -> None:
#        for element in self.ui_elements:
#            element.handle_event(event)
#
#    def draw(self) -> None:
#        if self.is_visible:
#            self.animate_ui()
#        
#        for element in self.ui_elements:
#            element.draw(self.win)
#        
#    def create_button(self, x: float, y: float, width: float, height: float, text: str) -> PyButton:
#        button = PyButton(text, x, y, width, height, DEFAULT_BUTTON_COLOR, DEFAULT_HOVER_COLOR, DEFAULT_FONT_COLOR, DEFAULT_FONT)
#        return button
#    
#    def show_hide_ui(self) -> None:
#        if not self.is_visible:
#            self.is_visible = True
#            self.animation_start_time = pg.time.get_ticks()
#            self.animation_end_time = self.animation_start_time + self.show_animation_duration
#    
#    def hide_ui(self) -> None:
#        if self.is_visible:
#            self.is_visible = False
#            self.animation_start_time = pg.time.get_ticks()
#            self.animation_end_time = self.animation_start_time + self.hide_animation_duration
#    
#    def animate_ui(self) -> None:
#        current_time = pg.time.get_ticks()
#        if current_time < self.animation_end_time:
#            progress = (current_time - self.animation_start_time) / (self.animation_end_time - self.animation_start_time)
#            
#            for element in self.ui_elements:
#                element.rect.y = -element.rect.height + int(progress * element.rect.height)
#        else:
#            for element in self.ui_elements:
#                element.rect.y = 10