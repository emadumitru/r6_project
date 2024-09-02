import datetime

player_data = {
    'opperator': str,      # Example: 'Ash' - The name of the player's operator
    'kills': int,          # Example: 3 - Number of kills
    'assists': int,        # Example: 1 - Number of assists
    'survived': bool,      # Example: True - True if player survived the round
    'entryfrag': bool,     # Example: False - True if player got/was the first kill
    'diffuser': bool,      # Example: False - True if player planted/diffused the diffuser
    'cluth': bool          # Example: False - True if player clutched this round
}

round_data = {
    'site': str,                     # Example: 'Kitchen' - Site of the round
    'side': str,                     # Example: 'attack' - Side (e.g., 'attack' or 'defense')
    'win': bool,                     # Example: True - True if the round was won
    'rtype': str,                    # Example: 'normal' - Type of the round
    'endcondition': str,             # Example: 'time expired' - End condition of the round
    'date': datetime.date,           # Example: datetime.date(2021, 1, 1) - Date of the round

    # Player data for 'ema'
    'ema_opperator': str,            # Example: 'Ash' - Operator used by player 'ema'
    'ema_kills': int,                # Example: 3 - Number of kills by 'ema'
    'ema_assists': int,              # Example: 1 - Number of assists by 'ema'
    'ema_survived': bool,            # Example: True - True if 'ema' survived
    'ema_entryfrag': bool,           # Example: False - True if 'ema' got/was the first kill
    'ema_diffuser': bool,            # Example: False - True if 'ema' planted/diffused the diffuser
    'ema_cluth': bool,               # Example: False - True if 'ema' clutched the round

    # Player data for 'mihnea'
    'mihnea_opperator': str,         # Example: 'Thermite' - Operator used by player 'mihnea'
    'mihnea_kills': int,             # Example: 2 - Number of kills by 'mihnea'
    'mihnea_assists': int,           # Example: 2 - Number of assists by 'mihnea'
    'mihnea_survived': bool,         # Example: False - True if 'mihnea' survived
    'mihnea_entryfrag': bool,        # Example: True - True if 'mihnea' got/was the first kill
    'mihnea_diffuser': bool,         # Example: True - True if 'mihnea' planted/diffused the diffuser
    'mihnea_cluth': bool             # Example: False - True if 'mihnea
}

site_data = {
    'site_id': str,          # Example: 'Kitchen_attack' - Unique site identifier
    'map_name': str,         # Example: 'Clubhouse' - Map name
    'site_name': str,        # Example: 'Kitchen' - Site name
    'side': str              # Example: 'attack' - Side played
}

map_data = {
    'map_name': str,         # Example: 'Oregon' - Name of the map
    'site_names': list       # Example: ['Kitchen', 'Meeting'] - List of site names
}

game_data = {
    'date': str,             # Example: '2024-09-01' - Date of the game
    'map_name': str,         # Example: 'Bank' - Name of the map
    'game_win': bool,        # Example: True - Whether the game was won
    'ban_a_us': str,         # Example: 'Thermite' - Attack ban by user
    'ban_a_op': str,         # Example: 'Maverick' - Attack ban by opponent
    'ban_d_us': str,         # Example: 'Mira' - Defense ban by user
    'ban_d_op': str,         # Example: 'Echo' - Defense ban by opponent
    'gtype': str,            # Example: 'ranked' - Game type
    'nrounds': int,          # Example: 7 - Number of rounds
    'score_us': int,         # Example: 4 - User score
    'score_op': int          # Example: 3 - Opponent score
}

form_output = {
    'date': str,             # Format: %m/%d/%Y, Example: '2024-09-01' - Date of the game
    'map_name': str,         # Example: 'Bank' - Name of the map
    'game_win': bool,        # Example: True - Whether the game was won
    'ban_a_us': str,         # Example: 'Thermite' - Attack ban by user
    'ban_a_op': str,         # Example: 'Maverick' - Attack ban by opponent
    'ban_d_us': str,         # Example: 'Mira' - Defense ban by user
    'ban_d_op': str,         # Example: 'Echo' - Defense ban by opponent
    'gtype': str,            # Options: 'ranked', 'standard', 'quick' Example: 'ranked' - Game type
    'nrounds': int,          # Example: 7 - Number of rounds
    'score_us': int,         # Example: 4 - User score
    'score_op': int,         # Example: 3 - Opponent score

    # Round data under round_{number}_[]
    'site': str,             # Example: 'Kitchen' - Site of the round
    'side': str,             # Example: 'attack' - Side (e.g., 'attack' or 'defense')
    'win': bool,             # Example: True - True if the round was won
    'endcondition': str,     # Example: 'time expired' - End condition of the round

    # Round player data under {player}_round_{number}_[]
    'operator': str,         # Example: 'Ash' - Operator used by player
    'kills': int,            # Example: 3 - Number of kills by player
    'assists': int,          # Example: 1 - Number of assists by player
    'survived': bool,        # Example: True if player survived
    'entryfrag': bool,       # Example: True if player got/was the first kill
    'diffuser': bool,        # Example: True if player planted/diffused the diffuser
    'clutch': bool           # Example: True if player clutched the round
}