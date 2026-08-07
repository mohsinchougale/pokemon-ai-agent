from cg.api import OptionType

from features.combat_evaluator import CombatEvaluator
from features.board_evaluator import evaluate_board
from features.game_phase import (
    get_game_phase,
    GamePhase,
)


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

        phase = get_game_phase(features)



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
                features,
                phase
            )


        elif action == OptionType.PLAY:

            action_score = self.evaluate_play(
                features,
                phase
            )


        elif action == OptionType.EVOLVE:

            action_score = self.evaluate_evolution(
                features,
                phase
            )


        elif action == OptionType.RETREAT:

            action_score = self.evaluate_retreat(
                features,
                phase
            )


        elif action == OptionType.END:

            action_score = -100


        else:

            action_score = 0



        # ----------------------------------
        # Risk evaluation
        # ----------------------------------

        risk_score = self.evaluate_risk(
            action,
            features,
            phase
        )



        # ----------------------------------
        # Bench / survival evaluation
        # ----------------------------------

        bench_score = self.evaluate_bench_pressure(
            action,
            features
        )



        return (
            action_score
            +
            board_score
            +
            risk_score
            +
            bench_score
        )



    # ==================================================
    # Bench pressure / survival
    # ==================================================

    def evaluate_bench_pressure(
        self,
        action,
        features
    ):

        score = 0



        # ----------------------------------
        # Critical situation:
        # Active Pokemon is alone
        # ----------------------------------

        if features.my_bench_size == 0:


            # Building backup is extremely valuable

            if action == OptionType.PLAY:

                score += 250



            # Blind attacking risks losing game

            elif action == OptionType.ATTACK:

                score -= 100



        # ----------------------------------
        # Some backup exists
        # ----------------------------------

        elif features.my_bench_size == 1:


            if action == OptionType.PLAY:

                score += 100



        return score



    # ==================================================
    # Energy attachment
    # ==================================================

    def evaluate_energy(
        self,
        features,
        phase
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
        features,
        phase
    ):

        score = 0



        # Early setup

        if phase == GamePhase.EARLY:

            score += 100



        # ----------------------------------
        # Bench development
        # ----------------------------------

        if features.my_bench_size == 0:

            # Emergency:
            # need second Pokemon

            score += 250



        elif features.my_bench_size < 3:

            score += 150



        elif features.my_bench_size < 5:

            score += 40



        else:

            score -= 30



        # Late game avoid unnecessary setup

        if phase == GamePhase.ENDGAME:

            score -= 80



        return score



    # ==================================================
    # Evolution
    # ==================================================

    def evaluate_evolution(
        self,
        features,
        phase
    ):

        score = 120



        if phase == GamePhase.EARLY:

            score -= 20


        else:

            score += 60



        if (
            features.opponent_active_hp
            >
            features.my_best_attack_damage
        ):

            score += 40



        if phase == GamePhase.ENDGAME:

            score -= 100



        return score



    # ==================================================
    # Retreat
    # ==================================================

    def evaluate_retreat(
        self,
        features,
        phase
    ):

        score = 0



        hp = features.my_active_hp_ratio



        if hp < 0.25:

            score += 250


        elif hp < 0.5:

            score += 100


        else:

            score -= 50



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
        features,
        phase
    ):

        risk = 0



        # ----------------------------------
        # Early game:
        # don't sacrifice board development
        # ----------------------------------

        if (
            features.turn <= 5
            and
            features.my_bench_size == 0
            and
            action == OptionType.ATTACK
        ):

            risk -= 80



        # ----------------------------------
        # Endgame aggression
        # ----------------------------------

        if phase == GamePhase.ENDGAME:


            if action == OptionType.ATTACK:

                risk += 120



        # ----------------------------------
        # Opponent lethal threat
        # ----------------------------------

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