import pandas as pd


class CardDatabase:
    """
    Loads Pokémon card metadata and provides lookup utilities.

    This class is responsible for:
    - raw card access
    - metadata lookup
    - card classification
    - attack extraction
    """


    # -----------------------------------
    # Classification constants
    # -----------------------------------

    BASIC_ENERGY = {
        "Basic Energy"
    }

    SPECIAL_ENERGY = {
        "Special Energy"
    }


    POKEMON_STAGES = {
        "Basic Pokémon",
        "Stage 1 Pokémon",
        "Stage 2 Pokémon"
    }


    TRAINER_TYPES = {
        "Item",
        "Supporter",
        "Stadium",
        "Pokémon Tool"
    }


    BASIC_POKEMON = "Basic Pokémon"

    STAGE1_POKEMON = "Stage 1 Pokémon"

    STAGE2_POKEMON = "Stage 2 Pokémon"



    def __init__(self, csv_path: str):

        self.cards = pd.read_csv(csv_path)


        self.cards.drop_duplicates(
            subset=["Card ID"],
            inplace=True
        )


        self.cards.set_index(
            "Card ID",
            inplace=True
        )



    # -----------------------------------
    # Raw card access
    # -----------------------------------

    def get_card(self, card_id: int):

        if card_id not in self.cards.index:
            return None


        card = self.cards.loc[card_id]


        if isinstance(card, pd.DataFrame):
            card = card.iloc[0]


        return card



    def get_card_rows(self, card_id: int):

        if card_id not in self.cards.index:
            return None


        card = self.cards.loc[card_id]


        if isinstance(card, pd.Series):
            return card.to_frame().T


        return card



    # -----------------------------------
    # Generic lookup
    # -----------------------------------

    def _get_value(
        self,
        card_id: int,
        column: str
    ):

        card = self.get_card(card_id)


        if card is None:
            return None


        return card[column]



    # -----------------------------------
    # Metadata
    # -----------------------------------

    def get_name(self, card_id: int):

        value = self._get_value(
            card_id,
            "Card Name"
        )


        if value is None or pd.isna(value):
            return f"Unknown Card ({card_id})"


        return value



    def get_stage(self, card_id: int):

        value = self._get_value(
            card_id,
            "Stage (Pokémon)/Type (Energy and Trainer)"
        )


        if value is None or pd.isna(value):
            return ""


        return str(value)



    def get_category(self, card_id: int):

        return self._get_value(
            card_id,
            "Category"
        )



    def get_hp(self, card_id: int):

        return self._get_value(
            card_id,
            "HP"
        )



    def get_type(self, card_id: int):

        return self._get_value(
            card_id,
            "Type"
        )



    def get_rule(self, card_id: int):

        return self._get_value(
            card_id,
            "Rule"
        )



    def get_previous_stage(self, card_id: int):

        value = self._get_value(
            card_id,
            "Previous stage"
        )


        if value is None or pd.isna(value):
            return ""


        return value



    # -----------------------------------
    # Classification helpers
    # -----------------------------------

    def is_energy(self, card_id: int):

        return (
            self.is_basic_energy(card_id)
            or
            self.is_special_energy(card_id)
        )



    def is_basic_energy(self, card_id: int):

        return (
            self.get_stage(card_id)
            in self.BASIC_ENERGY
        )



    def is_special_energy(self, card_id: int):

        return (
            self.get_stage(card_id)
            in self.SPECIAL_ENERGY
        )



    def is_pokemon(self, card_id: int):

        return (
            self.get_stage(card_id)
            in self.POKEMON_STAGES
        )



    def is_basic_pokemon(self, card_id: int):

        return (
            self.get_stage(card_id)
            ==
            self.BASIC_POKEMON
        )



    def is_stage1_pokemon(self, card_id: int):

        return (
            self.get_stage(card_id)
            ==
            self.STAGE1_POKEMON
        )



    def is_stage2_pokemon(self, card_id: int):

        return (
            self.get_stage(card_id)
            ==
            self.STAGE2_POKEMON
        )



    def is_trainer(self, card_id: int):

        return (
            self.get_stage(card_id)
            in self.TRAINER_TYPES
        )



    # -----------------------------------
    # Energy lookup
    # -----------------------------------

    def get_basic_energy_id(self, energy_type):

        mapping = {

            "Grass": 1,
            "Fire": 2,
            "Water": 3,
            "Lightning": 4,
            "Psychic": 5,
            "Fighting": 6,
            "Darkness": 7,
            "Metal": 8

        }

        return mapping.get(energy_type)


    def is_ace_spec(self, card_id):

        stage = self.get_stage(card_id)

        return (
            str(stage).strip()
            ==
            "ACE SPEC"
        )
    # -----------------------------------
    # Attack utilities
    # -----------------------------------

    def get_attacks(self, card_id: int):

        rows = self.get_card_rows(card_id)


        if rows is None:
            return []


        attacks = []


        for _, row in rows.iterrows():

            move = row["Move Name"]


            if pd.notna(move):

                attacks.append(
                    {
                        "name": move,
                        "cost": row["Cost"],
                        "damage": row["Damage"],
                        "effect": row["Effect Explanation"]
                    }
                )


        return attacks

    def get_basic_energy_type(self, card_id):
    
            mapping = {
    
                "{G}": "Grass",
                "{R}": "Fire",
                "{W}": "Water",
                "{L}": "Lightning",
                "{P}": "Psychic",
                "{F}": "Fighting",
                "{D}": "Darkness",
                "{M}": "Metal"
    
            }
    
            energy = str(
                self.get_type(card_id)
            ).strip()
    
            return mapping.get(energy)