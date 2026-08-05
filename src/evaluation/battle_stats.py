from collections import defaultdict


class BattleStats:


    def __init__(self):

        self.games = 0

        self.wins = {
            0:0,
            1:0
        }

        self.turns = []


        self.first_player = {
            0:0,
            1:0
        }


        self.first_player_wins = 0



        self.action_counts = {

            0:defaultdict(int),
            1:defaultdict(int)

        }



    def add(
        self,
        winner,
        turns,
        first_player,
        action_counts
    ):


        self.games += 1


        self.wins[winner] += 1


        self.turns.append(
            turns
        )


        if first_player != -1:
            self.first_player[first_player] += 1


        if (
            first_player != -1
            and winner == first_player
        ):

            self.first_player_wins += 1



        for player in [0,1]:

            for action,count in action_counts[player].items():

                self.action_counts[player][action] += count





    def report(self):


        print("\n====================")
        print("BATTLE REPORT")
        print("====================")


        print(
            "Games:",
            self.games
        )


        print(
            "Wins:",
            self.wins
        )



        print(
            "Average turns:",
            sum(self.turns)/len(self.turns)
        )



        print(
            "\nFirst player games:",
            self.first_player
        )



        print(
            "First player win rate:",
            self.first_player_wins / self.games
        )



        print(
            "\nAction distribution"
        )


        for player in [0,1]:

            print(
                f"Player {player}:"
            )

            print(
                dict(self.action_counts[player])
            )