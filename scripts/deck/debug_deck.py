from cg.api import all_card_data
from collections import Counter


cards = {
    c.cardId: c
    for c in all_card_data()
}


def validate(deck):

    print("Deck size:", len(deck))

    # ID validation
    missing = [
        cid for cid in deck
        if cid not in cards
    ]

    print("Invalid IDs:", missing)


    # Name counts
    names = Counter(
        cards[cid].name
        for cid in deck
    )

    print("\nCopies >4:")
    for name,count in names.items():
        if count > 4:
            print(name,count)


    # ACE SPEC
    ace = [
        cards[cid].name
        for cid in deck
        if cards[cid].aceSpec
    ]

    print("\nACE SPEC:")
    print(ace)


    # Pokemon count
    pokemon = [
        cards[cid]
        for cid in deck
        if cards[cid].cardType == 0
    ]

    print("\nPokemon:",len(pokemon))


    # Basic Pokemon
    basics = [
        c.name
        for c in pokemon
        if c.basic
    ]

    print("Basics:", basics)


if __name__ == "__main__":
    from deckbuilding.archetypes.balanced import BalancedArchetype
    from cards.card_database import CardDatabase

    db = CardDatabase(
        "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
    )

    archetype = BalancedArchetype(db)
    deck = archetype.build_generator().generate()

    validate(deck)

    print("\n========== FULL DECK ==========\n")

    from collections import Counter

    for cid, count in Counter(deck.cards).items():
        print(
            f"{cid:4d}  x{count:<2}  {cards[cid].name}"
        )