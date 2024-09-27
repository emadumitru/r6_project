from backend.class_player import PS

class Round:
    def __init__(self, round_id, game_id, round_number, round_data):
        """
        Round class
        :param round_id: int - round number
        :param round_data: dictionary with round data
        """
        self.id = round_id
        self.game_id = game_id
        self.site = round_data['site']
        self.side = round_data['side']
        self.round_number = round_number
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
    
    def csv_line(self):
        i = self.round_number
        round_dict = {
            f'round_{i}_site': self.site,
            f'round_{i}_side': self.side,
            f'round_{i}_win': self.win,
            f'round_{i}_rtype': self.rtype,
            f'round_{i}_endcondition': self.endcondition,
            f'round_{i}_date': self.date,
            f'ema_round_{i}_opperator': self.player_stats['ema'].opperator,
            f'ema_round_{i}_kills': self.player_stats['ema'].kills,
            f'ema_round_{i}_assists': self.player_stats['ema'].assists,
            f'ema_round_{i}_survived': self.player_stats['ema'].survived,
            f'ema_round_{i}_entryfrag': self.player_stats['ema'].entryfrag,
            f'ema_round_{i}_diffuser': self.player_stats['ema'].diffuser,
            f'ema_round_{i}_cluth': self.player_stats['ema'].cluth,
            f'mihnea_round_{i}_opperator': self.player_stats['mihnea'].opperator,
            f'mihnea_round_{i}_kills': self.player_stats['mihnea'].kills,
            f'mihnea_round_{i}_assists': self.player_stats['mihnea'].assists,
            f'mihnea_round_{i}_survived': self.player_stats['mihnea'].survived,
            f'mihnea_round_{i}_entryfrag': self.player_stats['mihnea'].entryfrag,
            f'mihnea_round_{i}_diffuser': self.player_stats['mihnea'].diffuser,
            f'mihnea_round_{i}_cluth': self.player_stats['mihnea'].cluth
        }
        return round_dict