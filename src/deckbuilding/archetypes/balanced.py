from deckbuilding.archetypes.base import DeckArchetype

from deckbuilding.pokemon.pool import PokemonPool
from deckbuilding.pokemon.strategies.balanced import BalancedStrategy

from deckbuilding.trainers.pool import TrainerPool
from deckbuilding.trainers.selector import TrainerSelector

from deckbuilding.energy.selector import EnergySelector

from deckbuilding.deck_generator import DeckGenerator
from deckbuilding.deck_validator import DeckValidator


class BalancedArchetype(DeckArchetype):


    def build_generator(self):

        pokemon_pool = PokemonPool(
            self.db
        )


        return DeckGenerator(

            BalancedStrategy(
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