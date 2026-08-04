from cg.api import OptionType, SelectType, to_observation_class


class HeuristicAgent:

    def __init__(self, deck):
        self.deck = deck


    def act(self, obs):

        if isinstance(obs, dict):
            obs = to_observation_class(obs)


        if obs.select is None:
            return None


        select = obs.select


        # ---------------------------------------
        # Main action selection
        # ---------------------------------------
        if select.type == SelectType.MAIN:

            return [
                self.choose_best_option(obs)
            ]


        # ---------------------------------------
        # Secondary selections
        # ---------------------------------------

        option_count = len(select.option)


        if option_count == 0:
            return []


        min_count = select.minCount
        max_count = select.maxCount


        count = max(1, min_count)

        count = min(
            count,
            max_count,
            option_count
        )


        return list(range(count))



    def choose_best_option(self, obs):

        best_index = 0
        best_score = float("-inf")


        for idx, option in enumerate(obs.select.option):

            score = self.score_action(
                option,
                obs
            )


            if score > best_score:
                best_score = score
                best_index = idx


        return best_index



    def score_action(self, option, obs):

        if option.type == OptionType.ATTACK:
            return 100


        if option.type == OptionType.ATTACH:
            return 50


        if option.type == OptionType.EVOLVE:
            return 40


        if option.type == OptionType.PLAY:
            return 30


        if option.type == OptionType.RETREAT:
            return 20


        if option.type == OptionType.END:
            return 0


        return -1