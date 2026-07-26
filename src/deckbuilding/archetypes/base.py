class DeckArchetype:
    """
    Base class for deck archetypes.

    An archetype defines:
    - Pokémon strategy
    - Trainer strategy
    - Energy strategy
    """

    def __init__(self, card_database):
        self.db = card_database


    def build_generator(self):
        raise NotImplementedError


    def generate(self):

        generator = self.build_generator()

        return generator.generate()