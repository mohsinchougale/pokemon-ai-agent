import random
from collections import Counter

from deckbuilding.deck import Deck


class DeckMutator:
    """
    Performs intelligent deck mutations.

    Mutation strategy:
    - Favor trainer optimization
    - Protect evolution cores
    - Track mutation history
    """

    def __init__(self, card_database):

        self.db = card_database

        self.trainer_pool = []
        self.energy_pool = []
        self.pokemon_pool = []

        self.last_mutation = None

        self._categorize()



    def _categorize(self):

        for card_id in self.db.cards.index:

            if self.db.is_energy(card_id):

                self.energy_pool.append(card_id)


            elif self.db.is_trainer(card_id):

                self.trainer_pool.append(card_id)


            elif self.db.is_pokemon(card_id):

                self.pokemon_pool.append(card_id)



    def mutate(self, deck):

        cards = deck.cards.copy()


        mutation = random.choices(
            [
                "trainer",
                "pokemon",
                "energy"
            ],
            weights=[
                0.6,
                0.3,
                0.1
            ]
        )[0]


        self.last_mutation = None


        if mutation == "trainer":

            self._replace(
                cards,
                self.trainer_pool,
                self.db.is_trainer,
                "trainer"
            )


        elif mutation == "pokemon":

            self._replace(
                cards,
                self.pokemon_pool,
                self.db.is_pokemon,
                "pokemon"
            )


        else:

            self._replace(
                cards,
                self.energy_pool,
                self.db.is_energy,
                "energy"
            )


        return Deck(cards)



    def _replace(
        self,
        cards,
        pool,
        predicate,
        mutation_type
    ):

        indices = [
            i
            for i, c in enumerate(cards)
            if predicate(c)
        ]


        if not indices:
            return


        random.shuffle(indices)

        counts = Counter(cards)


        for idx in indices:

            old_card = cards[idx]


            if mutation_type == "pokemon":

                if self._is_evolution_piece(
                    old_card,
                    cards
                ):
                    continue



            for _ in range(100):

                candidate = random.choice(pool)


                limit = (
                    1
                    if self.db.is_ace_spec(candidate)
                    else 4
                )


                if counts[candidate] < limit:

                    cards[idx] = candidate


                    self.last_mutation = {

                        "type": mutation_type,

                        "removed": old_card,

                        "added": candidate

                    }


                    return




    def _is_evolution_piece(
        self,
        card_id,
        cards
    ):

        """
        Prevent removal of cards
        that are part of an evolution chain.
        """


        name = self.db.get_name(card_id)


        for other in cards:

            if other == card_id:
                continue


            other_name = self.db.get_name(other)


            if (
                name in str(other_name)
                or other_name in str(name)
            ):

                return True


        return False