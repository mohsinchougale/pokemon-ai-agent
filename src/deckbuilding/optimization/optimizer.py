from deckbuilding.optimization.mutator import DeckMutator
from deckbuilding.engine_validator import EngineDeckValidator


class DeckOptimizer:
    """
    Improves a deck through iterative mutation.

    Uses beam search:
    - Generate multiple mutations
    - Evaluate all valid candidates
    - Keep the strongest candidate
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

        self.engine_validator = EngineDeckValidator()

        self.mutator = DeckMutator(card_database)


    def optimize(
        self,
        iterations=100,
        beam_width=5
    ):

        # -----------------------------
        # Generate starting deck
        # -----------------------------

        current = self.archetype.generate()

        if not self.engine_validator.validate(current):
            raise RuntimeError(
                "Generated starting deck failed engine validation"
            )

        initial_result = self.evaluator.evaluate(
            current,
            battles=10
        )

        initial_score = initial_result["deck_score"]

        current_score = initial_score

        best_deck = current
        best_score = current_score

        improvements = 0

        history = [
            {
                "iteration": 0,
                "score": best_score,
                "mutation": None
            }
        ]

        # -----------------------------
        # Optimization loop
        # -----------------------------

        for i in range(iterations):

            candidates = []

            for _ in range(beam_width):

                candidate = self.mutator.mutate(current)

                mutation_info = self.mutator.last_mutation

                if mutation_info is None:
                    continue

                if not self.validator.validate(candidate):
                    continue

                if not self.engine_validator.validate(candidate):
                    continue

                result = self.evaluator.evaluate(
                    candidate,
                    battles=10
                )

                candidates.append(
                    (
                        result["deck_score"],
                        candidate,
                        mutation_info
                    )
                )

            if not candidates:
                continue

            score, candidate, mutation_info = max(
                candidates,
                key=lambda x: x[0]
            )

            # Local improvement

            if score >= current_score:

                current = candidate
                current_score = score

            # Global improvement

            if score > best_score:

                old_score = best_score

                best_score = score
                best_deck = candidate

                improvements += 1

                history.append(
                    {
                        "iteration": i + 1,
                        "score": best_score,
                        "mutation": mutation_info
                    }
                )

                print("\nNEW BEST FOUND")
                print("----------------")
                print(
                    f"Iteration: {i + 1}"
                )

                print(
                    f"Score: {old_score} -> {best_score}"
                )

                print("Mutation:")
                print(
                    f"Type: {mutation_info['type']}"
                )

                print(
                    f"Removed: "
                    f"{self.mutator.db.get_name(mutation_info['removed'])}"
                )

                print(
                    f"Added: "
                    f"{self.mutator.db.get_name(mutation_info['added'])}"
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