import sys
sys.path.append("src")

from environment.ptcg_env import PTCGEnvironment
from agent.random_agent import RandomAgent
from deckbuilding.deck import load_deck

# deck = [
#     1158,
#     721,721,
#     722,722,722,722,
#     723,723,723,723,
#     1145,1145,1145,1145,
#     1205,1205,
#     1227,1227,1227,1227,
#     1235,1235,1235,1235
# ]


# # temporary fill to 60 cards
# deck += [3] * (60-len(deck))


# Way 2: Load deck from csv file
deck = load_deck(
    "data/raw/kaggle/pokemon-tcg-ai-battle/sample_submission/sample_submission/deck.csv"
)

agent1 = RandomAgent(deck)
agent2 = RandomAgent(deck)


env = PTCGEnvironment()


obs = env.reset(deck, deck)


turn = 0

while True:

    turn += 1

    # Which player is choosing?
    current_player = obs["current"]["yourIndex"]

    if current_player == 0:
        action = agent1.act(obs)
    else:
        action = agent2.act(obs)


    obs = env.step(action)


    result = obs["current"]["result"]

    if result != -1:

        print("Battle finished")
        print("Winner:", result)

        break


print("Turns:", turn)


env.close()