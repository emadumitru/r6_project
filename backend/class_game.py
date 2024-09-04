from backend.class_round import Round

class Game:
    def __init__(self, game_id, game_data, round_ids = []):
        self.id = game_id
        self.date = game_data['date']
        self.map_name = game_data['map_name']
        self.win = game_data['game_win']
        self.bans_a = [game_data['ban_a_us'], game_data['ban_a_op']]
        self.bans_d = [game_data['ban_d_us'], game_data['ban_d_op']]
        self.gtype = game_data['gtype']
        self.nrounds = game_data['nrounds']
        self.score = (game_data['score_us'], game_data['score_op'])

        self.round_ids = round_ids
        

    def csv_line(self):
        dictionary = {
            'date': self.date,
            'map_name': self.map_name,
            'game_win': self.win,
            'ban_a_us': self.bans_a[0],
            'ban_a_op': self.bans_a[1],
            'ban_d_us': self.bans_d[0],
            'ban_d_op': self.bans_d[1],
            'gtype': self.gtype,
            'nrounds': self.nrounds,
            'score_us': self.score[0],
            'score_op': self.score[1],
        }


        # for round in self.rounds.values():
        #     i = round.round_number
        #     round_dict = {
        #         f'round_{i}_site': round.site,
        #         f'round_{i}_side': round.side,
        #         f'round_{i}_win': round.win,
        #         f'round_{i}_rtype': round.rtype,
        #         f'round_{i}_endcondition': round.endcondition,
        #         f'round_{i}_date': round.date,
        #         f'ema_round_{i}_opperator': round.player_stats['ema'].opperator,
        #         f'ema_round_{i}_kills': round.player_stats['ema'].kills,
        #         f'ema_round_{i}_assists': round.player_stats['ema'].assists,
        #         f'ema_round_{i}_survived': round.player_stats['ema'].survived,
        #         f'ema_round_{i}_entryfrag': round.player_stats['ema'].entryfrag,
        #         f'ema_round_{i}_diffuser': round.player_stats['ema'].diffuser,
        #         f'ema_round_{i}_cluth': round.player_stats['ema'].cluth,
        #         f'mihnea_round_{i}_opperator': round.player_stats['mihnea'].opperator,
        #         f'mihnea_round_{i}_kills': round.player_stats['mihnea'].kills,
        #         f'mihnea_round_{i}_assists': round.player_stats['mihnea'].assists,
        #         f'mihnea_round_{i}_survived': round.player_stats['mihnea'].survived,
        #         f'mihnea_round_{i}_entryfrag': round.player_stats['mihnea'].entryfrag,
        #         f'mihnea_round_{i}_diffuser': round.player_stats['mihnea'].diffuser,
        #         f'mihnea_round_{i}_cluth': round.player_stats['mihnea'].cluth
        #     }
        #     dictionary.update(round_dict)

        return dictionary
