import pygame as pg
from pygame_extensions.pyui_elements import PyButton, PyUiElement
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
        return x, y, width, height
    
    def bottom_left_to_top_left(self, x: float, y: float, width: float, height: float) -> tuple:
        return x, y - height, width, height
    
class PySimulationUi(PyDefaultUi):
    def __init__(self, win: Surface, go_back_action, skip_generation_action) -> None:
        super().__init__(win, go_back_action)
        self.skip_generation_button: PyButton = self.create_button(self.back_button.rect.bottomright[0] + DEFAULT_SPACE_BETWEEN_BUTTONS, 10, 200, DEFAULT_BUTTON_HEIGHT, "Skip Generation")
        self.skip_generation_button.action = skip_generation_action
        
        self.ui_elements.append(self.skip_generation_button)
       
class NeatDiagram:
    def __init__(self, win: Surface, bottom_x: float, bottom_y: float, diagram_filename: str) -> None:
        self.win: Surface = win
        self.diagram_filename: str = diagram_filename
        self.bottom_x: float = bottom_x
        self.bottom_y: float = bottom_y
        self.neural_net_image: Surface | None = pg.image.load(diagram_filename)    
        
    def draw(self) -> None:   
        if self.neural_net_image is not None:     
            y: float = self.bottom_y - self.neural_net_image.get_height()     
            self.win.blit(self.neural_net_image, (self.bottom_x, y))
            
class PyNeatSimulationUi(PySimulationUi):
    CLOSE_BUTTON_WIDTH = 200
    
    def __init__(self, win: Surface, go_back_action, skip_generation_action) -> None:
        super().__init__(win, go_back_action, skip_generation_action)
        self.neat_diagram: NeatDiagram | None = None
        self.close_button: PyButton | None = None
        
    def draw(self) -> None:
        super().draw()
        if self.neat_diagram is not None:
            self.neat_diagram.draw()
        
    def create_neat_diagram(self, bottom_x: float, bottom_y: float, diagram_filename: str) -> None:
        self.neat_diagram = NeatDiagram(self.win, bottom_x, bottom_y, diagram_filename)
        button_position = self.bottom_left_to_top_left(self.neat_diagram.bottom_x, self.neat_diagram.bottom_y, self.CLOSE_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT)
        self.close_button = self.create_button(*button_position, "Close")
        self.close_button.connect(self.close)
        self.ui_elements.append(self.close_button)
        
    def close(self):
        self.neat_diagram = None        
    
        
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
                