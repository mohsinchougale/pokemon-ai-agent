from deckbuilding.optimization.mutator import DeckMutator


class DeckOptimizer:
    """
    Improves a deck through iterative mutation.

    Process:
    - Generate initial deck
    - Mutate current deck
    - Keep improvements
    - Track optimization progress
    - Return best deck discovered
    """

    def __init__(
        self,
        archetype,
        evaluator,
        validator,
        card_database
    ):

        self.archetype = archetype
        self.evaluator = evaluator
        self.validator = validator

        self.mutator = DeckMutator(
            card_database
        )


    def optimize(
        self,
        iterations=100
    ):

        # -----------------------------
        # Generate starting deck
        # -----------------------------

        current = self.archetype.generate()

        initial_score = (
            self.evaluator
            .evaluate(current)["deck_score"]
        )


        current_score = initial_score

        best_deck = current
        best_score = current_score


        improvements = 0

        history = [
            {
                "iteration": 0,
                "score": best_score
            }
        ]


        # -----------------------------
        # Optimization loop
        # -----------------------------

        for i in range(iterations):

            candidate = self.mutator.mutate(
                current
            )


            # Invalid deck
            if not self.validator.validate(candidate):
                continue


            score = (
                self.evaluator
                .evaluate(candidate)["deck_score"]
            )


            # Accept improvement
            if score >= current_score:

                current = candidate
                current_score = score



            # New global best
            if score > best_score:

                best_deck = candidate
                best_score = score

                improvements += 1

                history.append(
                    {
                        "iteration": i + 1,
                        "score": best_score
                    }
                )



            if i % 10 == 0:

                print(
                    f"{self.archetype.__class__.__name__}: "
                    f"{i}/{iterations} "
                    f"best={best_score}"
                )


        return {

            "deck": best_deck,

            "initial_score": initial_score,

            "best_score": best_score,

            "improvements": improvements,

            "iterations": iterations,

            "history": history
        }