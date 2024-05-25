import pygame as pg
from pyui_elements import PyButton, PyUiElement
from pygame.surface import Surface

DEFAULT_BUTTON_COLOR = pg.Color(44, 45, 47)
DEFAULT_HOVER_COLOR = pg.Color(30, 31, 32)
DEFAULT_FONT_COLOR = pg.Color(138, 180, 247)
DEFAULT_FONT = pg.font.Font(None, 32)

DEFAULT_BUTTON_HEIGHT = 64
DEFAULT_SPACE_BETWEEN_BUTTONS = 20

class PyDefaultUi:
    def __init__(self, win: Surface, go_back_action) -> None:
        self.back_button: PyButton = self.create_button(10, 10, 200, DEFAULT_BUTTON_HEIGHT, "Main Menu")
        self.back_button.action = go_back_action
        
        self.ui_elements: list[PyUiElement] = [self.back_button]
        
        self.win: Surface = win
        
    def handle_event(self, event) -> None:
        for element in self.ui_elements:
            element.handle_event(event)

    def draw(self) -> None:
        for element in self.ui_elements:
            element.draw(self.win)
        
    def create_button(self, x: float, y: float, width: float, height: float, text: str) -> PyButton:
        button = PyButton(text, x, y, width, height, DEFAULT_BUTTON_COLOR, DEFAULT_HOVER_COLOR, DEFAULT_FONT_COLOR, DEFAULT_FONT)
        return button

    def from_center_position_to_top_left(self, x_centre: float, y_centre: float, width: float, height: float) -> tuple:
        x: float = x_centre - width // 2
        y: float = y_centre - height // 2
        return x, y
    
class PySimulationUi(PyDefaultUi):
    def __init__(self, win: Surface, go_back_action, skip_generation_action) -> None:
        super().__init__(win, go_back_action)
        self.skip_generation_button: PyButton = self.create_button(self.back_button.rect.bottomright[0] + DEFAULT_SPACE_BETWEEN_BUTTONS, 10, 200, DEFAULT_BUTTON_HEIGHT, "Skip Generation")
        self.skip_generation_button.action = skip_generation_action
        
        self.ui_elements.append(self.skip_generation_button)