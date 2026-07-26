import sys
sys.path.append("src")

from environment.ptcg_env import PTCGEnvironment
from agent.random_agent import RandomAgent
from agent.heuristic_agent import HeuristicAgent
from agent.strategic_agent import StrategicAgent
from cards.deck import load_deck
from evaluation.battle_stats import BattleStats


deck = load_deck(
    "data/raw/kaggle/pokemon-tcg-ai-battle/sample_submission/sample_submission/deck.csv"
)


stats = BattleStats()


for i in range(1000):

    print(f"Running game {i+1}/1000")

    agent1 = StrategicAgent(deck)
    agent2 = HeuristicAgent(deck)

    env = PTCGEnvironment()

    obs = env.reset(deck, deck)

    turns = 0


    while True:

        turns += 1

        player = obs["current"]["yourIndex"]

        if player == 0:
            action = agent1.act(obs)
        else:
            action = agent2.act(obs)

        try:
            obs = env.step(action)

        except Exception as e:

            print("\n========== CRASH ==========")
            print("Player:", player)
            print("Action returned:", action)

            print("\nAvailable options:")

            for i, option in enumerate(obs["select"]["option"]):
                print(
                    i,
                    option
                )

            raise e


        result = obs["current"]["result"]

        if result != -1:

            stats.add(
                winner=result,
                turns=turns
            )

            break


    env.close()


stats.report()