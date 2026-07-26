from cards.card_database import CardDatabase
from cards.card_features import CardFeatureExtractor
from cards.evolution_builder import EvolutionLineBuilder


path = (
    "data/raw/kaggle/"
    "pokemon-tcg-ai-battle/"
    "EN_Card_Data.csv"
)


db = CardDatabase(path)

extractor = CardFeatureExtractor(db)

builder = EvolutionLineBuilder(
    db,
    extractor
)


# Test with a random Pokémon pool
pokemon_ids = [
    30,
    33,
    34,
    40,
    76,
    232,
    974,
    913,
    903
]

for card_id in pokemon_ids:
    f = extractor.extract(card_id)

    print(
        f.card_id,
        f.name,
        "|",
        f.stage,
        "| evolves from:",
        f.previous_stage
    )

for idx, row in db.cards.iterrows():

    if "slugma" in str(row["Card Name"]).lower():

        print("Tryto get slugma id: ",
            idx,
            row["Card Name"]
        )
lines = builder.build(
    pokemon_ids
)


for line in lines:
    print(line)
