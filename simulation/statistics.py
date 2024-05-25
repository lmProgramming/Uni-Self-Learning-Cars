class SimulationStatistics:
    def __init__(self) -> None:
        self.scores: list[float] = []
    
    def add_score(self, score: float) -> None:
        self.scores.append(score)
        
    @property
    def average_score(self) -> float:
        return sum(self.scores) / len(self.scores) if self.scores != [] else 0.0
    
    @property
    def max_score(self) -> float:        
        return max(self.scores) if self.scores != [] else 0.0