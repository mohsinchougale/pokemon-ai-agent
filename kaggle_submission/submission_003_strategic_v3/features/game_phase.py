from enum import Enum


class GamePhase(Enum):

    EARLY = 0
    MID = 1
    LATE = 2
    ENDGAME = 3


def get_game_phase(features):

    # Endgame takes priority
    if (
        features.my_prize_remaining <= 2
        or
        features.opponent_prize_remaining <= 2
    ):
        return GamePhase.ENDGAME


    if features.turn <= 4:
        return GamePhase.EARLY


    if features.turn <= 10:
        return GamePhase.MID


    return GamePhase.LATE