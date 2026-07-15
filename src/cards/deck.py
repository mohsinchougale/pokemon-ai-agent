from pathlib import Path


def load_deck(path):

    with open(path) as f:
        cards = [
            int(x.strip())
            for x in f.readlines()
            if x.strip()
        ]

    if len(cards) != 60:
        raise ValueError(
            f"Deck must have 60 cards, got {len(cards)}"
        )

    return cards