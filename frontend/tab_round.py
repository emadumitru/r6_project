import streamlit as st
import json
import os
from st_clickable_images import clickable_images
from copy import deepcopy  # Import deepcopy


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
    """Initialize session state variables if not already set."""
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
        st.session_state["name_sites"] = ["Site 1", "Site 2", "Site 3", "Site 4"]
    if "current_side" not in st.session_state:
        st.session_state["current_side"] = None  # To track the side change

# Function to display operator selection using clickable images
def display_operator_selection(player_name, operators_dict):
    st.subheader(f"{player_name}'s Round")
    st.write("##### Operator")

    # Ensure unique session state for each player's operator based on side
    if f"{player_name}_selected_operator" not in st.session_state:
        st.session_state[f"{player_name}_selected_operator"] = None

    operator_names = list(operators_dict.keys())
    images = [operators_dict[name] for name in operator_names]

    # Display clickable images for the current player only
    clicked = clickable_images(
        images,
        titles=operator_names,
        div_style={
            "display": "flex",
            "justify-content": "left",
            "flex-wrap": "wrap",
            "gap": "auto"
        },
        img_style={
            "flex": "1 0 14.28%",
            "max-width": "14.28%",
            "height": "auto",
            "cursor": "pointer"
        },
        key=f"{player_name}_clickable_images_{st.session_state['current_side']}"  # Ensure unique key per player/side
    )

    # Update session state based on clicked image
    if clicked > -1:
        selected_operator = operator_names[clicked]
        st.session_state[f"{player_name}_selected_operator"] = selected_operator
        st.session_state["current_round"]["players"][player_name]["operator"] = selected_operator

    # Display the selected operator
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
        f"Did {player_name} get the first kill?", value=st.session_state["current_round"]["players"][player_name]["entryfrag"],
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
    round = st.session_state['current_round']
    st.write(f'**Round {len(st.session_state.rounds)+1}**: {round["site"]} - {round["side"]} - {"Win" if round["win"] else "Loss"} - {round["endcondition"]}')
    ema = round["players"]["Ema"]
    mihnea = round["players"]["Mihnea"]

    # Using icons for True/False values
    def icon(value):
        return "✅" if value else "❌"

    # Display player data in a nicely formatted table
    st.markdown(
        """
        | **Player** | **Operator** | **Kills** | **Assists** | **Survived** | **EntryFrag** | **Diffuser** | **Clutch** | **TKills** | **TDeaths** | **TAssists** |
        |------------|-------------------|-----------|-------------|---------------|----------------|--------------|------------|-|-|-|
        | **Ema**    | {ema_operator} | {ema_kills} | {ema_assists} | {ema_surv} | {ema_ef} | {ema_dif} | {ema_cl} | {ema_tkills} | {ema_tdeaths} | {ema_tassists} |
        | **Mihnea** | {mihnea_operator} | {mihnea_kills} | {mihnea_assists} | {mihnea_surv} | {mihnea_ef} | {mihnea_dif} | {mihnea_cl} | {mihnea_tkills} | {mihnea_tdeaths} | {mihnea_tassists} |
        """.format(
            ema_operator=ema["operator"],
            ema_kills=ema["kills"],
            ema_assists=ema["assists"],
            ema_surv=icon(ema["survived"]),
            ema_ef=icon(ema["entryfrag"]),
            ema_dif=icon(ema["diffuser"]),
            ema_cl=icon(ema["clutch"]),
            ema_tkills=ema["kills"]+sum([int(r["players"]["Ema"]["kills"]) for r in st.session_state["rounds"]]),
            ema_tdeaths=(not ema["survived"])+(sum([(not r["players"]["Ema"]["survived"]) for r in st.session_state["rounds"]])),
            ema_tassists=ema["assists"]+sum([int(r["players"]["Ema"]["assists"]) for r in st.session_state["rounds"]]),
            mihnea_operator=mihnea["operator"],
            mihnea_kills=mihnea["kills"],
            mihnea_assists=mihnea["assists"],
            mihnea_surv=icon(mihnea["survived"]),
            mihnea_ef=icon(mihnea["entryfrag"]),
            mihnea_dif=icon(mihnea["diffuser"]),
            mihnea_cl=icon(mihnea["clutch"]),
            mihnea_tkills=mihnea["kills"]+sum([int(r["players"]["Mihnea"]["kills"]) for r in st.session_state["rounds"]]),
            mihnea_tdeaths=(not mihnea["survived"])+(sum([(not r["players"]["Mihnea"]["survived"]) for r in st.session_state["rounds"]])),
            mihnea_tassists=mihnea["assists"]+sum([int(r["players"]["Mihnea"]["assists"]) for r in st.session_state["rounds"]])
        )
    )
    len_rounds = len(st.session_state['rounds']) + 1
    score_us = len([round for round in st.session_state['rounds'] if round['win']]) + round['win']
    score_op = len_rounds - score_us
    st.write(f'Current score: {score_us} - {score_op}')

def add_new_round():
    # Initialize session state for rounds
    initialize_session_state()

    st.write(f"#### Round {len(st.session_state['rounds']) + 1}")

    # Side selection, updating only if a change is detected to prevent re-renders
    col1, col2 = st.columns(2)
    with col1:
        selected_side = st.radio("Side", ["Attack", "Defense"], key="side", horizontal=True)
        st.session_state["current_round"]["side"] = selected_side

        # Only change the side if it's different from the previous one
        if "current_side" not in st.session_state or st.session_state["current_side"] != selected_side:
            st.session_state["current_side"] = selected_side
            # Reset the selected operators for the current side to prevent double loading
            st.session_state["Ema_selected_operator"] = None
            st.session_state["Mihnea_selected_operator"] = None

            st.write(f"Side changed to {selected_side}. Operators reset.")
        else:
            st.write(f"Side unchanged. Current side: {st.session_state['current_side']}")

    # Result and End Condition
    with col2:
        st.session_state["current_round"]["win"] = st.radio(
            "Result", ["Win", "Loss"], key="round_result", horizontal=True) == "Win"
    st.session_state["current_round"]["endcondition"] = st.radio(
        "End Condition", ["Time Expired", "Wiped Out", "Defused"], key="end_condition", horizontal=True)

    # Load the correct operator dictionary based on the current side
    if selected_side == "Attack":
        operator_dict = attackers
        st.write("Attackers loaded for operator selection.")
    else:
        operator_dict = defenders
        st.write("Defenders loaded for operator selection.")

    # Create columns for Ema and Mihnea operator selection
    col1, col2 = st.columns(2)
    
    # Ema's column
    with col1:
        # st.write(f"Displaying Ema's Selection for **{selected_side}**")
        display_operator_selection("Ema", operator_dict)

    # Mihnea's column
    with col2:
        # st.write(f"Displaying Mihnea's Selection for **{selected_side}**")
        display_operator_selection("Mihnea", operator_dict)

    # Print round overview and add submit button
    st.divider()
    print_round_overview()

    if st.button("Submit Round Data", key=f"submit_newround_{len(st.session_state['rounds'])}"):
        st.session_state["rounds"].append(deepcopy(st.session_state["current_round"]))
        st.success("Round data submitted successfully!")
        initialize_session_state()  # Re-initialize for the next round

    