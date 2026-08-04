from cards.card_database import CardDatabase
from deckbuilding.deck import Deck
from deckbuilding.deck_validator import DeckValidator


CSV = "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"


def build_energy_test_deck(pokemon_id, energy_ids):
    """
    Creates a legal 60-card deck for energy-only validation.

    Remaining slots are filled with Grass Energy.
    Basic Energy can exceed 4 copies.
    """

    cards = []

    # Add tested Pokemon
    cards.append(pokemon_id)

    # Add tested energy
    cards.extend(energy_ids)

    # Fill remaining slots with Basic Energy
    while len(cards) < 60:
        cards.append(1)  # Grass Basic Energy

    return Deck(cards)



def test(name, pokemon_id, energy_ids, expected):

    print("=" * 60)
    print(name)
    print("=" * 60)


    db = CardDatabase(CSV)

    validator = DeckValidator(db)


    deck = build_energy_test_deck(
        pokemon_id,
        energy_ids
    )


    result = validator.validate_energy(deck)


    print("Expected:", expected)
    print("Actual  :", result)
    print()



def main():

    # Roaring Moon -> {D}{D}
    test(
        "Roaring Moon + Darkness",
        61,
        [
            7,
            7
        ],
        True
    )


    test(
        "Roaring Moon + Fire",
        61,
        [
            2,
            2
        ],
        False
    )


    # Gouging Fire ex -> {R}●
    test(
        "Gouging Fire ex + Fire",
        46,
        [
            2
        ],
        True
    )


    # Raging Bolt -> {L}{F}
    test(
        "Raging Bolt + Lightning + Fighting",
        171,
        [
            4,
            6
        ],
        True
    )


    test(
        "Raging Bolt + Lightning only",
        171,
        [
            4
        ],
        False
    )



if __name__ == "__main__":
    main()