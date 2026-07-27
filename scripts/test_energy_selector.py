from cards.card_database import CardDatabase
from deckbuilding.energy.selector import EnergySelector


def main():

    db = CardDatabase(
         "data/raw/kaggle/"
            "pokemon-tcg-ai-battle/"
            "EN_Card_Data.csv"
    )

    selector = EnergySelector(db)


    test_costs = [

        "{G}",
        "{R}●",
        "{W}{W}",
        "●●",
        "{F}{M}",
        "No cost"

    ]


    print("\nENERGY PARSER TEST\n")

    for cost in test_costs:

        print(
            cost,
            "=>",
            selector._parse_cost(cost)
        )


    print("\n==============================")
    print("ENERGY SELECTION TEST")
    print("==============================\n")


    pokemon_cards = []


    wanted = [
        "Leafeon",
        "Gouging Fire ex",
        "Froakie",
        "Raging Bolt",
        "Roaring Moon"
    ]


    for name in wanted:

        found = False

        for card_id in db.cards.index:

            if db.get_name(card_id) == name:

                pokemon_cards.append(card_id)
                found = True
                break


        if not found:
            print(
                "Could not find:",
                name
            )


    print(
        "\nPokemon tested:"
    )

    for card_id in pokemon_cards:

        print(
            card_id,
            db.get_name(card_id)
        )



    energy = selector.select_energy(
        pokemon_cards,
        15
    )


    print(
        "\nSelected Energy IDs:"
    )

    print(energy)


    print(
        "\nSelected Energy Names:"
    )

    for e in energy:

        print(
            e,
            db.get_name(e)
        )

    print("\nALLOCATION STRESS TEST\n")


    fake_requirements = {

        "Fire": 7,
        "Water": 3,
        "Grass": 2

    }


    energy = selector._allocate_energy(
        fake_requirements,
        15
    )


    print(energy)

    print(
        [
            db.get_name(x)
            for x in energy
        ]
    )

if __name__ == "__main__":
    main()