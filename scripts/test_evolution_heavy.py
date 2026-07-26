from cards.card_database import CardDatabase
from deckbuilding.pokemon.pool import PokemonPool
from deckbuilding.pokemon.strategies.evolution_heavy import EvolutionHeavyStrategy
from collections import Counter


db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)


pool = PokemonPool(db)


strategy = EvolutionHeavyStrategy(pool)


cards = strategy.select_pokemon(15)


print("\nEvolution Heavy Pokémon Pool")


for card, count in Counter(cards).items():

    print(
        count,
        "x",
        card,
        db.get_name(card)
    )


print(
    "\nTotal:",
    len(cards)
)