import streamlit as st

# Define lists for the dropdown menus
maps = [
    "Bank", "Border", "Chalet", "Clubhouse", "Coastline", 
    "Consulate", "Favela", "Hereford Base", 
    "House", "Kafe Dostoyevsky", "Kanal", "Oregon", 
    "Outback", "Plane", "Skyscraper", "Theme Park", "Tower", 
    "Villa", "Yacht", "Emerald Plains", "Nighthaven Labs",
    "Lair", "Stadium"
]

game_types = ["Standard", "Ranked"]
sides = ["Attack", "Defense"]

# Set up the main title
st.title("Rainbow 6 Siege Match Tracker")

# Sidebar Configuration
st.sidebar.header("Match Settings")
selected_map = st.sidebar.selectbox("Select Map", maps)
selected_game_type = st.sidebar.radio("Game Type", game_types)
selected_side = st.sidebar.radio("Starting Side", sides)

# Main page content
st.write(f"### Selected Match Settings")
st.write(f"**Map:** {selected_map}")
st.write(f"**Game Type:** {selected_game_type}")
st.write(f"**Starting Side:** {selected_side}")

st.write(
    """
    Use the sidebar to configure the match settings. 
    Once you have selected your map, game type, and starting side, 
    you can begin tracking your matches.
    """
)
