import datetime

player_data = {
    'opperator': str,          # Example: 'Ash' - The name of the player's operator
    'kills': int,              # Example: 3 - Number of kills
    'assists': int,            # Example: 1 - Number of assists
    'survived': bool,          # Example: True - True if player survived the round
    'entry_frag': bool,        # Example: False - True if player got/was the first kill
    'cluth': bool,             # Example: False - True if player clutched this round
    'diffuser': bool           # Example: False - True if player planted/diffused the diffuser
}

round_data = {
    'site': str,               # Example: 'A' - Site of the round
    'side': str,               # Example: 'attack' - Side (e.g., 'attack' or 'defense')
    'win': bool,               # Example: True - True if the round was won
    'rtype': str,              # Example: 'normal' - Type of the round
    'endcondition': str,       # Example: 'time expired' - End condition of the round
    'date': datetime.date,     # Example: datetime.date(2021, 1, 1) - Date of the round
    
    # Player data for 'ema'
    'ema_opperator': str,      # Example: 'Ash' - Operator used by player 'ema'
    'ema_kills': int,          # Example: 3 - Number of kills by 'ema'
    'ema_assists': int,        # Example: 1 - Number of assists by 'ema'
    'ema_survived': bool,      # Example: True - True if 'ema' survived
    'ema_entry_frag': bool,    # Example: False - True if 'ema' got/was the first kill
    'ema_diffuser': bool,      # Example: False - True if 'ema' planted/diffused the diffuser
    
    # Player data for 'mihnea'
    'mihnea_opperator': str,   # Example: 'Thermite' - Operator used by player 'mihnea'
    'mihnea_kills': int,       # Example: 2 - Number of kills by 'mihnea'
    'mihnea_assists': int,     # Example: 2 - Number of assists by 'mihnea'
    'mihnea_survived': bool,   # Example: False - True if 'mihnea' survived
    'mihnea_entry_frag': bool, # Example: True - True if 'mihnea' got/was the first kill
    'mihnea_diffuser': bool    # Example: True - True if 'mihnea' planted/diffused the diffuser
}