from deckbuilding.archetypes.base import DeckArchetype

from deckbuilding.pokemon.pool import PokemonPool

from deckbuilding.pokemon.strategies.evolution_heavy import (
    EvolutionHeavyStrategy
)

from deckbuilding.trainers.pool import TrainerPool
from deckbuilding.trainers.selector import TrainerSelector

from deckbuilding.energy.selector import EnergySelector

from deckbuilding.deck_generator import DeckGenerator
from deckbuilding.deck_validator import DeckValidator


class EvolutionHeavyArchetype(DeckArchetype):


    def build_generator(self):

        pokemon_pool = PokemonPool(
            self.db
        )


        pokemon_strategy = EvolutionHeavyStrategy(
            pokemon_pool
        )


        trainer_pool = TrainerPool(
            self.db
        )


        trainer_selector = TrainerSelector(
            trainer_pool
        )


        energy_selector = EnergySelector(
            self.db
        )


        return DeckGenerator(
            pokemon_strategy,
            trainer_selector,
            energy_selector,
            DeckValidator(self.db)
        )