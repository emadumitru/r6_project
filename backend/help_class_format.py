import datetime
from class_player import  PS
from class_round import Round
from class_game import Game
from class_site import Site
from class_map import Rmap

PS_attributes = {
    'opperator': str,  # Player's operator, e.g., 'Ash'
    'kills': int,      # Number of kills, e.g., 3
    'assists': int,    # Number of assists, e.g., 1
    'survived': bool,  # True if player survived the round, e.g., True
    'entryfrag': bool, # True if player got/was the first kill, e.g., False
    'diffuser': bool,  # True if player planted/diffused the diffuser, e.g., False
    'cluth': bool,     # True if player clutched this round, e.g., False
    'kos': int         # 1 if (kills > 0 or survived or diffuser), otherwise 0, e.g., 1
}

Round_attributes = {
    'id': int,                       # Round number, e.g., 1
    'game_id': int,                  # ID of the game, e.g., 101
    'site': str,                     # Site of the round, e.g., 'Kitchen'
    'side': str,                     # Side played, e.g., 'attack'
    'round_number': int,             # The specific round number in the game, e.g., 3
    'win': bool,                     # Whether the round was won, e.g., True
    'player_stats': dict[PS],        # Player stats for the round, e.g., {'ema': PS, 'mihnea': PS}
    'rtype': str,                    # Round type, e.g., 'bomb'
    'endcondition': str,             # End condition of the round, e.g., 'time expired'
    'date': datetime.date            # Date of the round, e.g., datetime.date(2024, 9, 1)
}

Site_attributes = {
    'id': str,               # Unique identifier of the site, e.g., 'Kitchen_attack'
    'map_name': str,         # Name of the map, e.g., 'Clubhouse'
    'side': str,             # Side played on the site, e.g., 'attack'
    'name': str,             # Name of the site, e.g., 'Kitchen'
    'rounds': dict[Round],   # Dictionary of rounds played at the site, e.g., {1: Round}
    'games_in_site': list,   # List of game IDs played at the site, e.g., [101]
    'statistics': dict       # Win statistics, e.g., {'win': 2, 'winperc': 50.0}
}

Rmap_attributes = {
    'name': str,             # Name of the map, e.g., 'Oregon'
    'sites': dict[Site],     # Sites available on the map, e.g., {'Kitchen_attack': Site}
    'rounds': dict[Round],   # Rounds played on the map, e.g., {1: Round}
    'games': dict[Game],     # Games played on the map, e.g., {101: Game}
    'statistics': dict       # Win statistics, e.g., {'win': 5, 'winperc': 60.0}
}

Game_attributes = {
    'id': int,               # Game ID, e.g., 101
    'date': str,             # Date of the game, e.g., '2024-09-01'
    'map_name': str,         # Map name, e.g., 'Bank'
    'win': bool,             # Whether the game was won, e.g., True
    'bans_a': list,          # Attack bans, e.g., ['Thermite', 'Maverick']
    'bans_d': list,          # Defense bans, e.g., ['Mira', 'Echo']
    'gtype': str,            # Game type, e.g., 'ranked'
    'nrounds': int,          # Number of rounds, e.g., 7
    'score': tuple,          # Game score, e.g., (4, 3)
    'rounds_ids': list       # List of round IDs, e.g., [1, 2, 3, 4, 5, 6, 7]
}

Recommender_attributes = {
    'games': dict[Game],           # All games tracked, e.g., {101: Game}
    'rounds': dict[Round],         # All rounds tracked, e.g., {1: Round}
    'maps': dict[Rmap]             # Maps available, e.g., {'Oregon': Rmap}
}
