import pygame as pg
from typing import Callable

pg.font.init()

COLOR_INACTIVE = pg.Color('gray')
COLOR_ACTIVE = pg.Color('black')
FONT = pg.font.Font(None, 32)

class PyInputBox:
    def __init__(self, x, y, w, h, text='') -> None:
        self.rect = pg.Rect(x, y, w, h)
        self.color: pg.Color = COLOR_INACTIVE
        self.text: str = text
        self.txt_surface: pg.Surface = FONT.render(text, True, self.color)
        self.active: bool = False

    def handle_event(self, event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.set_active(not self.active)
            else:
                self.set_active(False)
                
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.set_active(False)
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)
                
    def set_active(self, active: bool) -> None:
        self.active = active
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self) -> None:
        # Resize the box if the text is too long.
        width: int = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen) -> None:
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
        
class PyButton:
    def __init__(self, text, x, y, width, height, color, hover_color, font_color) -> None:
        self.text = text
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font_color = font_color
        self.font = pg.font.SysFont(None, 40)
        self.action: Callable[[], None]
    
    def draw(self, surface) -> None:
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pg.draw.rect(surface, self.hover_color, self.rect)
        else:
            pg.draw.rect(surface, self.color, self.rect)
        
        text_surface: pg.Surface = self.font.render(self.text, True, self.font_color)
        text_rect: pg.Rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def connect(self, action) -> None:
        self.action = action
        
    def check_if_clicked(self, event) -> None:
        print(event)
        print(self.is_clicked(event))
        if self.is_clicked(event):
            self.action()
                
    def is_clicked(self, event) -> bool:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False