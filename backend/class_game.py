from class_round import Round

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

