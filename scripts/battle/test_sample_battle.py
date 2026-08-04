from engine.cg.game import battle_start


def load_deck(path):

    with open(path) as f:
        return [
            int(x.strip())
            for x in f.readlines()
            if x.strip()
        ]


def main():

    deck = load_deck(
        "data/raw/kaggle/pokemon-tcg-ai-battle/sample_submission/sample_submission/deck.csv"
    )

    print("Deck size:", len(deck))

    obs, start = battle_start(
        deck,
        deck
    )

    print("====================")
    print("Battle Pointer:")
    print(start.battlePtr)

    print("====================")
    print("Error Player:")
    print(start.errorPlayer)

    print("====================")
    print("Error Type:")
    print(start.errorType)

    print("====================")
    print("Observation:")
    print(obs)


if __name__ == "__main__":
    main()