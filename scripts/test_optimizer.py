from cards.card_database import CardDatabase
from cards.card_features import CardFeatureExtractor

from deckbuilding.pokemon.evolution_database import EvolutionLineDatabase
from deckbuilding.pokemon.evolution import EvolutionAnalyzer

from deckbuilding.deck_evaluator import DeckEvaluator
from deckbuilding.deck_validator import DeckValidator

from deckbuilding.archetypes.evolution_heavy import EvolutionHeavyArchetype
from deckbuilding.archetypes.balanced import BalancedArchetype
from deckbuilding.archetypes.aggressive_ex import AggressiveEXArchetype

from deckbuilding.optimization.search import ArchetypeSearch



# -----------------------------------
# Load Card Database
# -----------------------------------

db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)



# -----------------------------------
# Feature Extraction
# -----------------------------------

extractor = CardFeatureExtractor(
    db
)



# -----------------------------------
# Evolution Database
# -----------------------------------

evolution_db = EvolutionLineDatabase(
    db,
    extractor
)


evolution_db.build()



# -----------------------------------
# Evolution Analyzer
# -----------------------------------

evolution_analyzer = EvolutionAnalyzer()



# -----------------------------------
# Evaluation + Validation
# -----------------------------------

evaluator = DeckEvaluator(
    extractor,
    evolution_analyzer
)


validator = DeckValidator(
    db
)



# -----------------------------------
# Archetypes
# -----------------------------------

archetypes = [

    EvolutionHeavyArchetype(
        db
    ),

    BalancedArchetype(
        db
    ),

    AggressiveEXArchetype(
        db
    )

]



# -----------------------------------
# Search
# -----------------------------------

search = ArchetypeSearch(
    archetypes,
    evaluator,
    validator
)



results = search.search(
    iterations=50
)



# -----------------------------------
# Results
# -----------------------------------

print("\n====================")
print("Optimization Results")
print("====================")


for result in results:

    print("\n")
    print(
        result["archetype"]
    )

    print(
        "Score:",
        result["score"]
    )


    deck = result["deck"]

    print(
        "Deck size:",
        len(deck.cards)
    )