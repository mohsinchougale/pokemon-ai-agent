import random

from cg.api import to_observation_class


class RandomAgent:

    def __init__(self, deck, card_db=None):
        self.deck = deck
        self.card_db = card_db

    def act(self, obs_dict):

        obs = to_observation_class(obs_dict)

        # Initial deck selection
        if obs.select is None:
            return self.deck

        options = len(obs.select.option)

        count = obs.select.maxCount

        return random.sample(
            range(options),
            count
        )