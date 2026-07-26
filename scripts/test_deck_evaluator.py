from cards.card_database import CardDatabase
from cards.card_features import CardFeatureExtractor
from cards.deck import load_deck
from cards.deck_evaluator import DeckEvaluator
from cards.evolution import EvolutionAnalyzer

path = (
    "data/raw/kaggle/"
    "pokemon-tcg-ai-battle/"
    "EN_Card_Data.csv"
)


db = CardDatabase(path)

extractor = CardFeatureExtractor(db)

evaluator = DeckEvaluator(extractor)


deck = load_deck(
    "data/raw/kaggle/"
    "pokemon-tcg-ai-battle/"
    "sample_submission/"
    "sample_submission/deck.csv"
)


result = evaluator.evaluate(deck)

print(result)