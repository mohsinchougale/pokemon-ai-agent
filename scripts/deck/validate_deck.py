from cards.card_database import CardDatabase
from deckbuilding.deck import load_deck


db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)


deck = load_deck(
    "kaggle_submission/deck.csv"
)


print("Deck size:", len(deck))


print("\nDuplicate check:")
print(deck.validate_duplicates(db))


print("\nCard counts:")
for card, count in deck.card_counts().items():

    if count > 4 and not db.is_energy(card):

        print(
            "INVALID:",
            db.get_name(card),
            count
        )


print("\nEnergy count:")

energy = [
    c for c in deck
    if db.is_energy(c)
]

print(len(energy))


print("\nValidation complete")