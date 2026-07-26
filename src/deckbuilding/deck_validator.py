from collections import Counter


class DeckValidator:
    """
    Validates generated Pokémon TCG decks.

    Checks:
    - Exactly 60 cards
    - Copy limits
    - Evolution legality
    - At least one Basic Pokémon
    """


    def __init__(self, card_database):

        self.db = card_database



    def validate(self, deck):

        checks = [

            self.validate_size(deck),

            self.validate_duplicates(deck),

            self.validate_basic_pokemon(deck),

            self.validate_evolutions(deck)

        ]


        return all(checks)



    def validate_size(self, deck):

        if len(deck) != 60:

            print(
                f"Invalid deck size: {len(deck)}"
            )

            return False


        return True



    def validate_duplicates(self, deck):

        counts = Counter(deck.cards)


        for card_id, count in counts.items():

            stage = self.db.get_stage(card_id)


            # Energy has unlimited copies
            if "Energy" in str(stage):

                continue


            if count > 4:

                print(
                    f"Too many copies: "
                    f"{self.db.get_name(card_id)} ({count})"
                )

                return False


        return True



    def validate_basic_pokemon(self, deck):

        basics = 0


        for card_id in deck.cards:

            stage = self.db.get_stage(card_id)


            if stage == "Basic Pokémon":

                basics += 1


        if basics == 0:

            print(
                "No Basic Pokémon found"
            )

            return False


        return True



    def validate_evolutions(self, deck):

        counts = Counter(deck.cards)


        for card_id in deck.cards:

            stage = self.db.get_stage(card_id)


            if stage == "Stage 1":

                if not self._has_previous_stage(
                    card_id,
                    counts
                ):

                    print(
                        "Missing evolution for:",
                        self.db.get_name(card_id)
                    )

                    return False



            if stage == "Stage 2":

                if not self._has_previous_stage(
                    card_id,
                    counts
                ):

                    print(
                        "Missing Stage 1 for:",
                        self.db.get_name(card_id)
                    )

                    return False


        return True



    def _has_previous_stage(
        self,
        card_id,
        counts
    ):

        previous = self.db.get_previous_stage(
            card_id
        )


        if not previous:

            return False


        for existing_id in counts:

            name = self.db.get_name(
                existing_id
            )


            if name == previous:

                return True


        return False