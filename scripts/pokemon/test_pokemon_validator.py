from cards.card_database import CardDatabase
from deckbuilding.pokemon.pool import PokemonPool
from deckbuilding.pokemon.validator import PokemonDeckValidator


path = (
    "data/raw/kaggle/"
    "pokemon-tcg-ai-battle/"
    "EN_Card_Data.csv"
)


db = CardDatabase(path)

pool = PokemonPool(db)

validator = PokemonDeckValidator(pool)


# Invalid:
# Garchomp without Gible/Gabite

bad_stage2 = [
    381
]


print(
    "Stage 2 alone:",
    validator.validate(
        bad_stage2
    )
)


# Invalid:
# Gabite without Gible

bad_stage1 = [
    380
]


print(
    "Stage 1 alone:",
    validator.validate(
        bad_stage1
    )
)


# Valid:
# Full evolution line

good = [
    379,
    380,
    381
]


print(
    "Full line:",
    validator.validate(
        good
    )
)