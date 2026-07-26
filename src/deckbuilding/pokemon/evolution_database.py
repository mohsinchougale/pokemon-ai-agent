from deckbuilding.pokemon.evolution_builder import EvolutionLineBuilder


class EvolutionLineDatabase:

    def __init__(self, card_database, extractor):

        self.db = card_database
        self.extractor = extractor

        self.builder = EvolutionLineBuilder(
            card_database,
            extractor
        )

        self.lines = []

        self.build()


    def build(self):

        pokemon_ids = []

        for card_id in self.db.cards.index:

            feature = self.extractor.extract(
                card_id
            )

            if feature.is_pokemon:
                pokemon_ids.append(card_id)


        raw_lines = self.builder.build(
            pokemon_ids
        )


        self.lines = self.deduplicate(
            raw_lines
        )


        return self.lines



    def deduplicate(self, lines):

        """
        Removes duplicate evolution families caused by
        alternate card printings.

        Example:
        Tepig -> Pignite -> Mega Emboar ex
        Tepig -> Pignite -> Mega Emboar ex

        becomes one evolution line.
        """

        unique = {}


        for line in lines:

            key = (
                line.basic.lower().strip()
                if line.basic
                else "",

                line.stage1.lower().strip()
                if line.stage1
                else "",

                line.stage2.lower().strip()
                if line.stage2
                else ""
            )


            if key not in unique:

                unique[key] = line


        return list(
            unique.values()
        )



    def get_lines(self):

        return self.lines