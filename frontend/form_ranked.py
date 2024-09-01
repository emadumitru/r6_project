import streamlit as st
import json
import os
from st_clickable_images import clickable_images

def add_space(spaces):
    for _ in range(spaces):
        st.write("")

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

# Function to display operator selection using clickable images
def display_operator_selection(player_name, operators_dict):
    st.subheader(f"{player_name}'s Round")

    st.write("##### Operator")
    # Initialize selected operator with a default value if not set
    if f"{player_name}_selected_operator" not in st.session_state:
        st.session_state[f"{player_name}_selected_operator"] = None

    # Prepare image paths for clickable images
    operator_names = list(operators_dict.keys())

    images = [operators_dict[name] for name in operator_names]
    
    # Display clickable images and get the index of the clicked image
    clicked = clickable_images(
        images,
        titles=operator_names,
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "3px", "height": "75px", "cursor": "pointer"},
        key=f"{player_name}_clickable_images",
    )

    # Update session state if an image is clicked
    if clicked > -1:
        selected_operator = operator_names[clicked]
        st.session_state[f"{player_name}_selected_operator"] = selected_operator

    # Show the currently selected operator
    selected_operator = st.session_state[f"{player_name}_selected_operator"]
    if selected_operator:
        st.write(f"Selected Operator: **{selected_operator}**")

    st.divider()
    st.write("##### Performance")
    
    # Kills section
    kills = st.select_slider(f"{player_name}'s Kills", list(range(6)))

    # Survived section
    survived = st.checkbox(f"Did {player_name} Survive?")

    return {
        "operator": selected_operator,
        "kills": kills,
        "survived": survived == "Yes",
    }

def ranked_input_form():
    # Sidebar configuration (optional if you want a different setup)
    st.sidebar.header("Round Data Input")

    # Main input form
    st.header("Input Round Data")
    
    col1, col2 = st.columns(2)

    with col1:
        # Side Selection
        side = st.radio("Side", ["Attack", "Defense"], horizontal=True)

        # Round Win/Loss
        round_win = st.radio("Round Result", ["Win", "Lose"],horizontal=True)

    with col2:
        # End Condition
        end_condition = st.radio(
            "End Condition", ["Timed Out", "Wiped Out", "Defused"], horizontal=True
        )

        # Site played
        sites = ["Site 1", "Site 2", "Site 3", "Site 4"]
        site_played = st.radio("Site Played", sites, horizontal=True)
        
    st.divider()

    # Use the appropriate dictionary based on the selected side
    if side == "Attack":
        operator_dict = attackers
    else:
        operator_dict = defenders

    # Input sections for Ema and Mihnea using the loaded dictionaries
    col1, col2 = st.columns(2)
    with col1:
        ema_data = display_operator_selection("Ema", operator_dict)
    with col2:
        mihnea_data = display_operator_selection("Mihnea", operator_dict)
    
    add_space(2)
    
    # Submit Button
    if st.button("Submit Round Data"):
        st.write("### Round Summary")
        col1, col2 = st.columns(2)
        
        with col1:

            # Display submitted data (for testing purposes)
            
            st.write(f"**Side:** {side}")
            st.write(f"**Round Result:** {round_win}")
            
            st.write("#### Ema's Performance")
            st.write(f"Operator: {ema_data['operator']}")
            st.write(f"Kills: {ema_data['kills']}")
            st.write(f"Survived: {ema_data['survived']}")
            
        with col2:
            st.write(f"**End Condition:** {end_condition}")
            st.write(f"**Site Played:** {site_played}")

            

            st.write("#### Mihnea's Performance")
            st.write(f"Operator: {mihnea_data['operator']}")
            st.write(f"Kills: {mihnea_data['kills']}")
            st.write(f"Survived: {mihnea_data['survived']}")

        # Logic to save the data goes here
        st.success("Round data submitted successfully!")