from cards.card_database import CardDatabase

from deckbuilding.archetypes.balanced import BalancedArchetype
from deckbuilding.archetypes.evolution_heavy import EvolutionHeavyArchetype
from deckbuilding.archetypes.aggressive_ex import AggressiveEXArchetype

from deckbuilding.io.deck_exporter import DeckExporter



DB_PATH = (
    "data/raw/kaggle/pokemon-tcg-ai-battle/"
    "EN_Card_Data.csv"
)


OUTPUT_DIR = "generated"


def generate_and_export(name, archetype):

    print("=" * 60)
    print(name)
    print("=" * 60)


    deck = (
        archetype
        .build_generator()
        .generate()
    )


    safe_name = (
        name.lower()
        .replace(" ", "_")
    )

    output = (
        f"{OUTPUT_DIR}/{safe_name}_deck.csv"
    )


    DeckExporter.export(
        deck,
        output
    )


    print(
        f"Saved: {output}"
    )

    print(
        f"Cards: {len(deck.cards)}"
    )



def main():

    db = CardDatabase(DB_PATH)


    generate_and_export(
        "Balanced",
        BalancedArchetype(db)
    )


    generate_and_export(
        "Evolution Heavy",
        EvolutionHeavyArchetype(db)
    )


    generate_and_export(
        "Aggressive EX",
        AggressiveEXArchetype(db)
    )



if __name__ == "__main__":
    main()