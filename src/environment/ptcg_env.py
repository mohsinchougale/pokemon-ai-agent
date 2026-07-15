from engine.cg.game import (
    battle_start,
    battle_select,
    battle_finish,
)


class PTCGEnvironment:

    def __init__(self):
        self.obs = None

    def reset(self, deck0, deck1):
        self.obs, _ = battle_start(deck0, deck1)
        return self.obs

    def step(self, action):
        self.obs = battle_select(action)
        return self.obs

    def close(self):
        battle_finish()