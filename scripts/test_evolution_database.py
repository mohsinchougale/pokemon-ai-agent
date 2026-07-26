from cards.card_database import CardDatabase
from cards.card_features import CardFeatureExtractor
from deckbuilding.pokemon.evolution_database import EvolutionLineDatabase


path = (
    "data/raw/kaggle/"
    "pokemon-tcg-ai-battle/"
    "EN_Card_Data.csv"
)


db = CardDatabase(path)

extractor = CardFeatureExtractor(db)


evo_db = EvolutionLineDatabase(
    db,
    extractor
)


lines = evo_db.build()


print(
    "Evolution lines found:",
    len(lines)
)


for line in lines[:20]:
    print(line)