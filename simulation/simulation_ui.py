import pygame as pg
from pygame.font import Font
from pygame_extensions.pyui_elements import PyButton, PyUiElement, PyInputBox, PyImage, PyPlot
from pygame.surface import Surface
from simulation.statistics import SimulationStatistics
from simulation.pygame_plot import py_plot

DEFAULT_BUTTON_COLOR = pg.Color(44, 45, 47)
DEFAULT_HOVER_COLOR = pg.Color(30, 31, 32)
DEFAULT_FONT_COLOR = pg.Color(138, 180, 247)
DEFAULT_FONT = pg.font.Font(None, 32)

DEFAULT_BUTTON_HEIGHT = 64
DEFAULT_SPACE_BETWEEN_BUTTONS = 20

class PyDefaultUi:
    def __init__(self, win: Surface, go_back_action) -> None:
        self.back_button: PyButton = self.create_button(10, 10, 200, DEFAULT_BUTTON_HEIGHT, "Main Menu")
        self.back_button.connect(go_back_action)
        
        self.ui_elements: list[PyUiElement] = [self.back_button]
        
        self.win: Surface = win
        self.font: Font = DEFAULT_FONT
        
    def set_font(self, font: Font) -> None:
        self.font = font
        
    def handle_event(self, event) -> None:
        for element in self.ui_elements:
            element.handle_event(event)

    def draw(self) -> None:
        for element in self.ui_elements:
            element.draw(self.win)
        
    def create_button(self, x: float, y: float, width: float, height: float, text: str) -> PyButton:
        button = PyButton(text, x, y, width, height, DEFAULT_BUTTON_COLOR, DEFAULT_HOVER_COLOR, DEFAULT_FONT_COLOR, DEFAULT_FONT)
        return button

    def from_center_position_to_top_left(self, x_centre: float, y_centre: float, width: float, height: float) -> tuple[float, float, float, float]:
        x: float = x_centre - width // 2
        y: float = y_centre - height // 2
        return x, y, width, height
    
    def bottom_left_to_top_left(self, x: float, y: float, width: float, height: float) -> tuple[float, float, float, float]:
        return x, y - height, width, height
    
class PySimulationUi(PyDefaultUi):
    PLOT_WIDTH = 400
    PLOT_HEIGHT = 200
    
    CLOSE_BUTTON_WIDTH = 150
    CLOSE_BUTTON_HEIGHT = 50
    
    def __init__(self, win: Surface, go_back_action, skip_generation_action) -> None:
        super().__init__(win, go_back_action)
        self.skip_generation_button: PyButton = self.create_button(self.back_button.rect.bottomright[0] + DEFAULT_SPACE_BETWEEN_BUTTONS, 10, 200, DEFAULT_BUTTON_HEIGHT, "Skip Generation")
        self.skip_generation_button.action = skip_generation_action
                
        self.plot: Surface | None = None
        
        self.ui_elements.append(self.skip_generation_button)
        
    def draw_simulation_info(self, score, average_score, generation_number, right_x_position: float) -> None:
        score_text: Surface = self.font.render("Highest Score - {:.2f}".format(score), True, (255, 255, 255))
        self.win.blit(score_text, (right_x_position - score_text.get_width(), 10))
        
        score_text: Surface = self.font.render("Average Score - {:.2f}".format(average_score), True, (255, 255, 255))
        self.win.blit(score_text, (right_x_position - score_text.get_width(), 50))

        gen_text: Surface = self.font.render(f"Generation {generation_number}", True, (255, 255, 255))
        self.win.blit(gen_text, (right_x_position - gen_text.get_width(), 90))
                
    def plot_values(self, right_x: float, bottom_y: float, values_to_plot: list[SimulationStatistics], show_plot: bool = False) -> None:
        self.plot: Surface = PyPlot(
            right_x, 
            bottom_y, 
            self.PLOT_WIDTH, 
            self.PLOT_HEIGHT, 
            ("max score", [value.max_score for value in values_to_plot]), 
            ("avg score", [value.average_score for value in values_to_plot]))
        
        button_position: tuple[float, float, float, float] = (
            right_x - self.CLOSE_BUTTON_WIDTH - 3, 
            bottom_y - self.PLOT_HEIGHT - self.CLOSE_BUTTON_HEIGHT - 3, 
            self.CLOSE_BUTTON_WIDTH, 
            self.CLOSE_BUTTON_HEIGHT)
        
        self.close_plot_button: PyButton = self.create_button(*button_position, text="Close")
        self.close_plot_button.connect(self.close_plot)
        
        self.show_plot_button: PyButton = self.create_button(
            right_x - self.CLOSE_BUTTON_WIDTH - 3, 
            bottom_y - self.CLOSE_BUTTON_HEIGHT - 3, 
            self.CLOSE_BUTTON_WIDTH, 
            self.CLOSE_BUTTON_HEIGHT, 
            "Show Plot")
        
        self.show_plot_button.connect(self.show_plot)
        
        if show_plot:
            self.show_plot()
        else:
            self.close_plot()
        
    def close_plot(self) -> None:
        if self.close_plot_button in self.ui_elements:
            self.ui_elements.remove(self.close_plot_button)        
            self.ui_elements.remove(self.plot)  
          
        self.ui_elements.append(self.show_plot_button)
        
    def show_plot(self) -> None:
        self.ui_elements.append(self.plot)
        self.ui_elements.append(self.close_plot_button)
        
        if self.show_plot_button in self.ui_elements:        
            self.ui_elements.remove(self.show_plot_button)
            
class PyNeatSimulationUi(PySimulationUi):    
    def __init__(self, win: Surface, go_back_action, skip_generation_action) -> None:
        super().__init__(win, go_back_action, skip_generation_action)
        self.neat_diagram: PyImage | None = None
        self.close_button: PyButton | None = None
        
    def create_neat_diagram(self, left_x: float, bottom_y: float, diagram_filename: str) -> None:
        self.neat_diagram = PyImage(self.win, left_x, bottom_y, diagram_filename)        
        self.ui_elements.append(self.neat_diagram) 
        
        button_position: tuple[float, float, float, float] = self.bottom_left_to_top_left(
            self.neat_diagram.bottom_x + 3, 
            self.neat_diagram.bottom_y - self.neat_diagram.image.get_height() - 3, 
            self.CLOSE_BUTTON_WIDTH, 
            self.CLOSE_BUTTON_HEIGHT)        
        
        self.close_button = self.create_button(*button_position, text="Close")
        self.close_button.connect(self.close_diagram)
        self.ui_elements.append(self.close_button) 
        
    def close_diagram(self) -> None:
        self.ui_elements.remove(self.close_button)        
        self.ui_elements.remove(self.neat_diagram)        
        self.neat_diagram = None

class PyMapMakerUi(PyDefaultUi):
    def __init__(self, win: Surface, go_back_action, save_map_action, map_width: float, map_height: float) -> None:
        super().__init__(win, go_back_action)     
          
        self.map_name_input: PyInputBox = PyInputBox(*self.from_center_position_to_top_left(map_width // 2, 37, 300, 32), "Input map name here...") 
        self.ui_elements.append(self.map_name_input)
        
        save_map_position: tuple[float, float, float, float] = self.from_center_position_to_top_left(
            map_width // 2, 
            map_height - DEFAULT_BUTTON_HEIGHT - 20, 
            200, 
            DEFAULT_BUTTON_HEIGHT)
        self.save_map_button: PyButton = self.create_button(*save_map_position, "Save")
        self.save_map_button.connect(save_map_action)        
        self.ui_elements.append(self.save_map_button)
        
    def draw(self) -> None:
        super().draw()
        
    @property    
    def map_name(self) -> str:
        return self.map_name_input.text
    
    @property
    def map_name_input_active(self) -> bool:
        return self.map_name_input.active
    
    def set_map_name(self, name: str) -> None:
        self.map_name_input.text = name
        self.map_name_input.render_text()
        self.map_name_input.update_width()