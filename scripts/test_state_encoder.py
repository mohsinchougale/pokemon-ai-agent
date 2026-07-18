import sys

sys.path.append("src")

from agent.random_agent import RandomAgent
from cards.deck import load_deck
from environment.ptcg_env import PTCGEnvironment
from features.state_encoder import encode_state


def main():

    deck = load_deck(
        "/Users/mohsinchougale/Downloads/pokemon-ai-agent/data/raw/kaggle/pokemon-tcg-ai-battle/sample_submission/sample_submission/deck.csv"
    )

    env = PTCGEnvironment()

    obs = env.reset(deck, deck)

    agent0 = RandomAgent(deck)
    agent1 = RandomAgent(deck)

    previous_turn = -1

    while obs["current"]["result"] == -1:

        features = encode_state(obs)

        if features.turn != previous_turn:
            print(features)
            previous_turn = features.turn


        if obs["current"]["yourIndex"] == 0:
            action = agent0.act(obs)
        else:
            action = agent1.act(obs)


        obs = env.step(action)

    env.close()


if __name__ == "__main__":
    main()