import neat # type: ignore
import os
from neat.nn.feed_forward import FeedForwardNetwork # type: ignore
import pygame as pg
from pygame.font import Font
from pygame.key import ScancodeWrapper
from pygame.math import Vector2
import random
from typing import List, Sequence, Callable
from processing_functions import Linear, Quadratic

from pygame.surface import Surface
from cars.car import Car, AICar, HumanCar
from maps.map import Wall, Gate
import time
import visualize

from maps.map_reader import read_map_txt

pg.font.init()

pg.display.set_caption("Simulation")

WIDTH = 1280
HEIGHT = 960

PLAYER_ONLY = False
LOAD_MAP = True

GEN = 0

BG_IMG = pg.image.load(os.path.join("imgs", "bg_img.png"))

STAT_FONT = pg.font.SysFont("comic sans", 25)

STARTING_CAR_POSITION = Vector2(450, HEIGHT - 472)

RAY_DISTANCE_KILL: float = 10

RAY_COUNT: int = 8
RAY_LENGTH: float = 200

NON_RAY_INPUTS: int = 1

'''
Do funkcjonalności chciałbym dodać jeszcze możliwość modyfikacji pliku konfiguracyjnego NEAT za pomocą GUI. 
GUI pozwalałoby na szeroką interakcję z mapami: dodanie nowej mapy, a także modyfikacja lub usunięcie istniejącej. 
Planuję dodać zbieranie i wizualizowanie statystyk agentów: np. zależność między fitness a czasem trenowania 
czy zależność między fitness a wielkością sieci neuronowej. Potrzebne więc będą moduły NumPy i Matplotlib. Lider każdej generacji byłby oznaczony 
podczas jazdy po mapie. Przy tworzeniu nowej symulacji, można podać parę parametrów, na przykład to, czy wszystkie samochody startują z punktu 
startowego pod tym samym kątem albo to, czy mapy zmieniają się co parę generacji, by ograniczyć overfitting.
Spróbuję użyć Cythona lub CPythona do optymalizacji wykrywania odległości do ścian przez samochody (podstawa ich poruszania się).
Tryb konsolowy pozwoli zrobić wszystko, co jest dostępne w głównym menu GUI (w którym można zmienić parametry symulacji, uruchomić ją, wczytać 
zapis sieci neuronowych poprzednio wytrenowanych). W menu GUI podczas gry będzie można przejrzeć statystyki i wrócić do menu głównego, a także 
kliknąć samochód, by w rogu zobaczyć jego sieć neuronową z wartościami aktualizowanymi na żywo.
'''

def draw_line(position, angle, line_length, line_width, color, screen) -> None:
    vector = Vector2()
    vector.from_polar((line_length, angle))
    pg.draw.line(screen, color, position, position+vector, line_width)

def draw_window(win, cars: List[Car], walls, gates, bg_img, score, gen, debug=False) -> None:
    win.blit(bg_img, (0, 0))
    
    text: pg.surface.Surface

    for car in cars:
        if debug:
            for line in car.lines:
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

def run_new_generation(genomes: List[neat.DefaultGenome], config: neat.Config):    
    global GEN
    GEN += 1
    
    cars, walls, gates = setup_generation(genomes, config)
    
    simulation(cars, walls, gates, config, False)
    
def test_drive(processing_function: Callable[[float, float], float]=Linear) -> None:
    walls, gates, starting_point = setup_map()
            
    while True:        
        cars: List[Car] = spawn_player_cars(starting_point, processing_function)
        
        simulation(cars, walls, gates, infinite_time=True)
        time.sleep(0.1)
    
def setup_map() -> tuple[list, list, Vector2]:
    walls, gates, starting_point = read_map_txt()
    return walls, gates, starting_point
    
def setup_generation(genomes: List[neat.DefaultGenome], config, processing_function=Quadratic) -> tuple[list[Car], list, list]:
    cars: List[Car] = []
    
    walls: List[Wall]
    gates: List[Gate]
    starting_point: Vector2

    if LOAD_MAP:
        walls, gates, starting_point = read_map_txt()
    else:
        walls = []
        gates = []
        starting_point = STARTING_CAR_POSITION
 
    cars = spawn_ai_cars(genomes, config, starting_point, processing_function)
            
    return cars, walls, gates

def spawn_ai_cars(genomes: List[neat.DefaultGenome], config: neat.Config, starting_point, processing_function) -> List[Car]:
    cars: List[Car] = []
    
    for _, genome in genomes:
        genome.fitness = 0
        new_car = AICar(starting_point.x, starting_point.y, random.randrange(-180, 180))
        
        neural_net: FeedForwardNetwork = FeedForwardNetwork.create(genome, config)
        
        new_car.set_neural_net(neural_net)
        
        new_car.genome = genome
        new_car.generate_rays(RAY_COUNT, RAY_LENGTH, processing_function)
        cars.append(new_car)
        
    return cars

def spawn_player_cars(starting_point, processing_function, count: int=1) -> List[Car]:
    cars: List[Car] = []
    
    for _ in range(count):
        human_car: HumanCar = HumanCar(starting_point.x, starting_point.y, random.randrange(-180, 180))
        
        human_car.generate_rays(RAY_COUNT, RAY_LENGTH, processing_function)
        cars.append(human_car)
        
    return cars

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

def simulation(cars: List[Car], walls, gates, config=None, infinite_time: bool=False) -> None:
    win: pg.surface.Surface = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    score = 0
    frames = 0
    while len(cars) > 0 and (frames < 60 * (10 + GEN) or infinite_time):
        clock.tick(60)        

        score = max([car.get_score() for car in cars])
                    
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

            car.get_reward(car.speed / 60)
            
            if car.get_shortest_last_distance() < RAY_DISTANCE_KILL:
                car.get_reward(-5)

                cars.pop(i)
            else:
                i += 1                
                
        for car in cars:
            car.move()

        frames += 1
        
        draw_window(win, cars, walls, gates, BG_IMG, score, GEN, True)
        
def run(config_path) -> None:
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(run_new_generation, 500)

    print(winner)
    
def get_ray_count_from_config() -> int:
    with open('config', 'r') as f:
        for line in f:
            if line.startswith("num_inputs"):
                return int(line.strip().split(" = ")[1]) - NON_RAY_INPUTS
    return 0

def main() -> None:
    global RAY_COUNT
    RAY_COUNT = get_ray_count_from_config()
    
    local_dir: str = os.path.dirname(__file__)
    config_path: str = os.path.join(local_dir, "config")
    run(config_path)
        
if __name__ == "__main__":    
    main()