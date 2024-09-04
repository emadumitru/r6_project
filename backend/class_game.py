from backend.class_round import Round

##TODO: make function csv_line for exporting data to csv

class Game:
    def __init__(self, game_id, rounds, game_data):
        self.id = game_id
        self.date = game_data['date']
        self.map_name = game_data['map_name']
        self.win = game_data['game_win']
        self.bans_a = [game_data['ban_a_us'], game_data['ban_a_op']]
        self.bans_d = [game_data['ban_d_us'], game_data['ban_d_op']]
        self.gtype = game_data['gtype']
        self.nrounds = game_data['nrounds']
        self.score = (game_data['score_us'], game_data['score_op'])

        # self.rounds = self.get_rounds(round_id, game_data)
        self.rounds = rounds
        self.player_stats = self.get_player_stats()
        self.game_stats = self.get_game_stats()

    # def get_rounds(self, round_id, game_data):
    #     rounds = {}
    #     for i in range(1, self.nrounds + 1):
    #         relevant_data = {key: value for key, value in game_data.items() if f'round_{i}' in key}
    #         rounds[i] = Round(round_id, self.id, i, relevant_data)
    #         round_id += 1
    #     return rounds
    
    def get_player_stats(self):
        player_stats = {}
        for round in self.rounds.values():
            for player, ps in round.player_stats.items():
                if player in player_stats:
                    player_stats[player].append(ps)
                else:
                    player_stats[player] = [ps]
        return player_stats
    
    def get_game_stats(self):
        game_stats = {}
        for player, ps_list in self.player_stats.items():
            game_stats[player] = {
                'kills': sum([ps.kills for ps in ps_list if ps.kills is not None]),
                'assists': sum([ps.assists for ps in ps_list if ps.assists is not None]),
                'survives': sum([ps.survived for ps in ps_list if ps.survived is not None]),
                'kos': sum([ps.kos for ps in ps_list if ps.kos is not None]),
                'entryfrags': sum([ps.entryfrag for ps in ps_list if ps.entryfrag is not None]),
                'diffusers': sum([ps.diffuser for ps in ps_list if ps.diffuser is not None]),
                'clutches': sum([ps.cluth for ps in ps_list if ps.cluth is not None]),
            }
            game_stats[player]['kpr'] = game_stats[player]['kills'] / self.nrounds
            game_stats[player]['apr'] = game_stats[player]['assists'] / self.nrounds
            game_stats[player]['spr'] = game_stats[player]['survives'] / self.nrounds
            game_stats[player]['gkos'] = game_stats[player]['kos'] / self.nrounds
            game_stats[player]['efpr'] = game_stats[player]['entryfrags'] / self.nrounds
            game_stats[player]['dfr'] = game_stats[player]['diffusers'] / self.nrounds
            game_stats[player]['cpr'] = game_stats[player]['clutches'] / self.nrounds
            deaths = self.nrounds - game_stats[player]['survives']
            game_stats[player]['kd'] = game_stats[player]['kills'] / deaths if deaths > 0 else (game_stats[player]['kills'] + 1)
        return game_stats

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


        for round in self.rounds.values():
            i = round.round_number
            round_dict = {
                f'round_{i}_site': round.site,
                f'round_{i}_side': round.side,
                f'round_{i}_win': round.win,
                f'round_{i}_rtype': round.rtype,
                f'round_{i}_endcondition': round.endcondition,
                f'round_{i}_date': round.date,
                f'ema_round_{i}_opperator': round.player_stats['ema'].opperator,
                f'ema_round_{i}_kills': round.player_stats['ema'].kills,
                f'ema_round_{i}_assists': round.player_stats['ema'].assists,
                f'ema_round_{i}_survived': round.player_stats['ema'].survived,
                f'ema_round_{i}_entryfrag': round.player_stats['ema'].entryfrag,
                f'ema_round_{i}_diffuser': round.player_stats['ema'].diffuser,
                f'ema_round_{i}_cluth': round.player_stats['ema'].cluth,
                f'mihnea_round_{i}_opperator': round.player_stats['mihnea'].opperator,
                f'mihnea_round_{i}_kills': round.player_stats['mihnea'].kills,
                f'mihnea_round_{i}_assists': round.player_stats['mihnea'].assists,
                f'mihnea_round_{i}_survived': round.player_stats['mihnea'].survived,
                f'mihnea_round_{i}_entryfrag': round.player_stats['mihnea'].entryfrag,
                f'mihnea_round_{i}_diffuser': round.player_stats['mihnea'].diffuser,
                f'mihnea_round_{i}_cluth': round.player_stats['mihnea'].cluth
            }
            dictionary.update(round_dict)

        return dictionary
