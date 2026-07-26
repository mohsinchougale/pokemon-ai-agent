from deckbuilding.optimization.mutator import DeckMutator


class DeckOptimizer:
    """
    Improves a deck through iterative mutation.

    Process:
    - Generate initial deck
    - Mutate it repeatedly
    - Keep better mutations
    - Return best deck found
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
        self.mutator = DeckMutator(card_database)


    def optimize(
        self,
        iterations=100
    ):

        current = self.archetype.generate()

        current_score = (
            self.evaluator
            .evaluate(current)["deck_score"]
        )

        best_deck = current
        best_score = current_score


        for i in range(iterations):

            candidate = self.mutator.mutate(current)

            if not self.validator.validate(candidate):

                continue

            score = (
                self.evaluator
                .evaluate(candidate)["deck_score"]
            )

            # Hill climbing: keep improvements
            if score >= current_score:

                current = candidate
                current_score = score

            if score > best_score:

                best_deck = candidate
                best_score = score

            if i % 10 == 0:

                print(
                    f"{self.archetype.__class__.__name__}: "
                    f"{i}/{iterations} best={best_score}"
                )

        return {
            "deck": best_deck,
            "score": best_score
        }