from collections import defaultdict

from cards.card_features import CardFeatureExtractor
from deckbuilding.pokemon.evolution_database import EvolutionLineDatabase


class PokemonPool:

    """
    Stores every Pokémon in a format useful for deck generation.
    """

    def __init__(self, card_database):

        self.db = card_database
        self.extractor = CardFeatureExtractor(card_database)

        self.evolution_db = EvolutionLineDatabase(
            card_database,
            self.extractor
        )

        self.all_pokemon = []
        self.basic = []
        self.stage1 = []
        self.stage2 = []
        self.ex = []

        self._build()

        self.two_stage_lines = []
        self.three_stage_lines = []

        self._categorize_lines()

    def _categorize_lines(self):

        for line in self.evolution_db.lines:

            if line.stage2:
                self.three_stage_lines.append(line)
            else:
                self.two_stage_lines.append(line)



    def _build(self):

        for card_id in self.db.cards.index:

            feature = self.extractor.extract(card_id)

            if not feature.is_pokemon:
                continue

            self.all_pokemon.append(feature)

            if feature.stage == "Basic Pokémon":
                self.basic.append(feature)

            elif feature.stage == "Stage 1 Pokémon":
                self.stage1.append(feature)

            elif feature.stage == "Stage 2 Pokémon":
                self.stage2.append(feature)

            if feature.is_ex:
                self.ex.append(feature)