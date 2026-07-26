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
# Evaluation
# -----------------------------------

evolution_analyzer = EvolutionAnalyzer()


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
    validator,
    db
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


print("\n====================")
print("Optimization Complete")
print("====================")