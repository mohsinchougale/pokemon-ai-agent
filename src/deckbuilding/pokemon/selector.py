from deckbuilding.pokemon.scoring import EvolutionScorer


class PokemonSelector:

    """
    Provides Pokémon selection utilities.

    Strategies decide the final deck composition.
    This class only provides ranked Pokémon pools.
    """

    def __init__(self, pokemon_pool):

        self.pool = pokemon_pool
        self.scorer = EvolutionScorer()


    def get_best_evolution_lines(self, limit=None):

        lines = sorted(
            self.pool.evolution_db.lines,
            key=lambda line:
                self.scorer.score(
                    line,
                    self.pool.extractor
                ),
            reverse=True
        )

        if limit:
            return lines[:limit]

        return lines



    def build_evolution_line(
        self,
        line,
        basic_count=3,
        stage1_count=2,
        stage2_count=1
    ):

        cards = []


        # Basic
        cards.extend(
            [line.cards[0]] * basic_count
        )


        # Stage 1
        if line.stage1:

            cards.extend(
                [line.cards[1]] * stage1_count
            )


        # Stage 2
        if line.stage2:

            cards.extend(
                [line.cards[2]] * stage2_count
            )


        return cards



    def get_best_basic_attackers(self, limit=None):

        basics = sorted(
            self.pool.basic,
            key=lambda pokemon:
                (
                    pokemon.max_damage / 10
                    +
                    pokemon.hp / 50
                    +
                    (15 if pokemon.is_ex else 0)
                ),
            reverse=True
        )


        if limit:
            return basics[:limit]


        return basics



    def get_best_ex_attackers(self, limit=None):

        ex_cards = [
            pokemon
            for pokemon in self.pool.all_pokemon
            if pokemon.is_ex
        ]


        ex_cards.sort(
            key=lambda pokemon:
                (
                    pokemon.max_damage / 10
                    +
                    pokemon.hp / 50
                ),
            reverse=True
        )


        if limit:
            return ex_cards[:limit]


        return ex_cards