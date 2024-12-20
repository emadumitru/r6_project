import streamlit as st
# Set page configuration to use the full width of the screen
st.set_page_config(page_title="R6 Siege Tracker", layout="wide")

from frontend.app_format import *
from frontend.tab_round import *
import frontend.tab_summary as ts
import frontend.tab_recommandation as tr
import frontend.tab_statistics as tstat
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
        if st.session_state.selected_game_type == "Ranked":
            bans = st.session_state["bans"]
        else:
            bans = ["", "", "", ""]
        game, rounds_round = pass_on_rounds_game(st.session_state["rounds"], st.session_state.selected_map, bans[0], bans[1], bans[2], bans[3], st.session_state.selected_game_type)

        rec = update_rec(rec, game, rounds_round)
        st.session_state["rounds"] = []

with col2:
    if reset_game:
        st.session_state["rounds"] = []

if st.sidebar.button("Save to csv"):
    rec.save_to_csv()




tab1, tab2, tab3, tab4, tab5 = st.tabs(["Statistics", "Round", "Summary", "Recommendation", "Edit"])
with tab1:
    tstat.print_map_stats(rec)
    tstat.print_site_stats(rec, st.session_state.selected_map)

with tab2:
    add_new_round()

with tab3:
    ts.print_summary_match()

with tab4:
    if get_random_opperators:
        tr.print_random_recommendations(rec)