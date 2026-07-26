from deckbuilding.archetypes.base import DeckArchetype

from deckbuilding.pokemon.pool import PokemonPool
from deckbuilding.pokemon.strategies.aggressive_ex import (
    AggressiveEXStrategy
)

from deckbuilding.trainers.pool import TrainerPool
from deckbuilding.trainers.selector import TrainerSelector

from deckbuilding.energy.selector import EnergySelector

from deckbuilding.deck_generator import DeckGenerator
from deckbuilding.deck_validator import DeckValidator


class AggressiveEXArchetype(DeckArchetype):


    def build_generator(self):

        pokemon_pool = PokemonPool(
            self.db
        )


        return DeckGenerator(

            AggressiveEXStrategy(
                pokemon_pool
            ),

            TrainerSelector(
                TrainerPool(self.db)
            ),

            EnergySelector(
                self.db
            ),

            DeckValidator(
                self.db
            )
        )