from cg.api import (
    SelectType,
    to_observation_class,
)

from features.state_encoder import encode_state
from features.action_evaluator import ActionEvaluator
from agent.selection_policy import SelectionPolicy
from src.utils.logger import BattleLogger


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


        # Handles secondary selections

        self.selection_policy = SelectionPolicy(
            card_db
        )


        # Logger

        self.logger = BattleLogger(
            agent_name="StrategicAgent"
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

        if obs_class.select is None:

            return None



        select = obs_class.select



        # ---------------------------------
        # Encode state
        # ---------------------------------

        features = encode_state(
            obs,
            self.card_db
        )



        # ---------------------------------
        # Secondary selections
        # ---------------------------------

        if select.type != SelectType.MAIN:


            action = self.selection_policy.choose(
                obs_class
            )


            self.logger.log_action(
                observation=obs,
                select=select,
                selected_action=action,
                scores=None,
                action_type="SECONDARY"
            )


            if self.debug:

                print(
                    "SECONDARY ACTION:",
                    select.type,
                    action
                )


            return action



        # ---------------------------------
        # Main action selection
        # ---------------------------------

        if len(select.option) == 0:

            return []



        best_index = 0
        best_score = float("-inf")

        scores = []



        for idx, option in enumerate(
            select.option
        ):


            score = self.action_evaluator.evaluate(
                option,
                features
            )


            scores.append(
                score
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



        selected_option = select.option[
            best_index
        ]



        # ---------------------------------
        # Logging
        # ---------------------------------

        self.logger.log_action(
            observation=obs,
            select=select,
            selected_action=[
                best_index
            ],
            scores=scores,
            action_type=str(
                selected_option.type
            )
        )



        # ---------------------------------
        # Track action distribution
        # ---------------------------------

        action_type = str(
            selected_option.type
        )


        self.action_counts[action_type] = (
            self.action_counts.get(
                action_type,
                0
            )
            + 1
        )



        if self.debug:

            print(
                "SELECTED:",
                best_index,
                "SCORE:",
                best_score
            )



        return [
            best_index
        ]