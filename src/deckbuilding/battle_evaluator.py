from environment.ptcg_env import PTCGEnvironment
from agent.random_agent import RandomAgent
from agent.strategic_agent import StrategicAgent

class BattleEvaluator:
    """
    Evaluates a deck by measuring its win rate.
    """

    def __init__(self, opponent_deck):

        self.opponent_deck = opponent_deck


    def evaluate(
        self,
        candidate_deck,
        battles=10
    ):

        wins = 0
        completed = 0


        for _ in range(battles):

            env = PTCGEnvironment()


            try:

                agent0 = StrategicAgent(candidate_deck)
                agent1 = StrategicAgent(self.opponent_deck)


                obs = env.reset(
                    candidate_deck,
                    self.opponent_deck
                )


                if obs is None:

                    print(
                        "Battle failed to initialize. Skipping."
                    )

                    env.close()
                    continue



                while True:

                    player = obs["current"]["yourIndex"]


                    if player == 0:

                        action = agent0.act(obs)

                    else:

                        action = agent1.act(obs)


                    obs = env.step(action)


                    if obs is None:

                        break


                    result = obs["current"]["result"]


                    if result != -1:

                        completed += 1


                        if result == 0:

                            wins += 1


                        break


            except Exception as e:

                print(
                    "Battle error:",
                    e
                )


            finally:

                env.close()



        if completed == 0:

            return 0



        print(
            f"Player 0 wins: {wins}"
        )

        print(
            f"Player 1 wins: {completed - wins}"
        )


        return wins / completed