

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
    for _, dict in counts.items():
        normal_part = dict['wins']
        missing_games = most_games - dict['games']
        missing_part = average_winperc * missing_games
        dict['weighted_percentage'] = round((normal_part + missing_part) * 100 / most_games, 2)

    return counts

def get_counts_sites(map):
    """Function to get counts of sites"""
    counts = {'Attack':{}, 'Defense':{}}
    for name, site in map.sites["Attack"].items():
        counts['Attack'][name] = {'rounds':len(site.rounds), 'wins':site.statistics['win']}
        counts['Attack'][name]['normal_percentage'] = round(counts['Attack'][name]['wins'] * 100 / max(counts['Attack'][name]['rounds'], 1), 2)
    for name, site in map.sites["Defense"].items():
        counts['Defense'][name] = {'rounds':len(site.rounds), 'wins':site.statistics['win']}
        counts['Defense'][name]['normal_percentage'] = round(counts['Defense'][name]['wins'] * 100 /  max(counts['Defense'][name]['rounds'], 1), 2)
    return counts

def get_weighten_stats_sites(map):
    """Function to get weighted statistics of sites"""
    counts = get_counts_sites(map)
    most_rounds_attack = max([count['rounds'] for count in counts['Attack'].values()]) 
    most_rounds_defense = max([count['rounds'] for count in counts['Defense'].values()])
    average_winperc_attack = sum([count['wins'] for count in counts['Attack'].values()]) / sum([count['rounds'] for count in counts['Attack'].values()])
    average_winperc_defense = sum([count['wins'] for count in counts['Defense'].values()]) / sum([count['rounds'] for count in counts['Defense'].values()])

    for _, dict in counts['Attack'].items():
        normal_part = dict['wins']
        missing_rounds = most_rounds_attack - dict['rounds']
        missing_part = average_winperc_attack * missing_rounds
        dict['weighted_percentage'] = round((normal_part + missing_part) * 100 / most_rounds_attack, 2)

    for _, dict in counts['Defense'].items():
        normal_part = dict['wins']
        missing_rounds = most_rounds_defense - dict['rounds']
        missing_part = average_winperc_defense * missing_rounds
        dict['weighted_percentage'] = round((normal_part + missing_part) * 100 / most_rounds_defense, 2)

    counts['Attack']['Overall'] = round(average_winperc_attack*100, 2)
    counts['Defense']['Overall'] = round(average_winperc_defense*100, 2)

    return counts

def get_stats_sites(rec, map_name):
    """Function to get statistics of sites"""
    if map_name not in rec.maps:
        return None
    map = rec.maps[map_name]
    counts = get_weighten_stats_sites(map)
    return counts