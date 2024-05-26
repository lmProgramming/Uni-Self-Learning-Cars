import neat # type: ignore
import os
import pygame as pg
from pygame.math import Vector2
from typing import List, Optional
from simulation.simulation import Simulation, BreakTrainingException
from simulation.simulation_setup import setup_generation
from simulation.simulation_config import SimulationConfig
from map_scripts.map_tools import DEFAULT_MAP
import random
from simulation.statistics import SimulationStatistics
from datetime import datetime   
from neat_save_load import save_config, get_timestamp, NEAT_INFIX, get_config

WIDTH = 1280
HEIGHT = 960

PLAYER_ONLY = False
LOAD_MAP = True

STARTING_CAR_POSITION = Vector2(450, HEIGHT - 472)

RAY_DISTANCE_KILL: float = 10

RAY_COUNT: int = 8
RAY_LENGTH: float = 200

NON_RAY_INPUTS: int = 2

class NeatTrainingAttempt:
    def __init__(self, config_path, simulation_config: Optional[SimulationConfig] = None) -> None:
        self.gen: int = 0

        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, config_path)
        
        self.statistics: List[SimulationStatistics] = []

        self.simulation_config: Optional[SimulationConfig] = None
        if simulation_config is not None:
            self.simulation_config = simulation_config
            NeatTrainingAttempt.inject_simulation_config(self.config, simulation_config)
        
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
            "ray_count": NeatTrainingAttempt.get_ray_count_from_config(config)}
        if self.simulation_config is not None:
            arguments["random_angle"] = self.simulation_config.random_angle
            
        cars, walls, gates = setup_generation(**arguments)

        simulation = Simulation(cars, walls, gates, self.gen, config, infinite_time=False)
        simulation.plot_values(self.statistics)
        simulation.simulation_loop()   
        
        self.statistics.append(simulation.get_statistics())
        
    def get_simulation_config(self) -> SimulationConfig:
        if self.simulation_config is not None:
            return self.simulation_config
        
        return SimulationConfig(
            500,
            [DEFAULT_MAP],
            self.config.genome_config.num_hidden, 
            True,
            self.config.genome_config.num_inputs - NON_RAY_INPUTS, 
            self.config.pop_size)

    @staticmethod
    def inject_simulation_config(config: neat.Config, simulation_config: SimulationConfig) -> neat.Config:
        config.pop_size = simulation_config.initial_population
        config.genome_config.num_hidden = simulation_config.hidden_layers
        if simulation_config.ray_count is not None:
            config.genome_config.num_inputs = simulation_config.ray_count + NON_RAY_INPUTS
            
        return config

    def run(self, p: neat.Population, filename_prefix: str) -> None:
        p.add_reporter(neat.StdOutReporter(True))
        p.add_reporter(neat.Checkpointer(1, 1, filename_prefix))   
        save_config(self.get_simulation_config(), filename_prefix)     
         
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        
        pg.font.init()    
        pg.display.set_caption("Simulation - NEAT-Python")

        try:
            winner = p.run(self.run_new_generation, 500)

            print(winner)
        except BreakTrainingException:
            print("Training ended.")
            pg.quit()
            
    def default_run(self) -> None:
        p = neat.Population(self.config)
        
        cur_date: datetime = datetime.now()
        filename_prefix: str = cur_date.strftime("%Y-%m-%d-%H-%M-%S") + NEAT_INFIX
        
        self.run(p, filename_prefix)        
        
    def load_run(self, checkpoint_filename: str) -> None:
        p: neat.Population = neat.Checkpointer.restore_checkpoint(checkpoint_filename)
        
        timestamp: str = get_timestamp(checkpoint_filename)
        filename_prefix: str = timestamp + NEAT_INFIX
        simulation_config: SimulationConfig = get_config(timestamp)
        
        self.gen = p.generation
        
        self.config = self.inject_simulation_config(p.config, simulation_config)
        
        self.run(p, filename_prefix)       

def load_checkpoint(simulation_config: SimulationConfig, checkpoint_filename) -> None:    
    local_dir: str = os.path.dirname(__file__)
    config_path: str = os.path.join(local_dir, "config")
    
    neat_run = NeatTrainingAttempt(config_path, simulation_config)
    neat_run.load_run(checkpoint_filename)

def main(simulation_config: Optional[SimulationConfig] = None) -> None:    
    local_dir: str = os.path.dirname(__file__)
    config_path: str = os.path.join(local_dir, "config")
    
    neat_run = NeatTrainingAttempt(config_path, simulation_config)
    neat_run.default_run()

if __name__ == "__main__":    
    main()
