from cards.card_database import CardDatabase

from deckbuilding.pokemon.pool import PokemonPool

from deckbuilding.pokemon.strategies.evolution_heavy import (
    EvolutionHeavyStrategy
)

from deckbuilding.trainers.pool import TrainerPool
from deckbuilding.trainers.selector import TrainerSelector

from deckbuilding.energy.selector import EnergySelector

from deckbuilding.deck_generator import DeckGenerator

from deckbuilding.deck_validator import DeckValidator



db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)


pokemon_pool = PokemonPool(db)


pokemon_strategy = EvolutionHeavyStrategy(
    pokemon_pool
)


trainer_pool = TrainerPool(db)


trainer_selector = TrainerSelector(
    trainer_pool
)


energy_selector = EnergySelector(
    db
)
validator = DeckValidator(db)

generator = DeckGenerator(
    pokemon_strategy,
    trainer_selector,
    energy_selector,
    validator
)


deck = generator.generate()





print(
    "Deck valid:",
    validator.validate(deck)
)