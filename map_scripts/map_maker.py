import os
import pygame as pg
from pygame import Vector2
from pygame.surface import Surface
from maps.map import Wall, Gate

from maps.map_reader import read_map_txt
from maps.map_tools import format_map_name
from py_input_field import InputBox

pg.font.init()

WIDTH = 1280
HEIGHT = 960

BG_IMG: Surface = pg.image.load(os.path.join("imgs", "bg_img.png"))

def draw_window(win, walls, gates, starting_point, bg_img, map_name) -> None:
    win.blit(bg_img, (0, 0))
        
    for wall in walls:
        wall.draw(win)

    for gate in gates:
        gate.draw(win)      
    
    pg.draw.circle(win, (0, 255, 0), starting_point, 10)     
    
    topbar_rect = pg.Rect(0, 0, WIDTH, 40)
    pg.draw.rect(win, (255, 255, 255), topbar_rect)    
        
    map_name.draw(win)

    pg.display.update()
    
def create_map_name_input(x_centre, y_centre, width, height, text) -> InputBox:
    x = x_centre - width // 2
    y = y_centre - height // 2
    return InputBox(x, y, width, height, text)

def create_blank_map():
    walls = []
    gates = []
    starting_point = Vector2(0, 0)
    return walls, gates, starting_point

def create_edit_map(walls=[], gates=[], starting_point=Vector2(0,0), map_filename="") -> None:       
    win = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    
    map_name_input = create_map_name_input(WIDTH // 2, 20, 140, 32, map_filename)

    run = True
    placing_wall = False
    placing_gate = False

    while run:
        clock.tick(60)

        m_x, m_y = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()

        if mouse_pressed[0]:
            place_wall(walls, placing_wall, m_x, m_y)
        else:
            placing_wall = False

        if mouse_pressed[2]:
            place_gate(gates, placing_gate, m_x, m_y)
        else:
            placing_gate = False

        keys = pg.key.get_pressed()

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

        if not map_name_input.active:            
            if keys[pg.K_s]:
                run = False
                pg.quit()
                save_data_to_file(walls, gates, starting_point, map_name_input.text)

            if keys[pg.K_SPACE]:
                starting_point = Vector2(m_x, m_y)

        draw_window(win, walls, gates, starting_point, BG_IMG, map_name_input)

def place_gate(gates, placing_gate, m_x, m_y):
    if not placing_gate:
        placing_gate = True
        gates.append(Gate(len(gates), m_x, m_y, m_x, m_y, 6))

    gates[-1].end_position = Vector2(m_x, m_y)

def place_wall(walls, placing_wall, m_x, m_y):
    if not placing_wall:
        placing_wall = True
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