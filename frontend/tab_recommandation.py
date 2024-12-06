import streamlit as st
import pandas as pd
from backend.algo_randomizer import *
from backend.algo_recommender import *

def print_random_recommendations(rec):
    period_start, period_end = st.session_state["season_periods"][st.session_state["period_random_opperators"]]

    current_random = st.session_state["random_opperators"]

    if current_random == (None, None, 0, None, None):
        st.session_state["random_opperators"] = algo_get_random(rec, formula_weight=st.session_state["balance_random_opperators"], op_count=5, period_start=period_start, period_end=period_end)
    if current_random[2] != st.session_state["balance_random_opperators"] or current_random[3] != period_start or current_random[4] != period_end:
        st.session_state["random_opperators"] = algo_get_random(rec, formula_weight=st.session_state["balance_random_opperators"], op_count=5, period_start=period_start, period_end=period_end)
    attack, defense, _, _, _ = st.session_state["random_opperators"]

    st.title("Operators Overview")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    # Display attackers in the first column
    with col1:
        st.subheader("Attackers")
        if attack:
            st.markdown("**Attackers List:**")
            for ema, mihnea in attack:
                st.markdown(f"- **Ema**: {ema} | **Mihnea**: {mihnea}")
        else:
            st.markdown("No attackers available.")

    # Display defenders in the second column
    with col2:
        st.subheader("Defenders")
        if defense:
            st.markdown("**Defenders List:**")
            for ema, mihnea in defense:
                st.markdown(f"- **Ema**: {ema} | **Mihnea**: {mihnea}")
        else:
            st.markdown("No defenders available.")



def display_site_recommendations_in_streamlit(site_recommendations):
    site_names = list(site_recommendations['Attack'].keys())
    tabs = st.tabs(site_names)

    for i, site_name in enumerate(site_names):
        with tabs[i]:
            st.header(f"Site: {site_name}")
            for side in ['Defense', 'Attack']:
                st.subheader(f"{side}")
                max_recs = max(len(site_recommendations[side][site_name]['ema']), len(site_recommendations[side][site_name]['mihnea']))
                columns = [f"Rec {j + 1}" for j in range(max_recs)]
                table_data = []
                for player in ['ema', 'mihnea']:
                    row = [
                        f"{op[0]} **{op[1]['score']:.2f}** ({op[1]['play_rate_site'] * 100:.2f}%)"
                        for op in site_recommendations[side][site_name][player]
                    ]
                    # Fill in with blanks if less than max_recs
                    row += [""] * (max_recs - len(row))
                    table_data.append([player.capitalize()] + row)

                st.markdown("<style>table {width: 100%;}</style>", unsafe_allow_html=True)
                st.markdown(
                    "| Player | " + " | ".join(columns) + " |\n" +
                    "|--------|" + "-------|" * len(columns) + "\n" +
                    "\n".join(
                        [
                            "| " + " | ".join(row) + " |"
                            for row in table_data
                        ]
                    ),
                    unsafe_allow_html=True
                )


def print_opperator_recommendations(rec):
    period_start = st.session_state["recommender_periods"][st.session_state["period_recommender_opperators"]][0]
    # st.write(period_start)

    if st.session_state["recommended_opperators"] == (None, None):
        st.session_state["recommended_opperators"] = algo_get_recom(rec, period_start, st.session_state.selected_map, 5)
    if st.session_state["recommended_opperators"][1] != st.session_state.selected_map or st.session_state["recommended_opperators"][2] != period_start:
        st.session_state["recommended_opperators"] = algo_get_recom(rec, period_start, st.session_state.selected_map, 5)

    recomm = st.session_state["recommended_opperators"]

    display_site_recommendations_in_streamlit(recomm[0])


    rounds = recomm[-1]
    game_ids = [round.game_id for round in rounds]
    st.write(set(game_ids))
    # st.write(recomm[0])


