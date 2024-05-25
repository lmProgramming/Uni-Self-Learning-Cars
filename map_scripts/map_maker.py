import os
import pygame as pg
from pygame import Vector2
from pygame.surface import Surface
from map_scripts.map import Wall, Gate
from map_scripts.map_reader import read_map_txt
from map_scripts.map_tools import format_map_name
from pygame_extensions.pyui_elements import PyInputBox, PyButton
from simulation.simulation_ui import PyMapMakerUi

pg.font.init()

WIDTH = 1280
HEIGHT = 960

USE_BG_IMG: bool = False
BG_IMG = pg.image.load(os.path.join("imgs", "bg_img.png"))
BG_COLOR = pg.Color(32, 32, 32)

class MapMaker:
    def __init__(self, walls=[], gates=[], starting_point=None, default_filename="") -> None:
        pg.init()
        pg.font.init()
        
        self.walls: list[Wall] = walls
        self.gates: list[Gate] = gates
        if starting_point is None:
            self.starting_point = Vector2(WIDTH // 2, HEIGHT // 2)
        else:
            self.starting_point = starting_point
        self.win: Surface = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        
        self.ui: PyMapMakerUi = PyMapMakerUi(self.win, self.close, self.save_map_to_file, WIDTH, HEIGHT)
        self.ui.set_map_name(default_filename)

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
        
        #topbar_rect = pg.Rect(0, 0, WIDTH, 40)
        #pg.draw.rect(win, (255, 255, 255), topbar_rect)    
        
    def close(self) -> None:
        pg.quit()
        
    # def create_map_name_input(x_centre, y_centre, width, height, text) -> PyInputBox:
    #     x, y = from_center_position_to_top_left(x_centre, y_centre, width, height)
    #     return PyInputBox(x, y, width, height, text)
# 
    # def create_back_button(x_centre, y_centre, width, height) -> PyButton:
    #     x, y = from_center_position_to_top_left(x_centre, y_centre, width, height)
    #     button = PyButton("Main Menu", x, y, width, height, color=(0, 255, 0), hover_color=(0, 200, 0), font_color=(100, 0, 0))
    #     button.action = clos
    #     return button

    #def create_blank_map():
    #    walls = []
    #    gates = []
    #    starting_point = Vector2(0, 0)
    #    return walls, gates, starting_point

    def edit_loop(self) -> None:   
        win = pg.display.set_mode((WIDTH, HEIGHT))
        clock = pg.time.Clock()

        run = True
        placing_wall = False
        placing_gate = False

        while run:
            clock.tick(60)
            
            self.draw_background(BG_IMG)

            m_x, m_y = pg.mouse.get_pos()
            mouse_pressed = pg.mouse.get_pressed()

            self.draw_window(win)
            
            self.ui.draw()
        
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                self.ui.handle_event(event)       

            pg.display.update()      
                        
            if self.ui.map_name_input.mouse_over(pg.mouse.get_pos()):
                continue

            if mouse_pressed[0]:
                self.place_wall(placing_wall, m_x, m_y)
                placing_wall = True            
            else:
                placing_wall = False

            if mouse_pressed[2]:
                self.place_gate(placing_gate, m_x, m_y)
                placing_gate = True
            else:
                placing_gate = False

            keys = pg.key.get_pressed()         

            if not self.ui.map_name_input_active:        
                if keys[pg.K_SPACE]:
                    self.starting_point = Vector2(m_x, m_y) 

    def place_gate(self, placing_gate, m_x, m_y):
        if not placing_gate:
            self.gates.append(Gate(len(self.gates), m_x, m_y, m_x, m_y))

        self.gates[-1].end_position = Vector2(m_x, m_y)

    def place_wall(self, placing_wall, m_x, m_y):
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
        
def create_new_map():
    map_maker = MapMaker()
    map_maker.edit_loop()

if __name__ == "__main__":
    create_new_map()