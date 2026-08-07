import os

from cg.api import to_observation_class

from agent.strategic_agent import StrategicAgent
from cards.card_database import CardDatabase

import glob


def read_deck_csv():

    

    candidates = [
        "deck.csv",
        "./deck.csv",
        "/kaggle_simulations/agent/deck.csv",
    ]

    candidates.extend(glob.glob("**/deck.csv", recursive=True))
    candidates.extend(glob.glob("/kaggle_simulations/**/deck.csv", recursive=True))

    for path in candidates:
        if os.path.exists(path):
            print("Using deck:", path)
            with open(path) as f:
                return [int(x.strip()) for x in f if x.strip()]

    print("cwd =", os.getcwd())
    print("Candidates =", candidates)
    raise FileNotFoundError("Could not find deck.csv")


# ---------------------------------------
# Load deck
# ---------------------------------------

deck = read_deck_csv()



# ---------------------------------------
# Load card database
# ---------------------------------------
possible_paths = [
    "../shared/cards/EN_Card_Data.csv",
    "cards/EN_Card_Data.csv",
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv",
    "/kaggle_simulations/agent/cards/EN_Card_Data.csv"
]

for path in possible_paths:
    if os.path.exists(path):
        card_db_path = path
        break
else:
    raise FileNotFoundError(
        "Could not find card database CSV"
    )


card_db = CardDatabase(
    card_db_path
)

# ---------------------------------------
# Initialize agent
# ---------------------------------------

player_agent = StrategicAgent(deck,card_db)



def agent(obs_dict):

    obs = to_observation_class(
        obs_dict
    )


    print("SELECT:", obs.select)


    # Initial deck selection
    if obs.select is None:

        return deck


    return player_agent.act(obs)