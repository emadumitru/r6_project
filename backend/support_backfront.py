from backend.class_recommender import Recommender
from backend.support_functions import *
import datetime

def load_rec():
    rec = Recommender().load()
    return rec

def update_rec(rec, game, rounds):
    rec.add_game(game, rounds)
    rec.save()
    return rec

def get_site_for_map(rec, map_name):
    if map_name not in rec.maps:
        return []
    sites = rec.maps[map_name].sites["Attack"].values()
    sites = [site.name for site in sites]
    return list(set(sites))

def create_game_level_dict(map_name, win, ban_a_us, ban_a_op, ban_d_us, ban_d_op, gtype, nrounds, score_us, score_op):
    return {
        'date': datetime.datetime.now().strftime('%m/%d/%Y'),
        'map_name': map_name,
        'game_win': win,
        'ban_a_us': ban_a_us,
        'ban_a_op': ban_a_op,
        'ban_d_us': ban_d_us,
        'ban_d_op': ban_d_op,
        'gtype': gtype,
        'nrounds': nrounds,
        'score_us': score_us,
        'score_op': score_op
    }

def create_rounds_dict(rounds):
    dict_rounds = {}
    for i in range(1, len(rounds) + 1):
        entry_round = rounds[i-1]
        dict_rounds[f'round_{i}_site'] = entry_round['site']
        dict_rounds[f'round_{i}_side'] = entry_round['side']
        dict_rounds[f'round_{i}_win'] = entry_round['win']
        dict_rounds[f'round_{i}_endcondition'] = entry_round['endcondition']

        for player_old, player_new in zip(['Ema', 'Mihnea'], ['ema', 'mihnea']):
            dict_rounds[f'{player_new}_round_{i}_opperator'] = entry_round['players'][player_old]['operator']
            dict_rounds[f'{player_new}_round_{i}_kills'] = entry_round['players'][player_old]['kills']
            dict_rounds[f'{player_new}_round_{i}_assists'] = entry_round['players'][player_old]['assists']
            dict_rounds[f'{player_new}_round_{i}_survived'] = entry_round['players'][player_old]['survived']
            dict_rounds[f'{player_new}_round_{i}_entryfrag'] = entry_round['players'][player_old]['entryfrag']
            dict_rounds[f'{player_new}_round_{i}_diffuser'] = entry_round['players'][player_old]['diffuser']
            dict_rounds[f'{player_new}_round_{i}_cluth'] = entry_round['players'][player_old]['clutch']

    return dict_rounds

def pass_on_rounds_game(rounds, map_name, ban_a_us, ban_a_op, ban_d_us, ban_d_op, gtype):
    n_rounds = len(rounds)
    rounds = create_rounds_dict(rounds)
    n_wins = [rounds[f'round_{i}_win'] for i in range(1, n_rounds + 1)].count(True)
    score_us = n_wins
    score_op = n_rounds - n_wins
    gwin = score_us > score_op

    game = create_game_level_dict(map_name, gwin, ban_a_us, ban_a_op, ban_d_us, ban_d_op, gtype, n_rounds, score_us, score_op)

    aggregated_dictionary = {**game, **rounds}

    clean_inoput = form_input_clean(aggregated_dictionary)

    game, rounds = create_game_and_rounds(clean_inoput)

    return game, rounds
            


