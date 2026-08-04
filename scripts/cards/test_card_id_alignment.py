from cards.card_database import CardDatabase
from engine.cg.api import all_card_data


CSV = "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"

db = CardDatabase(CSV)

engine_cards = {
    c.cardId: c
    for c in all_card_data()
}


for cid in [1, 30, 61, 171, 1200]:
    print("\nCARD ID:", cid)

    print("CSV:")
    print(db.get_name(cid))

    print("ENGINE:")
    print(engine_cards[cid].name)