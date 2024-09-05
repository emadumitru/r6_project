import streamlit as st
from backend.algo_statistics import *

def print_map_stats(rec):
    stats = get_weighten_stats(rec)
    ordered_stats = sorted(stats.items(), key=lambda x: x[1]['weighted_percentage'], reverse=True)
    
    ordered_stats = {name: stats for name, stats in ordered_stats}

    st.write(ordered_stats)

    for name, stats in ordered_stats.items():
        st.write(f'{name}: {stats["games"]} games, {stats["wins"]} wins, {stats["normal_percentage"]} win%, {stats["weighted_percentage"]} weighted win%')