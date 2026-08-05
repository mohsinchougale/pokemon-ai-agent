from environment.ptcg_env import PTCGEnvironment
from agent.strategic_agent import StrategicAgent
from agent.heuristic_agent import HeuristicAgent
from agent.random_agent import RandomAgent
from deckbuilding.deck import load_deck
from cards.card_database import CardDatabase
from cg.api import to_observation_class

from collections import defaultdict
import random


deck = load_deck(
    "data/raw/kaggle/pokemon-tcg-ai-battle/sample_submission/sample_submission/deck.csv"
)

card_db = CardDatabase(
    "data/raw/kaggle/pokemon-tcg-ai-battle/EN_Card_Data.csv"
)


def validate_action(obs, action):

    if action is None:
        return True

    obs_class = to_observation_class(obs)

    if obs_class.select is None:
        return True

    options = obs_class.select.option

    if len(action) == 0:
        return False

    for idx in action:

        if idx < 0 or idx >= len(options):
            return False

    if len(action) < obs_class.select.minCount:
        return False

    if len(action) > obs_class.select.maxCount:
        return False

    return True


games = 0

wins = {
    0: 0,
    1: 0
}


first_player_stats = {
    0: {
        "games": 0,
        "wins": 0
    },
    1: {
        "games": 0,
        "wins": 0
    }
}


action_counts = {
    0: defaultdict(int),
    1: defaultdict(int)
}


turn_counts = []

unfinished = 0
crashes = 0


num_games = 1000


for game in range(num_games):

    print(f"Running game {game+1}/{num_games}")

    starting_player = random.choice([0, 1])

    env = PTCGEnvironment()

    try:

        obs = env.reset(deck, deck)

        if obs is None:
            unfinished += 1
            continue


        agent0 = StrategicAgent(deck, card_db)
        agent1 = HeuristicAgent(deck, card_db)

        turns = 0


        while True:

            turns += 1

            current_player = obs["current"]["yourIndex"]

            agent = (
                agent0
                if current_player == 0
                else agent1
            )


            action = agent.act(obs)


            if not validate_action(obs, action):

                print("\nINVALID ACTION")
                print("================")
                print("Game:", game)
                print("Player:", current_player)
                print("Action:", action)

                obs_class = to_observation_class(obs)

                if obs_class.select:

                    print(
                        "Select type:",
                        obs_class.select.type
                    )

                    print(
                        "Select context:",
                        obs_class.select.context
                    )

                    print(
                        "Min:",
                        obs_class.select.minCount
                    )

                    print(
                        "Max:",
                        obs_class.select.maxCount
                    )

                    print(
                        "Options:"
                    )

                    for i, option in enumerate(obs_class.select.option):
                        print(i, option)

                raise RuntimeError(
                    "Agent returned invalid action"
                )


            if action is not None:

                action_counts[current_player][
                    str(action[0])
                ] += 1


            try:

                obs = env.step(action)

            except Exception as e:

                crashes += 1

                print("\nCRASH")
                print("================")
                print("Game:", game)
                print("Player:", current_player)
                print("Action:", action)

                obs_class = to_observation_class(obs)

                if obs_class.select:

                    print(
                        "Select type:",
                        obs_class.select.type
                    )

                    print(
                        "Select context:",
                        obs_class.select.context
                    )

                    print(
                        "Options:"
                    )

                    for i, option in enumerate(obs_class.select.option):
                        print(i, option)

                raise e


            result = obs["current"]["result"]


            if result != -1:

                games += 1

                wins[result] += 1

                turn_counts.append(turns)


                first_player_stats[starting_player]["games"] += 1

                if result == starting_player:

                    first_player_stats[starting_player]["wins"] += 1

                break


    finally:

        env.close()



print("\n====================")
print("BATTLE REPORT")
print("====================")

print(
    "Completed games:",
    games
)

print(
    "Unfinished:",
    unfinished
)

print(
    "Crashes:",
    crashes
)


print()

print(
    "Wins:",
    wins
)


if turn_counts:

    print(
        "Average turns:",
        sum(turn_counts) / len(turn_counts)
    )


print("\nFirst Player Advantage")
print("---------------------")


for player, data in first_player_stats.items():

    if data["games"]:

        print(
            f"Player {player}: "
            f"{data['wins']}/{data['games']} "
            f"="
            f"{data['wins']/data['games']:.3f}"
        )


print("\nAction Distribution")
print("-------------------")


for player in [0, 1]:

    print(
        f"\nPlayer {player}"
    )

    print(
        dict(action_counts[player])
    )