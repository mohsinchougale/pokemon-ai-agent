from dataclasses import dataclass


@dataclass
class OptimizationResult:
    """
    Stores the outcome of a deck optimization run.
    """

    deck: object

    score: float

    initial_score: float

    iterations: int

    improvements: int