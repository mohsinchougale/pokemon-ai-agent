import sys
sys.path.append("src")

from cg.game import battle_start, battle_select, battle_finish
from environment.ptcg_env import PTCGEnvironment
from agent.random_agent import RandomAgent

from cards.card_database import CardDatabase
from utils.pretty_print import pretty_print_state


DECK_PATH = (
    "data/raw/kaggle/"
    "pokemon-tcg-ai-battle/"
    "sample_submission/"
    "sample_submission/"
    "deck.csv"
)


CARD_PATH = (
    "data/raw/kaggle/"
    "pokemon-tcg-ai-battle/"
    "EN_Card_Data.csv"
)



def load_deck():

    with open(DECK_PATH) as f:

        return [
            int(x)
            for x in f.read().split()
        ]



def main():

    card_db = CardDatabase(
        CARD_PATH
    )

    deck = load_deck()


    env = PTCGEnvironment()


    obs = env.reset(
        deck,
        deck
    )


    agent = RandomAgent(deck)


    turns = 0


    while True:

        pretty_print_state(
            obs,
            card_db
        )


        if obs["current"]["result"] != -1:
            break


        player = obs["current"]["yourIndex"]


        action = agent.act(obs)


        obs = env.step(action)


        turns += 1


    env.close()


    print(
        "Battle finished after",
        turns,
        "actions"
    )



if __name__ == "__main__":
    main()