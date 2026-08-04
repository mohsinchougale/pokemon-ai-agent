from cards.card_database import CardDatabase
from cards.card_features import CardFeatureExtractor
from deckbuilding.deck_generator import DeckGenerator
from deckbuilding.pokemon.evolution import EvolutionAnalyzer


path = (
    "data/raw/kaggle/"
    "pokemon-tcg-ai-battle/"
    "EN_Card_Data.csv"
)


db = CardDatabase(path)

extractor = CardFeatureExtractor(db)

generator = DeckGenerator(db)

deck = generator.generate_random_deck()


features = [
    extractor.extract(card_id)
    for card_id in deck
]


pokemon = [
    f for f in features
    if f.is_pokemon
]

for p in pokemon:
    print(
        p.name,
        "|",
        p.stage,
        "| evolves from:",
        p.previous_stage
    )
    
analyzer = EvolutionAnalyzer()

print(
    analyzer.analyze(pokemon)
)