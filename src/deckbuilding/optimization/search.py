from deckbuilding.optimization.optimizer import DeckOptimizer


class ArchetypeSearch:
    """
    Runs optimization across multiple deck archetypes.
    """

    def __init__(
        self,
        archetypes,
        evaluator,
        validator,
        card_database
    ):

        self.archetypes = archetypes
        self.evaluator = evaluator
        self.validator = validator
        self.card_database = card_database



    def search(
        self,
        iterations=50
    ):

        results = []


        for archetype in self.archetypes:

            optimizer = DeckOptimizer(
                archetype,
                self.evaluator,
                self.validator,
                self.card_database
            )


            result = optimizer.optimize(
                iterations
            )


            results.append(
                {
                    "archetype":
                        archetype.__class__.__name__,

                    "deck":
                        result["deck"],

                    "initial_score":
                        result["initial_score"],

                    "score":
                        result["best_score"],

                    "improvements":
                        result["improvements"],

                    "iterations":
                        result["iterations"],

                    "history":
                        result["history"]
                }
            )


        # Best decks first

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )


        return results