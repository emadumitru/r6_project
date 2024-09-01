

class PS:
    def __init__(self, player_data):
        """
        Player Statistics class
        :param player_data: dictionary with player data
        """
        self.opperator = player_data['opperator']       # Player's opperator
        self.kills = player_data['kills']               # Number of kills
        self.assists = player_data['assists']           # Number of assists
        self.survived = player_data['survived']         # True if player survived the round
        self.entryfrag = player_data['entryfrag']       # True if player got/was the first kill
        self.diffuser = player_data['diffuser']         # True if player planted/diffused the diffuser
        self.cluth = player_data['cluth']               # True if player clutched this round
        self.kos = self.get_kos()                       # 1 if (kills > 0 or survived or diffuser), otherwise 0
        ##TODO: add more calculated attributes

    def get_kos(self):
        if self.kills == None:
            kills = 0
        else:
            kills = self.kills

        return 1 if (kills > 0 or self.survived or self.diffuser) else 0