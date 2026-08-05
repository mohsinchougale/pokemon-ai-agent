from dataclasses import dataclass

from cg.api import Observation, to_observation_class


@dataclass
class StateFeatures:

    # Game
    turn: int
    turn_action_count: int

    # Active Pokemon
    my_active_hp: int
    my_active_max_hp: int
    my_active_hp_ratio: float

    opponent_active_hp: int
    opponent_active_max_hp: int
    opponent_active_hp_ratio: float

    # Resources
    my_hand_size: int
    opponent_hand_size: int

    my_deck_size: int
    opponent_deck_size: int

    my_prize_count: int
    opponent_prize_count: int

    # Board
    my_bench_size: int
    opponent_bench_size: int

    # Energy
    my_active_energy_count: int
    opponent_active_energy_count: int

    # Status
    my_poisoned: bool
    my_burned: bool
    my_asleep: bool
    my_paralyzed: bool
    my_confused: bool

    # Turn resources
    energy_attached: bool
    supporter_played: bool
    stadium_played: bool



def get_active_pokemon(player):

    if player and len(player.active) > 0:
        return player.active[0]

    return None



def encode_state(obs_input) -> StateFeatures:
    """
    Converts Observation into numerical features.

    Accepts:
        - dict from Kaggle environment
        - Observation dataclass from cg.api
    """

    # Handle both cases
    if isinstance(obs_input, dict):
        obs = to_observation_class(obs_input)

    else:
        obs = obs_input


    state = obs.current


    # During very early game states
    # current may not exist yet
    if state is None:

        return StateFeatures(

            turn=0,
            turn_action_count=0,

            my_active_hp=0,
            my_active_max_hp=0,
            my_active_hp_ratio=0,

            opponent_active_hp=0,
            opponent_active_max_hp=0,
            opponent_active_hp_ratio=0,

            my_hand_size=0,
            opponent_hand_size=0,

            my_deck_size=60,
            opponent_deck_size=60,

            my_prize_count=0,
            opponent_prize_count=0,

            my_bench_size=0,
            opponent_bench_size=0,

            my_active_energy_count=0,
            opponent_active_energy_count=0,

            my_poisoned=False,
            my_burned=False,
            my_asleep=False,
            my_paralyzed=False,
            my_confused=False,

            energy_attached=False,
            supporter_played=False,
            stadium_played=False,
        )


    my_index = state.yourIndex

    me = state.players[my_index]
    opponent = state.players[1 - my_index]


    my_active = get_active_pokemon(me)
    opponent_active = get_active_pokemon(opponent)


    # -----------------------------
    # My active Pokemon
    # -----------------------------

    if my_active:

        my_hp = my_active.hp
        my_max_hp = my_active.maxHp

        my_ratio = (
            my_hp / my_max_hp
            if my_max_hp > 0
            else 0
        )

        my_energy = len(my_active.energies)

    else:

        my_hp = 0
        my_max_hp = 0
        my_ratio = 0
        my_energy = 0



    # -----------------------------
    # Opponent active Pokemon
    # -----------------------------

    if opponent_active:

        opp_hp = opponent_active.hp
        opp_max_hp = opponent_active.maxHp

        opp_ratio = (
            opp_hp / opp_max_hp
            if opp_max_hp > 0
            else 0
        )

        opp_energy = len(opponent_active.energies)

    else:

        opp_hp = 0
        opp_max_hp = 0
        opp_ratio = 0
        opp_energy = 0



    return StateFeatures(

        turn=state.turn,
        turn_action_count=state.turnActionCount,


        my_active_hp=my_hp,
        my_active_max_hp=my_max_hp,
        my_active_hp_ratio=my_ratio,


        opponent_active_hp=opp_hp,
        opponent_active_max_hp=opp_max_hp,
        opponent_active_hp_ratio=opp_ratio,


        my_hand_size=me.handCount,
        opponent_hand_size=opponent.handCount,


        my_deck_size=me.deckCount,
        opponent_deck_size=opponent.deckCount,


        my_prize_count=len(me.prize),
        opponent_prize_count=len(opponent.prize),


        my_bench_size=len(me.bench),
        opponent_bench_size=len(opponent.bench),


        my_active_energy_count=my_energy,
        opponent_active_energy_count=opp_energy,


        my_poisoned=me.poisoned,
        my_burned=me.burned,
        my_asleep=me.asleep,
        my_paralyzed=me.paralyzed,
        my_confused=me.confused,


        energy_attached=state.energyAttached,
        supporter_played=state.supporterPlayed,
        stadium_played=state.stadiumPlayed,

    )