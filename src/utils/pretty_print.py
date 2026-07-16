from engine.cg.api import OptionType, to_observation_class


def print_card(card_db, card_id):

    print(
        card_db.get_name(card_id),
        f"(ID: {card_id})"
    )


def option_type_name(option_type):

    mapping = {

        OptionType.YES: "YES",
        OptionType.NO: "NO",

        OptionType.PLAY: "PLAY",
        OptionType.ATTACH: "ATTACH",
        OptionType.ATTACK: "ATTACK",
        OptionType.END: "END",

        OptionType.RETREAT: "RETREAT",
        OptionType.EVOLVE: "EVOLVE",

    }

    return mapping.get(
        option_type,
        str(option_type)
    )


def pretty_print_actions(obs, card_db):

    if isinstance(obs, dict):
        obs = to_observation_class(obs)

    if obs.select is None:
        print("No actions available")
        return


    print("\nAVAILABLE ACTIONS")
    print("------------------")


    for idx, option in enumerate(obs.select.option):

        print(
            f"{idx}: ",
            end=""
        )


        if option.type == OptionType.PLAY:

            print(
                "Play",
                card_db.get_name(option.cardId)
            )

        elif option.type == OptionType.ATTACH:

            print(
                "Attach energy"
            )

        elif option.type == OptionType.ATTACK:

            print(
                "Attack"
            )

        elif option.type == OptionType.END:

            print(
                "End turn"
            )

        else:
            print(option_type_name(option.type))




def pretty_print_state(obs, card_db):

    if isinstance(obs, dict):
        obs = to_observation_class(obs)

    state = obs.current

    if state is None:
        return


    player = state.players[state.yourIndex]


    print("="*50)

    print(
        f"TURN {state.turn}"
    )

    print("="*50)


    print("\nYOUR ACTIVE")


    if len(player.active) > 0:

        pokemon = player.active[0]

        if pokemon is None:

            print("Facedown Pokémon")

        else:

            print(
                card_db.get_name(pokemon.id),
                f"HP {pokemon.hp}/{pokemon.maxHp}"
            )

    else:

        print("No Active Pokémon")


    print("\nHAND")

    if player.hand:

        for card in player.hand:

            print(
                "-",
                card_db.get_name(card.id)
            )

    else:

        print(
            f"{player.handCount} cards"
        )


    print("\nDECK COUNT:")
    print(player.deckCount)


    pretty_print_actions(
        obs,
        card_db
    )