from deckbuilding.pokemon.selector import PokemonSelector
from deckbuilding.pokemon.validator import PokemonDeckValidator

class BalancedStrategy:

    """
    Balanced Pokémon strategy.

    Mix:
    - Strong evolution cores
    - Standalone attackers

    Goal:
    More consistent than EvolutionHeavy,
    but still keeps evolution power.
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


        #
        # Select two strongest evolution lines
        #
        lines = self.selector.get_best_evolution_lines(
            limit=2
        )


        for line in lines:

            cards.extend(
                self.selector.build_evolution_line(
                    line
                )
            )


        #
        # Fill remaining slots with attackers
        #
        remaining = target_count - len(cards)


        used = set(cards)


        if remaining > 0:

            attackers = (
                self.selector
                .get_best_basic_attackers()
            )


            for pokemon in attackers:

                if pokemon.card_id in used:
                    continue


                cards.append(
                    pokemon.card_id
                )

                used.add(
                    pokemon.card_id
                )


                remaining -= 1


                if remaining == 0:
                    break
        
        if not self.validator.validate(cards):

            print(
                "Invalid Pokémon pool generated."
            )

            return []

        return cards