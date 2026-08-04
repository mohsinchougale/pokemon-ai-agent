from cards.card_database import CardDatabase

from deckbuilding.archetypes.balanced import BalancedArchetype

from environment.ptcg_env import PTCGEnvironment
from agent.random_agent import RandomAgent

db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)

deck = BalancedArchetype(db).build_generator().generate()

wins = [0, 0]

for game in range(20):

    env = PTCGEnvironment()

    obs = env.reset(deck, deck)

    agent0 = RandomAgent(deck)
    agent1 = RandomAgent(deck)

    while True:

        player = obs["current"]["yourIndex"]

        if player == 0:
            action = agent0.act(obs)
        else:
            action = agent1.act(obs)

        obs = env.step(action)

        result = obs["current"]["result"]

        if result != -1:
            wins[result] += 1
            break

    env.close()

print("Player 0 wins:", wins[0])
print("Player 1 wins:", wins[1])