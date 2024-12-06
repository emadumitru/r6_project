import streamlit as st
import os
from importer.importer import run_r6_dissect_on_new_matches
from importer.clean_json import clean_json

def tab_import():
    st.title("Import Matches")

    # Button to search for new games
    if st.button("Search for New Games"):
        new_json_files = run_r6_dissect_on_new_matches()
        if new_json_files:
            st.success(f"Found {len(new_json_files)} new match(es)!")
            st.session_state["new_json_files"] = new_json_files
        else:
            st.info("No new matches found.")

    # Show the list of new JSON files if available
    if "new_json_files" in st.session_state and st.session_state["new_json_files"]:
        st.write("### Newly Processed Matches:")
        for idx, json_file in enumerate(st.session_state["new_json_files"]):
            st.write(f"{idx + 1}. {json_file}")
            with open(json_file, 'r') as file:
                json_data = file.read()
            st.json(json_data)

            # Clean JSON and add the game
            if st.button(f"Add Match {idx + 1}", key=f"add_match_{idx}"):
                cleaned_path = clean_json(json_file, ["Puuuumkin", "Pumkiiiin"])
                st.success(f"Match cleaned and added from: {cleaned_path}")
                with open(cleaned_path, 'r') as file:
                    json_data = file.read()
                st.json(json_data)
                
                # Remove the cleaned JSON after adding the game
                # os.remove(cleaned_path)
                st.session_state["new_json_files"].remove(json_file)

if __name__ == "__main__":
    tab_import()
