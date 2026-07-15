class BattleStats:

    def __init__(self):
        self.games = 0
        self.wins = {0:0,1:0}
        self.turns = []


    def add(self, winner, turns):

        self.games += 1
        self.wins[winner]+=1
        self.turns.append(turns)


    def report(self):

        print(
            f"Games: {self.games}"
        )

        print(
            self.wins
        )

        print(
            "Average turns:",
            sum(self.turns)/len(self.turns)
        )