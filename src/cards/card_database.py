import pandas as pd


class CardDatabase:
    """
    Loads Pokémon card metadata and provides lookup utilities.
    """

    def __init__(self, csv_path: str):

        self.cards = pd.read_csv(csv_path)

        # Fast lookup by Card ID
        self.cards.set_index(
            "Card ID",
            inplace=True
        )

    def get_rule(self, card_id):

        card = self.get_card(card_id)

        if card is None:
            return None

        return card["Rule"]

    def get_card(self, card_id: int):
        """
        Return complete card information.
        """

        if card_id not in self.cards.index:
            return None


        card = self.cards.loc[card_id]


        # Some cards have multiple rows because
        # they have multiple attacks.
        if isinstance(card, pd.DataFrame):
            card = card.iloc[0]


        return card

    def get_card_rows(self, card_id: int):
        """
        Return all rows associated with a card.
        """

        if card_id not in self.cards.index:
            return None


        card = self.cards.loc[card_id]


        if isinstance(card, pd.Series):
            return card.to_frame().T


        return card

    def _get_value(
        self,
        card_id: int,
        column: str
    ):
        """
        Internal helper for column lookup.
        """

        card = self.get_card(card_id)

        if card is None:
            return None

        return card[column]



    def get_name(self, card_id: int):

        name = self._get_value(
            card_id,
            "Card Name"
        )

        return (
            name
            if name is not None
            else f"Unknown Card ({card_id})"
        )



    def get_stage(self, card_id: int):

        return self._get_value(
            card_id,
            "Stage (Pokémon)/Type (Energy and Trainer)"
        )



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



    def get_previous_stage(self, card_id: int):

        card = self.get_card(card_id)

        if card is None:
            return ""

        value = card["Previous stage"]

        if pd.isna(value):
            return ""

        return value


    def get_attacks(self, card_id: int):
        """
        Return attack rows only.
        """

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


    def get_attack_name(self, card_id: int):

        return self._get_value(
            card_id,
            "Move Name"
        )



    def get_attack_cost(self, card_id: int):

        return self._get_value(
            card_id,
            "Cost"
        )



    def get_damage(self, card_id: int):

        return self._get_value(
            card_id,
            "Damage"
        )



    def get_effect(self, card_id: int):

        return self._get_value(
            card_id,
            "Effect Explanation"
        )



    def get_retreat_cost(self, card_id: int):

        return self._get_value(
            card_id,
            "Retreat"
        )



if __name__ == "__main__":

    path = (
        "data/raw/kaggle/"
        "pokemon-tcg-ai-battle/"
        "EN_Card_Data.csv"
    )


    db = CardDatabase(path)


    card_id = 1158


    print(db.get_name(card_id))
    print(db.get_category(card_id))
    print(db.get_card(card_id))