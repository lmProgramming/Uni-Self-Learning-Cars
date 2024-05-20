import neat # type: ignore
import os
import pygame as pg
from pygame.font import Font
from pygame.math import Vector2
import random
from typing import List, Sequence

from pygame.surface import Surface
from car import Car, AICar, HumanCar

from map_reader import read_map_txt

pg.font.init()

WIDTH = 1280
HEIGHT = 960

PLAYER_ONLY = False
LOAD_MAP = True

GEN = 0

BG_IMG: Surface = pg.image.load(os.path.join("imgs", "bg_img.png"))

STAT_FONT: Font = pg.font.SysFont("comic sans", 25)

WHEEL_TURN_SPEED = 3

STARTING_CAR_POSITION = Vector2(450, HEIGHT - 472)

RAY_DISTANCE_KILL = 10

RAY_COUNT = 8
RAY_LENGTH = 200

'''
Do funkcjonalności chciałbym dodać jeszcze możliwość modyfikacji pliku konfiguracyjnego NEAT za pomocą GUI. 
GUI pozwalałoby na szeroką interakcję z mapami: dodanie nowej mapy, a także modyfikacja lub usunięcie istniejącej. 
Mapy planuję zapisać w formacie JSON lub CSV i przechowują pozycje ścian, pozycję startową oraz pozycje "bramek", które nagradzają 
samochód za przejechanie przez nie. Planuję dodać zbieranie i wizualizowanie statystyk agentów: np. zależność między fitness a czasem trenowania 
czy zależność między fitness a wielkością sieci neuronowej. Potrzebne więc będą moduły NumPy i Matplotlib. Lider każdej generacji byłby oznaczony 
podczas jazdy po mapie. Przy tworzeniu nowej symulacji, można podać parę parametrów, na przykład to, czy wszystkie samochody startują z punktu 
startowego pod tym samym kątem albo to, czy mapy zmieniają się co parę generacji, by ograniczyć overfitting.
Spróbuję użyć Cythona lub CPythona do optymalizacji wykrywania odległości do ścian przez samochody (podstawa ich poruszania się).
Tryb konsolowy pozwoli zrobić wszystko, co jest dostępne w głównym menu GUI (w którym można zmienić parametry symulacji, uruchomić ją, wczytać 
zapis sieci neuronowych poprzednio wytrenowanych). W menu GUI podczas gry będzie można przejrzeć statystyki i wrócić do menu głównego, a także 
kliknąć samochód, by w rogu zobaczyć jego sieć neuronową z wartościami aktualizowanymi na żywo.
Dodatkowo użyję Regexa, by sparsować na przykład nazwę pliku zawierającego poprzednie dane treningowe, by wyciągnąć z tego na przykład datę zapisu.
Użyję modułu abc, by stworzyć abstrakcyjną klasę Car oraz klasy dziedziczące PlayerCar i ComputerCar - będzie można więc przejechać się samochodem po 
mapie, by je przetestować.
'''

def draw_line(position, angle, line_length, line_width, color, screen) -> None:
    vector = Vector2()
    vector.from_polar((line_length, angle))
    pg.draw.line(screen, color, position, position+vector, line_width)

def draw_window(win, cars: List[Car], walls, gates, bg_img, score, gen, debug=False) -> None:
    win.blit(bg_img, (0, 0))
    
    text: pg.surface.Surface

    for car in cars:
        car.draw(win)
        if debug:
            for line in car.lines:
                line.set_debug_color()
                line.draw(win)
            text = STAT_FONT.render(str(int(car.genome.fitness)), True, (255, 255, 255))
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
    
    nets, ges, cars, walls, gates = setup_generation(genomes, config)
    
    simulation(nets, ges, cars, walls, gates)
    
def setup_generation(genomes, config) -> tuple[list, list, list[Car], list, list]:
    nets = []
    ges = []
    cars: List[Car] = []

    if LOAD_MAP:
        walls, gates, starting_point = read_map_txt()
    else:
        walls = []
        gates = []
        starting_point = STARTING_CAR_POSITION

    if PLAYER_ONLY:
        human_car: HumanCar = HumanCar(starting_point.x, starting_point.y, random.randrange(-180, 180))
        _, genome = genomes[0]
        genome.fitness = 0
        human_car.genome = genome
        human_car.generate_rays(RAY_COUNT, RAY_LENGTH)
        cars.append(human_car)
        
        ges.append(genomes[0][1])
        nets.append(neat.nn.FeedForwardNetwork.create(genomes[0][1], config))
    else:    
        for _, genome in genomes:
            genome.fitness = 0
            ges.append(genome)
            nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
            
            new_car = AICar(starting_point.x, starting_point.y, random.randrange(-180, 180))
            new_car.genome = genome
            new_car.generate_rays(RAY_COUNT, RAY_LENGTH)
            new_car.set_neural_net(nets[-1])
            cars.append(new_car)
            
    return nets, ges, cars, walls, gates
    
def simulation(nets: List[neat.nn.FeedForwardNetwork], ges: List[neat.DefaultGenome], cars: List[Car], walls, gates) -> None:
    win: pg.surface.Surface = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    score = 0
    run = True
    frames = 0
    while run:
        clock.tick(60)
                    
        if check_if_quit():
            run = False
            pg.quit()
            quit()
            
        i = 0
        while i < len(cars):
            genome: neat.DefaultGenome
            car: Car
            genome, car = ges[i], cars[i]

            car.calculate_line_distances(walls)
            outputs: Vector2 = car.get_desired_movement()

            car.move_forward(outputs[0])
            car.steer(outputs[1])    

            if car.check_if_in_next_gate(gates):
                genome.fitness += 10

            genome.fitness += car.speed / 60
            
            if car.get_shortest_last_distance() < RAY_DISTANCE_KILL:
                car.die()
                
            if car.dead:
                genome.fitness -= 10

                nets.pop(i)
                ges.pop(i)
                cars.pop(i)
            else:
                i += 1
                
        for car in cars:
            car.move()

        if len(cars) == 0 or frames > 60 * (10 + GEN):
            return

        score = max([car.genome.fitness for car in cars])
        draw_window(win, cars, walls, gates, BG_IMG, score, GEN, True)

        frames += 1

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(run_new_generation, 500)

    print(winner)
    
def get_ray_count_from_config():
    with open('config', 'r') as f:
        for line in f:
            if line.startswith("num_inputs"):
                return int(line.strip().split(" = ")[1])
    return 0

def main() -> None:
    global RAY_COUNT
    RAY_COUNT = get_ray_count_from_config()
    
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config")
    run(config_path)
        
if __name__ == "__main__":    
    main()