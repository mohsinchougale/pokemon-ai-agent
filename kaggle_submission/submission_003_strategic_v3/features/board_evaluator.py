def evaluate_board(features):

    score = 0


    # ==================================================
    # Prize Race
    # ==================================================

    prize_difference = (
        features.opponent_prize_remaining
        -
        features.my_prize_remaining
    )


    # Early game:
    # board matters more than prizes

    if features.turn <= 5:

        score += prize_difference * 80


    # Mid/Late game:
    # prizes become critical

    else:

        score += prize_difference * 200



    # ==================================================
    # Active Pokemon Advantage
    # ==================================================

    hp_difference = (
        features.my_active_hp
        -
        features.opponent_active_hp
    )

    score += hp_difference * 0.6



    hp_ratio_difference = (
        features.my_active_hp_ratio
        -
        features.opponent_active_hp_ratio
    )


    score += hp_ratio_difference * 120



    # ==================================================
    # Energy Advantage
    # ==================================================

    energy_difference = (
        features.my_active_energy_count
        -
        features.opponent_active_energy_count
    )


    score += energy_difference * 60



    # ==================================================
    # Bench / Board Development
    # ==================================================

    my_bench = features.my_bench_size
    opp_bench = features.opponent_bench_size


    # Diminishing returns

    score += min(
        my_bench,
        5
    ) * 35


    score -= min(
        opp_bench,
        5
    ) * 20



    # ==================================================
    # Hand Advantage
    # ==================================================

    hand_difference = (
        features.my_hand_size
        -
        features.opponent_hand_size
    )


    score += hand_difference * 15



    # ==================================================
    # Status Conditions
    # ==================================================

    if features.my_poisoned:
        score -= 40

    if features.my_burned:
        score -= 40

    if features.my_asleep:
        score -= 80

    if features.my_paralyzed:
        score -= 100

    if features.my_confused:
        score -= 60



    # ==================================================
    # Opponent Threat
    # ==================================================

    if features.opponent_can_attack:


        # Opponent can KO us

        if (
            features.opponent_attack_damage
            >=
            features.my_active_hp
        ):

            score -= 250


        # Opponent has strong attack setup

        elif (
            features.opponent_attack_damage
            >
            features.my_active_hp * 0.5
        ):

            score -= 80



    # ==================================================
    # Our Win Pressure
    # ==================================================

    if (
        features.opponent_active_hp
        <=
        features.my_best_attack_damage
    ):

        score += 250



    # ==================================================
    # Tempo
    # ==================================================

    if features.energy_attached:

        score += 25


    if features.supporter_played:

        score += 15



    # ==================================================
    # Game Phase Adjustment
    # ==================================================

    if features.turn <= 5:

        # prioritize setup

        score += features.my_bench_size * 20


    elif features.turn >= 15:

        # prioritize closing game

        if features.opponent_prize_remaining <= 2:

            score += 150



    return score