import neat # type: ignore
from neat.nn.feed_forward import FeedForwardNetwork # type: ignore
from pygame.math import Vector2
from math import degrees
import random
from typing import List, Optional
from processing_functions import Linear, Quadratic
from map_scripts.map_reader import read_map_txt

from cars.car import Car, AICar, HumanCar
from map_scripts.map import Wall, Gate

RAY_LENGTH: float = 200
NON_RAY_INPUTS: int = 1

def find_angle_to_first_gate(position: Vector2, gates: List[Gate]) -> float:
    if gates:
        print(position, gates[0].get_centre_position())
        return degrees(position.angle_to(gates[0].get_centre_position()))
    else:
        return 0.0
    
def setup_generation(map_name: str, genomes: List[neat.DefaultGenome], config, ray_count, random_angle: bool=True, processing_function=Quadratic) -> tuple[list[Car], list, list]:
    cars: List[Car] = []
    
    walls: List[Wall]
    gates: List[Gate]
    starting_point: Vector2

    walls, gates, starting_point = read_map_txt(map_name)
    
    intended_angle: float | None = find_angle_to_first_gate(starting_point, gates) if not random_angle else None
    
    print(intended_angle)
 
    cars = spawn_ai_cars(genomes, config, starting_point, intended_angle) 
    generate_rays(cars, ray_count, processing_function)
            
    return cars, walls, gates

def generate_rays(cars: list[Car], ray_count, processing_function) -> None:
    for car in cars:        
        car.generate_rays(ray_count, RAY_LENGTH, processing_function)

def spawn_ai_cars(genomes: List[neat.DefaultGenome], config: neat.Config, starting_point: Vector2, default_angle=None) -> List[Car]:
    cars: List[Car] = []
    
    for _, genome in genomes:
        genome.fitness = 0
        new_car = AICar(
            starting_point.x, 
            starting_point.y, 
            random.randrange(-180, 180) if default_angle is None else default_angle)
        
        neural_net: FeedForwardNetwork = FeedForwardNetwork.create(genome, config)
        
        new_car.set_neural_net(neural_net)
        
        new_car.genome = genome
        cars.append(new_car)
        
    return cars

def spawn_player_cars(starting_point: Vector2, default_angle=None, count: int=1) -> List[Car]:
    cars: List[Car] = []
    
    for _ in range(count):
        human_car: HumanCar = HumanCar(
            starting_point.x, 
            starting_point.y, 
            random.randrange(-180, 180) if default_angle is None else default_angle)
        
        cars.append(human_car)
        
    return cars