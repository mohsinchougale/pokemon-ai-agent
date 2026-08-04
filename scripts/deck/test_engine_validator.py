from cards.card_database import CardDatabase

from deckbuilding.archetypes.balanced import BalancedArchetype
from deckbuilding.archetypes.evolution_heavy import EvolutionHeavyArchetype
from deckbuilding.archetypes.aggressive_ex import AggressiveEXArchetype

from deckbuilding.engine_validator import EngineDeckValidator



def test_archetype(name, archetype):

    print("=" * 60)
    print(name)
    print("=" * 60)


    generator = archetype.build_generator()

    deck = generator.generate()


    print(
        "Deck size:",
        len(deck.cards)
    )


    validator = EngineDeckValidator()


    result = validator.validate(
        deck
    )


    print(
        "Engine Valid:",
        result
    )

    print()



def main():

    db = CardDatabase( "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv")


    tests = [

        (
            "Balanced",
            BalancedArchetype(db)
        ),

        (
            "Evolution Heavy",
            EvolutionHeavyArchetype(db)
        ),

        (
            "Aggressive EX",
            AggressiveEXArchetype(db)
        )

    ]


    for name, archetype in tests:

        test_archetype(
            name,
            archetype
        )



if __name__ == "__main__":

    main()