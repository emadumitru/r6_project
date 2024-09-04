import streamlit as st

def print_summary_match():
    st.write('### Summary match')
    
    # st.write(st.session_state['rounds']) # Debug purpose

    len_rounds = len(st.session_state['rounds'])
    score_us = len([round for round in st.session_state['rounds'] if round['win']])
    score_op = len_rounds - score_us

    # write map, game type and if ranked then bans
    st.write(f'#### {st.session_state.selected_map} - {st.session_state.selected_game_type} ({score_us} - {score_op})')
    if st.session_state.selected_game_type == 'Ranked':
        bans = st.session_state['bans']
        st.write(f'Bans: {bans[0]}, {bans[1]}, {bans[2]}, {bans[3]}')

    for i in range(len_rounds):
        round = st.session_state['rounds'][i]
        st.write(f'**Round {i+1}**: {round["site"]} - {round["side"]} - {"Win" if round["win"] else "Loss"}')
        ema = round["players"]["Ema"]
        mihnea = round["players"]["Mihnea"]

        # Using icons for True/False values
        def icon(value):
            return "✅" if value else "❌"

        # Display player data in a nicely formatted table
        st.markdown(
            """
            | **Player** | **Operator** | **Kills** | **Assists** | **Survived** | **EntryFrag** | **Diffuser** | **Clutch** |
            |------------|-------------------|-----------|-------------|---------------|----------------|--------------|------------|
            | **Ema**    | {ema_operator} | {ema_kills} | {ema_assists} | {ema_surv} | {ema_ef} | {ema_dif} | {ema_cl} |
            | **Mihnea** | {mihnea_operator} | {mihnea_kills} | {mihnea_assists} | {mihnea_surv} | {mihnea_ef} | {mihnea_dif} | {mihnea_cl} |
            """.format(
                ema_operator=ema["operator"],
                ema_kills=ema["kills"],
                ema_assists=ema["assists"],
                ema_surv=icon(ema["survived"]),
                ema_ef=icon(ema["entryfrag"]),
                ema_dif=icon(ema["diffuser"]),
                ema_cl=icon(ema["clutch"]),
                mihnea_operator=mihnea["operator"],
                mihnea_kills=mihnea["kills"],
                mihnea_assists=mihnea["assists"],
                mihnea_surv=icon(mihnea["survived"]),
                mihnea_ef=icon(mihnea["entryfrag"]),
                mihnea_dif=icon(mihnea["diffuser"]),
                mihnea_cl=icon(mihnea["clutch"]),
            )
        )
        st.divider()