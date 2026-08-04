from cards.card_database import CardDatabase
from cards.card_features import CardFeatureExtractor


db = CardDatabase(
    "data/raw/kaggle/"
    "pokemon-tcg-ai-battle/"
    "EN_Card_Data.csv"
)


extractor = CardFeatureExtractor(db)
print(db.get_attacks(232))
print(db.get_attacks(30))

for card_id in [30, 232, 1245]:

    features = extractor.extract(card_id)

    print()
    print(features)