from typing import List, Callable
from simulation_setup import setup_map, spawn_player_cars, generate_rays, find_angle_to_first_gate
from simulation import simulation_loop
from cars.car import Car
from time import sleep
from processing_functions import Linear

RAY_COUNT = 8
PLAYER_CAR_COUNT = 1

def test_drive(random_angle: bool=True, processing_function=Linear) -> None:
    walls, gates, starting_point = setup_map()
    
    default_angle: float | None = find_angle_to_first_gate(starting_point, gates) if not random_angle else None
                
    while True:        
        cars: List[Car] = spawn_player_cars(starting_point, default_angle, PLAYER_CAR_COUNT)
        generate_rays(cars, RAY_COUNT, processing_function)
        
        simulation_loop(cars, walls, gates, infinite_time=True)
        sleep(0.1)
        
if __name__ == "__main__":
    test_drive()