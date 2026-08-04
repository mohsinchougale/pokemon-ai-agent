from engine.cg.game import battle_start


def main():

    deck = [1] * 60

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