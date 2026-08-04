from engine.cg.game import (
    battle_start,
    battle_finish,
)


class EngineDeckValidator:
    """
    Validates whether a deck can initialize inside
    the Pokémon TCG simulator engine.

    The normal DeckValidator checks Pokémon TCG rules.
    This validator checks simulator compatibility.
    """

    def __init__(self):
        pass


    def validate(self, deck):

        try:

            cards = deck.cards

            obs, start_data = battle_start(
                cards,
                cards
            )


            # Battle initialized successfully
            if start_data.battlePtr:

                return True


            print(
                "Engine rejected deck:",
                {
                    "error_player": start_data.errorPlayer,
                    "error_type": start_data.errorType
                }
            )


            return False


        except Exception as e:

            print(
                "Engine validation error:",
                e
            )

            return False


        finally:

            try:

                battle_finish()

            except Exception:

                pass