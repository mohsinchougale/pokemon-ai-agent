from deckbuilding.pokemon.selector import PokemonSelector
from deckbuilding.pokemon.validator import PokemonDeckValidator

class EvolutionHeavyStrategy:

    """
    Builds a Pokémon pool focused on evolution lines.

    Goal:
    - Maximum evolution synergy
    - Multiple Stage 2 attackers
    - Minimal filler Pokémon
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


        # Take the strongest evolution cores
        lines = self.selector.get_best_evolution_lines(
            limit=3
        )


        for line in lines:

            cards.extend(
                self.selector.build_evolution_line(
                    line
                )
            )


        # Trim if we exceed Pokémon budget
        if len(cards) > target_count:

            return cards[:target_count]


        # Fill remaining slots with strong attackers
        remaining = target_count - len(cards)


        if remaining > 0:

            attackers = (
                self.selector
                .get_best_basic_attackers()
            )


            used = set(cards)


            for pokemon in attackers:

                if pokemon.card_id not in used:

                    cards.append(
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