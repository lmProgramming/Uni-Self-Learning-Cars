import os
import pygame as pg
from pygame import Vector2
from pygame.key import ScancodeWrapper
from pygame.surface import Surface
from map_scripts.map import Wall, Gate
from map_scripts.map_reader import read_map_txt
from map_scripts.map_tools import format_map_name
from pygame_extensions.pyui_elements import PyInputBox, PyButton
from simulation.simulation_ui import PyMapMakerUi
import ctypes

WIDTH = 1280
HEIGHT = 960

USE_BG_IMG: bool = False
BG_IMG = pg.image.load(os.path.join("imgs", "bg_img.png"))
BG_COLOR = pg.Color(32, 32, 32)
            
def show_info_box(title, text, style) -> None:
    ctypes.windll.user32.MessageBoxW(0, text, title, style)
    
def ask_yes_no_question(title, text):
    result = ctypes.windll.user32.MessageBoxW(0, text, title, 4)
    return result == 6

class MapMaker:
    def __init__(self, walls=[], gates=[], starting_point=None, default_filename="") -> None:        
        self.walls: list[Wall] = walls
        self.gates: list[Gate] = gates
        self.starting_point: Vector2
        if starting_point is None:
            self.starting_point = Vector2(WIDTH // 2, HEIGHT // 2)
        else:
            self.starting_point = starting_point
        self.win: Surface = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.placing_wall = False
        self.placing_gate = False
        self.quit_pygame = False
        
        self.ui: PyMapMakerUi = PyMapMakerUi(self.win, self.ask_to_close, self.try_to_save, WIDTH, HEIGHT)
        self.ui.set_map_name(default_filename)
        
    def load_map(self, map_name: str) -> None:
        walls, gates, starting_point = read_map_txt(map_name)
        self.walls = walls
        self.gates = gates
        self.starting_point = starting_point

    def draw_background(self, bg_img: Surface) -> None:
        if USE_BG_IMG:
            self.win.blit(bg_img, (0, 0))
        else:
            self.win.fill(BG_COLOR)

    def draw_window(self, win) -> None:            
        for wall in self.walls:
            wall.draw(win)

        for gate in self.gates:
            gate.draw(win)      
        
        pg.draw.circle(win, (0, 255, 0), self.starting_point, 10)     
        
    def ask_to_close(self):
        close_app = ask_yes_no_question( "Go back to main menu", "You might lose changes. Are you sure?")
        if close_app:
            self.close()
            
    def try_to_save(self):
        try:
            self.save_map_to_file()
        except Exception as e:
            show_info_box("Error", str(e), 0)
        
    def close(self) -> None:
        self.quit_pygame = True

    def edit_loop(self) -> None:   
        win = pg.display.set_mode((WIDTH, HEIGHT))
        clock = pg.time.Clock()

        run = True
        self.placing_wall = False
        self.placing_gate = False

        while run:
            clock.tick(60)
            
            self.draw_background(BG_IMG)

            m_x, m_y = pg.mouse.get_pos()
            mouse_pressed = pg.mouse.get_pressed()

            self.draw_window(win)
            
            self.ui.draw()   
                        
            if not self.ui.map_name_input.mouse_over(pg.mouse.get_pos()):
                self.process_map_building(m_x, m_y, mouse_pressed)                
            
            pg.display.update()   
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                self.ui.handle_event(event)   
                
            if self.quit_pygame:
                run = False
                return

    def process_map_building(self, m_x, m_y, mouse_pressed) -> None:
        if mouse_pressed[0]:
            self.place_wall(self.placing_wall, m_x, m_y)
            self.placing_wall = True            
        else:
            self.placing_wall = False

        if mouse_pressed[2]:
            self.place_gate(self.placing_gate, m_x, m_y)
            self.placing_gate = True
        else:
            self.placing_gate = False

        keys: ScancodeWrapper = pg.key.get_pressed()         

        if not self.ui.map_name_input_active:        
            if keys[pg.K_SPACE]:
                self.starting_point = Vector2(m_x, m_y)

    def place_gate(self, placing_gate, m_x, m_y) -> None:
        if not placing_gate:
            self.gates.append(Gate(len(self.gates), m_x, m_y, m_x, m_y))

        self.gates[-1].end_position = Vector2(m_x, m_y)

    def place_wall(self, placing_wall, m_x, m_y) -> None:
        if not placing_wall:
            self.walls.append(Wall(m_x, m_y, m_x, m_y))

        self.walls[-1].end_position = Vector2(m_x, m_y)

    def save_map_to_file(self) -> None:
        map_name: str = self.ui.map_name
        
        if map_name == "":
            raise ValueError("Map name cannot be empty")
        
        map_name = format_map_name(map_name)
            
        if len(self.gates) == 0:
            raise ValueError("Map must have at least one gate")
                
        with open(os.path.join("maps", map_name), 'w+') as f:
            f.write("walls: x1;x2;y1;y2\n")
            for wall in self.walls:
                line_text = (str(wall.start_position) + ";" + str(wall.end_position) + "\n").replace("[", "").replace("]", "").replace(" ", "")
                f.write(line_text)  
            f.write("\ngates: num;x1;x2;y1;y2\n")
            for gate in self.gates:
                line_text = (str(gate.num) + ";" + str(gate.start_position) + ";" + str(gate.end_position) + "\n").replace("[", "").replace("]", "").replace(" ", "")
                f.write(line_text)  
            f.write("\nstart: " + str(int(self.starting_point[0])) + ";" + str(int(self.starting_point[1])))
        self.close()
        
def create_new_map() -> None:    
    pg.init()
    pg.font.init()
    pg.display.set_caption("Creating new map")
    
    map_maker = MapMaker()
    map_maker.edit_loop()
    
    pg.quit()
    
def edit_existing_map(file_name: str) -> None:    
    pg.init()
    pg.font.init()
    pg.display.set_caption("Editing map")
    
    map_maker = MapMaker()
    map_maker.load_map(file_name)
    map_maker.edit_loop()
    
    pg.quit()    

if __name__ == "__main__":
    create_new_map()