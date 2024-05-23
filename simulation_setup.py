import neat # type: ignore
from neat.nn.feed_forward import FeedForwardNetwork # type: ignore
from pygame.math import Vector2
import random
from typing import List
from processing_functions import Linear, Quadratic
from maps.map_reader import read_map_txt

from cars.car import Car, AICar, HumanCar
from maps.map import Wall, Gate

RAY_LENGTH: float = 200
NON_RAY_INPUTS: int = 1

def setup_map() -> tuple[list, list, Vector2]:
    walls, gates, starting_point = read_map_txt()
    return walls, gates, starting_point
    
def setup_generation(genomes: List[neat.DefaultGenome], config, processing_function=Quadratic) -> tuple[list[Car], list, list]:
    cars: List[Car] = []
    
    walls: List[Wall]
    gates: List[Gate]
    starting_point: Vector2

    walls, gates, starting_point = read_map_txt()
 
    cars = spawn_ai_cars(genomes, config, starting_point, processing_function, get_ray_count_from_config())
            
    return cars, walls, gates

def spawn_ai_cars(genomes: List[neat.DefaultGenome], config: neat.Config, starting_point, processing_function, ray_count) -> List[Car]:
    cars: List[Car] = []
    
    for _, genome in genomes:
        genome.fitness = 0
        new_car = AICar(starting_point.x, starting_point.y, random.randrange(-180, 180))
        
        neural_net: FeedForwardNetwork = FeedForwardNetwork.create(genome, config)
        
        new_car.set_neural_net(neural_net)
        
        new_car.genome = genome
        new_car.generate_rays(ray_count, RAY_LENGTH, processing_function)
        cars.append(new_car)
        
    return cars

def spawn_player_cars(starting_point, processing_function, ray_count: int, count: int=1) -> List[Car]:
    cars: List[Car] = []
    
    for _ in range(count):
        human_car: HumanCar = HumanCar(starting_point.x, starting_point.y, random.randrange(-180, 180))
        
        human_car.generate_rays(ray_count, RAY_LENGTH, processing_function)
        cars.append(human_car)
        
    return cars   

def get_ray_count_from_config() -> int:
    with open('config', 'r') as f:
        for line in f:
            if line.startswith("num_inputs"):
                return int(line.strip().split(" = ")[1]) - NON_RAY_INPUTS
    return 0