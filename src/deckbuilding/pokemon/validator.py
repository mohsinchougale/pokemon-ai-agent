from collections import Counter


class PokemonDeckValidator:
    """
    Validates Pokémon composition inside a deck.

    Checks:
    - Evolution chains are complete
    - No orphan evolutions
    - No impossible Stage 2 lines
    """


    def __init__(self, pokemon_pool):

        self.pool = pokemon_pool

        self.extractor = pokemon_pool.extractor



    def validate(self, cards):

        """
        Validate a list of Pokémon card IDs.

        Returns:
            True if valid
            False otherwise
        """


        counts = Counter(cards)


        for card_id in counts:

            feature = self.extractor.extract(
                card_id
            )


            if feature.stage == "Stage 1 Pokémon":

                if not self.has_basic(
                    feature.previous_stage,
                    cards
                ):

                    print(
                        "Invalid Stage 1:",
                        feature.name
                    )

                    return False



            if feature.stage == "Stage 2 Pokémon":

                if not self.has_stage1(
                    feature.previous_stage,
                    cards
                ):

                    print(
                        "Invalid Stage 2:",
                        feature.name
                    )

                    return False


        return True



    def has_basic(
        self,
        name,
        cards
    ):

        for card_id in cards:

            feature = self.extractor.extract(
                card_id
            )

            if (
                feature.name == name
                and
                feature.stage == "Basic Pokémon"
            ):

                return True


        return False



    def has_stage1(
        self,
        name,
        cards
    ):

        for card_id in cards:

            feature = self.extractor.extract(
                card_id
            )


            if (
                feature.name == name
                and
                feature.stage == "Stage 1 Pokémon"
            ):

                return True


        return False