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

from deckbuilding.hybrid_evaluator import HybridEvaluator

from deckbuilding.io.deck_exporter import DeckExporter


# -----------------------------------
# Card Database
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
# Static Deck Evaluation
# -----------------------------------

evolution_analyzer = EvolutionAnalyzer()


deck_evaluator = DeckEvaluator(
    extractor,
    evolution_analyzer
)



# -----------------------------------
# Create Opponent Deck
# -----------------------------------
#
# This is the deck every candidate
# deck will battle against.
#
# Later we can replace this with
# strongest discovered deck.
#

opponent_deck = BalancedArchetype(
    db
).build_generator().generate()



# -----------------------------------
# Hybrid Evaluation
# -----------------------------------
#
# Combines:
#
# 1. Static deck quality
# 2. Actual battle win rate
#

evaluator = HybridEvaluator(
    deck_evaluator,
    opponent_deck
)



# -----------------------------------
# Validator
# -----------------------------------

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
    validator,
    db
)



# -----------------------------------
# Run Optimization
# -----------------------------------
#
# Start small.
# Increase after confirming it works.
#

results = search.search(
    iterations=10
)



# -----------------------------------
# Results
# -----------------------------------

print("\n====================")
print("Optimization Results")
print("====================")



for rank, result in enumerate(results, start=1):
    
    print("\nRank:", rank)

    print(
        "Archetype:",
        result["archetype"]
    )

    print(
        "Initial Score:",
        result["initial_score"]
    )

    print(
        "Best Score:",
        result["score"]
    )

    print(
        "Improvements:",
        result["improvements"]
    )

    print(
        "Iterations:",
        result["iterations"]
    )


    print(
        "Deck Size:",
        len(result["deck"].cards)
    )

# Export top ranked deck
best_result = results[0]

DeckExporter.export(
    best_result["deck"],
    "kaggle_submission/deck.csv"
)
print("\nFINAL BEST DECK")

for card in best_result["deck"].cards:
    print(
        card,
        db.get_name(card)
    )
    
print("\nBest deck exported to kaggle_submission/deck.csv")

print("\n====================")
print("Optimization Complete")
print("====================")