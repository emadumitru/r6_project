import streamlit as st
from backend.algo_statistics import *

def print_map_stats(rec):
    stats = get_weighten_stats(rec)
    ordered_stats = sorted(stats.items(), key=lambda x: x[1]['weighted_percentage'], reverse=True)
    ordered_stats = {name: stats for name, stats in ordered_stats}

    

    for name, stats in ordered_stats.items():
        st.write(f'{name}: {stats["games"]} games, {stats["wins"]} wins, {stats["normal_percentage"]} win%, {stats["weighted_percentage"]} weighted win%')


    st.write(ordered_stats)

def print_site_stats(rec, map_name):
    stat_sites = get_stats_sites(rec, map_name)

    st.write(f'Statistics for {map_name}')

    st.write(stat_sites)

    if stat_sites: # none if no info
        st.write(f'Attack ({stat_sites["Attack"]["Overall"]}%):')
        for site, dict in stat_sites["Attack"].items():
            if site != "Overall":
                st.write(f'{site} - {dict["wins"]} / {dict["rounds"]}')

    
