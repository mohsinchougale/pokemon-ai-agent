from collections import defaultdict

from cards.evolution_builder import EvolutionLineBuilder


class EvolutionLineDatabase:

    def __init__(self, card_database, extractor):

        self.db = card_database
        self.extractor = extractor

        self.builder = EvolutionLineBuilder(
            card_database,
            extractor
        )

        self.lines = []


    def build(self):

        pokemon_ids = []

        for card_id in self.db.cards.index:

            feature = self.extractor.extract(
                card_id
            )

            if feature.is_pokemon:
                pokemon_ids.append(card_id)


        self.lines = self.builder.build(
            pokemon_ids
        )


        return self.lines


    def get_lines(self):

        return self.lines