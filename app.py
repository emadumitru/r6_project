import streamlit as st
# Set page configuration to use the full width of the screen
st.set_page_config(page_title="R6 Siege Tracker", layout="wide")

from frontend.app_format import *
from frontend.tab_round import *
from frontend.tab_summary import *
from frontend.support_frontend import *
from backend.support_backfront import *


initialize_session_var()
opperators = get_op_names()

game_choices = recommender_format(opperators)
selected_side, get_random_opperators, get_recommendations, submit_game, reset_game = game_choices
rec = load_rec()
st.session_state["name_sites"] = get_site_for_map(rec, st.session_state.selected_map)

col1, col2 = st.sidebar.columns(2)
with col1:
    if submit_game:
        bans = st.session_state["bans"]
        game = pass_on_rounds_game(st.session_state["rounds"], st.session_state.selected_map, bans[0], bans[1], bans[2], bans[3], st.session_state.selected_game_type)
        print(game.__dict__)
        print("Player stats\n")
        for stat_list in game.player_stats.values():
            for stat in stat_list:
                print(stat.__dict__)
        rec = update_rec(rec, game)
        st.session_state["rounds"] = []

with col2:
    if reset_game:
        st.session_state["rounds"] = []

if st.sidebar.button("Save to csv"):
    rec.save_to_csv()




tab1, tab2, tab3, tab4, tab5 = st.tabs(["Statistics", "Round", "Summary", "Recommendation", "Edit"])
with tab1:
    st.write("Statistics")

with tab2:
    add_new_round()

with tab3:
    print_summary_match()