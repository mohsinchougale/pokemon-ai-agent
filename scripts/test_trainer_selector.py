from cards.card_database import CardDatabase
from deckbuilding.trainers.pool import TrainerPool
from deckbuilding.trainers.selector import TrainerSelector
from collections import Counter


db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)


pool = TrainerPool(db)


selector = TrainerSelector(pool)


cards = selector.select_trainers(
    30
)


print("\nSelected Trainers\n")


for card, count in Counter(cards).items():

    print(
        count,
        "x",
        card,
        db.get_name(card)
    )


print(
    "\nTotal:",
    len(cards)
)