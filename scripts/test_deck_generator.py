from cards.card_database import CardDatabase
from cards.card_features import CardFeatureExtractor
from cards.deck_generator import DeckGenerator
from cards.deck_evaluator import DeckEvaluator
from cards.evolution import EvolutionAnalyzer

path = (
    "data/raw/kaggle/"
    "pokemon-tcg-ai-battle/"
    "EN_Card_Data.csv"
)


db = CardDatabase(path)

extractor = CardFeatureExtractor(db)

generator = DeckGenerator(db)

deck = generator.generate_random_deck()


print("Deck size:", len(deck))

print("\nFirst 10 cards:")

for card in deck.cards[:10]:

    print(
        card,
        db.get_name(card)
    )


evolution_analyzer = EvolutionAnalyzer()


evaluator = DeckEvaluator(
    extractor,
    evolution_analyzer
)

result = evaluator.evaluate(deck)

print(result)