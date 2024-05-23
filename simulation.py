import os
import pygame as pg
from pygame.math import Vector2
from typing import List, Sequence
from pygame_input import PyButton
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

class PySimulationUi:
    def __init__(self, skip_generation_button: PyButton) -> None:
        self.skip_generation_button: PyButton = skip_generation_button
        
    def handle_event(self, event) -> None:
        if self.skip_generation_button.is_clicked(event):
            ...

    def draw(self, win: Surface) -> None:
        self.skip_generation_button.draw(win)

class Simulation:
    def __init__(self, cars: List[Car], walls, gates, config=None, infinite_time: bool=False):
        self.cars: List[Car] = cars
        self.walls = walls
        self.gates = gates
        self.config = config
        self.infinite_time: bool = infinite_time
        self.win: pg.surface.Surface = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.score: float = 0
        self.frames = 0
        
    def draw_simulation(self, bg_img, gen, debug=False) -> None:
        self.win.blit(bg_img, (0, 0))
        
        text: pg.surface.Surface

        for car in self.cars:
            if debug:
                for line in car.rays:
                    line.set_debug_color()
                    line.draw_debug(self.win)
            car.draw(self.win)        
            if debug:
                text = STAT_FONT.render(str(int(car.get_score())), True, (255, 255, 255))
                self.win.blit(text, car.get_centre_position())

        for wall in self.walls:
            wall.draw(self.win)

        for gate in self.gates:
            gate.draw(self.win)
            if debug:
                text = STAT_FONT.render(str(gate.num), True, (255, 255, 255))
                self.win.blit(text, gate.get_centre_position())

        text = STAT_FONT.render("Score: {:.2f}".format(self.score), True, (255, 255, 255))
        self.win.blit(text, (WIDTH - 10 - text.get_width(), 10))

        text = STAT_FONT.render("Gen: " + str(gen), True, (255, 255, 255))
        self.win.blit(text, (10, 10))

        pg.display.update()
        
    def draw_ui(self, win: Surface, skip_generation_button: PyButton) -> None:
        skip_generation_button.draw(win)
        pg.display.update()
        
    def draw_neural_network(self, win: Surface, filename: str) -> None:
        neural_net_image = pg.image.load(filename)
        
        win.blit(neural_net_image, (100, 100))
        
    def check_if_quit(self) -> bool:
        keys: Sequence[bool] = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True

        return keys[pg.K_ESCAPE]

    def input(self) -> None:
        m_x, m_y = pg.mouse.get_pos()
        mouse_pressed: tuple[bool, bool, bool] | tuple[bool, bool, bool, bool, bool] = pg.mouse.get_pressed()

        if mouse_pressed[0]:
            print(m_x, ",", m_y)  

    def selected_car(self, cars: List[Car], mouse_pos: Vector2) -> Car | None:
        for car in cars:
            if car.rect.collidepoint(mouse_pos.x, mouse_pos.y):
                return car
        return None

    def process_input(self, cars, config, win) -> None:
        mouse_position = Vector2(pg.mouse.get_pos())
        mouse_pressed: Sequence[bool] = pg.mouse.get_pressed()

        if mouse_pressed[0] and config is not None:
            self.handle_car_selection(cars, mouse_position, config, win)

    def handle_car_selection(self, cars: List[Car], mouse_pos: Vector2, config, win) -> None:
        selected: Car | None = self.selected_car(cars, mouse_pos)
        if selected and isinstance(selected, AICar):
            visualize.draw_net(config, selected.genome, view=False, filename="neural_net", fmt="png")  
            self.draw_neural_network(win, "neural_net.png")            

    def simulation_loop(self) -> None:
        win: pg.surface.Surface = pg.display.set_mode((WIDTH, HEIGHT))
        clock = pg.time.Clock()

        score: float = 0
        frames = 0
        while len(self.cars) > 0 and (frames < 60 * (10 + GEN) or self.infinite_time):
            clock.tick(60)        

            score = max([score] + [car.get_score() for car in self.cars])
                        
            if self.check_if_quit():
                pg.quit()
                quit()
                
            self.process_input(self.cars, self.config, win)

            # keys: ScancodeWrapper = pg.key.get_pressed()
                
            i = 0
            while i < len(self.cars):
                car: Car = self.cars[i]
                
                car.calculate_line_distances(self.walls)
                outputs: Vector2 = car.get_desired_movement()

                car.move_forward(outputs[0])
                car.steer(outputs[1])    

                if car.check_if_in_next_gate(self.gates):
                    car.get_reward(100)

                car.get_reward(car._speed / 60)
                
                if car.get_shortest_last_distance() < RAY_DISTANCE_KILL:
                    car.get_reward(-50)

                    self.cars.pop(i)
                else:
                    i += 1                
                    
            for car in self.cars:
                car.move()

            frames += 1
            
            self.draw_simulation(BG_IMG, GEN, True)
