import os
import datetime
from backend.class_round import Round
from backend.class_game import Game

def get_relative_path(target_file, directory='data', curent_file=__file__):
    curent_dir = os.path.dirname(curent_file)
    one_dir_up = os.path.join(curent_dir, os.pardir)
    data_dir = os.path.join(one_dir_up, directory)
    path = os.path.join(data_dir, target_file)
    return path

def determine_round_type(gtype, round_number, roundwins):
    """
    Determine the type of the round based on the game type and round number.

    :param gtype: A string representing the game type.
    :param round_number: An integer representing the round number.
    :param roundwins: A list of booleans representing the round wins.
    :return: A string representing the round type.
    """
    if gtype == 'ranked':
        if round_number in [7, 9]:
            return 'overtime'
        elif roundwins.count(True) == 4:
            return 'matchpoint-us'
        elif roundwins.count(False) == 4:
            return 'matchpoint-op'
        elif roundwins.count(True) == 3:
            return 'matchpoint-us'
        elif roundwins.count(False) == 3:
            return 'matchpoint-op'
        else:
            return 'normal'
    if gtype == 'standard':
        if round_number == 7:
            return 'overtime'
        elif roundwins.count(True) == 3:
            return 'matchpoint-us'
        elif roundwins.count(False) == 3:
            return 'matchpoint-op'
        else:
            return 'normal'
    if gtype == 'quick':
        if round_number == 5:
            return 'overtime'
        elif roundwins.count(True) == 2:
            return 'matchpoint-us'
        elif roundwins.count(False) == 2:
            return 'matchpoint-op'
        else:
            return 'normal'
    return None

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
    rounds = []
    round_wins = [input_dict[f'round_{i}_win'] for i in range(1, nrounds + 1)]

    # Create rounds based on available rounds in input_dict
    for i in range(1, nrounds + 1):
        # Extract round-specific data
        round_number = input_dict[f'round_{i}_number']
        site = input_dict[f'round_{i}_site']
        side = input_dict[f'round_{i}_side']
        win = input_dict[f'round_{i}_win']
        rtype = determine_round_type(gtype, round_number, round_wins)
        endcondition = input_dict[f'round_{i}_endcondition']

        # Extract player-specific data for this round
        round_data = {
            'site': site,
            'side': side,
            'win': win,
            'rtype': rtype,
            'endcondition': endcondition,
            'date': date,
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
        rounds.append(round_obj)
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
    game_obj = Game(game_id, game_data)

    return game_obj, rounds

def form_input_clean(input_dict):
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

    def to_str(value):
        """Convert to string or return None if conversion fails."""
        try:
            return str(value) if value is not None else None
        except (TypeError, ValueError):
            return None
        
    def to_date(value):
        """Convert to datetime.date or return None if conversion fails."""
        try:
            if type(value) == datetime.date:
                return value
            elif type(value) == str:
                return datetime.datetime.strptime(value, '%m/%d/%Y').date()
            else:
                return None
        except (TypeError, ValueError):
            return None

    # Clean game-level data
    cleaned_dict = {
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
    for i in range(1, cleaned_dict['nrounds'] + 1):
        # Round-specific keys
        cleaned_dict[f'round_{i}_number'] = i
        cleaned_dict[f'round_{i}_site'] = to_str(input_dict.get(f'round_{i}_site'))
        cleaned_dict[f'round_{i}_side'] = to_str(input_dict.get(f'round_{i}_side')).lower()
        cleaned_dict[f'round_{i}_win'] = to_bool(input_dict.get(f'round_{i}_win'))
        cleaned_dict[f'round_{i}_endcondition'] = to_str(input_dict.get(f'round_{i}_endcondition'))
        cleaned_dict[f'round_{i}_date'] = cleaned_dict['date']

        # Player-specific keys for 'ema'
        cleaned_dict[f'ema_round_{i}_opperator'] = to_str(input_dict.get(f'ema_round_{i}_opperator'))
        cleaned_dict[f'ema_round_{i}_kills'] = to_int(input_dict.get(f'ema_round_{i}_kills'))
        cleaned_dict[f'ema_round_{i}_assists'] = to_int(input_dict.get(f'ema_round_{i}_assists'))
        cleaned_dict[f'ema_round_{i}_survived'] = to_bool(input_dict.get(f'ema_round_{i}_survived'))
        cleaned_dict[f'ema_round_{i}_entryfrag'] = to_bool(input_dict.get(f'ema_round_{i}_entryfrag'))
        cleaned_dict[f'ema_round_{i}_diffuser'] = to_bool(input_dict.get(f'ema_round_{i}_diffuser'))
        cleaned_dict[f'ema_round_{i}_cluth'] = to_bool(input_dict.get(f'ema_round_{i}_cluth'))

        # Player-specific keys for 'mihnea'
        cleaned_dict[f'mihnea_round_{i}_opperator'] = to_str(input_dict.get(f'mihnea_round_{i}_opperator'))
        cleaned_dict[f'mihnea_round_{i}_kills'] = to_int(input_dict.get(f'mihnea_round_{i}_kills'))
        cleaned_dict[f'mihnea_round_{i}_assists'] = to_int(input_dict.get(f'mihnea_round_{i}_assists'))
        cleaned_dict[f'mihnea_round_{i}_survived'] = to_bool(input_dict.get(f'mihnea_round_{i}_survived'))
        cleaned_dict[f'mihnea_round_{i}_entryfrag'] = to_bool(input_dict.get(f'mihnea_round_{i}_entryfrag'))
        cleaned_dict[f'mihnea_round_{i}_diffuser'] = to_bool(input_dict.get(f'mihnea_round_{i}_diffuser'))
        cleaned_dict[f'mihnea_round_{i}_cluth'] = to_bool(input_dict.get(f'mihnea_round_{i}_cluth'))

    return cleaned_dict




def load_instances_from_csv(path):
    pass


## Functions for OLD CSV data processing
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

    # check if all bas exist (not "") or all bans do not exist ("")
    if input_dict['ban_a_op'] == "" and input_dict['ban_d_op'] == "" and input_dict['ban_a_us'] == "" and input_dict['ban_d_us'] == "":
        input_dict['gtype'] = "Standard"
    elif input_dict['ban_a_op'] != "" and input_dict['ban_d_op'] != "" and input_dict['ban_a_us'] != "" and input_dict['ban_d_us'] != "":
        input_dict['gtype'] = "Ranked"
    
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
            if type(value) == datetime.date:
                return value
            elif type(value) == str:
                return datetime.datetime.strptime(value, '%m/%d/%Y').date()
            else:
                return None
        except (TypeError, ValueError):
            return None
        
    def to_sides(value):
        """Convert to string or return None if conversion fails."""
        if value in ['1', 1]:
            return 'Attack'
        elif value in ['2', 2]:
            return 'Defense'
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
    for i in range(1, cleaned_dict['nrounds']+1):
        # Round-specific keys
        cleaned_dict[f'round_{i}_id'] = to_int(input_dict.get(f'round_{i}_id'))
        cleaned_dict[f'round_{i}_number'] = to_int(input_dict.get(f'round_{i}_number'))
        cleaned_dict[f'round_{i}_site'] = to_str(input_dict.get(f'round_{i}_site'))
        cleaned_dict[f'round_{i}_side'] = to_sides(input_dict.get(f'round_{i}_side'))
        cleaned_dict[f'round_{i}_win'] = to_bool(input_dict.get(f'round_{i}_win'))
        round_wins_so_far = [cleaned_dict[f'round_{j}_win'] for j in range(1, i)]
        cleaned_dict[f'round_{i}_type'] = determine_round_type(cleaned_dict['gtype'], i, round_wins_so_far)
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

def old_input_clean_data(rec):
    # rec had dictionaries with games, rounds, maps

    # change map names
    # map names exist in Map, Game, Site
    # change in rec.maps, rec.maps.sites, rec.maps.games
    list_old_names = ['Club House', 'Kafe', 'Emerald', 'Nighthaven']
    list_new_names = ['Clubhouse', 'Kafe Dostoyevsky', 'Emerald Plains', 'Nighthaven Labs']

    for old_name, new_name in zip(list_old_names, list_new_names):
        try:
            rec.maps[new_name] = rec.maps.pop(old_name)
        except KeyError:
            pass
        rec.maps[new_name].name = new_name
        for site in rec.maps[new_name].sites["Attack"].values():
            site.map_name = new_name
        for site in rec.maps[new_name].sites["Defense"].values():
            site.map_name = new_name
        for game in rec.maps[new_name].games.values():
            if game.map_name == old_name:
                game.map_name = new_name

    list_sites_per_map = {}
    list_sites_per_map = {
        'Clubhouse': {'1': 'Gym', '2': 'Cash', '3': 'Bar', '4': 'Basement'},
        'Kafe Dostoyevsky': {'1': 'Cocktail', '2': 'Mining', '3': 'Reading', '4': 'Kitchen'},
        'Emerald Plains': {'1': 'CEO', '2': 'Painting', '3': 'Bat', '4': 'Kitchen'},
        # 'Nighthaven Labs': {'1': '', '2': '', '3': '', '4': ''},
        # 'Bank': {'1': 'CEO', '2': 'Open Area', '3': '', '4': ''},
        # 'Border': {'1': '', '2': ' ', '3': '  ', '4': '   '},
        # 'Chalet': {'1': 'Bedroom', '2': ' ', '3': '  ', '4': 'Garage'},
        'Coastline': {'1': 'Hooka', '2': 'Theater', '3': 'Bar', '4': 'Kitchen'},
        # 'Consulate': {'1': '', '2': ' ', '3': '  ', '4': '   '},
        # 'Favela': {'1': '', '2': ' ', '3': '  ', '4': '   '},
        # 'Hereford Base': {'1': '', '2': ' ', '3': '  ', '4': '   '},
        # 'House': {'1': '', '2': ' ', '3': '  ', '4': '   '},
        # 'Kanal': {'1': '', '2': ' ', '3': '  ', '4': '   '},
        # 'Oregon': {'1': 'Dorms', '2': '', '3': 'Open Area', '4': 'Basement'},
        'Outback': {'1': 'Laundry', '2': 'Party', '3': 'Green/Red', '4': 'Kitchen'},
        # 'Plane': {'1': '', '2': ' ', '3': '  ', '4': '   '},
        'Skyscraper': {'1': 'Tea Room', '2': 'Exhibition', '3': 'Bedroom', '4': 'BBQ'},
        'Theme Park': {'1': 'Initiation', '2': 'Daycare', '3': 'Throne', '4': 'Lab'},
        # 'Tower': {'1': '', '2': ' ', '3': '  ', '4': '   '},
        # 'Villa': {'1': 'Aviator', '2': 'Statuary', '3': '', '4': ''},
        # 'Yacht': {'1': '', '2': ' ', '3': '  ', '4': '   '},
        # 'Lair': {'1': '', '2': ' ', '3': '  ', '4': '   '},
        # 'Stadium': {'1': '', '2': ' ', '3': '  ', '4': '   '}
    }

    # change site names
    # site names exist in Site, Round and in dictionary key in Map.site
    # change in rec.maps.sites.names, rec.maps.sites second key, rec.maps.rounds.site, rec.maps.sites.rounds.site

    for map_name, sites_dictionary in list_sites_per_map.items():
        if map_name in rec.maps.keys():
            for old, new in sites_dictionary.items():
                if old in rec.maps[map_name].sites["Attack"]:
                    rec.maps[map_name].sites["Attack"][new] = rec.maps[map_name].sites["Attack"].pop(old)
                    rec.maps[map_name].sites["Attack"][new].name = new
                    for round in rec.maps[map_name].sites["Attack"][new].rounds.values():
                        if round.site == old:
                            round.site = new
                else:
                    print(f"Attack {old} not found in {map_name}")
                if old in rec.maps[map_name].sites["Defense"]:
                    rec.maps[map_name].sites["Defense"][new] = rec.maps[map_name].sites["Defense"].pop(old)
                    rec.maps[map_name].sites["Defense"][new].name = new
                    for round in rec.maps[map_name].sites["Defense"][new].rounds.values():
                        if round.site == old:
                            round.site = new
                else:
                    print(f"Defense {old} not found in {map_name}")

                # change round site names in rec.maps[map_name].rounds
                for round in rec.maps[map_name].rounds.values():
                    if round.site == old:
                        round.site = new

    return rec