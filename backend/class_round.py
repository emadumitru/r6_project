from class_player import PS

class Round:
    def __init__(self, round_id, game_id, round_number, round_data):
        """
        Round class
        :param round_id: int - round number
        :param round_data: dictionary with round data
        """
        self.id = round_id
        self.game_id = game_id
        self.round_number = round_number
        self.site = round_data['site']
        self.side = round_data['side']
        self.win = round_data['win']
        self.player_stats = {'ema': self.get_player_data('ema', round_data), 'mihnea': self.get_player_data('mihnea', round_data)}
        self.rtype = round_data['rtype']
        self.endcondition = round_data['endcondition']
        self.date = round_data['date']
        

    def get_player_data(self, player, round_data):
        """
        Get player data from round. Get dictionary subset with player name in key.
        :param player: str - player name
        :param round_data: dictionary with round data
        :return: PS object
        """
        related_data = {key: value for key, value in round_data.items() if player in key}
        # rename keys to remove player name
        player_data = {key.split('_')[1]: value for key, value in related_data.items()}
        return PS(player_data)