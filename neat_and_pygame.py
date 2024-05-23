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
from simulation import simulation_loop
from simulation_setup import setup_generation
from simulation_config import SimulationConfig

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
Planuję dodać zbieranie i wizualizowanie statystyk agentów: np. zależność między fitness a czasem trenowania 
czy zależność między fitness a wielkością sieci neuronowej. Potrzebne więc będą moduły NumPy i Matplotlib. Lider każdej generacji byłby oznaczony 
podczas jazdy po mapie. Przy tworzeniu nowej symulacji, można podać parę parametrów, na przykład to, czy wszystkie samochody startują z punktu 
startowego pod tym samym kątem albo to, czy mapy zmieniają się co parę generacji, by ograniczyć overfitting.
Tryb konsolowy pozwoli zrobić wszystko, co jest dostępne w głównym menu GUI (w którym można zmienić parametry symulacji, uruchomić ją, wczytać 
zapis sieci neuronowych poprzednio wytrenowanych). W menu GUI podczas gry będzie można przejrzeć statystyki i wrócić do menu głównego, a także 
kliknąć samochód, by w rogu zobaczyć jego sieć neuronową z wartościami aktualizowanymi na żywo.
'''  

def run_new_generation(genomes: List[neat.DefaultGenome], config: neat.Config) -> None:    
    global GEN
    GEN += 1
    
    cars, walls, gates = setup_generation(genomes, config)
    
    simulation_loop(cars, walls, gates, config, False)

def run(config_path, simulation_config: SimulationConfig | None=None) -> None:
    print(simulation_config)
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    
    if simulation_config is not None:        
        config.pop_size = simulation_config.initial_population
        if simulation_config.ray_count is not None:
            config.genome_type.num_inputs = simulation_config.ray_count + NON_RAY_INPUTS
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(run_new_generation, 500)

    print(winner)

def main(simulation_config: SimulationConfig | None=None) -> None:    
    local_dir: str = os.path.dirname(__file__)
    config_path: str = os.path.join(local_dir, "config")
    run(config_path, simulation_config)
        
if __name__ == "__main__":    
    main()