from cg.api import (
    SelectType,
    to_observation_class,
)

from features.state_encoder import encode_state
from features.action_evaluator import ActionEvaluator
from agent.selection_policy import SelectionPolicy


class StrategicAgent:


    def __init__(
        self,
        deck,
        card_db
    ):

        self.deck = deck
        self.card_db = card_db
        self.action_counts = {}


        # Main decision engine

        self.action_evaluator = ActionEvaluator(
            card_db
        )


        # Handles secondary selections:
        # evolution cards,
        # yes/no choices,
        # energy selections, etc.

        self.selection_policy = SelectionPolicy(
            card_db
        )


        # Debug flag

        self.debug = False



    def act(
        self,
        obs
    ):


        # ---------------------------------
        # Convert observation
        # ---------------------------------

        if isinstance(obs, dict):

            obs_class = to_observation_class(
                obs
            )

        else:

            obs_class = obs



        # ---------------------------------
        # No action required
        # ---------------------------------

        if (
            obs_class.select is None
        ):

            return None



        select = obs_class.select



        # ---------------------------------
        # Secondary selections
        # ---------------------------------

        if select.type != SelectType.MAIN:

            action = self.selection_policy.choose(
                obs_class
            )

            if action is None:
                action = [0]

            if self.debug:
                print(
                    "SECONDARY ACTION:",
                    select.type,
                    action
                )

            return action



        # ---------------------------------
        # Encode state for MAIN actions only
        # ---------------------------------

        features = encode_state(
            obs,
            self.card_db
        )


        if features is None:
            return [0]



        # ---------------------------------
        # Main action selection
        # ---------------------------------

        if len(select.option) == 0:

            return []



        best_index = 0
        best_score = float("-inf")



        for idx, option in enumerate(
            select.option
        ):


            score = self.action_evaluator.evaluate(
                option,
                features
            )


            if self.debug:

                print(
                    idx,
                    option.type,
                    score
                )



            if score > best_score:

                best_score = score
                best_index = idx



        if self.debug:

            print(
                "SELECTED:",
                best_index,
                "SCORE:",
                best_score
            )


        action_type = str(
            select.option[best_index].type
        )


        self.action_counts[action_type] = (
            self.action_counts.get(action_type,0)
            + 1
        )
        
        return [
            best_index
        ]