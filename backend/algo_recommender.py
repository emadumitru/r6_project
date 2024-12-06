import random
from collections import defaultdict
import math

attack_operators = ['Blitz', 'Jackal', 'Iq', 'Thatcher', 'Nokk', 'Nomad', 'Striker', 'Thermite', 'Dokkaebi', 'Hibana', 'Ace', 'Blackbeard', 'Lion', 'Iana', 'Ash', 'Grim', 'Buck', 'Sledge', 'Fuze', 'Capitao', 'Ying', 'Zofia', 'Brava', 'Amaru', 'Gridlock', 'Maverick', 'Osa', 'Zero', 'Sens', 'Flores', 'Deimos', 'Montagne', 'Kali', 'Twitch', 'Glaz', 'Finka']
defense_operators = ['Thunderbird', 'Maestro', 'Tachanka', 'Warden', 'Melusi', 'Wamai', 'Mira', 'Kaid', 'Frost', 'Rook', 'Oryx', 'Mozzie', 'Jager', 'Echo', 'Vigil', 'Valkyrie', 'Kapkan', 'Sentry', 'Bandit', 'Lesion', 'Fenrir', 'Doc', 'Smoke', 'Azami', 'Castle', 'Caveira', 'Pulse', 'Aruni', 'Goyo', 'Mute', 'Solis', 'Tubarao', 'Thorn', 'Ela', 'Alibi', 'Clash', 'Skopos']



class OperatorRecommender:
    def __init__(self, rec, period_start, map_name):
        self.rec = rec
        self.period_start = period_start
        self.map_name = map_name
        self.rounds = self.get_rounds()
        self.total_rounds_map_attack = len([r for r in self.rounds if r.side == 'Attack'])
        self.total_rounds_map_defense = len([r for r in self.rounds if r.side == 'Defense'])
        self.player_operator_stats = {'ema': self.collect_operator_stats('ema'), 'mihnea': self.collect_operator_stats('mihnea')}
        self.site_specific_stats = self.collect_site_specific_stats()

    def get_rounds(self):
        rounds = []
        for _ in self.rec.maps[self.map_name].games.values():
            for round in self.rec.maps[self.map_name].rounds.values():
                if self.period_start is None:
                    rounds.append(round)
                elif (round.date not in [None, 'None', '']) and (round.date >= self.period_start):
                    rounds.append(round)
                        
        return rounds

    def collect_operator_stats(self, player_name):
        stats = defaultdict(lambda: {'kills': 0, 'assists': 0, 'defuses': 0, 'wins': 0, 'losses': 0, 'plays': 0})
        for round in self.rounds:
            player_stats = round.player_stats.get(player_name)
            if player_stats:
                operator = player_stats.opperator
                # make teh firts letetr a capital letter
                operator = operator.capitalize()
                if operator in attack_operators or operator in defense_operators:
                    stats[operator]['kills'] += player_stats.kills or 0
                    stats[operator]['assists'] += player_stats.assists or 0
                    stats[operator]['defuses'] += 1 if player_stats.diffuser else 0
                    if round.win:
                        stats[operator]['wins'] += 1
                    else:
                        stats[operator]['losses'] += 1
                    stats[operator]['plays'] += 1
        return stats

    def collect_site_specific_stats(self):
        site_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {'kills': 0, 'assists': 0, 'defuses': 0, 'wins': 0, 'losses': 0, 'plays': 0})))
        for round in self.rounds:
            site_name = round.site
            side = round.side
            if side == 'Attack':
                operator_list = attack_operators
            elif side == 'Defense':
                operator_list = defense_operators
            else:
                print("help that is not how side looks", side)
                operator_list = []
            for player, player_stats in round.player_stats.items():
                operator = player_stats.opperator
                if operator in operator_list:
                    site_stats[site_name].setdefault(round.side, {}).setdefault(player, {}).setdefault(operator, {'kills': 0, 'assists': 0, 'defuses': 0, 'wins': 0, 'losses': 0, 'plays': 0})
                    site_stats[site_name][round.side][player][operator]['kills'] += player_stats.kills or 0
                    site_stats[site_name][round.side][player][operator]['assists'] += player_stats.assists or 0
                    site_stats[site_name][round.side][player][operator]['defuses'] += 1 if player_stats.diffuser else 0
                    if round.win:
                        site_stats[site_name][round.side][player][operator]['wins'] += 1
                    else:
                        site_stats[site_name][round.side][player][operator]['losses'] += 1
                    site_stats[site_name][round.side][player][operator]['plays'] += 1
        return site_stats

    def compute_operator_score(self, operator_stats, site_stats=None, total_rounds_site=None, side=None):
        # Score calculation based on the operator's performance
        # A higher weight is assigned to kills, defuses compared to just winning
        win_rate = operator_stats['wins'] / (operator_stats['plays'] + 1e-9)
        avg_kills = operator_stats['kills'] / (operator_stats['plays'] + 1e-9)
        avg_assists = operator_stats['assists'] / (operator_stats['plays'] + 1e-9)
        avg_defuses = operator_stats['defuses'] / (operator_stats['plays'] + 1e-9)

        site_weight = 1
        if site_stats:
            site_win_rate = site_stats['wins'] / (site_stats['plays'] + 1e-9)
            site_avg_kills = site_stats['kills'] / (site_stats['plays'] + 1e-9)
            site_avg_assists = site_stats['assists'] / (site_stats['plays'] + 1e-9)
            site_avg_defuses = site_stats['defuses'] / (site_stats['plays'] + 1e-9)

            site_weight = (site_avg_kills * 3) + (site_avg_assists * 1.5) + (site_avg_defuses * 4) + (site_win_rate * 2)

        base_score = ((avg_kills * 3) + (avg_assists * 1.5) + (avg_defuses * 4) + (win_rate * 2)) * site_weight

        # Calculate play rates for the specific side (Attack or Defense)
        if side == 'Attack':
            total_rounds_map = self.total_rounds_map_attack
        elif side == 'Defense':
            total_rounds_map = self.total_rounds_map_defense
        else:
            total_rounds_map = 1  # To avoid division by zero

        play_rate_map = operator_stats['plays'] / (total_rounds_map + 1e-9)
        play_rate_site = (site_stats['plays'] if site_stats else 0) / (total_rounds_site + 1e-9 if total_rounds_site else 1e-9)

        # Calculate confidence weights using play rates
        map_confidence = math.log(1 + play_rate_map)
        site_confidence = math.log(1 + play_rate_site)

        # Combined confidence weight (you can also take the average if you prefer)
        combined_confidence = (map_confidence + site_confidence) / 2

        # Final score, with α as a tunable parameter to control the influence of confidence
        alpha = 0.5  # You can adjust this value to control how much confidence affects the score
        final_score = base_score * (1 + alpha * combined_confidence)

        return final_score, play_rate_site, play_rate_map, combined_confidence

    def rank_operators(self, site_name, player, side):
        operator_scores = {}
        player_stats = self.player_operator_stats[player]
        total_rounds_site = sum([player_stats['plays'] for player_stats in self.site_specific_stats[site_name][side].get(player, {}).values()])
        for operator, stats in player_stats.items():
            site_stats = self.site_specific_stats[site_name][side].get(player, {}).get(operator, None)
            score, play_rate_site, play_rate_map, combined_confidence = self.compute_operator_score(stats, site_stats, total_rounds_site, side)
            operator_scores[operator] = {
                'score': score,
                'play_rate_site': play_rate_site,
                'play_rate_map': play_rate_map,
                'combined_confidence': combined_confidence
            }
        # Sort operators by their computed score in descending order
        ranked_operators = sorted(operator_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        return ranked_operators

    def get_top_operators_for_site(self, site_name, side, player, op_count):
        ranked_operators = self.rank_operators(site_name, player, side)
        side_operators = attack_operators if side == 'Attack' else defense_operators
        # Filter the ranked operators by side and return the top op_count along with their scores and additional info
        top_operators = [(op, info) for op, info in ranked_operators if op in side_operators][:op_count]
        return top_operators

def algo_get_recom(rec, period_start, map_name, op_count):
    recommender = OperatorRecommender(rec, period_start, map_name)
    site_recommendations = {}
    map_instance = rec.maps[map_name]

    for side in ['Attack', 'Defense']:
        site_recommendations[side] = {}
        for site_name, site in map_instance.sites[side].items():
            site_recommendations[side][site_name] = {
                'ema': recommender.get_top_operators_for_site(site_name, side, 'ema', op_count),
                'mihnea': recommender.get_top_operators_for_site(site_name, side, 'mihnea', op_count)
            }

    return site_recommendations, map_name, period_start, recommender.rounds