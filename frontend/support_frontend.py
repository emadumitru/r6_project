import streamlit as st
import datetime
import json
import os


def initialize_session_var():
    if "rounds" not in st.session_state:
        st.session_state["rounds"] = []
    if "name_sites" not in st.session_state:
        st.session_state["name_sites"] = []
    if "bans" not in st.session_state:
        st.session_state["bans"] = ["nothing"] * 4
    if "selected_map" not in st.session_state:
        st.session_state["selected_map"] = "Bank"
    if "selected_game_type" not in st.session_state:
        st.session_state["selected_game_type"] = "Standard"
    if "balance_random_opperators" not in st.session_state:
        st.session_state["balance_random_opperators"] = 50
    if "period_random_opperators" not in st.session_state:
        st.session_state["period_random_opperators"] = "All"
    if "season_periods" not in st.session_state:
        st.session_state["season_periods"] = {
            "All": (None, None),
            "Last Season": (datetime.date(2024, 4, 15), datetime.date(2024, 7, 15)),
            "2 seasons": (datetime.date(2024, 4, 15), None),
            "This season": (datetime.date(2024, 7, 15), None)
        }


def load_operators(json_path):
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            return json.load(f)
    else:
        st.error(f"File not found: {json_path}")
        return {}

def get_op_names():
    attackers_json_path = 'data/attackers.json'
    defenders_json_path = 'data/defenders.json'
    attackers = load_operators(attackers_json_path)
    defenders = load_operators(defenders_json_path)
    return list(attackers.keys()), list(defenders.keys())
