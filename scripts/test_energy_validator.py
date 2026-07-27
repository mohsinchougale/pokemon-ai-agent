from cards.card_database import CardDatabase
from deckbuilding.deck import Deck
from deckbuilding.deck_validator import DeckValidator


CSV = "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"


ROARING_MOON = 61
GOUGING_FIRE = 46
RAGING_BOLT = 171


DARKNESS = 7
FIRE = 2
LIGHTNING = 4
FIGHTING = 6
GRASS = 1



def build_deck(main_cards, energies):

    cards = []

    cards.extend(main_cards)

    cards.extend(energies)


    # Fill remaining slots with Basic Energy.
    # Basic Energy has unlimited copies.
    while len(cards) < 60:
        cards.append(GRASS)


    return Deck(cards)



def test(
    name,
    deck,
    expected,
    validator
):

    print("=" * 60)
    print(name)
    print("=" * 60)

    result = validator.validate(deck)

    print("Expected:", expected)
    print("Actual  :", result)

    print()



def main():

    db = CardDatabase(CSV)

    validator = DeckValidator(db)


    test(
        "Roaring Moon + Darkness Energy",
        build_deck(
            [ROARING_MOON],
            [DARKNESS]
        ),
        True,
        validator
    )


    test(
        "Roaring Moon + Fire Energy",
        build_deck(
            [ROARING_MOON],
            [FIRE]
        ),
        False,
        validator
    )


    test(
        "Gouging Fire ex + Fire Energy",
        build_deck(
            [GOUGING_FIRE],
            [FIRE]
        ),
        True,
        validator
    )


    test(
        "Raging Bolt + Lightning + Fighting",
        build_deck(
            [RAGING_BOLT],
            [
                LIGHTNING,
                FIGHTING
            ]
        ),
        True,
        validator
    )


    test(
        "Raging Bolt + Lightning Only",
        build_deck(
            [RAGING_BOLT],
            [LIGHTNING]
        ),
        False,
        validator
    )



if __name__ == "__main__":
    main()