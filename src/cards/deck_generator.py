import random

from cards.deck import Deck


class DeckGenerator:
    """
    Generates legal Pokémon TCG decks.

    Initial version:
    - Random sampling
    - Respects card copy limits
    - Uses rough deck composition ratios
    """

    def __init__(self, card_database):

        self.db = card_database

        self.pokemon_cards = []
        self.trainer_cards = []
        self.energy_cards = []

        self._categorize_cards()


    def _categorize_cards(self):

        """
        Split cards into Pokémon, Trainer, and Energy pools.
        """

        for card_id in self.db.cards.index:

            stage = self.db.get_stage(card_id)


            if stage in [
                "Basic Energy",
                "Special Energy"
            ]:
                self.energy_cards.append(card_id)


            elif stage in [
                "Item",
                "Supporter",
                "Stadium",
                "Pokémon Tool"
            ]:
                self.trainer_cards.append(card_id)


            elif "Pokémon" in str(stage):
                self.pokemon_cards.append(card_id)



    def generate_random_deck(
        self,
        pokemon_count=15,
        trainer_count=30,
        energy_count=15
    ):

        cards = []


        cards.extend(
            self._sample_cards(
                self.pokemon_cards,
                pokemon_count
            )
        )


        cards.extend(
            self._sample_cards(
                self.trainer_cards,
                trainer_count
            )
        )


        cards.extend(
            self._sample_cards(
                self.energy_cards,
                energy_count
            )
        )


        random.shuffle(cards)

        return Deck(cards)



    def _sample_cards(self, pool, count):

        """
        Sample cards respecting max 4 copies.

        Energy cards are handled separately.
        """

        selected = []

        counts = {}

        while len(selected) < count:

            card = random.choice(pool)


            current = counts.get(card, 0)


            if current >= 4:

                continue


            selected.append(card)

            counts[card] = current + 1


        return selected