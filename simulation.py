import os
import pygame as pg
from pygame.math import Vector2
from typing import List, Sequence

from pygame.surface import Surface
from cars.car import Car, AICar
import visualize

pg.font.init()

pg.display.set_caption("Simulation")

WIDTH = 1280
HEIGHT = 960

GEN = 0

BG_IMG = pg.image.load(os.path.join("imgs", "bg_img.png"))

STAT_FONT = pg.font.SysFont("arial", 25)

STARTING_CAR_POSITION = Vector2(WIDTH // 2, HEIGHT // 2)

RAY_DISTANCE_KILL: float = 10

def draw_line(position, angle, line_length, line_width, color, screen) -> None:
    vector = Vector2()
    vector.from_polar((line_length, angle))
    pg.draw.line(screen, color, position, position+vector, line_width)

def draw_window(win, cars: List[Car], walls, gates, bg_img, score, gen, debug=False) -> None:
    win.blit(bg_img, (0, 0))
    
    text: pg.surface.Surface

    for car in cars:
        if debug:
            for line in car.rays:
                line.set_debug_color()
                line.draw_debug(win)
        car.draw(win)        
        if debug:
            text = STAT_FONT.render(str(int(car.get_score())), True, (255, 255, 255))
            win.blit(text, car.get_centre_position())

    for wall in walls:
        wall.draw(win)

    for gate in gates:
        gate.draw(win)
        if debug:
            text = STAT_FONT.render(str(gate.num), True, (255, 255, 255))
            win.blit(text, gate.get_centre_position())

    text = STAT_FONT.render("Score: {:.2f}".format(score), True, (255, 255, 255))
    win.blit(text, (WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), True, (255, 255, 255))
    win.blit(text, (10, 10))

    pg.display.update()
    
def draw_neural_network(win: Surface, filename: str) -> None:
    neural_net_image = pg.image.load(filename)
    
    win.blit(neural_net_image, (100, 100))
    
def check_if_quit() -> bool:
    keys: Sequence[bool] = pg.key.get_pressed()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            return True

    return keys[pg.K_ESCAPE]

def input() -> None:
    m_x, m_y = pg.mouse.get_pos()
    mouse_pressed: tuple[bool, bool, bool] | tuple[bool, bool, bool, bool, bool] = pg.mouse.get_pressed()

    if mouse_pressed[0]:
        print(m_x, ",", m_y)  

def selected_car(cars: List[Car], mouse_pos: Vector2) -> Car | None:
    for car in cars:
        if car.rect.collidepoint(mouse_pos.x, mouse_pos.y):
            return car
    return None

def handle_car_selection(cars: List[Car], mouse_pos: Vector2, config, win) -> None:
    selected: Car | None = selected_car(cars, mouse_pos)
    if selected and isinstance(selected, AICar):
        visualize.draw_net(config, selected.genome, view=False, filename="neural_net", fmt="png")  
        draw_neural_network(win, "neural_net.png")            

def simulation_loop(cars: List[Car], walls, gates, config=None, infinite_time: bool=False) -> None:
    win: pg.surface.Surface = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    score: float = 0
    frames = 0
    while len(cars) > 0 and (frames < 60 * (10 + GEN) or infinite_time):
        clock.tick(60)        

        score = max([score] + [car.get_score() for car in cars])
                    
        if check_if_quit():
            pg.quit()
            quit()
            
        mouse_position = Vector2(pg.mouse.get_pos())
        mouse_pressed: Sequence[bool] = pg.mouse.get_pressed()

        if mouse_pressed[0] and config is not None:
            handle_car_selection(cars, mouse_position, config, win)

        # keys: ScancodeWrapper = pg.key.get_pressed()
            
        i = 0
        while i < len(cars):
            car: Car = cars[i]
            
            car.calculate_line_distances(walls)
            outputs: Vector2 = car.get_desired_movement()

            car.move_forward(outputs[0])
            car.steer(outputs[1])    

            if car.check_if_in_next_gate(gates):
                car.get_reward(100)

            car.get_reward(car._speed / 60)
            
            if car.get_shortest_last_distance() < RAY_DISTANCE_KILL:
                car.get_reward(-50)

                cars.pop(i)
            else:
                i += 1                
                
        for car in cars:
            car.move()

        frames += 1
        
        draw_window(win, cars, walls, gates, BG_IMG, score, GEN, True)