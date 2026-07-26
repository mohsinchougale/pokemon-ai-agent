from deckbuilding.optimization.optimizer import DeckOptimizer


class ArchetypeSearch:

    def __init__(
        self,
        archetypes,
        evaluator,
        validator
    ):

        self.archetypes = archetypes
        self.evaluator = evaluator
        self.validator = validator


    def search(
        self,
        iterations=100
    ):

        results = []

        for archetype in self.archetypes:

            optimizer = DeckOptimizer(
                archetype,
                self.evaluator,
                self.validator,
                archetype.db
            )

            result = optimizer.optimize(iterations)

            results.append(
                {
                    "archetype": archetype.__class__.__name__,
                    "score": result["score"],
                    "deck": result["deck"]
                }
            )

        return sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )