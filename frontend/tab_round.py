import streamlit as st
import json
import os
from st_clickable_images import clickable_images

# Paths to the JSON files containing attacker and defender data
attackers_json_path = 'data/attackers.json'
defenders_json_path = 'data/defenders.json'

# Function to load operators from JSON files
def load_operators(json_path):
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            return json.load(f)
    else:
        st.error(f"File not found: {json_path}")
        return {}

# Load attacker and defender operators from JSON files
attackers = load_operators(attackers_json_path)
defenders = load_operators(defenders_json_path)

# Function to initialize session state for rounds if not already set
def initialize_session_state():
    if "rounds" not in st.session_state:
        st.session_state["rounds"] = []
    if "current_round" not in st.session_state:
        st.session_state["current_round"] = {
            "site": "",
            "side": "",
            "win": False,
            "endcondition": "",
            "players": {
                "Ema": {
                    "operator": None,
                    "kills": 0,
                    "assists": 0,
                    "survived": False,
                    "entryfrag": False,
                    "diffuser": False,
                    "clutch": False,
                },
                "Mihnea": {
                    "operator": None,
                    "kills": 0,
                    "assists": 0,
                    "survived": False,
                    "entryfrag": False,
                    "diffuser": False,
                    "clutch": False,
                }
            }
        }
    if "name_sites" not in st.session_state:
        # Initialize name_sites with some default values if not already set
        st.session_state["name_sites"] = ["Site 1", "Site 2", "Site 3", "Site 4"]

# Function to display operator selection using clickable images
def display_operator_selection(player_name, operators_dict):
    st.subheader(f"{player_name}'s Round")
    st.write("##### Operator")

    if f"{player_name}_selected_operator" not in st.session_state:
        st.session_state[f"{player_name}_selected_operator"] = None

    # Prepare operator names and images
    operator_names = list(operators_dict.keys())
    images = [operators_dict[name] for name in operator_names]

    # Display clickable images and get the index of the clicked image
    clicked = clickable_images(
        images,
        titles=operator_names,
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "3px", "height": "75px", "cursor": "pointer"},
        key=f"{player_name}_newround_clickable_images",
    )

    # Update session state if an image is clicked
    if clicked > -1:
        selected_operator = operator_names[clicked]
        st.session_state[f"{player_name}_selected_operator"] = selected_operator
        st.session_state["current_round"]["players"][player_name]["operator"] = selected_operator

    # Show the currently selected operator
    selected_operator = st.session_state[f"{player_name}_selected_operator"]
    if selected_operator:
        st.write(f"Selected Operator: **{selected_operator}**")

    st.divider()
    st.write("##### Performance")

    # Collecting player performance metrics, initializing to None if not already set
    st.session_state["current_round"]["players"][player_name]["kills"] = st.select_slider(
        f"{player_name}'s Kills", list(range(6)), value=st.session_state["current_round"]["players"][player_name]["kills"],
        key=f"{player_name}_newround_kills_slider"
    )

    st.session_state["current_round"]["players"][player_name]["assists"] = st.select_slider(
        f"{player_name}'s Assists", list(range(6)), value=st.session_state["current_round"]["players"][player_name]["assists"],
        key=f"{player_name}_newround_assists_slider"
    )

    st.session_state["current_round"]["players"][player_name]["survived"] = st.checkbox(
        f"Did {player_name} Survive?", value=st.session_state["current_round"]["players"][player_name]["survived"],
        key=f"{player_name}_newround_survived_checkbox"
    )

    st.session_state["current_round"]["players"][player_name]["entryfrag"] = st.checkbox(
        f"Did {player_name} get/was the first kill?", value=st.session_state["current_round"]["players"][player_name]["entryfrag"],
        key=f"{player_name}_newround_entryfrag_checkbox"
    )

    st.session_state["current_round"]["players"][player_name]["diffuser"] = st.checkbox(
        f"Did {player_name} plant/defuse the diffuser?", value=st.session_state["current_round"]["players"][player_name]["diffuser"],
        key=f"{player_name}_newround_diffuser_checkbox"
    )

    st.session_state["current_round"]["players"][player_name]["clutch"] = st.checkbox(
        f"Did {player_name} clutch the round?", value=st.session_state["current_round"]["players"][player_name]["clutch"],
        key=f"{player_name}_newround_clutch_checkbox"
    )

def print_round_overview():
    # Display summary of the submitted round
        st.write("### Round Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"{st.session_state['current_round']['site']}")
        with col2:
            st.write(f"{st.session_state['current_round']['side']}")
        with col3:
            st.write(f"{'Win' if st.session_state['current_round']['win'] else 'Loss'}")
        with col4:
            st.write(f"{st.session_state['current_round']['endcondition']}")


        # Display players' performance summaries
        col1, col2 = st.columns(2)
        with col1:
            player = "Ema"
            st.write(f"#### {player}'s Performance")
            player_data = st.session_state["current_round"]["players"][player]
            st.write(f"Operator: {player_data['operator']}")
            st.write(f"Kills: {player_data['kills']}")
            st.write(f"Assists: {player_data['assists']}")
            st.write(f"Survived: {'✅' if player_data['survived'] else '❌'}")
            st.write(f"Entry Frag: {'✅' if player_data['entryfrag'] else '❌'}")
            st.write(f"Diffuser: {'✅' if player_data['diffuser'] else '❌'}")
            st.write(f"Clutch: {'✅' if player_data['clutch'] else '❌'}")
        with col2:
            player = "Mihnea"
            st.write(f"#### {player}'s Performance")
            player_data = st.session_state["current_round"]["players"][player]
            st.write(f"Operator: {player_data['operator']}")
            st.write(f"Kills: {player_data['kills']}")
            st.write(f"Assists: {player_data['assists']}")
            st.write(f"Survived: {'✅' if player_data['survived'] else '❌'}")
            st.write(f"Entry Frag: {'✅' if player_data['entryfrag'] else '❌'}")
            st.write(f"Diffuser: {'✅' if player_data['diffuser'] else '❌'}")
            st.write(f"Clutch: {'✅' if player_data['clutch'] else '❌'}")

# Function to add a new round form
def add_new_round():

    # Initialize session state for rounds
    initialize_session_state()


    # Round Information with Side and Result side by side
    st.subheader(f"Round {len(st.session_state.rounds)+1} Information")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state["current_round"]["side"] = st.radio("Side", ["Attack", "Defense"], key="side", horizontal=True)
    with col2:
        st.session_state["current_round"]["win"] = st.radio("Result", ["Win", "Loss"], key="round_result", horizontal=True) == "Win"
    st.session_state["current_round"]["endcondition"] = st.radio(
        "End Condition", ["Time Expired", "Wiped Out", "Defused"], key="end_condition", horizontal=True)
    # Display site options from session state
    site_options = st.session_state["name_sites"][:]
    if len(site_options) == 4:
        st.session_state["current_round"]["site"] = st.radio(
        "Site", site_options, key="site_full", horizontal=True)
    else:
        col1, col2 = st.columns([len(site_options)/2, 1])
        with col1:
            st.session_state["current_round"]["site"] = st.radio(
            "Site", site_options + ['Other'], key="site_nonfull", horizontal=True)
        with col2:
            new_option_site = st.text_input("New Site", key="new_site")

    if st.session_state["current_round"]["site"] == 'Other':
        if new_option_site:
            st.session_state["name_sites"].append(new_option_site)
            st.session_state["current_round"]["site"] = new_option_site

    st.divider()

    # Use the appropriate operator dictionary based on the selected side
    operator_dict = attackers if st.session_state["current_round"]["side"] == "Attack" else defenders

    # Display operator selection and performance input for each player
    col1, col2 = st.columns(2)
    with col1:
        display_operator_selection("Ema", operator_dict)
    with col2:
        display_operator_selection("Mihnea", operator_dict)

    st.divider()

    print_round_overview()

    # Add button to submit the current round data
    if st.button("Submit Round Data", key=f"submit_newround_{len(st.session_state['rounds'])}"):
        st.session_state["rounds"].append(st.session_state["current_round"])
        st.success("Round data submitted successfully!")

        # Reset the current round data for new input
        initialize_session_state()