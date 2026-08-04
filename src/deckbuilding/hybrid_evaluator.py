from deckbuilding.deck_evaluator import DeckEvaluator
from deckbuilding.battle_evaluator import BattleEvaluator


class HybridEvaluator:

    def __init__(
        self,
        deck_evaluator,
        opponent_deck
    ):

        self.deck_evaluator = deck_evaluator
        self.battle_evaluator = BattleEvaluator(
            opponent_deck
        )


    def evaluate(
        self,
        deck,
        battles=10
    ):

        # Static score
        static = self.deck_evaluator.evaluate(
            deck
        )


        # Actual battle performance
        win_rate = self.battle_evaluator.evaluate(
            deck,
            battles
        )


        final_score = (
            win_rate * 100
            +
            static["deck_score"] * 0.2
        )


        return {
            "deck_score": final_score,
            "win_rate": win_rate,
            "static_score": static["deck_score"]
        }