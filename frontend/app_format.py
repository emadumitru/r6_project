import streamlit as st

def recommender_format(opperators):

    
    # Define lists for the dropdown menus
    maps = [
        "Bank", "Border", "Chalet", "Clubhouse", "Coastline", 
        "Consulate", "Favela", "Hereford Base", 
        "House", "Kafe Dostoyevsky", "Kanal", "Oregon", 
        "Outback", "Plane", "Skyscraper", "Theme Park", "Tower", 
        "Villa", "Yacht", "Emerald Plains", "Nighthaven Labs",
        "Lair", "Stadium"
    ]

    game_types = ["Standard", "Ranked", "Quick"]
    sides = ["Attack", "Defense"]

    attackers, defenders = opperators

    # Set up the main title
    st.title("Rainbow 6 Siege Match Tracker")

    if "rounds" not in st.session_state:
        st.session_state["rounds"] = []

    # Sidebar Configuration
    st.sidebar.header("Match Settings")
    st.session_state.selected_map = st.sidebar.selectbox("Select Map", maps, key="map_sidebar")
    st.session_state.selected_game_type = st.sidebar.radio("Game Type", game_types, key="game_type_sidebar", horizontal=True)
    selected_side = st.sidebar.radio("Starting Side", sides, key="side_sidebar", horizontal=True)
    get_random_opperators = st.sidebar.checkbox("Get Random Opperators", key="get_random_opperators")
    get_recommendations = st.sidebar.checkbox("Get Recommendations", key="get_recommendations")
    submit_game = st.sidebar.button("Submit Match", key="submit_game")
    reset_game = st.sidebar.button("Reset Match", key="reset_game")

    if st.session_state.selected_game_type == "Ranked":
        st.sidebar.header("Bans")
        selected_a_us = st.sidebar.selectbox(f"Attacker us", attackers, key=f"ban_attacker_us")
        selected_a_op = st.sidebar.selectbox(f"Attacker op", attackers, key=f"ban_attacker_op")
        selected_d_us = st.sidebar.selectbox(f"Defender us", defenders, key=f"ban_defender_us")
        selected_d_op = st.sidebar.selectbox(f"Defender op", defenders, key=f"ban_defender_op")
        st.session_state.bans = [selected_a_us, selected_a_op, selected_d_us, selected_d_op]

    if get_random_opperators:
        st.sidebar.header("Random Opperators")
        # get balancing percentage
        st.session_state.balance_random_opperators = st.sidebar.slider("Balance (random - play#)", 0, 100, 50, 5)
        st.session_state.period_random_opperators = st.sidebar.select_slider("Period", options=["All", "Last Season", "2 seasons", "This season"], key="timeline_random_opperators")

    if get_recommendations:
        st.sidebar.header("Recommendations")
        # get balancing 
        
    

    # Main page content
    # st.write(f"##### Selected Match Settings")
    st.write(f"Playing a **{st.session_state.selected_game_type}** game on **{st.session_state.selected_map}**.")
    # st.write(f"**Game Type:** {selected_game_type}")
    # st.write(f"**Starting Side:** {selected_side}")

    return selected_side, get_random_opperators, get_recommendations, submit_game, reset_game