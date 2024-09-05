

def get_counts_maps(rec):
    """Function to get counts of maps"""
    counts = {}
    for name, map in rec.maps.items():
        counts[name] = {'games':len(map.games), 'wins':map.statistics['win']}
        counts[name]['normal_percentage'] = round(counts[name]['wins'] * 100 / counts[name]['games'], 2)
    return counts

def get_weighten_stats(rec):
    """Function to get weighted statistics of maps"""
    counts = get_counts_maps(rec)
    most_games = max([count['games'] for count in counts.values()])
    average_winperc = sum([count['wins'] for count in counts.values()]) / sum([count['games'] for count in counts.values()])
    for name, dict in counts.items():
        normal_part = dict['wins']
        missing_games = most_games - dict['games']
        missing_part = average_winperc * missing_games
        dict['weighted_percentage'] = round((normal_part + missing_part) * 100 / most_games, 2)

    return counts
