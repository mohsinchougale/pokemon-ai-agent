import random
from collections import Counter

from deckbuilding.deck import Deck


class DeckMutator:
    """
    Performs small mutations on a deck while trying to keep it legal.

    Initial mutations:
    - Replace one Trainer card
    - Replace one Energy card
    - Replace one Pokémon card
    """

    def __init__(self, card_database):

        self.db = card_database

        self.trainer_pool = []
        self.energy_pool = []
        self.pokemon_pool = []

        self._categorize()


    def _categorize(self):

        for card_id in self.db.cards.index:

            stage = self.db.get_stage(card_id)

            if stage in ["Basic Energy", "Special Energy"]:

                self.energy_pool.append(card_id)

            elif stage in ["Item", "Supporter", "Stadium", "Pokémon Tool"]:

                self.trainer_pool.append(card_id)

            elif "Pokémon" in str(stage):

                self.pokemon_pool.append(card_id)


    def mutate(self, deck):

        cards = deck.cards.copy()

        mutation = random.choice(
            [
                "trainer",
                "energy",
                "pokemon"
            ]
        )

        if mutation == "trainer":

            self._replace(cards, self.trainer_pool, self._is_trainer)

        elif mutation == "energy":

            self._replace(cards, self.energy_pool, self._is_energy)

        else:

            self._replace(cards, self.pokemon_pool, self._is_pokemon)

        return Deck(cards)


    def _replace(self, cards, pool, predicate):

        indices = [
            i for i, c in enumerate(cards)
            if predicate(c)
        ]

        if not indices:

            return

        idx = random.choice(indices)

        counts = Counter(cards)

        for _ in range(50):

            candidate = random.choice(pool)

            stage = self.db.get_stage(candidate)

            limit = 1 if "ACE SPEC" in str(stage) else 4

            if counts[candidate] < limit:

                cards[idx] = candidate
                return


    def _is_trainer(self, card_id):

        stage = self.db.get_stage(card_id)

        return stage in ["Item", "Supporter", "Stadium", "Pokémon Tool"]


    def _is_energy(self, card_id):

        stage = self.db.get_stage(card_id)

        return stage in ["Basic Energy", "Special Energy"]


    def _is_pokemon(self, card_id):

        return "Pokémon" in str(self.db.get_stage(card_id))