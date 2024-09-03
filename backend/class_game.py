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
        # get first element of rounds
        round_1 = list(self.rounds.values())[0] if len(self.rounds) > 0 else None
        round_2 = list(self.rounds.values())[1] if len(self.rounds) > 1 else None
        round_3 = list(self.rounds.values())[2] if len(self.rounds) > 2 else None
        round_4 = list(self.rounds.values())[3] if len(self.rounds) > 3 else None
        round_5 = list(self.rounds.values())[4] if len(self.rounds) > 4 else None
        round_6 = list(self.rounds.values())[5] if len(self.rounds) > 5 else None
        round_7 = list(self.rounds.values())[6] if len(self.rounds) > 6 else None
        round_8 = list(self.rounds.values())[7] if len(self.rounds) > 7 else None
        round_9 = list(self.rounds.values())[8] if len(self.rounds) > 8 else None
        dictionary = {
            'win': self.win,
            'score_us': self.score[0],
            'score_opp': self.score[1],
            'rounds': self.nrounds,
            'map': self.map_name,
            'bans_a_us': self.bans_a[0],
            'bans_a_opp': self.bans_a[1],
            'bans_d_us': self.bans_d[0],
            'bans_d_opp': self.bans_d[1],
            'location_1': round_1.site if round_1 else None,
            'location_2': round_2.site if round_2 else None,
            'location_3': round_3.site if round_3 else None,
            'location_4': round_4.site if round_4 else None,
            'location_5': round_5.site if round_5 else None,
            'location_6': round_6.site if round_6 else None,
            'location_7': round_7.site if round_7 else None,
            'location_8': round_8.site if round_8 else None,
            'location_9': round_9.site if round_9 else None,
            'side_1': round_1.side if round_1 else None,
            'side_2': round_2.side if round_2 else None,
            'side_3': round_3.side if round_3 else None,
            'side_4': round_4.side if round_4 else None,
            'side_5': round_5.side if round_5 else None,
            'side_6': round_6.side if round_6 else None,
            'side_7': round_7.side if round_7 else None,
            'side_8': round_8.side if round_8 else None,
            'side_9': round_9.side if round_9 else None,
            'opperator_1': round_1.player_stats['ema'].opperator if round_1 else None,
            'opperator_2': round_2.player_stats['ema'].opperator if round_2 else None,
            'opperator_3': round_3.player_stats['ema'].opperator if round_3 else None,
            'opperator_4': round_4.player_stats['ema'].opperator if round_4 else None,
            'opperator_5': round_5.player_stats['ema'].opperator if round_5 else None,
            'opperator_6': round_6.player_stats['ema'].opperator if round_6 else None,
            'opperator_7': round_7.player_stats['ema'].opperator if round_7 else None,
            'opperator_8': round_8.player_stats['ema'].opperator if round_8 else None,
            'opperator_9': round_9.player_stats['ema'].opperator if round_9 else None,
            'win_1': round_1.win if round_1 else None,
            'win_2': round_2.win if round_2 else None,
            'win_3': round_3.win if round_3 else None,
            'win_4': round_4.win if round_4 else None,
            'win_5': round_5.win if round_5 else None,
            'win_6': round_6.win if round_6 else None,
            'win_7': round_7.win if round_7 else None,
            'win_8': round_8.win if round_8 else None,
            'win_9': round_9.win if round_9 else None,
            'kill_1': round_1.player_stats['ema'].kills if round_1 else None,
            'kill_2': round_2.player_stats['ema'].kills if round_2 else None,
            'kill_3': round_3.player_stats['ema'].kills if round_3 else None,
            'kill_4': round_4.player_stats['ema'].kills if round_4 else None,
            'kill_5': round_5.player_stats['ema'].kills if round_5 else None,
            'kill_6': round_6.player_stats['ema'].kills if round_6 else None,
            'kill_7': round_7.player_stats['ema'].kills if round_7 else None,
            'kill_8': round_8.player_stats['ema'].kills if round_8 else None,
            'kill_9': round_9.player_stats['ema'].kills if round_9 else None,
            'death_1': round_1.player_stats['ema'].deaths if round_1 else None,
        }
