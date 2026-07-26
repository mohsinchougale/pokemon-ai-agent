from dataclasses import dataclass
import pandas as pd

@dataclass
class CardFeatures:

    card_id: int
    name: str

    # Classification
    stage: str
    category: str

    is_pokemon: bool
    is_trainer: bool
    is_energy: bool

    # Pokemon stats
    hp: float
    pokemon_type: str

    # Attack information
    attack_count: int
    max_damage: int
    min_attack_energy: int

    # Special properties
    is_ex: bool
    has_ability: bool


class CardFeatureExtractor:
    """
    Converts raw card data into useful strategic features.
    """


    def __init__(self, card_database):

        self.db = card_database



    def extract(self, card_id: int):

        category = self.db.get_category(card_id)

        stage = self.db.get_stage(card_id)


        is_energy = (
            stage in [
                "Basic Energy",
                "Special Energy"
            ]
        )


        is_pokemon = (
            "Pokémon" in str(stage)
        )


        is_trainer = (
            stage in [
                "Item",
                "Supporter",
                "Stadium",
                "Pokémon Tool"
            ]
        )


        attacks = self.db.get_attacks(card_id)

        attack_features = self._extract_attack_features(attacks)


        return CardFeatures(

            card_id=card_id,

            name=self.db.get_name(card_id),

            category=(
                str(category)
                if not pd.isna(category)
                else ""
            ),

            stage=stage,


            hp=self._parse_number(
                self.db.get_hp(card_id)
            ),

            pokemon_type=(
                str(self.db.get_type(card_id))
                if not pd.isna(self.db.get_type(card_id))
                else ""
            ),


            # Attack features
            attack_count=attack_features["attack_count"],

            max_damage=attack_features["max_damage"],

            min_attack_energy=attack_features["min_attack_energy"],


            # Classification
            is_pokemon=is_pokemon,

            is_trainer=is_trainer,

            is_energy=is_energy,


            # Extra properties
            is_ex=self._is_ex(card_id),

            has_ability=self._has_ability(attacks)
        )



    def _parse_number(self, value):

        """
        Extract numeric values.

        Example:
            "120" -> 120
            "20×" -> 20
            NaN -> 0
        """

        if value is None:
            return 0
        
        if pd.isna(value):
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

        if cost is None:
            return 0

        if pd.isna(cost):
            return 0


        cost = str(cost)


        # Normal energy symbols
        # Example:
        # {R}{W}{C}
        if "{" in cost:
            return cost.count("{")


        # Generic energy symbols
        # Example:
        # ●●●
        return cost.count("●")
    

    def _extract_attack_features(self, attacks):

        damages = []
        costs = []

        attack_count = 0


        for attack in attacks:

            name = attack["name"]


            # Ignore rules, abilities, tera effects
            if name.startswith("["):
                continue


            attack_count += 1


            damage = self._parse_number(
                attack["damage"]
            )

            if damage > 0:
                damages.append(damage)


            energy_cost = self._count_energy(
                attack["cost"]
            )

            if energy_cost > 0:
                costs.append(energy_cost)



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

        for attack in attacks:

            if attack["name"].startswith("[Ability]"):
                return True

        return False