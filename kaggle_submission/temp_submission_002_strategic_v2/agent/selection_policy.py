from cg.api import (
    OptionType,
    SelectType,
)


class SelectionPolicy:


    def __init__(
        self,
        card_db
    ):

        self.card_db = card_db



    def choose(
        self,
        obs
    ):

        select = obs.select


        if select is None or len(select.option) == 0:
            return None



        if select.type == SelectType.YES_NO:
            return self.choose_yes_no(select)


        if select.type == SelectType.EVOLVE:
            return self.choose_evolution(select)


        if select.type == SelectType.ATTACK:
            return self.choose_attack(select)


        if select.type == SelectType.ENERGY:
            return self.choose_energy(select)


        if select.type == SelectType.CARD:
            return self.choose_card(select)


        if select.type == SelectType.ATTACHED_CARD:
            return self.choose_attached_card(select)


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
        select
    ):


        best_idx = None
        best_score = float("-inf")



        for idx, option in enumerate(
            select.option
        ):


            attack_id = getattr(
                option,
                "attackId",
                None
            )


            if attack_id is None:
                continue



            try:

                attack = self.card_db.get_attack(
                    attack_id
                )

            except Exception:

                continue



            if attack is None:
                continue



            damage = self.parse_damage(
                getattr(
                    attack,
                    "damage",
                    0
                )
            )


            score = 0



            # Damage priority

            score += damage * 5



            # Prefer cheaper attacks

            cost = getattr(
                attack,
                "cost",
                []
            )


            try:

                score -= len(cost) * 5

            except:

                pass



            # Strong preference for knockout attacks

            # (simulator may not expose HP here,
            # so only use available information)

            if damage >= 100:

                score += 50



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
        select
    ):


        scored = []


        for idx, option in enumerate(
            select.option
        ):


            card_id = getattr(
                option,
                "cardId",
                None
            )


            score = 0



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


                except:

                    pass



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
        select
    ):


        scored = []



        for idx, option in enumerate(
            select.option
        ):


            card_id = getattr(
                option,
                "cardId",
                None
            )


            score = 0



            if card_id is not None:


                try:


                    if self.card_db.is_pokemon(
                        card_id
                    ):

                        score += 100


                    if self.card_db.is_basic_pokemon(
                        card_id
                    ):

                        score += 40


                    if self.card_db.is_ex(
                        card_id
                    ):

                        score += 80



                    hp = self.card_db.get_hp(
                        card_id
                    )


                    score += float(hp) * 0.5



                    attacks = self.card_db.get_attacks(
                        card_id
                    )


                    for attack in attacks:

                        score += (
                            self.parse_damage(
                                getattr(
                                    attack,
                                    "damage",
                                    0
                                )
                            )
                            *
                            0.5
                        )


                except:

                    pass



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
        select
    ):


        return self.safe_default(
            select
        )



    # ==================================================
    # Evolution
    # ==================================================

    def choose_evolution(
        self,
        select
    ):


        scored = []



        for idx, option in enumerate(
            select.option
        ):


            card_id = getattr(
                option,
                "cardId",
                None
            )


            score = 0



            if card_id is not None:


                try:


                    if self.card_db.is_stage2_pokemon(
                        card_id
                    ):

                        score += 120


                    elif self.card_db.is_stage1_pokemon(
                        card_id
                    ):

                        score += 70



                    if self.card_db.is_ex(
                        card_id
                    ):

                        score += 80



                    hp = self.card_db.get_hp(
                        card_id
                    )


                    score += float(hp)



                except:

                    pass



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