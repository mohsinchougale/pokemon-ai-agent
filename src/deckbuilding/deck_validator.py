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

            self.validate_evolutions(deck),

            self.validate_energy(deck)

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

            if self.db.is_energy(card_id):
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

            if self.db.is_basic_pokemon(card_id):
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

            if self.db.is_basic_pokemon(card_id):

                if not self._has_previous_stage(
                    card_id,
                    counts
                ):

                    print(
                        "Missing evolution for:",
                        self.db.get_name(card_id)
                    )

                    return False



            if self.db.is_stage2_pokemon(card_id):

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

    def validate_energy(self, deck):

        energy_types = set()

        for card_id in deck.cards:

            if self.db.is_basic_energy(card_id):

                energy = self.db.get_basic_energy_type(
                    card_id
                )

                if energy is not None:

                    energy_types.add(
                        energy
                    )

        required = set()

        for card_id in deck.cards:

            if not self.db.is_pokemon(card_id):
                continue

            for attack in self.db.get_attacks(card_id):

                cost = attack["cost"]

                if cost is None:
                    continue

                for energy in self._parse_energy_cost(cost):

                    required.add(
                        energy
                    )

        missing = required - energy_types

        if missing:

            print(
                "Missing required energy:",
                missing
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

    def _parse_energy_cost(self, cost):

        mapping = {

            "G": "Grass",
            "R": "Fire",
            "W": "Water",
            "L": "Lightning",
            "P": "Psychic",
            "F": "Fighting",
            "D": "Darkness",
            "M": "Metal"

        }

        result = []

        text = str(cost)

        for symbol, energy in mapping.items():

            if f"{{{symbol}}}" in text:

                result.append(
                    energy
                )

        return result

    