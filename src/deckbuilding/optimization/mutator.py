import random
from collections import Counter

from deckbuilding.deck import Deck


class DeckMutator:


    def __init__(self, card_database):

        self.db = card_database

        self.item_pool = []
        self.supporter_pool = []
        self.stadium_pool = []
        self.ace_spec_pool = []
        self.energy_pool = []
        self.pokemon_pool = []

        self.last_mutation = None

        self._categorize()



    def _categorize(self):

        for card_id in self.db.cards.index:

            if self.db.is_energy(card_id):
                self.energy_pool.append(card_id)

            elif self.db.is_trainer(card_id):

                if self.db.is_ace_spec(card_id):
                    self.ace_spec_pool.append(card_id)

                elif self.db.is_item(card_id):
                    self.item_pool.append(card_id)

                elif self.db.is_supporter(card_id):
                    self.supporter_pool.append(card_id)

                elif self.db.is_stadium(card_id):
                    self.stadium_pool.append(card_id)

            elif self.db.is_pokemon(card_id):
                self.pokemon_pool.append(card_id)



    def mutate(self, deck):

        original = deck.cards.copy()

        cards = deck.cards.copy()


        mutation = random.choices(
            [
                "trainer",
                "pokemon",
                "energy"
            ],
            weights=[
                0.55,
                0.40,
                0.05
            ]
        )[0]


        self.last_mutation = None


        if mutation == "trainer":

            self._replace(
                cards,
                (
                    self.item_pool
                    + self.supporter_pool
                    + self.stadium_pool
                    + self.ace_spec_pool
                ),
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


        if len(cards) != 60:

            return Deck(original)


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
            for i,c in enumerate(cards)
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


                if mutation_type == "pokemon":

                    candidate = self._choose_valid_pokemon(
                        old_card,
                        cards
                    )


                elif mutation_type == "trainer":

                    candidate = self._choose_valid_trainer(
                        old_card
                    )


                else:

                    candidate = random.choice(
                        pool
                    )



                if candidate == old_card:
                    continue



                limit = (
                    1
                    if self.db.is_ace_spec(candidate)
                    else 4
                )


                if counts[candidate] >= limit:
                    continue



                cards[idx] = candidate



                if mutation_type == "pokemon":

                    self._repair_energy(cards)



                self.last_mutation = {

                    "type": mutation_type,

                    "removed": old_card,

                    "added": candidate

                }


                return



    def _repair_energy(self, cards):


        required = set()


        for card_id in cards:

            if self.db.is_pokemon(card_id):

                required.update(
                    self.db.get_required_energy_types(card_id)
                )



        current = set()


        for card_id in cards:

            if self.db.is_energy(card_id):

                energy_type = (
                    self.db.get_basic_energy_type(card_id)
                )

                if energy_type:
                    current.add(energy_type)



        missing = required - current



        for energy_type in missing:


            energy_id = (
                self.db.get_basic_energy_id(
                    energy_type
                )
            )


            if energy_id is None:
                continue



            removable = [

                c
                for c in cards
                if self.db.is_energy(c)

            ]



            if removable:

                old_energy = random.choice(
                    removable
                )

                cards.remove(
                    old_energy
                )

                cards.append(
                    energy_id
                )



    def _choose_valid_pokemon(
        self,
        old_card,
        cards
    ):


        candidates = []


        old_ex = self.db.is_ex(old_card)



        for card_id in self.pokemon_pool:


            if card_id == old_card:
                continue


            if not self.db.is_basic_pokemon(card_id):
                continue


            if self.db.is_ex(card_id) != old_ex:
                continue



            candidates.append(card_id)



        if not candidates:
            return old_card



        return random.choice(candidates)



    def _choose_valid_trainer(
        self,
        old_card
    ):


        if self.db.is_ace_spec(old_card):

            return (
                random.choice(self.ace_spec_pool)
                if self.ace_spec_pool
                else old_card
            )



        if self.db.is_item(old_card):

            return (
                random.choice(self.item_pool)
                if self.item_pool
                else old_card
            )


        if self.db.is_supporter(old_card):

            return (
                random.choice(self.supporter_pool)
                if self.supporter_pool
                else old_card
            )


        if self.db.is_stadium(old_card):

            return (
                random.choice(self.stadium_pool)
                if self.stadium_pool
                else old_card
            )


        return old_card



    def _is_evolution_piece(
        self,
        card_id,
        cards
    ):


        if self.db.get_previous_stage(card_id):
            return True



        name = self.db.get_name(card_id)



        for other in cards:


            if other == card_id:
                continue


            if str(
                self.db.get_previous_stage(other)
            ) == str(name):

                return True



        return False