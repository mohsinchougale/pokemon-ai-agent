import pandas as pd
from pathlib import Path


class CardDatabase:
    """
    Loads Pokémon card metadata and provides lookup utilities.
    """

    def __init__(self, csv_path: str):
        self.cards = pd.read_csv(csv_path)

        # Make Card ID the index for fast lookup
        self.cards.set_index("Card ID", inplace=True)


    def get_card(self, card_id: int):
        """
        Return complete card information.
        """

        if card_id not in self.cards.index:
            return None


        card = self.cards.loc[card_id]


        # Handle duplicate Card IDs
        if isinstance(card, pd.DataFrame):
            card = card.iloc[0]


        return card

    def get_name(self, card_id: int):
        """
        Return card name from ID.
        """
        card = self.get_card(card_id)

        if card is None:
            return f"Unknown Card ({card_id})"

        return card["Card Name"]


    def get_type(self, card_id: int):
        card = self.get_card(card_id)

        if card is None:
            return None

        return card["Category"]


    def get_hp(self, card_id: int):
        card = self.get_card(card_id)

        if card is None:
            return None

        return card["HP"]



if __name__ == "__main__":

    path = (
        "data/raw/kaggle/"
        "pokemon-tcg-ai-battle/"
        "EN_Card_Data.csv"
    )

    db = CardDatabase(path)

    print(db.get_name(1158))
    print(db.get_card(1158))