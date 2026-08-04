from collections import Counter


class Deck:

    def __init__(self, cards):

        if len(cards) != 60:
            raise ValueError(
                f"Deck must contain 60 cards, got {len(cards)}"
            )

        self.cards = cards


    def count(self):
        return len(self.cards)


    def card_counts(self):

        return Counter(self.cards)


    def validate_duplicates(self, card_database):

        counts = self.card_counts()

        for card_id, count in counts.items():

            # Basic Energy can exceed 4 copies
            if card_database.is_basic_energy(card_id):
                continue


            # ACE SPEC max 1
            if card_database.is_ace_spec(card_id):

                if count > 1:
                    return False

                continue


            # Everything else max 4
            if count > 4:
                return False


        return True


    def __len__(self):
        return len(self.cards)


    def __iter__(self):
        """
        Allow Deck to behave like a list of card IDs.
        Example:
            for card_id in deck:
                ...
        """
        return iter(self.cards)



def load_deck(path):

    with open(path) as f:

        cards = [
            int(x.strip())
            for x in f.readlines()
            if x.strip()
        ]

    return Deck(cards)