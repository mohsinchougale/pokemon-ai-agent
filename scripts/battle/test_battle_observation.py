from cards.card_database import CardDatabase

from deckbuilding.archetypes.balanced import BalancedArchetype

from cg.game import battle_start


CSV = "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"


def print_deck_summary(deck, db, name):

    print("=" * 40)
    print(name)
    print("=" * 40)

    print("Deck size:", len(deck))

    print("\nFirst 20 cards:")

    for card_id in deck.cards[:20]:
        print(
            card_id,
            db.get_name(card_id)
        )

    print()



def main():

    db = CardDatabase(CSV)


    print("Generating decks...")

    generator = BalancedArchetype(
        db
    ).build_generator()


    deck1 = generator.generate()
    deck2 = generator.generate()


    print_deck_summary(
        deck1,
        db,
        "PLAYER 0 DECK"
    )


    print_deck_summary(
        deck2,
        db,
        "PLAYER 1 DECK"
    )


    print("Starting battle...")


    obs, start_data = battle_start(
    deck1.cards,
    deck2.cards
)


    print("\n")
    print("=" * 40)
    print("BATTLE POINTER DEBUG")
    print("=" * 40)

    from cg.sim import Battle

    print(
        "Battle pointer:",
        Battle.battle_ptr
    )


    print("\n")
    print("=" * 40)
    print("START DATA")
    print("=" * 40)

    print(start_data)


    print("\n")
    print("=" * 40)
    print("START DATA ATTRIBUTES")
    print("=" * 40)


    try:
        print(vars(start_data))

    except Exception as e:
        print(
            "Could not inspect start data:",
            e
        )


    print("\n")
    print("=" * 40)
    print("OBSERVATION")
    print("=" * 40)


    if obs is None:

        print(
            "Battle failed to initialize."
        )

    else:

        print(
            "Observation type:",
            type(obs)
        )


        print(
            "Observation keys:"
        )

        for key in obs.keys():

            print(
                "-",
                key
            )


        print("\nObservation:")

        print(obs)



if __name__ == "__main__":
    main()