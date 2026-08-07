from environment.ptcg_env import PTCGEnvironment

from agent.strategic_agent import StrategicAgent
from agent.heuristic_agent import HeuristicAgent

from deckbuilding.deck import load_deck
from cards.card_database import CardDatabase

from cg.api import to_observation_class

from utils.logger import BattleLogger

from collections import defaultdict
import random


DECK_PATH = (
    "data/raw/kaggle/pokemon-tcg-ai-battle/"
    "sample_submission/sample_submission/deck.csv"
)

CARD_PATH = (
    "data/raw/kaggle/pokemon-tcg-ai-battle/"
    "EN_Card_Data.csv"
)


deck = load_deck(DECK_PATH)

card_db = CardDatabase(
    CARD_PATH
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


# -------------------------
# Statistics
# -------------------------

completed_games = 0
unfinished = 0
crashes = 0

turn_counts = []


strategic_stats = {

    "games": 0,
    "wins": 0,

    "first_player_games": 0,
    "first_player_wins": 0,

    "second_player_games": 0,
    "second_player_wins": 0
}


action_counts = {

    0: defaultdict(int),
    1: defaultdict(int)
}


# -------------------------
# Benchmark
# -------------------------

num_games = 500


for game in range(num_games):

    print(
        f"Running game {game + 1}/{num_games}"
    )


    env = PTCGEnvironment()

    logger = BattleLogger(
        game_id=game
    )


    try:

        obs = env.reset(
            deck,
            deck
        )


        if obs is None:

            unfinished += 1
            continue



        #
        # Randomize agent assignment
        #
        if random.choice([True, False]):

            player_agents = {

                0: StrategicAgent(
                    deck,
                    card_db
                ),

                1: HeuristicAgent(
                    deck,
                    card_db
                )
            }

            strategic_player = 0
            logger.strategic_player = strategic_player


        else:

            player_agents = {

                0: HeuristicAgent(
                    deck,
                    card_db
                ),

                1: StrategicAgent(
                    deck,
                    card_db
                )
            }

            strategic_player = 1
            logger.strategic_player = strategic_player



        turns = 0



        while True:

            turns += 1


            current_player = (
                obs["current"]["yourIndex"]
            )


            agent = player_agents[
                current_player
            ]


            action = agent.act(
                obs
            )


            logger.log_step({

                "player": current_player,

                "turn": turns,

                "state": obs,

                "action": action

            })


            if not validate_action(
                obs,
                action
            ):

                print("\nINVALID ACTION")
                print("================")

                print(
                    "Game:",
                    game
                )

                print(
                    "Player:",
                    current_player
                )

                print(
                    "Action:",
                    action
                )


                obs_class = to_observation_class(
                    obs
                )


                if obs_class.select:

                    print(
                        "Select type:",
                        obs_class.select.type
                    )

                    print(
                        "Context:",
                        obs_class.select.context
                    )

                    print(
                        "Options:"
                    )


                    for i, option in enumerate(
                        obs_class.select.option
                    ):

                        print(
                            i,
                            option
                        )


                raise RuntimeError(
                    "Invalid agent action"
                )



            if action is not None:

                action_key = (
                    f"type_{obs['select']['type']}"
                    f"_action_{action}"
                    if obs.get("select")
                    else str(action)
                )

                action_counts[
                    current_player
                ][action_key] += 1



            try:

                obs = env.step(
                    action
                )


            except Exception as e:

                crashes += 1

                print("\nENGINE CRASH")

                print(
                    "Game:",
                    game
                )

                print(
                    "Action:",
                    action
                )

                raise e



            result = (
                obs["current"]["result"]
            )



            if result != -1:


                completed_games += 1


                turn_counts.append(
                    turns
                )


                #
                # Strategic Agent statistics
                #

                strategic_stats["games"] += 1


                if result == strategic_player:

                    strategic_stats["wins"] += 1



                if strategic_player == 0:

                    strategic_stats[
                        "first_player_games"
                    ] += 1


                    if result == strategic_player:

                        strategic_stats[
                            "first_player_wins"
                        ] += 1


                else:

                    strategic_stats[
                        "second_player_games"
                    ] += 1


                    if result == strategic_player:

                        strategic_stats[
                            "second_player_wins"
                        ] += 1



                logger.save(

                    winner=result,
                    turns=turns,
                    strategic_player=strategic_player

                )


                break



    finally:

        env.close()



# -------------------------
# Report
# -------------------------

print("\n====================")
print("BATTLE REPORT")
print("====================")


print(
    "Completed games:",
    completed_games
)


print(
    "Unfinished:",
    unfinished
)


print(
    "Crashes:",
    crashes
)



if turn_counts:

    print(
        "Average turns:",
        sum(turn_counts) / len(turn_counts)
    )



print("\nStrategic Agent Performance")
print("---------------------------")


print(

    f"Overall: "
    f"{strategic_stats['wins']}/"
    f"{strategic_stats['games']} "
    f"="
    f"{strategic_stats['wins']/strategic_stats['games']:.3f}"

)



if strategic_stats["first_player_games"]:

    print(

        f"First player: "
        f"{strategic_stats['first_player_wins']}/"
        f"{strategic_stats['first_player_games']} "
        f"="
        f"{strategic_stats['first_player_wins']/strategic_stats['first_player_games']:.3f}"

    )



if strategic_stats["second_player_games"]:

    print(

        f"Second player: "
        f"{strategic_stats['second_player_wins']}/"
        f"{strategic_stats['second_player_games']} "
        f"="
        f"{strategic_stats['second_player_wins']/strategic_stats['second_player_games']:.3f}"

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