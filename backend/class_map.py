from backend.class_site import Site

class Rmap:
    def __init__(self, map_name, site_names):
        self.name = map_name
        self.sites = {'Attack': {}, 'Defense': {}}
        self.initialize_sites(site_names)
        self.games = {}
        self.rounds = {}
        self.statistics = {'win': 0, 'winperc': 0}

    def __repr__(self):
        return f'{self.name} ({self.statistics["winperc"]} win% - {self.statistics["win"]}/{len(self.games)})'
    
    def __repr__(self):
        return f'{self.name} ({self.statistics["winperc"]} win% - {self.statistics["win"]}/{len(self.games)})'

    def initialize_sites(self, site_names):
        for site_name in site_names:
            self.sites["Attack"][site_name] = Site(site_name, self.name, site_name, "Attack")
            self.sites["Defense"][site_name] = Site(site_name, self.name, site_name, "Defense")

    def update_map(self, game, rounds):
        self.games[game.id] = game
        for round in rounds:
            if round.site not in self.sites[round.side]:
                self.initialize_sites([round.site])
            self.sites[round.side][round.site].add_round(round)
            self.rounds[round.id] = round
        self.update_statistics(game.win)
    
    def update_statistics(self, game_win):
        self.statistics['win'] += 1 if game_win else 0
        self.statistics['winperc'] = round(self.statistics['win'] * 100 / len(self.games), 2)

    def to_csv(self):
        list_of_game_dicts = []
        for game in self.games.values():
            game_dict = game.csv_line()
            list_of_rounds = game.round_ids
            for round_id in list_of_rounds:
                if round_id in self.rounds.keys():
                    round_dict = self.rounds[round_id].csv_line()
                    game_dict.update(round_dict)
                else:
                    print(f'Round with id {round_id} not found in map {self.name}')
            list_of_game_dicts.append(game_dict)
        return list_of_game_dicts
        