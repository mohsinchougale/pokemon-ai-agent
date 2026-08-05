from cg.api import (
    OptionType,
    SelectType,
    to_observation_class,
)

from features.state_encoder import encode_state


class StrategicAgent:

    def __init__(self, deck):
        self.deck = deck


    def act(self, obs):

        if isinstance(obs, dict):

            obs_class = to_observation_class(obs)

            features = encode_state(obs)

        else:

            obs_class = obs

            features = encode_state(obs)


        if obs_class.select is None:
            return None


        select = obs_class.select

        # print(
        #     "SELECT DEBUG:",
        #     select.type,
        #     select.context,
        #     [(x.type, x.area, x.index) for x in select.option]
        # )

        # -------------------------------------------------
        # Handle non-main selections
        # -------------------------------------------------

        # Card selection, evolution selection, etc.
        # Pick the first legal option.
        #
        # Future improvement:
        # use card value evaluation here.
        #
        # Only score real actions
        if select.type != SelectType.MAIN:

            return self.handle_selection(
                obs_class
            )

        # -------------------------------------------------
        # Main action selection
        # -------------------------------------------------

        best_index = 0
        best_score = float("-inf")


        for idx, option in enumerate(select.option):

            score = self.score_action(
                option,
                features
            )


            if score > best_score:

                best_score = score
                best_index = idx


        if best_index >= len(select.option):
            return [0]

        return [best_index]


    
    def handle_selection(self, obs):

        select = obs.select

        if len(select.option) == 0:
            return None


        if select.type == SelectType.YES_NO:

            for idx, option in enumerate(select.option):

                if option.type == OptionType.YES:
                    return [idx]

            return [0]


        count = max(
            1,
            select.minCount
        )

        count = min(
            count,
            select.maxCount,
            len(select.option)
        )

        return list(range(count))
    

    def score_action(self, option, features):

        action = option.type


        # ---------------------------------------------
        # Attack
        # ---------------------------------------------

        if action == OptionType.ATTACK:

            score = 50


            # KO opportunity
            if features.opponent_active_hp <= 50:

                score += 50


            # Dangerous if we are almost dead
            if features.my_active_hp_ratio < 0.3:

                score -= 25


            # Having energy means attacks are more meaningful
            score += (
                features.my_active_energy_count * 5
            )


            return score



        # ---------------------------------------------
        # Attach Energy
        # ---------------------------------------------

        if action == OptionType.ATTACH:


            score = 40


            # Build energy early
            if features.my_active_energy_count < 3:

                score += 30


            # Less valuable when already powered
            else:

                score -= 20


            return score



        # ---------------------------------------------
        # Play Pokemon
        # ---------------------------------------------

        if action == OptionType.PLAY:


            score = 30


            # Build board
            if features.my_bench_size < 3:

                score += 40


            return score



        # ---------------------------------------------
        # Evolution
        # ---------------------------------------------

        if action == OptionType.EVOLVE:


            score = 60


            # Evolution becomes better later
            if features.turn > 3:

                score += 20


            return score



        # ---------------------------------------------
        # Retreat
        # ---------------------------------------------

        if action == OptionType.RETREAT:


            score = 10


            # Save dying Pokemon
            if features.my_active_hp_ratio < 0.3:

                score += 70


            else:

                score -= 20


            return score



        # ---------------------------------------------
        # End turn
        # ---------------------------------------------

        if action == OptionType.END:

            return 0



        # Unknown action
        return -10