import pickle
from simulation.simulation_config import SimulationConfig
import os
import re

SIMULATION_CONFIG_FILENAME_END = "simulation-config.pkl"
NEAT_INFIX = "-NEAT-"

def save_config(simulation_config: SimulationConfig, filename_prefix) -> None:
    with open(filename_prefix + SIMULATION_CONFIG_FILENAME_END, 'wb') as file:
        pickle.dump(simulation_config, file)
        
def get_config(timestamp: str) -> SimulationConfig:
    with open(timestamp + NEAT_INFIX + SIMULATION_CONFIG_FILENAME_END, 'rb') as file:
        return pickle.load(file)
                    
def get_saved_checkpoints(timestamp: str="") -> list[str]:
    saved_trainings: list[str] = []
    
    for file in os.listdir():
        if re.match(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-NEAT-\d+$', file):
            saved_trainings.append(file)
    
    return saved_trainings
            
def delete_checkpoint(checkpoint: str):   
    timestamp: str = get_timestamp(checkpoint)
    
    os.remove(checkpoint)
    
    if len(get_saved_checkpoints(timestamp)) > 0:
        return
    
    # delete config file, if no checkpoint uses it anymore
    for file in os.listdir():
        if file.startswith(timestamp):
            os.remove(file)
    
def clear_all_checkpoints():
    for file in os.listdir():
        if re.match(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-NEAT-*$', file):
            os.remove(file)
    
def get_timestamp(checkpoint: str) -> str:
    return checkpoint.split("-NEAT")[0]