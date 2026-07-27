from dataclasses import dataclass
import pandas as pd


@dataclass
class CardFeatures:

    card_id: int
    name: str

    stage: str
    category: str
    previous_stage: str

    is_pokemon: bool
    is_basic_pokemon: bool
    is_stage1_pokemon: bool
    is_stage2_pokemon: bool

    is_trainer: bool
    is_energy: bool

    hp: float
    pokemon_type: str

    attack_count: int
    max_damage: int
    min_attack_energy: int

    is_ex: bool
    has_ability: bool



class CardFeatureExtractor:
    """
    Converts raw card data into strategic features.
    """


    def __init__(self, card_database):

        self.db = card_database



    def extract(self, card_id: int):

        attacks = self.db.get_attacks(card_id)

        attack_features = (
            self._extract_attack_features(attacks)
        )


        category = self.db.get_category(card_id)


        return CardFeatures(

            card_id=card_id,

            name=self.db.get_name(card_id),

            stage=self.db.get_stage(card_id),

            category=(
                ""
                if category is None or pd.isna(category)
                else str(category)
            ),

            previous_stage=(
                self.db.get_previous_stage(card_id)
            ),


            is_pokemon=(
                self.db.is_pokemon(card_id)
            ),
            
            is_basic_pokemon=(
                self.db.is_basic_pokemon(card_id)
            ),
            is_stage1_pokemon=(
                self.db.is_stage1_pokemon(card_id)
            ),
            is_stage2_pokemon=(
                self.db.is_stage2_pokemon(card_id)
            ),

            is_trainer=(
                self.db.is_trainer(card_id)
            ),

            is_energy=(
                self.db.is_energy(card_id)
            ),


            hp=self._parse_number(
                self.db.get_hp(card_id)
            ),


            pokemon_type=(
                ""
                if pd.isna(self.db.get_type(card_id))
                else str(self.db.get_type(card_id))
            ),


            attack_count=(
                attack_features["attack_count"]
            ),

            max_damage=(
                attack_features["max_damage"]
            ),

            min_attack_energy=(
                attack_features["min_attack_energy"]
            ),


            is_ex=self._is_ex(card_id),

            has_ability=(
                self._has_ability(attacks)
            )
        )



    def _parse_number(self, value):

        if value is None or pd.isna(value):
            return 0


        try:
            return float(value)

        except:

            digits = ""

            for c in str(value):

                if c.isdigit():
                    digits += c

                elif digits:
                    break


            return float(digits) if digits else 0



    def _count_energy(self, cost):

        if cost is None or pd.isna(cost):
            return 0


        cost = str(cost)


        if "{" in cost:
            return cost.count("{")


        return cost.count("●")



    def _extract_attack_features(self, attacks):

        damages = []

        costs = []

        attack_count = 0


        for attack in attacks:

            name = attack["name"]


            if name.startswith("["):
                continue


            attack_count += 1


            damage = self._parse_number(
                attack["damage"]
            )


            if damage > 0:
                damages.append(damage)


            energy = self._count_energy(
                attack["cost"]
            )


            if energy > 0:
                costs.append(energy)



        return {

            "attack_count": attack_count,

            "max_damage": max(
                damages,
                default=0
            ),

            "min_attack_energy": min(
                costs,
                default=0
            )
        }



    def _is_ex(self, card_id):

        rule = self.db.get_rule(card_id)


        if rule is None:
            return False


        return "ex" in str(rule).lower()



    def _has_ability(self, attacks):

        return any(
            attack["name"].startswith("[Ability]")
            for attack in attacks
        )