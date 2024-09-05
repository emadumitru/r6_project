import random
import datetime

def get_round_in_period(rec, period_start, period_end):
    """Function to get rounds in a period"""
    rounds = []
    if period_start is None:
        for map in rec.maps.values():
            for round in map.rounds.values():
                rounds.append(round)
    else:
        if period_end is None:
            # get period_end to be tomorrow
            period_end = datetime.date.today() + datetime.timedelta(days=1)
        for map in rec.maps.values():
            for round in map.rounds.values():
                if round.date not in [None, 'None', '']:
                    if period_start <= round.date <= period_end:
                        rounds.append(round)
    return rounds


def get_opperators_history(rounds):
    history = {'Ema-Attack': [], 'Ema-Defense': [], 'Mihnea-Attack': [], 'Mihnea-Defense': []}
    for round in rounds:
        side = round.side
        ema = round.player_stats['ema'].opperator
        mihnea = round.player_stats['mihnea'].opperator
        if ema not in ['-', 'None', None, '', 'Nothing', 'nothing']:
            history[f'Ema-{side}'].append(ema.capitalize())
        if mihnea not in ['-', 'None', None, '', 'Nothing', 'nothing']:
            history[f'Mihnea-{side}'].append(mihnea.capitalize())

    return history


def get_history_balance(history):
    """Function to get distribution of operators for each player and side as well as the maximum amount"""
    balance = {'Ema-Attack': {}, 'Ema-Defense': {}, 'Mihnea-Attack': {}, 'Mihnea-Defense': {}}
    for key, value in history.items():
        balance[key] = {op: value.count(op) for op in value}
    return balance


def compute_weights(balance_count, formula_weight):
    """
    Compute weights for operators based on play counts and formula_weight.
    
    :param balance_count: Dictionary with operators as keys and play counts as values.
    :param formula_weight: Weight indicating the influence of play count (0: random, 100: inverse of play count).
    :return: Tuple of (operators, normalized_weights)
    """
    operators = list(balance_count.keys())
    operators_playcount = list(balance_count.values())

    if formula_weight == 100:
        # Prefer less frequently played operators
        weights = [1 / (count + 1) for count in operators_playcount]
    elif formula_weight == 0:
        # Completely random (uniform distribution)
        weights = [1 for _ in operators_playcount]
    else:
        # Blend between uniform and inverse of play count
        uniform_weight = 1 / len(operators)
        play_count_weights = [1 / (count + 1) for count in operators_playcount]
        weights = [(1 - formula_weight / 100) * uniform_weight + (formula_weight / 100) * play_count_weight
                   for play_count_weight in play_count_weights]

    # Normalize weights to sum to 1
    total_weight = sum(weights)
    normalized_weights = [weight / total_weight for weight in weights]

    return operators, normalized_weights


def get_two_unique_random_operators(balance_count_ema, balance_count_mihnea, formula_weight):
    """Function to get two unique random operators from two different balance counts"""

    # Compute weights for both balance counts
    operators_ema, weights_ema = compute_weights(balance_count_ema, formula_weight)
    operators_mihnea, weights_mihnea = compute_weights(balance_count_mihnea, formula_weight)

    # Ensure the two operators are different
    while True:
        chosen_operator_ema = random.choices(operators_ema, weights=weights_ema, k=1)[0]
        chosen_operator_mihnea = random.choices(operators_mihnea, weights=weights_mihnea, k=1)[0]
        
        if chosen_operator_ema != chosen_operator_mihnea:
            return chosen_operator_ema, chosen_operator_mihnea
        

def get_random_operators(rec, formula_weight=50, op_count=5, period_start=None, period_end=None):
    """
    Function to get random operators op_count times for a given recommender for both sides
    :param rec: Recommender object
    :param formula_weight: int - weight for formula
    :param op_count: int - number of operators to get
    :return: tuple - (attack operators, defense operators)
    """
    rounds = get_round_in_period(rec, period_start, period_end)
    history = get_opperators_history(rounds)
    balance = get_history_balance(history)
    operators_attack, operators_defense = [], []

    for _ in range(op_count):
        op_ema_attack, op_mihnea_attack = get_two_unique_random_operators(balance['Ema-Attack'], balance['Mihnea-Attack'], formula_weight)
        op_ema_defense, op_mihnea_defense = get_two_unique_random_operators(balance['Ema-Defense'], balance['Mihnea-Defense'], formula_weight)
        operators_attack.append((op_ema_attack, op_mihnea_attack))
        operators_defense.append((op_ema_defense, op_mihnea_defense))

    return operators_attack, operators_defense