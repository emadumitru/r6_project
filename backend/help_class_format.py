import datetime

PS_attributes = {
    'opperator': str,       # Player's operator, e.g., 'Ash'
    'kills': int,           # Number of kills, e.g., 3
    'assists': int,         # Number of assists, e.g., 1
    'survived': bool,       # True if player survived the round, e.g., True
    'entry_frag': bool,     # True if player got/was the first kill, e.g., False
    'diffuser': bool,       # True if player planted/diffused the diffuser, e.g., False
    'cluth': bool,          # True if player clutched this round, e.g., False
    'kos': int              # 1 if (kills > 0 or survived or diffuser), otherwise 0, e.g., 1
}

Round_attributes = {
    'id': int,                               # Round number, e.g., 1
    'round_number': int,                     # Round number, e.g., 1
    'site': str,                             # Site of the round, e.g., 'A'
    'side': str,                             # Side (e.g., 'attack' or 'defense'), e.g., 'attack'
    'win': bool,                             # True if the round was won, e.g., True
    'player_stats': dict,                    # Dictionary containing PS objects for players, e.g., {'ema': PS, 'mihnea': PS}
    'rtype': str,                            # Type of the round, e.g., 'normal'
    'endcondition': str,                     # End condition of the round, e.g., 'time expired'
    'date': datetime.date                    # Date of the round, e.g., datetime.date(2021, 1, 1)
}