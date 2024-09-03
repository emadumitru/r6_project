import streamlit as st
from form_ranked import *
from tab_round import *
from app_format import *


selected_map, selected_game_type, selected_side, submit_game = recommender_format()
# rec = load_rec()
# st.session_state["name_sites"] = get_site_for_map(rec, selected_map)


print(selected_map, selected_game_type, selected_side, submit_game)



if submit_game:
    # create game
    st.session_state["rounds"] = []


st.session_state["name_sites"] = ['kitchen', 'kitchen2', '1F']

tab1, tab2 = st.tabs(["try mihnea", "try ema"])
with tab1:
    ranked_input_form()
with tab2:
    add_new_round('Attack', 2)