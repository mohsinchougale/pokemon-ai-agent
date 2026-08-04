from cards.card_database import CardDatabase
from cards.card_features import CardFeatureExtractor
from deckbuilding.deck import load_deck
from deckbuilding.deck_evaluator import DeckEvaluator
from deckbuilding.pokemon.evolution import EvolutionAnalyzer

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