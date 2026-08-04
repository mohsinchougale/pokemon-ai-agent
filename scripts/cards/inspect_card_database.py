from cards.card_database import CardDatabase


db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)

print("Cards loaded:", len(db.cards))

print(db.get_name(33))
print(db.get_name(40))