from typing import List, Callable
from simulation.simulation_setup import spawn_player_cars, generate_rays, find_angle_to_first_gate
from map_scripts.map_reader import read_map_txt as setup_map
from map_scripts.map_tools import DEFAULT_MAP
from simulation.simulation import Simulation, BreakTrainingException
from cars.car import Car
from time import sleep
from simulation.processing_functions import Linear
import pygame as pg

RAY_COUNT = 8
PLAYER_CAR_COUNT = 1
TEST_INTENDED_ANGLE = True
TESTED_MAP = DEFAULT_MAP

def test_drive(random_angle: bool=True, processing_function=Linear) -> None:
    pg.init()
    pg.font.init()    
    pg.display.set_caption("Simulation - Test Drive")
    
    walls, gates, starting_point = setup_map(TESTED_MAP)
    
    default_angle: float | None = find_angle_to_first_gate(starting_point, gates) if not random_angle else None
                                
    test_number: int = 0
    while True:        
        cars: List[Car] = spawn_player_cars(starting_point, default_angle, PLAYER_CAR_COUNT)
        generate_rays(cars, RAY_COUNT, processing_function)
        
        try:
            simulation = Simulation(cars, walls, gates, generation_number=test_number, infinite_time=True)
            simulation.simulation_loop()
        except BreakTrainingException:
            pg.quit()
            return
        sleep(0.1)
        test_number += 1
        
if __name__ == "__main__":
    test_drive(not TEST_INTENDED_ANGLE)