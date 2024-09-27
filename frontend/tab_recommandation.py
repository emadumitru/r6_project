import streamlit as st
from backend.algo_randomizer import *

def print_random_recommendations(rec):
    period_start, period_end = st.session_state["season_periods"][st.session_state["period_random_opperators"]]
    attack, defense = get_random_operators(rec, formula_weight=st.session_state["balance_random_opperators"], op_count=5, period_start=period_start, period_end=period_end)

    st.title("Operators Overview")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    # Display attackers in the first column
    with col1:
        st.subheader("Attackers")
        if attack:
            st.markdown("**Attackers List:**")
            for ema,mihnea in attack:
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