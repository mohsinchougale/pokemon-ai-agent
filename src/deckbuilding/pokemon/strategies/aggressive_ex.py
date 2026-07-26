from deckbuilding.pokemon.selector import PokemonSelector
from deckbuilding.pokemon.validator import PokemonDeckValidator

class AggressiveEXStrategy:

    """
    Aggressive EX-focused strategy.

    Prioritizes:
    - EX Pokémon
    - High damage
    - High HP

    Avoids evolution dependency.
    """


    def __init__(self, pokemon_pool):

        self.selector = PokemonSelector(
            pokemon_pool
        )

        self.validator = PokemonDeckValidator(
        pokemon_pool
    )


    def select_pokemon(self, target_count=15):

        cards = []


        attackers = (
            self.selector
            .get_best_basic_attackers()
        )


        used = set()


        for pokemon in attackers:

            copies = 2


            for _ in range(copies):

                if len(cards) >= target_count:
                    break


                cards.append(
                    pokemon.card_id
                )


            used.add(
                pokemon.card_id
            )


            if len(cards) >= target_count:
                break

        if not self.validator.validate(cards):

            print(
                "Invalid Pokémon pool generated."
            )

            return []

        return cards