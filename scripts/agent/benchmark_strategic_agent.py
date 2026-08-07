from agent.strategic_agent import StrategicAgent
from agent.random_agent import RandomAgent
from cards.card_database import CardDatabase

from cg.game import play_battle


card_db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)

deck = "generated/balanced_deck.csv"

strategic = StrategicAgent(deck, card_db)
random_agent = RandomAgent()


wins = 0
games = 100

for i in range(games):

    winner = play_battle(
        strategic,
        random_agent,
        deck,
        deck
    )

    if winner == 0:
        wins += 1

    print(
        f"Game {i+1}/{games}  "
        f"Wins={wins}"
    )

print()

print("=" * 50)
print("WIN RATE:", wins / games)
print("=" * 50)