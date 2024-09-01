

class PS:
    def __init__(self, player_data):
        self.opperator = player_data['opperator']       # Player's opperator
        self.kills = player_data['kills']               # Number of kills
        self.assists = player_data['assists']           # Number of assists
        self.survived = player_data['survived']         # True if player survived the round
        self.entry_frag = player_data['entry_frag']     # True if player got/was the first kill
        self.diffuser = player_data['diffuser']         # True if player planted/diffused the diffuser
        self.kos = 1 if (self.kills > 0 or self.survived or self.diffuser) else 0
        ##TODO: add more calculated attributes