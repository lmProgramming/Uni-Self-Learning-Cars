import typer
from neat_training import main as start_simulation
from simulation.player_test import test_drive
from map_scripts.map_maker import create_new_map
from main import open_main_menu
from simulation.simulation_config import SimulationConfig

app = typer.Typer()

@app.command()
def start_simulation_command_cmd():
    """Starts the simulation."""
    start_simulation()

@app.command()
def open_main_menu_screen_cmd():
    """Opens the main menu screen."""
    open_main_menu()

@app.command()
def open_parameters_screen_cmd(car_count: int, hidden_layers_count: int, random_angle: bool, map_pool: list[str]) -> None:
    config = SimulationConfig(
        num_iterations=100, 
        map_pool=map_pool, 
        hidden_layers=hidden_layers_count, 
        random_angle=random_angle,
        ray_count=8,
        initial_population=car_count)
    start_simulation(config)
    
@app.command()
def create_new_map_cmd():
    create_new_map()

@app.command()
def open_map_screen_cmd():
    """Opens the map screen."""
    
    typer.echo("Maps")

@app.command()
def start_test_drive():
    """Starts the test drive."""
    test_drive()

if __name__ == "__main__":
    app()