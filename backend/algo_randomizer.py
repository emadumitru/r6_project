import random
import datetime

attack_opperators = ['Blitz', 'Jackal', 'Iq', 'Thatcher', 'Nokk', 'Nomad', 'Striker', 'Thermite', 'Dokkaebi', 'Hibana', 'Ace', 'Blackbeard', 'Lion', 'Iana', 'Ash', 'Grim', 'Buck', 'Sledge', 'Fuze', 'Capitao', 'Ying', 'Zofia', 'Brava', 'Amaru', 'Gridlock', 'Maverick', 'Osa', 'Zero', 'Sens', 'Flores', 'Deimos', 'Montagne', 'Kali', 'Twitch', 'Glaz', 'Finka', 'Ram']
defense_opperators = ['Thunderbird', 'Maestro', 'Tachanka', 'Warden', 'Melusi', 'Wamai', 'Mira', 'Kaid', 'Frost', 'Rook', 'Oryx', 'Mozzie', 'Jager', 'Echo', 'Vigil', 'Valkyrie', 'Kapkan', 'Sentry', 'Bandit', 'Lesion', 'Fenrir', 'Doc', 'Smoke', 'Azami', 'Castle', 'Caveira', 'Pulse', 'Aruni', 'Goyo', 'Mute', 'Solis', 'Tubarao', 'Thorn', 'Ela', 'Alibi', 'Clash', 'Skopos']

def get_round_in_period(rec, period_start, period_end):
    rounds = []
    if period_start is None:
        for map in rec.maps.values():
            for round in map.rounds.values():
                rounds.append(round)
    else:
        for map in rec.maps.values():
            for round in map.rounds.values():
                if round.date not in [None, 'None', '']:
                    if period_start <= round.date:
                        if period_end is None or round.date <= period_end:
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
    balance = {'Ema-Attack': {}, 'Ema-Defense': {}, 'Mihnea-Attack': {}, 'Mihnea-Defense': {}}
    
    for key in balance:
        if "Attack" in key:
            balance[key] = {op: 0 for op in attack_opperators}
        elif "Defense" in key:
            balance[key] = {op: 0 for op in defense_opperators}
    
    for key, value in history.items():
        for op in value:
            try:
                balance[key][op] += 1
            except:
                pass
            
    return balance

def compute_weights(balance_count, formula_weight):
    operators = list(balance_count.keys())
    operators_playcount = list(balance_count.values())

    if formula_weight == 100:
        weights = [1 / (count + 1e-9) for count in operators_playcount]
    elif formula_weight == 0:
        weights = [1 for _ in operators_playcount]
    else:
        uniform_weight = 1 / len(operators)
        play_count_weights = [1 / (count + 1e-9) for count in operators_playcount]
        weights = [(1 - formula_weight / 100) * uniform_weight + (formula_weight / 100) * play_count_weight
                   for play_count_weight in play_count_weights]

    total_weight = sum(weights)
    if total_weight == 0:
        normalized_weights = [1 / len(weights)] * len(weights)
    else:
        normalized_weights = [weight / total_weight for weight in weights]

    return operators, normalized_weights

def get_two_unique_random_operators(balance_count_ema, balance_count_mihnea, formula_weight):
    operators_ema, weights_ema = compute_weights(balance_count_ema, formula_weight)
    operators_mihnea, weights_mihnea = compute_weights(balance_count_mihnea, formula_weight)

    while True:
        chosen_operator_ema = random.choices(operators_ema, weights=weights_ema, k=1)[0]
        chosen_operator_mihnea = random.choices(operators_mihnea, weights=weights_mihnea, k=1)[0]
        
        if chosen_operator_ema != chosen_operator_mihnea:
            return chosen_operator_ema, chosen_operator_mihnea

def algo_get_random(rec, formula_weight=50, op_count=5, period_start=None, period_end=None):
    rounds = get_round_in_period(rec, period_start, period_end)
    history = get_opperators_history(rounds)
    balance = get_history_balance(history)
    operators_attack, operators_defense = [], []

    for _ in range(op_count):
        op_ema_attack, op_mihnea_attack = get_two_unique_random_operators(balance['Ema-Attack'], balance['Mihnea-Attack'], formula_weight)
        op_ema_defense, op_mihnea_defense = get_two_unique_random_operators(balance['Ema-Defense'], balance['Mihnea-Defense'], formula_weight)
        operators_attack.append((op_ema_attack, op_mihnea_attack))
        operators_defense.append((op_ema_defense, op_mihnea_defense))

    return operators_attack, operators_defense, formula_weight, period_start, period_end