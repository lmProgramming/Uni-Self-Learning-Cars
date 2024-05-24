import neat # type: ignore
import os
import pygame as pg
from pygame.math import Vector2
from typing import List, Optional
from simulation import Simulation
from simulation_setup import setup_generation
from simulation_config import SimulationConfig
from map_scripts.map_tools import DEFAULT_MAP
import random

pg.font.init()

pg.display.set_caption("Simulation")

WIDTH = 1280
HEIGHT = 960

PLAYER_ONLY = False
LOAD_MAP = True

STARTING_CAR_POSITION = Vector2(450, HEIGHT - 472)

RAY_DISTANCE_KILL: float = 10

RAY_COUNT: int = 8
RAY_LENGTH: float = 200

NON_RAY_INPUTS: int = 2

'''
Planuję dodać zbieranie i wizualizowanie statystyk agentów: np. zależność między fitness a czasem trenowania 
czy zależność między fitness a wielkością sieci neuronowej. Potrzebne więc będą moduły NumPy i Matplotlib. Lider każdej generacji byłby oznaczony 
podczas jazdy po mapie. Tryb konsolowy pozwoli zrobić wszystko, co jest dostępne w głównym menu GUI (w którym można zmienić parametry symulacji, uruchomić ją, wczytać 
zapis sieci neuronowych poprzednio wytrenowanych). W menu GUI podczas gry będzie można przejrzeć statystyki i wrócić do menu głównego, a także 
kliknąć samochód, by w rogu zobaczyć jego sieć neuronową z wartościami aktualizowanymi na żywo.
'''
class NeatRun:
    def __init__(self, config_path, simulation_config: Optional[SimulationConfig] = None) -> None:
        self.gen: int = 0

        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, config_path)

        self.simulation_config: Optional[SimulationConfig] = None
        if simulation_config is not None:
            self.simulation_config: SimulationConfig = simulation_config
            NeatRun.inject_simulation_config(self.config, simulation_config)
        
    @staticmethod        
    def get_ray_count_from_config(config) -> int:
        return config.genome_config.num_inputs - NON_RAY_INPUTS
    
    def pick_map(self) -> str:
        if self.simulation_config is None:
            return DEFAULT_MAP
        return random.choice(self.simulation_config.map_pool)

    def run_new_generation(self, genomes: List[neat.DefaultGenome], config: neat.Config) -> None:
        self.gen += 1

        arguments = {
            "map_name": self.pick_map(),
            "genomes": genomes, 
            "config": config, 
            "ray_count": NeatRun.get_ray_count_from_config(config)}
        if self.simulation_config is not None:
            arguments["random_angle"] = self.simulation_config.random_angle
            
        cars, walls, gates = setup_generation(**arguments)

        simulation = Simulation(cars, walls, gates, self.gen, config, infinite_time=False)
        simulation.simulation_loop()    

    @staticmethod
    def inject_simulation_config(config: neat.Config, simulation_config: SimulationConfig) -> None:
        config.pop_size = simulation_config.initial_population
        config.genome_config.num_hidden = simulation_config.hidden_layers
        if simulation_config.ray_count is not None:
            config.genome_config.num_inputs = simulation_config.ray_count + NON_RAY_INPUTS

    def run(self) -> None:
        p = neat.Population(self.config)

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(self.run_new_generation, 500)

        print(winner)

def main(simulation_config: Optional[SimulationConfig] = None) -> None:    
    local_dir: str = os.path.dirname(__file__)
    config_path: str = os.path.join(local_dir, "config")
    
    neat_run = NeatRun(config_path, simulation_config)
    neat_run.run()

if __name__ == "__main__":    
    main()
