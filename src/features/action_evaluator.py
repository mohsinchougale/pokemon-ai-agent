from cg.api import OptionType

from features.combat_evaluator import CombatEvaluator
from features.board_evaluator import evaluate_board


class ActionEvaluator:


    def __init__(
        self,
        card_db
    ):

        self.card_db = card_db

        self.combat = CombatEvaluator(
            card_db
        )



    def evaluate(
        self,
        option,
        features
    ):


        action = option.type


        # ----------------------------------
        # Current board position
        # ----------------------------------

        board_score = evaluate_board(
            features
        )


        board_score *= 0.25



        # ----------------------------------
        # Action value
        # ----------------------------------

        if action == OptionType.ATTACK:

            action_score = self.combat.evaluate_attack(
                option,
                features
            )


        elif action == OptionType.ATTACH:

            action_score = self.evaluate_energy(
                features
            )


        elif action == OptionType.PLAY:

            action_score = self.evaluate_play(
                features
            )


        elif action == OptionType.EVOLVE:

            action_score = self.evaluate_evolution(
                features
            )


        elif action == OptionType.RETREAT:

            action_score = self.evaluate_retreat(
                features
            )


        elif action == OptionType.END:

            action_score = -100


        else:

            action_score = 0



        risk_score = self.evaluate_risk(
            action,
            features
        )



        return (
            action_score
            +
            board_score
            +
            risk_score
        )



    # ==================================================
    # Energy attachment
    # ==================================================

    def evaluate_energy(
        self,
        features
    ):

        score = 0



        # Energy accelerates attack potential

        if features.my_active_energy_count < 3:

            score += 120


        else:

            score -= 40



        # Extra value if opponent is weak

        if (
            features.opponent_active_hp
            <=
            features.my_best_attack_damage
        ):

            score -= 50



        # Avoid feeding opponent KO

        if features.opponent_can_attack:

            if (
                features.opponent_attack_damage
                >=
                features.my_active_hp
            ):

                score -= 200



        return score



    # ==================================================
    # Playing Pokemon / Trainer
    # ==================================================

    def evaluate_play(
        self,
        features
    ):

        score = 0



        # Early setup

        if features.turn <= 5:

            score += 100



        # Bench has value but diminishing returns

        if features.my_bench_size < 3:

            score += 120


        elif features.my_bench_size < 5:

            score += 40


        else:

            score -= 30



        # Late game avoid unnecessary setup

        if features.opponent_prize_remaining <= 2:

            score -= 80



        return score



    # ==================================================
    # Evolution
    # ==================================================

    def evaluate_evolution(
        self,
        features
    ):

        score = 120



        if features.turn <= 3:

            score -= 20



        else:

            score += 60



        # Evolution useful when behind

        if (
            features.opponent_active_hp
            >
            features.my_best_attack_damage
        ):

            score += 40



        # Don't evolve while about to lose

        if features.opponent_prize_remaining <= 2:

            score -= 100



        return score



    # ==================================================
    # Retreat
    # ==================================================

    def evaluate_retreat(
        self,
        features
    ):

        score = 0



        hp = features.my_active_hp_ratio



        if hp < 0.25:

            score += 250


        elif hp < 0.5:

            score += 100


        else:

            score -= 50



        # Retreat when opponent has lethal

        if (
            features.opponent_attack_damage
            >=
            features.my_active_hp
        ):

            score += 200



        return score



    # ==================================================
    # Risk model
    # ==================================================

    def evaluate_risk(
        self,
        action,
        features
    ):

        risk = 0



        # Losing position:
        # prioritize aggressive plays

        if features.my_prize_remaining <= 2:


            if action == OptionType.ATTACK:

                risk += 120



        # Opponent lethal threat

        if features.opponent_can_attack:


            lethal = (
                features.opponent_attack_damage
                >=
                features.my_active_hp
            )


            if lethal:


                if action == OptionType.RETREAT:

                    risk += 150


                elif action != OptionType.ATTACK:

                    risk -= 120



        return risk