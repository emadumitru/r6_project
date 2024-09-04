

class Site:
    def __init__(self, site_id, map_name, site_name, side):
        self.id = site_id
        self.map_name = map_name
        self.side = side
        self.name = site_name
        self.rounds = {}                                  # {round_id: Round}
        self.games_in_site = []                           # [game_id]
        self.statistics = self.initialize_statistics()

    def __str__(self):
        return f'{self.map_name} {self.name} {self.side} ({self.statistics["winperc"]} win% - {self.statistics["win"]}/{len(self.rounds)})'

    def add_round(self, round):
        self.rounds[round.id] = round
        if round.game_id not in self.games_in_site:
            self.games_in_site.append(round.game_id)
        self.update_statistics(round.win)

    def initialize_statistics(self):
        return {
            'win': 0,
            'winperc': 0
        }

    def update_statistics(self, round_win):
        self.statistics['win'] += 1 if round_win else 0
        self.statistics['winperc'] = round(self.statistics['win'] * 100 / len(self.rounds), 2)
