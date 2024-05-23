from typing import List, Callable
from simulation_setup import setup_map, spawn_player_cars
from simulation import simulation_loop
from cars.car import Car
from time import sleep
from processing_functions import Linear

RAY_COUNT = 8
PLAYER_CAR_COUNT = 1

def test_drive(processing_function=Linear) -> None:
    walls, gates, starting_point = setup_map()
            
    while True:        
        cars: List[Car] = spawn_player_cars(starting_point, processing_function, RAY_COUNT, PLAYER_CAR_COUNT)
        
        simulation_loop(cars, walls, gates, infinite_time=True)
        sleep(0.1)
        
if __name__ == "__main__":
    test_drive()