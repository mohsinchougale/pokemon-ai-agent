from cg.api import CardData, Attack


class CombatEvaluator:


    def __init__(
        self,
        card_db
    ):

        self.card_db = card_db



    def evaluate_attack(
        self,
        option,
        features
    ):

        """
        Strategic attack evaluation.

        Considers:
        - damage
        - knockout potential
        - overkill
        - prize pressure
        - opponent retaliation threat
        - attack efficiency
        """


        damage = self.get_attack_damage(
            option
        )


        score = 0



        # ==================================================
        # Base Damage
        # ==================================================

        score += damage * 2



        # ==================================================
        # Guaranteed KO
        # ==================================================

        if damage >= features.opponent_active_hp:

            # Taking a prize is extremely valuable

            score += 400



            # Additional pressure when opponent is close
            if features.opponent_prize_remaining <= 2:

                score += 150



        # ==================================================
        # Avoid wasting damage
        # ==================================================

        overkill = (
            damage
            -
            features.opponent_active_hp
        )


        if overkill > 100:

            score -= min(
                100,
                overkill
            )



        # ==================================================
        # Attack efficiency
        # ==================================================

        if features.my_active_energy_count > 0:


            # More damage with same energy is better

            efficiency = (
                damage
                /
                features.my_active_energy_count
            )


            score += efficiency * 10



        # ==================================================
        # Prize race evaluation
        # ==================================================

        prize_difference = (
            features.opponent_prize_remaining
            -
            features.my_prize_remaining
        )


        # If losing the prize race, prioritize aggressive plays

        if prize_difference < 0:

            score += 100



        # ==================================================
        # Survival consideration
        # ==================================================

        if features.opponent_can_attack:


            opponent_damage = (
                features.opponent_attack_damage
            )


            # Current Pokemon likely gets KO'd next turn

            if opponent_damage >= features.my_active_hp:


                # Still attack if we can KO opponent

                if damage < features.opponent_active_hp:

                    score -= 200


                else:

                    score += 50



        # ==================================================
        # End game aggression
        # ==================================================

        if features.opponent_prize_remaining <= 2:

            score += 100



        # ==================================================
        # Low HP opponent finishing bonus
        # ==================================================

        if features.opponent_active_hp <= 50:

            score += 100



        return score



    def get_attack_damage(
        self,
        option
    ):

        """
        Extract attack damage from simulator option.
        """


        attack_id = getattr(
            option,
            "attackId",
            None
        )


        if attack_id is None:

            return 0



        try:

            attack = self.card_db.get_attack(
                attack_id
            )


        except Exception:

            return 0



        if attack is None:

            return 0



        # Card database returns pandas row.
        # Support both dict and pandas Series.

        if hasattr(
            attack,
            "get"
        ):

            damage = attack.get(
                "Damage",
                None
            )

        else:

            try:

                damage = attack["Damage"]

            except Exception:

                damage = None



        return self.parse_damage(
            damage
        )



    def parse_damage(
        self,
        damage
    ):


        if damage is None:

            return 0



        text = str(
            damage
        )


        number = ""



        for char in text:


            if char.isdigit():

                number += char


            elif number:

                break



        if number:

            return int(number)



        return 0