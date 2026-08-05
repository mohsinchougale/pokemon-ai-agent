import os

from cg.api import to_observation_class

from agent.strategic_agent import StrategicAgent


def read_deck_csv():

    file_path = "deck.csv"

    if not os.path.exists(file_path):
        file_path = "/kaggle_simulations/agent/deck.csv"

    with open(file_path, "r") as file:

        cards = [
            int(x.strip())
            for x in file.readlines()
            if x.strip()
        ]

    return cards



deck = read_deck_csv()

player_agent = StrategicAgent(
    deck
)


def agent(obs_dict):

    obs = to_observation_class(
        obs_dict
    )

    print("SELECT:", obs.select)

    # Initial deck selection
    if obs.select is None:

        return deck


    return player_agent.act(obs)