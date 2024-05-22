import os
from typing import List

MAP_FOLDER: str = 'maps'
MAP_EXTENSION: str = '.txt'

def get_map_names() -> List[str]:
    map_folder = MAP_FOLDER
    filenames: List[str] = os.listdir(map_folder)
    return [file for file in filenames if file.endswith(MAP_EXTENSION)]

def rename_map(old_name: str, new_name: str) -> str:
    old_name = format_map_name(old_name)
    new_name = format_map_name(new_name)

    os.rename(os.path.join(MAP_FOLDER, old_name), os.path.join(MAP_FOLDER, new_name))
    
    return new_name
    
def delete_map(name: str) -> None:
    name = format_map_name(name)
    os.remove(os.path.join(MAP_FOLDER, name))
    
def format_map_name(name: str):
    return name.split('.')[0] + MAP_EXTENSION