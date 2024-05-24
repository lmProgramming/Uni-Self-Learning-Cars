from dataclasses import dataclass

@dataclass
class SimulationConfig:
    num_iterations: int
    map_pool: list[str]
    hidden_layers: int
    random_angle: bool
    ray_count: int | None = None
    initial_population: int | None = None    