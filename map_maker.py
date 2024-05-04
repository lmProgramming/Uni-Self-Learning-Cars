import os
import pygame as pg
from pygame.math import Vector2
from neat_and_pygame import Wall, Gate

from map_reader import read_map_txt

pg.font.init()

WIDTH = 1280
HEIGHT = 960

READ_MAP = True

CAR_IMG = pg.image.load(os.path.join("imgs", "car_img.png"))

CAR_WIDTH = CAR_IMG.get_width()
CAR_HEIGHT = CAR_IMG.get_height()

BG_IMG = pg.image.load(os.path.join("imgs", "bg_img.png"))

def draw_window(win, borders, gates, starting_point, bg_img):
    win.blit(bg_img, (0, 0))

    for border in borders:
        border.draw(win)

    for gate in gates:
        gate.draw(win)

    pg.draw.circle(win, (0, 255, 0), starting_point, 10)

    pg.display.update()


def main():       
    win = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    if READ_MAP:
        borders, gates, starting_point = read_map_txt()
    else:
        borders = []
        gates = []
        starting_point = (0, 0)

    run = True
    placing_wall = False
    placing_gate = False

    while run:
        clock.tick(60)

        m_x, m_y = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()

        if mouse_pressed[0]:
            if not placing_wall:
                placing_wall = True
                borders.append(Wall(m_x, m_y, m_x, m_y, 6))

            borders[-1].end_position = Vector2(m_x, m_y)
        else:
            placing_wall = False

        if mouse_pressed[2]:
            if not placing_gate:
                placing_gate = True
                gates.append(Gate(len(gates), m_x, m_y, m_x, m_y, 6))

            gates[-1].end_position = Vector2(m_x, m_y)
        else:
            placing_gate = False

        keys = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                save_data_to_file(borders, gates, starting_point, backup=True)
            if event.type == pg.KEYDOWN and event.key == pg.K_z and len(borders) > 0:
                borders.pop()
            if event.type == pg.KEYDOWN and event.key == pg.K_x and len(gates) > 0:
                gates.pop()

        if keys[pg.K_ESCAPE]:
            run = False
            pg.quit()
            save_data_to_file(borders, gates, starting_point, backup=True)
        
        if keys[pg.K_s]:
            run = False
            pg.quit()
            save_data_to_file(borders, gates, starting_point)

        if keys[pg.K_SPACE]:
            starting_point = (m_x, m_y)

        draw_window(win, borders, gates, starting_point, BG_IMG)


def save_data_to_file(borders, gates, starting_point, backup=False):
    with open('maps/map.txt' if not backup else 'maps/backup.txt', 'w+') as f:
        f.write("borders: x1,x2,y1,y2\n")
        for border in borders:
            line_text = (str(border.start_position) + "," + str(border.end_position) + "\n").replace("[", "").replace("]", "").replace(" ", "")
            print(line_text, end=None)
            f.write(line_text)  
        f.write("\ngates: num,x1,x2,y1,y2\n")
        for gate in gates:
            line_text = (str(gate.num) + "," + str(gate.start_position) + "," + str(gate.end_position) + "\n").replace("[", "").replace("]", "").replace(" ", "")

            print(line_text, end=None)
            f.write(line_text)  
        f.write("\nstart," + str(int(starting_point[0])) + "," + str(int(starting_point[1])))
    quit()

if __name__ == "__main__":
    main()