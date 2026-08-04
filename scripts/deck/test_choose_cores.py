from cards.card_database import CardDatabase
from deckbuilding.deck_generator import DeckGenerator

db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)

generator = DeckGenerator(db)

lines = generator.choose_evolution_cores()

for line in lines:
    print(line)