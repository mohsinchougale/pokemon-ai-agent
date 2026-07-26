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



    def validate_duplicates(self):

        counts = self.card_counts()


        for card_id, count in counts.items():

            # Energy cards are handled separately later
            if count > 4:

                return False


        return True



    def __len__(self):

        return len(self.cards)



def load_deck(path):

    with open(path) as f:

        cards = [
            int(x.strip())
            for x in f.readlines()
            if x.strip()
        ]


    return Deck(cards)