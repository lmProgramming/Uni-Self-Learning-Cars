from dataclasses import dataclass

@dataclass
class SimulationConfig:
    num_iterations: int = 1000
    initial_population: int = 1000
    growth_rate: float = 0.1

    # Output parameters
    output_path: str = "output.csv"
    verbose: bool = False