import json
import os
from datetime import datetime


class BattleLogger:

    def __init__(self, game_id, log_dir="logs/battles"):

        self.game_id = game_id
        self.log_dir = log_dir

        self.trajectory = []

        # Which player is controlled by StrategicAgent
        self.strategic_player = None

        os.makedirs(
            self.log_dir,
            exist_ok=True
        )


    def log_step(self, step_data):

        self.trajectory.append(
            step_data
        )


    def save(
        self,
        winner,
        turns,
        strategic_player=None
    ):

        if strategic_player is not None:
            self.strategic_player = strategic_player


        replay = {

            "timestamp": str(datetime.now()),

            "game_id": self.game_id,

            "winner": winner,

            "strategic_player": self.strategic_player,

            "turns": turns,

            "trajectory": self.trajectory
        }


        path = os.path.join(
            self.log_dir,
            f"battle_{self.game_id}.json"
        )


        with open(
            path,
            "w"
        ) as f:

            json.dump(
                replay,
                f,
                indent=2
            )


        print(
            f"Saved battle replay: {path}"
        )