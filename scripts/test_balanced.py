from cards.card_database import CardDatabase
from deckbuilding.pokemon.pool import PokemonPool
from deckbuilding.pokemon.strategies.balanced import BalancedStrategy
from collections import Counter


db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)


pool = PokemonPool(db)


strategy = BalancedStrategy(pool)


cards = strategy.select_pokemon(
    target_count=15
)


print("\nBalanced Pokémon Pool")


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