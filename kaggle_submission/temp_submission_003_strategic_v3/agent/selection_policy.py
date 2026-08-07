from cg.api import (
    OptionType,
    SelectType,
)
from features.combat_evaluator import CombatEvaluator

class SelectionPolicy:


    def __init__(
        self,
        card_db
    ):

        self.card_db = card_db
        self.combat = CombatEvaluator(card_db)



    def choose(
        self,
        obs,
        features
    ):

        select = obs.select


        if select is None or len(select.option) == 0:
            return None



        if select.type == SelectType.YES_NO:
            return self.choose_yes_no(select)


        if select.type == SelectType.EVOLVE:
            return self.choose_evolution(
                select,
                features
            )


        if select.type == SelectType.ATTACK:
            return self.choose_attack(
                select,
                features
            )


        if select.type == SelectType.ENERGY:
            return self.choose_energy(
                select,
                features
            )


        if select.type == SelectType.CARD:
            return self.choose_card(
                select,
                features
            )


        if select.type == SelectType.ATTACHED_CARD:
            return self.choose_attached_card(select, features)


        return self.choose_default(select)



    # ==================================================
    # Helpers
    # ==================================================

    def required_count(
        self,
        select
    ):

        minimum = max(
            0,
            select.minCount
        )


        maximum = max(
            minimum,
            select.maxCount
        )


        return min(
            maximum,
            len(select.option)
        )



    def safe_default(
        self,
        select
    ):

        count = self.required_count(
            select
        )


        if count <= 0:
            return []


        return list(
            range(count)
        )



    # ==================================================
    # YES / NO
    # ==================================================

    def choose_yes_no(
        self,
        select
    ):


        for idx, option in enumerate(
            select.option
        ):

            if option.type == OptionType.YES:

                return [
                    idx
                ]


        return self.safe_default(select)



    # ==================================================
    # Attack selection
    # ==================================================

    def choose_attack(
        self,
        select,
        features
    ):

        best_idx = None
        best_score = float("-inf")


        for idx, option in enumerate(
            select.option
        ):

            score = self.combat.evaluate_attack(
                option,
                features
            )


            if score > best_score:

                best_score = score
                best_idx = idx



        if best_idx is None:

            return self.safe_default(
                select
            )


        return [
            best_idx
        ]



    # ==================================================
    # Energy
    # ==================================================

    def choose_energy(
        self,
        select,
        features
    ):

        scored = []


        for idx, option in enumerate(
            select.option
        ):

            score = 0


            card_id = getattr(
                option,
                "cardId",
                None
            )


            # ---------------------------------
            # Basic energy preference
            # ---------------------------------

            if card_id is not None:

                try:

                    if self.card_db.is_basic_energy(
                        card_id
                    ):

                        score += 50


                    elif self.card_db.is_energy(
                        card_id
                    ):

                        score += 20


                except Exception:

                    pass



            # ---------------------------------
            # Energy attachment value
            # ---------------------------------

            # Need energy to attack

            if features.my_active_energy_count < 3:

                score += 100



            # ---------------------------------
            # Attack readiness
            # ---------------------------------

            if (
                features.my_best_attack_damage
                >=
                features.opponent_active_hp
            ):

                # Already close to KO:
                # prioritize energy that enables attack

                score += 80



            # ---------------------------------
            # Opponent lethal threat
            # ---------------------------------

            if features.opponent_can_attack:

                if (
                    features.opponent_attack_damage
                    >=
                    features.my_active_hp
                ):

                    # Attaching energy while dying is bad

                    score -= 100



            scored.append(
                (
                    score,
                    idx
                )
            )



        scored.sort(
            reverse=True
        )


        count = self.required_count(
            select
        )


        return [
            idx
            for _, idx in scored[:count]
        ]



    # ==================================================
    # Card selection
    # ==================================================

    def choose_card(
        self,
        select,
        features
    ):

        scored = []


        for idx, option in enumerate(
            select.option
        ):

            score = 0


            card_id = getattr(
                option,
                "cardId",
                None
            )


            if card_id is None:

                scored.append(
                    (
                        score,
                        idx
                    )
                )

                continue



            try:

                # ---------------------------------
                # Pokemon value
                # ---------------------------------

                if self.card_db.is_pokemon(
                    card_id
                ):

                    score += 80



                if self.card_db.is_basic_pokemon(
                    card_id
                ):

                    score += 50



                if self.card_db.is_ex(
                    card_id
                ):

                    score += 70



                # ---------------------------------
                # HP value
                # ---------------------------------

                hp = self.card_db.get_hp(
                    card_id
                )


                if hp:

                    score += float(hp) * 0.2



                # ---------------------------------
                # Attack strength
                # ---------------------------------

                attacks = self.card_db.get_attacks(
                    card_id
                )


                for attack in attacks:

                    damage = self.parse_damage(
                        attack.get(
                            "damage",
                            0
                        )
                    )

                    score += damage * 0.2



            except Exception:

                pass



            # ==================================================
            # Board context
            # ==================================================


            # ---------------------------------
            # Need bench development
            # ---------------------------------

            if features.my_bench_size < 3:

                if self.card_db.is_basic_pokemon(
                    card_id
                ):

                    score += 120



            # ---------------------------------
            # Avoid unnecessary Pokemon late
            # ---------------------------------

            if features.opponent_prize_remaining <= 2:

                if self.card_db.is_pokemon(
                    card_id
                ):

                    score -= 50



            # ---------------------------------
            # If active Pokemon is weak
            # ---------------------------------

            if features.my_active_hp_ratio < 0.4:

                if self.card_db.is_pokemon(
                    card_id
                ):

                    score += 80



            scored.append(
                (
                    score,
                    idx
                )
            )



        scored.sort(
            reverse=True
        )


        count = self.required_count(
            select
        )


        return [
            idx
            for _, idx in scored[:count]
        ]



    # ==================================================
    # Attached Card
    # ==================================================

    def choose_attached_card(
        self,
        select,
        features
    ):

        scored = []


        for idx, option in enumerate(
            select.option
        ):

            score = 0


            # ---------------------------------
            # Energy selection
            # ---------------------------------

            context_name = None

            if hasattr(select.context, "name"):
                context_name = select.context.name

            if context_name in [
                "DISCARD_ENERGY_CARD",
                "SWITCH_ENERGY_CARD"
            ]:

                energy_index = getattr(
                    option,
                    "energyIndex",
                    None
                )


                if energy_index is not None:

                    # Prefer removing lower value energy
                    # (future improvement: attack cost analysis)

                    score += 20



            # ---------------------------------
            # Tool selection
            # ---------------------------------

            if context_name == "DISCARD_TOOL_CARD":

                tool_index = getattr(
                    option,
                    "toolIndex",
                    None
                )


                if tool_index is not None:

                    score += 30



            # ---------------------------------
            # Survival logic
            # ---------------------------------

            if features.opponent_can_attack:

                if (
                    features.opponent_attack_damage
                    >=
                    features.my_active_hp
                ):

                    # In danger:
                    # prioritize choices that enable recovery

                    score += 50



            scored.append(
                (
                    score,
                    idx
                )
            )


        scored.sort(
            reverse=True
        )


        count = self.required_count(
            select
        )


        return [
            idx
            for _, idx in scored[:count]
        ]



    # ==================================================
    # Evolution
    # ==================================================

    def choose_evolution(
        self,
        select,
        features
    ):

        scored = []


        for idx, option in enumerate(
            select.option
        ):

            score = 0


            card_id = getattr(
                option,
                "cardId",
                None
            )


            if card_id is None:

                scored.append(
                    (
                        score,
                        idx
                    )
                )

                continue



            try:

                # ---------------------------------
                # Evolution value
                # ---------------------------------

                if self.card_db.is_stage2_pokemon(
                    card_id
                ):

                    score += 150


                elif self.card_db.is_stage1_pokemon(
                    card_id
                ):

                    score += 80



                # ---------------------------------
                # Strong Pokemon bonus
                # ---------------------------------

                if self.card_db.is_ex(
                    card_id
                ):

                    score += 100



                hp = self.card_db.get_hp(
                    card_id
                )


                if hp is not None:

                    score += float(hp) * 0.3



            except Exception:

                pass



            # ==================================================
            # Game context
            # ==================================================


            # ---------------------------------
            # Early game: evolution less urgent
            # ---------------------------------

            if features.turn <= 3:

                score -= 40



            # ---------------------------------
            # Mid game: evolution valuable
            # ---------------------------------

            elif features.turn >= 5:

                score += 50



            # ---------------------------------
            # Need power to close game
            # ---------------------------------

            if (
                features.opponent_active_hp
                >
                features.my_best_attack_damage
            ):

                score += 40



            # ---------------------------------
            # Don't evolve while about to lose
            # ---------------------------------

            if features.opponent_can_attack:

                if (
                    features.opponent_attack_damage
                    >=
                    features.my_active_hp
                ):

                    score -= 150



            # ---------------------------------
            # End game pressure
            # ---------------------------------

            if features.opponent_prize_remaining <= 2:

                score -= 50



            scored.append(
                (
                    score,
                    idx
                )
            )



        scored.sort(
            reverse=True
        )


        if not scored:

            return self.safe_default(
                select
            )


        return [
            scored[0][1]
        ]



    # ==================================================
    # Default
    # ==================================================

    def choose_default(
        self,
        select
    ):

        return self.safe_default(
            select
        )



    # ==================================================
    # Damage parser
    # ==================================================

    def parse_damage(
        self,
        damage
    ):


        if damage is None:

            return 0



        number = ""



        for char in str(damage):

            if char.isdigit():

                number += char


            elif number:

                break



        return int(number) if number else 0