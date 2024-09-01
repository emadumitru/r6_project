import os
import datetime
from class_round import Round
from class_game import Game

def get_relative_path(target_file, directory='data', curent_file=__file__):
    curent_dir = os.path.dirname(curent_file)
    one_dir_up = os.path.join(curent_dir, os.pardir)
    data_dir = os.path.join(one_dir_up, directory)
    path = os.path.join(data_dir, target_file)
    return path


def read_old_csv_line(line):
    """
    Reads an old CSV line, splits it by commas, and maps existing columns 
    to the required keys for create_game_and_rounds, filling missing values with None.

    :param line: A string representing a line from the old CSV file.
    :return: A dictionary formatted for create_game_and_rounds function.
    """
    # Split the line by commas
    values = line.strip().split(',')

    # Define the list of expected columns in the order they appear in the CSV
    expected_columns = [
        'win', 'score_us', 'score_opp', 'rounds', 'map', 'ban_a_us', 'ban_a_opp',
        'ban_d_us', 'ban_d_opp', 'location_1', 'location_2', 'location_3',
        'location_4', 'location_5', 'location_6', 'location_7', 'location_8', 'location_9',
        'side_1', 'side_2', 'side_3', 'side_4', 'side_5', 'side_6', 'side_7', 'side_8', 'side_9',
        'operator_1', 'operator_2', 'operator_3', 'operator_4', 'operator_5', 'operator_6',
        'operator_7', 'operator_8', 'operator_9', 'win_1', 'win_2', 'win_3', 'win_4', 'win_5',
        'win_6', 'win_7', 'win_8', 'win_9', 'kill_1', 'kill_2', 'kill_3', 'kill_4', 'kill_5',
        'kill_6', 'kill_7', 'kill_8', 'kill_9', 'death_1', 'death_2', 'death_3', 'death_4',
        'death_5', 'death_6', 'death_7', 'death_8', 'death_9', 'mihnea_1', 'mihnea_2', 'mihnea_3',
        'mihnea_4', 'mihnea_5', 'mihnea_6', 'mihnea_7', 'mihnea_8', 'mihnea_9', 'kill_m_1',
        'kill_m_2', 'kill_m_3', 'kill_m_4', 'kill_m_5', 'kill_m_6', 'kill_m_7', 'kill_m_8',
        'kill_m_9', 'death_m_1', 'death_m_2', 'death_m_3', 'death_m_4', 'death_m_5', 'death_m_6',
        'death_m_7', 'death_m_8', 'death_m_9', 'date'
    ]

    # Create a dictionary by mapping expected columns to the split values
    line_dict = {key: (values[i] if i < len(values) else None) for i, key in enumerate(expected_columns)}

    # Initialize the input dictionary with appropriate keys for create_game_and_rounds
    input_dict = {
        'game_id': 0,  # Default ID since not provided in the old CSV
        'date': line_dict.get('date'),
        'map_name': line_dict.get('map'),
        'game_win': line_dict.get('win'),  # Will be converted to boolean later
        'ban_a_us': line_dict.get('ban_a_us'),
        'ban_a_op': line_dict.get('ban_a_opp'),
        'ban_d_us': line_dict.get('ban_d_us'),
        'ban_d_op': line_dict.get('ban_d_opp'),
        'gtype': None,  # Game type not provided in the old CSV
        'nrounds': line_dict.get('rounds'),
        'score_us': line_dict.get('score_us'),
        'score_op': line_dict.get('score_opp'),
    }

    # Iterate over rounds to extract round-specific data
    for i in range(1, 10):
        input_dict[f'round_{i}_id'] = i
        input_dict[f'round_{i}_number'] = i
        input_dict[f'round_{i}_site'] = line_dict.get(f'location_{i}')
        input_dict[f'round_{i}_side'] = line_dict.get(f'side_{i}')
        input_dict[f'round_{i}_win'] = line_dict.get(f'win_{i}')
        input_dict[f'round_{i}_type'] = None  # Not provided in old CSV
        input_dict[f'round_{i}_endcondition'] = None  # Not provided in old CSV
        input_dict[f'round_{i}_date'] = line_dict.get('date')

        # Player 'ema' specific data
        input_dict[f'ema_round_{i}_opperator'] = line_dict.get(f'operator_{i}')
        input_dict[f'ema_round_{i}_kills'] = line_dict.get(f'kill_{i}')
        input_dict[f'ema_round_{i}_assists'] = None
        input_dict[f'ema_round_{i}_survived'] = line_dict.get(f'death_{i}')
        input_dict[f'ema_round_{i}_entryfrag'] = None
        input_dict[f'ema_round_{i}_diffuser'] = None
        input_dict[f'ema_round_{i}_cluth'] = None

        # Player 'mihnea' specific data
        input_dict[f'mihnea_round_{i}_opperator'] = line_dict.get(f'mihnea_{i}')
        input_dict[f'mihnea_round_{i}_kills'] = line_dict.get(f'kill_m_{i}')
        input_dict[f'mihnea_round_{i}_assists'] = None
        input_dict[f'mihnea_round_{i}_survived'] = line_dict.get(f'death_m_{i}')
        input_dict[f'mihnea_round_{i}_entryfrag'] = None
        input_dict[f'mihnea_round_{i}_diffuser'] = None
        input_dict[f'mihnea_round_{i}_cluth'] = None

    return input_dict

def clean_format(input_dict):
    """
    Cleans and formats the input dictionary to ensure all values are in the correct type
    or assigns None if the conversion fails.

    :param input_dict: A dictionary formatted for create_game_and_rounds function.
    :return: A cleaned and formatted dictionary.
    """
    def to_int(value):
        """Convert to integer or return None if conversion fails."""
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def to_bool(value):
        """Convert to boolean based on specific values or return None if not applicable."""
        if value in ['1', 1, 'True', True]:
            return True
        elif value in ['0', 0, 'False', False]:
            return False
        else:
            return None
        
    def to_bool_inverse(value):
        """Convert to boolean based on specific values or return None if not applicable."""
        if value in ['1', 1, 'True', True]:
            return False
        elif value in ['0', 0, 'False', False]:
            return True
        else:
            return None

    def to_str(value):
        """Convert to string or return None if conversion fails."""
        try:
            return str(value) if value is not None else None
        except (TypeError, ValueError):
            return None
        
    def to_date(value):
        """Convert to datetime.date or return None if conversion fails."""
        try:
            return datetime.date(value, '%m/%d/%Y') if value else None
        except (TypeError, ValueError):
            return None
        
    def to_sides(value):
        """Convert to string or return None if conversion fails."""
        if value in ['1', 1]:
            return 'attack'
        elif value in ['2', 2]:
            return 'defense'
        else:
            return None

    # Clean game-level data
    cleaned_dict = {
        'game_id': to_int(input_dict.get('game_id')),
        'date': to_date(input_dict.get('date')),
        'map_name': to_str(input_dict.get('map_name')),
        'game_win': to_bool(input_dict.get('game_win')),
        'ban_a_us': to_str(input_dict.get('ban_a_us')),
        'ban_a_op': to_str(input_dict.get('ban_a_op')),
        'ban_d_us': to_str(input_dict.get('ban_d_us')),
        'ban_d_op': to_str(input_dict.get('ban_d_op')),
        'gtype': to_str(input_dict.get('gtype')),
        'nrounds': to_int(input_dict.get('nrounds')),
        'score_us': to_int(input_dict.get('score_us')),
        'score_op': to_int(input_dict.get('score_op')),
    }

    # Clean round-specific and player-specific data
    for i in range(1, 10):
        # Round-specific keys
        cleaned_dict[f'round_{i}_id'] = to_int(input_dict.get(f'round_{i}_id'))
        cleaned_dict[f'round_{i}_number'] = to_int(input_dict.get(f'round_{i}_number'))
        cleaned_dict[f'round_{i}_site'] = to_str(input_dict.get(f'round_{i}_site'))
        cleaned_dict[f'round_{i}_side'] = to_sides(input_dict.get(f'round_{i}_side'))
        cleaned_dict[f'round_{i}_win'] = to_bool(input_dict.get(f'round_{i}_win'))
        cleaned_dict[f'round_{i}_type'] = to_str(input_dict.get(f'round_{i}_type'))
        cleaned_dict[f'round_{i}_endcondition'] = to_str(input_dict.get(f'round_{i}_endcondition'))
        cleaned_dict[f'round_{i}_date'] = to_str(input_dict.get(f'round_{i}_date'))

        # Player-specific keys for 'ema'
        cleaned_dict[f'ema_round_{i}_opperator'] = to_str(input_dict.get(f'ema_round_{i}_opperator'))
        cleaned_dict[f'ema_round_{i}_kills'] = to_int(input_dict.get(f'ema_round_{i}_kills'))
        cleaned_dict[f'ema_round_{i}_assists'] = to_int(input_dict.get(f'ema_round_{i}_assists'))
        cleaned_dict[f'ema_round_{i}_survived'] = to_bool_inverse(input_dict.get(f'ema_round_{i}_survived'))
        cleaned_dict[f'ema_round_{i}_entryfrag'] = to_bool(input_dict.get(f'ema_round_{i}_entryfrag'))
        cleaned_dict[f'ema_round_{i}_diffuser'] = to_bool(input_dict.get(f'ema_round_{i}_diffuser'))
        cleaned_dict[f'ema_round_{i}_cluth'] = to_bool(input_dict.get(f'ema_round_{i}_cluth'))

        # Player-specific keys for 'mihnea'
        cleaned_dict[f'mihnea_round_{i}_opperator'] = to_str(input_dict.get(f'mihnea_round_{i}_opperator'))
        cleaned_dict[f'mihnea_round_{i}_kills'] = to_int(input_dict.get(f'mihnea_round_{i}_kills'))
        cleaned_dict[f'mihnea_round_{i}_assists'] = to_int(input_dict.get(f'mihnea_round_{i}_assists'))
        cleaned_dict[f'mihnea_round_{i}_survived'] = to_bool_inverse(input_dict.get(f'mihnea_round_{i}_survived'))
        cleaned_dict[f'mihnea_round_{i}_entryfrag'] = to_bool(input_dict.get(f'mihnea_round_{i}_entryfrag'))
        cleaned_dict[f'mihnea_round_{i}_diffuser'] = to_bool(input_dict.get(f'mihnea_round_{i}_diffuser'))
        cleaned_dict[f'mihnea_round_{i}_cluth'] = to_bool(input_dict.get(f'mihnea_round_{i}_cluth'))

    return cleaned_dict

def create_game_and_rounds(input_dict):
    """
    Create Game and Round objects based on a flat input dictionary.

    :param input_dict: dictionary with game and rounds data in a single level.
    :return: Game object
    """
    game_id = 0
    round_id = 0

    # Extract game level data
    date = input_dict['date']
    map_name = input_dict['map_name']
    game_win = input_dict['game_win']
    ban_a_us = input_dict['ban_a_us']
    ban_a_op = input_dict['ban_a_op']
    ban_d_us = input_dict['ban_d_us']
    ban_d_op = input_dict['ban_d_op']
    gtype = input_dict['gtype']
    nrounds = input_dict['nrounds']
    score_us = input_dict['score_us']
    score_op = input_dict['score_op']

    # Initialize rounds dictionary
    rounds = {}

    # Create rounds based on available rounds in input_dict
    for i in range(1, nrounds + 1):
        # Extract round-specific data
        round_number = input_dict[f'round_{i}_number']
        site = input_dict[f'round_{i}_site']
        side = input_dict[f'round_{i}_side']
        win = input_dict[f'round_{i}_win']
        rtype = input_dict[f'round_{i}_type']
        endcondition = input_dict[f'round_{i}_endcondition']
        round_date = input_dict[f'round_{i}_date']

        # Extract player-specific data for this round
        round_data = {
            'site': site,
            'side': side,
            'win': win,
            'rtype': rtype,
            'endcondition': endcondition,
            'date': round_date,
            # Player 'ema' data
            'ema_opperator': input_dict[f'ema_round_{i}_opperator'],
            'ema_kills': input_dict[f'ema_round_{i}_kills'],
            'ema_assists': input_dict[f'ema_round_{i}_assists'],
            'ema_survived': input_dict[f'ema_round_{i}_survived'],
            'ema_entryfrag': input_dict[f'ema_round_{i}_entryfrag'],
            'ema_diffuser': input_dict[f'ema_round_{i}_diffuser'],
            'ema_cluth': input_dict[f'ema_round_{i}_cluth'],
            # Player 'mihnea' data
            'mihnea_opperator': input_dict[f'mihnea_round_{i}_opperator'],
            'mihnea_kills': input_dict[f'mihnea_round_{i}_kills'],
            'mihnea_assists': input_dict[f'mihnea_round_{i}_assists'],
            'mihnea_survived': input_dict[f'mihnea_round_{i}_survived'],
            'mihnea_entryfrag': input_dict[f'mihnea_round_{i}_entryfrag'],
            'mihnea_diffuser': input_dict[f'mihnea_round_{i}_diffuser'],
            'mihnea_cluth': input_dict[f'mihnea_round_{i}_cluth']
        }

        # Create Round object and add to rounds dictionary
        round_obj = Round(round_id, game_id, round_number, round_data)
        rounds[round_id] = round_obj
        round_id += 1

    # Create the game_data dictionary to pass to the Game constructor
    game_data = {
        'date': date,
        'map_name': map_name,
        'game_win': game_win,
        'ban_a_us': ban_a_us,
        'ban_a_op': ban_a_op,
        'ban_d_us': ban_d_us,
        'ban_d_op': ban_d_op,
        'gtype': gtype,
        'nrounds': nrounds,
        'score_us': score_us,
        'score_op': score_op
    }

    # Create Game object
    game_obj = Game(game_id, rounds, game_data)

    return game_obj