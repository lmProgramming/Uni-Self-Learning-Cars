import pickle
from simulation.simulation_config import SimulationConfig

SIMULATION_CONFIG_FILENAME_END = "simulation-config.pkl"

def save_config(simulation_config: SimulationConfig, filename_prefix):
    with open(filename_prefix + SIMULATION_CONFIG_FILENAME_END, 'wb') as file:
        pickle.dump(simulation_config, file)
        
def clean_saved_configs():
    import os
    for file in os.listdir():
        if file.endswith(SIMULATION_CONFIG_FILENAME_END):
            os.remove(file)
            
def clean_saved_checkpoints():
    import os
    for file in os.listdir():
        if file.endswith(SIMULATION_CONFIG_FILENAME_END):
            os.remove(file)