# Self Learning Cars

Simulating cars learning to drive on different maps based on NEAT-python and Pygame. Includes a GUI in PyQt and a CLI in Typer.
Includes many useful extensions of PyQt widgets, and implements some basic UI elements in Pygame using my abstract PyUiElement class.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [License](#license)
- [Issues](#issues)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/lmProgramming/SelfLearningCars
    ```
2. Navigate to the project directory:
    ```sh
    cd SelfLearningCars
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Build cython code:
   ```sh
    python cython_setup.py build_ext --inplace
    ```

## Usage

To start the GUI application, run:
```sh
python main.py
```
To start the CLI application, run:
```sh
python cli.py
```

## Features

1. A GUI, that allows you to start the simulation, manage maps and manage NEAT checkpoints
2. A graphical simulation of cars driving around the map
3. Map managing: creating a new map, editing it or deleting it
4. Loading a saved NEAT checkpoints
5. Test drive a map
6. CLI interface, that allows you to do pretty much everything specified above
7. The simulation also shows a graph of scores over time and it allows to click a car to see it's neural network
8. ScrollableGallery - a small extension for PyQt
9. PyUiElement, PyInputBox, PyButton, PyImage, PyPlot - Pygame UI extensions

## License

WTFPL

## Issues

A know issue is that Pygame will sometimes not create a window, for example, if you go back to main menu after creating a new map, and then do a test drive, and then try to create another map, the window might not be created.
