from cards.card_database import CardDatabase

from deckbuilding.archetypes import (
    EvolutionHeavyArchetype,
    BalancedArchetype,
    AggressiveEXArchetype
)


db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)



archetypes = [

    EvolutionHeavyArchetype(db),
    BalancedArchetype(db),
    AggressiveEXArchetype(db)

]


for archetype in archetypes:

    print("\n================")
    print(
        archetype.__class__.__name__
    )

    deck = archetype.generate()

    print(
        "Deck size:",
        len(deck)
    )
