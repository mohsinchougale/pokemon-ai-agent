from cards.card_database import CardDatabase
from deckbuilding.pokemon.pool import PokemonPool


db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)

pool = PokemonPool(db)

print("Total Pokémon:", len(pool.all_pokemon))
print("Basics:", len(pool.basic))
print("Stage 1:", len(pool.stage1))
print("Stage 2:", len(pool.stage2))
print("ex Pokémon:", len(pool.ex))
print("Evolution lines:", len(pool.evolution_db.lines))
print("2-stage lines:", len(pool.two_stage_lines))
print("3-stage lines:", len(pool.three_stage_lines))