from class_site import Site

class Rmap:
    def __init__(self, map_name, site_names):
        self.name = map_name
        self.sites = {}
        self.initialize_sites(site_names)
        self.rounds = {}
        self.games = {}
        self.statistics = {'win': 0, 'winperc': 0}

    def __repr__(self):
        return f'{self.name} ({self.statistics["winperc"]} win% - {self.statistics["win"]}/{len(self.games)})'
    
    def __repr__(self):
        return f'{self.name} ({self.statistics["winperc"]} win% - {self.statistics["win"]}/{len(self.games)})'

    def initialize_sites(self, site_names):
        sides = ['attack', 'defense']
        for site_name in site_names:
            for side in sides:
                site_id = f'{site_name}_{side}'
                self.sites[site_id] = Site(site_id, self.name, site_name, side)

    def update_map(self, game):
        self.games[game.id] = game
        for round in game.rounds.values():
            self.rounds[round.id] = round
            site_name = f'{round.site}_{round.side}'
            if site_name not in self.sites:
                self.initialize_sites([round.site])
            self.sites[site_name].add_round(round)
        self.update_statistics(game.win)
    
    def update_statistics(self, game_win):
        self.statistics['win'] += 1 if game_win else 0
        self.statistics['winperc'] = round(self.statistics['win'] * 100 / len(self.games), 2)
        