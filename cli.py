import typer
from neat_training import main
from simulation.player_test import test_drive
from map_scripts.map_maker import create_new_map, edit_existing_map
from map_scripts.map_tools import get_map_names, delete_map as delete_map_func, rename_map as rename_map_func
from neat_save_load import clear_all_checkpoints
from main import open_main_menu
from simulation.simulation_config import SimulationConfig

app = typer.Typer()

@app.command()
def start() -> None:
    main()

@app.command()
def main_menu() -> None:
    open_main_menu()

@app.command()
def start_with_params(car_count: int, hidden_layers_count: int, random_angle: bool, map_pool: list[str]) -> None:
    config = SimulationConfig(
        num_iterations=100, 
        map_pool=map_pool, 
        hidden_layers=hidden_layers_count, 
        random_angle=random_angle,
        ray_count=8,
        initial_population=car_count)
    main(config)
    
@app.command()
def new_map() -> None:
    create_new_map()

@app.command()
def show_maps() -> None:  
    typer.echo("Maps: ")  
    for map in get_map_names():
        typer.echo(map)
    
@app.command()    
def delete_map(map_name: str) -> None:    
    delete_map_func(map_name)
    
@app.command()    
def rename_map(map_name: str, new_name: str) -> None:    
    rename_map_func(map_name, new_name)
    
@app.command()    
def edit_map_cmd(map_name: str) -> None:    
    edit_existing_map(map_name)

@app.command()
def start_test_drive() -> None:
    test_drive()
    
@app.command()
def clear_checkpoints() -> None:
    clear_all_checkpoints()

if __name__ == "__main__":
    app()