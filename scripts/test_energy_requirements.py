from cards.card_database import CardDatabase


CSV = "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"


def main():

    db = CardDatabase(CSV)


    names = [
        "Leafeon",
        "Gouging Fire ex",
        "Raging Bolt",
        "Roaring Moon"
    ]


    for name in names:

        print("\n================")
        print(name)
        print("================")


        for card_id in db.cards.index:

            if db.get_name(card_id) == name:

                print(
                    "ID:",
                    card_id
                )


                for attack in db.get_attacks(card_id):

                    print(
                        attack["name"],
                        "=>",
                        attack["cost"]
                    )


                break



if __name__ == "__main__":
    main()