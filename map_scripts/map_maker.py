import os
import pygame as pg
from pygame import Vector2
from pygame.surface import Surface
from map_scripts.map import Wall, Gate
from map_scripts.map_reader import read_map_txt
from map_scripts.map_tools import format_map_name
from pygame_input import PyInputBox, PyButton

pg.font.init()

WIDTH = 1280
HEIGHT = 960

BG_IMG: Surface = pg.image.load(os.path.join("imgs", "bg_img.png"))

def draw_window(win, walls, gates, starting_point, bg_img, map_name_input, back_button) -> None:
    win.blit(bg_img, (0, 0))
        
    for wall in walls:
        wall.draw(win)

    for gate in gates:
        gate.draw(win)      
    
    pg.draw.circle(win, (0, 255, 0), starting_point, 10)     
    
    topbar_rect = pg.Rect(0, 0, WIDTH, 40)
    pg.draw.rect(win, (255, 255, 255), topbar_rect)    
    
    back_button.draw(win)
        
    map_name_input.draw(win)

    pg.display.update()
    
def clos():
    pg.display.set_mode((1, 1))
    
def create_map_name_input(x_centre, y_centre, width, height, text) -> PyInputBox:
    x, y = from_center_position_to_top_left(x_centre, y_centre, width, height)
    return PyInputBox(x, y, width, height, text)

def create_back_button(x_centre, y_centre, width, height) -> PyButton:
    x, y = from_center_position_to_top_left(x_centre, y_centre, width, height)
    button = PyButton("Main Menu", x, y, width, height, color=(0, 255, 0), hover_color=(0, 200, 0), font_color=(100, 0, 0))
    button.action = clos
    return button

def from_center_position_to_top_left(x_centre, y_centre, width, height) -> tuple:
    x = x_centre - width // 2
    y = y_centre - height // 2
    return x, y

def create_blank_map():
    walls = []
    gates = []
    starting_point = Vector2(0, 0)
    return walls, gates, starting_point

def create_edit_map(walls=[], gates=[], starting_point=Vector2(0,0), map_filename="") -> None:   
    win = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    
    map_name_input: PyInputBox = create_map_name_input(WIDTH // 2, 20, 140, 32, map_filename)
    back_button: PyButton = create_back_button(75, 20, 100, 32)

    run = True
    placing_wall = False
    placing_gate = False

    while run:
        clock.tick(60)

        m_x, m_y = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()

        if mouse_pressed[0]:
            place_wall(walls, placing_wall, m_x, m_y)
            placing_wall = True            
        else:
            placing_wall = False

        if mouse_pressed[2]:
            place_gate(gates, placing_gate, m_x, m_y)
            placing_gate = True
        else:
            placing_gate = False

        keys = pg.key.get_pressed()         

        if not map_name_input.active:            
            if keys[pg.K_s]:
                run = False
                pg.quit()
                save_data_to_file(walls, gates, starting_point, map_name_input.text)

            if keys[pg.K_SPACE]:
                starting_point = Vector2(m_x, m_y)

        draw_window(win, walls, gates, starting_point, BG_IMG, map_name_input, back_button)
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                save_data_to_file(walls, gates, starting_point, map_name_input.text)
            if not map_name_input.active:
                if event.type == pg.KEYDOWN and event.key == pg.K_z and len(walls) > 0:
                    walls.pop()
                if event.type == pg.KEYDOWN and event.key == pg.K_x and len(gates) > 0:
                    gates.pop()
            map_name_input.handle_event(event)            
            if back_button.handle_event(event):
                run = False  

def place_gate(gates, placing_gate, m_x, m_y):
    if not placing_gate:
        gates.append(Gate(len(gates), m_x, m_y, m_x, m_y, 6))

    gates[-1].end_position = Vector2(m_x, m_y)

def place_wall(walls, placing_wall, m_x, m_y):
    if not placing_wall:
        walls.append(Wall(m_x, m_y, m_x, m_y, 6))

    walls[-1].end_position = Vector2(m_x, m_y)

def save_data_to_file(walls, gates, starting_point, map_name: str):
    if map_name == "":
        raise ValueError("Map name cannot be empty")
    
    map_name = format_map_name(map_name)
        
    if len(gates) == 0:
        raise ValueError("Map must have at least one gate")
            
    with open(os.path.join("maps", map_name), 'w+') as f:
        f.write("walls: x1;x2;y1;y2\n")
        for wall in walls:
            line_text = (str(wall.start_position) + ";" + str(wall.end_position) + "\n").replace("[", "").replace("]", "").replace(" ", "")
            f.write(line_text)  
        f.write("\ngates: num;x1;x2;y1;y2\n")
        for gate in gates:
            line_text = (str(gate.num) + ";" + str(gate.start_position) + ";" + str(gate.end_position) + "\n").replace("[", "").replace("]", "").replace(" ", "")
            f.write(line_text)  
        f.write("\nstart: " + str(int(starting_point[0])) + ";" + str(int(starting_point[1])))
    quit()

if __name__ == "__main__":
    create_edit_map()