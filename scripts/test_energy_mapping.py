from cards.card_database import CardDatabase


CSV_PATH = (
    "data/raw/kaggle/"
    "pokemon-tcg-ai-battle/"
    "EN_Card_Data.csv"
)


def show(df, columns):

    temp = df.copy()

    temp.insert(
        0,
        "Card ID",
        temp.index
    )

    print(
        temp[columns]
        .to_string(index=False)
    )


def main():

    db = CardDatabase(CSV_PATH)


    print("\n==============================")
    print("1. BASIC / SPECIAL ENERGY CARDS")
    print("==============================\n")


    energy_cards = db.cards[
        db.cards[
            "Stage (Pokémon)/Type (Energy and Trainer)"
        ].isin(
            [
                "Basic Energy",
                "Special Energy"
            ]
        )
    ]


    show(
        energy_cards,
        [
            "Card ID",
            "Card Name",
            "Stage (Pokémon)/Type (Energy and Trainer)",
            "Type"
        ]
    )



    print("\n==============================")
    print("2. UNIQUE STAGE VALUES")
    print("==============================\n")


    print(
        db.cards[
            "Stage (Pokémon)/Type (Energy and Trainer)"
        ]
        .value_counts()
        .to_string()
    )



    print("\n==============================")
    print("3. ATTACK COST EXAMPLES")
    print("==============================\n")


    pokemon = db.cards[
        db.cards[
            "Stage (Pokémon)/Type (Energy and Trainer)"
        ].isin(
            [
                "Basic Pokémon",
                "Stage 1 Pokémon",
                "Stage 2 Pokémon"
            ]
        )
    ]


    attacks = (
        pokemon[
            [
                "Card Name",
                "Move Name",
                "Cost"
            ]
        ]
        .dropna(
            subset=[
                "Cost"
            ]
        )
        .head(100)
    )


    print(
        attacks.to_string(index=False)
    )



    print("\n==============================")
    print("4. UNIQUE COST SYMBOLS")
    print("==============================\n")


    symbols = set()


    for cost in (
        db.cards["Cost"]
        .dropna()
        .astype(str)
    ):

        for char in cost:
            symbols.add(char)


    print(
        sorted(symbols)
    )



    print("\n==============================")
    print("5. ENERGY TYPE COLUMN VALUES")
    print("==============================\n")


    print(
        energy_cards["Type"]
        .value_counts()
        .to_string()
    )



    print("\n==============================")
    print("6. ACE SPEC CHECK")
    print("==============================\n")


    ace = db.cards[
        db.cards[
            "Stage (Pokémon)/Type (Energy and Trainer)"
        ]
        .astype(str)
        .str.contains(
            "ACE",
            case=False
        )
    ]


    if len(ace) == 0:

        print(
            "No ACE SPEC cards found"
        )

    else:

        show(
            ace,
            [
                "Card ID",
                "Card Name",
                "Stage (Pokémon)/Type (Energy and Trainer)"
            ]
        )



    print("\n==============================")
    print("7. CURRENT ENERGY ID MAPPING TEST")
    print("==============================\n")


    energy_types = [
        "Grass",
        "Fire",
        "Water",
        "Lightning",
        "Psychic",
        "Fighting",
        "Darkness",
        "Metal"
    ]


    for energy in energy_types:

        print(
            energy,
            "->",
            db.get_basic_energy_id(energy)
        )


    print("\n==============================")
    print("DONE")
    print("==============================")



if __name__ == "__main__":
    main()