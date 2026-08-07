from dataclasses import dataclass

from cg.api import to_observation_class


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

    # Pokemon identity

    my_active_id: int | None
    opponent_active_id: int | None


    # Attack information

    my_attack_count: int
    opponent_attack_count: int

    my_best_attack_damage: int
    opponent_best_attack_damage: int

    
    # Threat assessment

    opponent_can_attack: bool
    opponent_attack_damage: int


    # Win conditions

    my_prize_remaining: int
    opponent_prize_remaining: int


    # Tempo

    is_first_player: bool



def get_active_pokemon(player):

    if len(player.active) > 0:
        return player.active[0]

    return None

def get_best_attack_damage(card_id, card_db):

    if card_id is None:
        return 0


    attacks = card_db.get_attacks(card_id)

    best = 0


    for attack in attacks:

        damage = attack.get("damage")


        if damage is None:
            continue


        damage = str(damage)


        number = ""


        for char in damage:

            if char.isdigit():
                number += char

            elif number:
                break


        if number:

            best = max(
                best,
                int(number)
            )


    return best



def can_attack(
    pokemon,
    card_db
):

    if pokemon is None:
        return False


    required = card_db.get_attacks(
        pokemon.id
    )


    if not required:
        return False


    # Basic approximation:
    # if pokemon has any attack, and has energy

    if len(pokemon.energies) == 0:
        return False


    return True

def encode_state(obs_dict: dict, card_db=None) -> StateFeatures:

    if isinstance(obs, dict):
        obs = to_observation_class(obs)

    state = obs.current


    my_index = state.yourIndex

    me = state.players[my_index]
    opponent = state.players[1 - my_index]


    my_active = get_active_pokemon(me)

    if my_active:
        my_active_id = my_active.id
    else:
        my_active_id = None

    opponent_active = get_active_pokemon(opponent)

    if opponent_active:
        opponent_active_id = opponent_active.id

    else:
        opponent_active_id = None

    my_best_attack_damage = 0
    opponent_best_attack_damage = 0


    if card_db:

        my_best_attack_damage = get_best_attack_damage(
            my_active_id,
            card_db
        )


        opponent_best_attack_damage = get_best_attack_damage(
            opponent_active_id,
            card_db
        )

    # Active Pokemon

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

        # opponent hand is hidden
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

        my_active_id=my_active_id,
        opponent_active_id=opponent_active_id,

        my_attack_count=len(
            card_db.get_attacks(my_active_id)
        )
        if card_db and my_active_id else 0,


        opponent_attack_count=len(
            card_db.get_attacks(opponent_active_id)
        )
        if card_db and opponent_active_id else 0,


        my_best_attack_damage=my_best_attack_damage,

        opponent_best_attack_damage=opponent_best_attack_damage,


        opponent_can_attack=(
            opponent_active is not None
            and len(opponent_active.energies) > 0
        ),


        opponent_attack_damage=opponent_best_attack_damage,

        my_prize_remaining=len(me.prize),
        opponent_prize_remaining=len(opponent.prize),

        is_first_player=(state.firstPlayer == my_index),

    )