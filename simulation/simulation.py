import os
import pygame as pg
from pygame.font import Font
from pygame.math import Vector2
from typing import List, Sequence
from pygame_extensions.pyui_elements import PyButton
from pygame.surface import Surface
from cars.car import Car, AICar
import visualization.visualize as visualize
from simulation.simulation_ui import PySimulationUi, PyNeatSimulationUi

WIDTH = 1280
HEIGHT = 960

USE_BG_IMG: bool = False
BG_IMG = pg.image.load(os.path.join("imgs", "bg_img.png"))
BG_COLOR = pg.Color(32, 32, 32)

RAY_DISTANCE_KILL: float = 10

DEBUG_KEY = pg.K_r

class BreakTrainingException(Exception):
    pass

class Simulation:
    def __init__(self, cars: List[Car], walls, gates, generation_number: int, config=None, infinite_time: bool=False) -> None:        
        self.cars: List[Car] = cars
        self.walls = walls
        self.gates = gates
        self.config = config
        self.infinite_time: bool = infinite_time
        self.win: pg.surface.Surface = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.score: float = 0
        self.frames: int = 0
        self.generation_number: int = generation_number
        self.simulation_ui: PySimulationUi | PyNeatSimulationUi
        self.create_appropriate_ui()
        self.font: Font = pg.font.SysFont("arial", 25)
                
    def create_appropriate_ui(self) -> None:
        if not self.is_neat_simulation:
            self.simulation_ui = PySimulationUi(self.win, self.end_training, self.end_simulation)
        else:
            self.simulation_ui = PyNeatSimulationUi(self.win, self.end_training, self.end_simulation)
            
    @property
    def is_neat_simulation(self) -> bool:
        return self.config is not None
        
    def draw_background(self, bg_img: Surface) -> None:
        self.win.blit(bg_img, (0, 0))
        
    def refresh(self):      
        pg.display.update()
        
    def end_simulation(self) -> None:
        self.cars = []     
        
    def end_training(self):
        raise BreakTrainingException("Training ended.")
        
    def draw_simulation(self, bg_img, gen, debug=False) -> None:
        if USE_BG_IMG:
            self.win.blit(bg_img, (0, 0))
        else:
            self.win.fill(BG_COLOR)
        
        text: pg.surface.Surface
       
        for gate in self.gates:
            gate.draw(self.win)
            if debug:
                text = self.font.render(str(gate.num), True, (255, 255, 255))
                self.win.blit(text, gate.get_centre_position())

        for car in self.cars:
            if debug:
                for line in car.rays:
                    line.draw_debug(self.win)
            car.draw(self.win)        
            if debug:
                text = self.font.render(str(int(car.get_score())), True, (255, 255, 255))
                self.win.blit(text, car.get_centre_position())

        for wall in self.walls:
            wall.draw(self.win)

        text = self.font.render("Score: {:.2f}".format(self.score), True, (255, 255, 255))
        self.win.blit(text, (WIDTH - 10 - text.get_width(), 10))

        text = self.font.render("Gen: " + str(gen), True, (255, 255, 255))
        self.win.blit(text, (10, 10))
        
    def check_if_quit(self, event) -> bool:
        keys: Sequence[bool] = pg.key.get_pressed()

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
            
        for event in pg.event.get():            
            if self.check_if_quit(event):
                pg.quit()
                quit()
            self.simulation_ui.handle_event(event)

    def handle_car_selection(self, cars: List[Car], mouse_pos: Vector2, config, win) -> None:
        selected: Car | None = self.selected_car(cars, mouse_pos)
        if selected and isinstance(self.simulation_ui, PyNeatSimulationUi) and isinstance(selected, AICar):
            visualize.draw_net(config, selected.genome, view=False, filename="neural_net", fmt="png")  
            self.simulation_ui.create_neat_diagram(0, HEIGHT, "neural_net.png")            

    def simulation_loop(self) -> None:
        win: pg.surface.Surface = pg.display.set_mode((WIDTH, HEIGHT), pg.SRCALPHA)
        clock = pg.time.Clock()

        score: float = 0
        frames = 0
        while len(self.cars) > 0 and (frames < 60 * (10 + self.generation_number) or self.infinite_time):
            clock.tick(60)        
            
            self.draw_background(BG_IMG)

            score = max([score] + [car.get_score() for car in self.cars])
                                        
            self.process_input(self.cars, self.config, win)
                
            i = 0
            while i < len(self.cars):
                car: Car = self.cars[i]
                
                car.calculate_line_distances_quick(self.walls)
                outputs: Vector2 = car.get_desired_movement()

                car.move_forward(outputs[0])
                car.steer(outputs[1])    

                if car.check_if_in_next_gate(self.gates):
                    car.reward(100)

                car.reward(car._speed / 60)
                
                if car.get_shortest_last_distance() < RAY_DISTANCE_KILL:
                    car.reward(-50)

                    self.cars.pop(i)
                else:
                    i += 1                
                    
            for car in self.cars:
                car.move()

            frames += 1
            
            debug: bool = pg.key.get_pressed()[DEBUG_KEY]
            self.draw_simulation(BG_IMG, self.generation_number, debug)
            self.simulation_ui.draw()
            
            self.refresh()
