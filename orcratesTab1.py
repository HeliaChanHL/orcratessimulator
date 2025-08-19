import streamlit as st
from cratesData import *
import pandas as pd
from os import path
from pygame import mixer


def modalContent():
    st.link_button("👑 Visit ORFinishes for Item Checklists! 👑","https://orfinishes.com",use_container_width=True)
    st.markdown(modalText)
def formUI():
    
    # Allow users to adjust rarity probabilities
    st.subheader("Adjust Rarity Probabilities")
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            # Initialize probabilities if not set
            if "rarity_probabilities" not in st.session_state:
                st.session_state["rarity_probabilities"] = {
                    "Legendary": 0.05,
                    "Epic": 0.13,
                    "Rare": 0.27,
                    "Common": 0.55
                }

            # Adjust sliders using existing session state values
            rarity_probabilities = {
                "Legendary": st.slider("Legendary Probability", min_value=0.0, max_value=1.0, value=st.session_state["rarity_probabilities"]["Legendary"], step=0.01),
                "Epic": st.slider("Epic Probability", min_value=0.0, max_value=1.0, value=st.session_state["rarity_probabilities"]["Epic"], step=0.01),
                "Rare": st.slider("Rare Probability", min_value=0.0, max_value=1.0, value=st.session_state["rarity_probabilities"]["Rare"], step=0.01),
                "Common": st.slider("Common Probability", min_value=0.0, max_value=1.0, value=st.session_state["rarity_probabilities"]["Common"], step=0.01)
            }

            # Normalize the probabilities to ensure they sum to 1
            total_probability = sum(rarity_probabilities.values())
            st.session_state["rarity_probabilities"] = {k: v / total_probability for k, v in rarity_probabilities.items()}

    # Load crates data
    df = pd.read_csv("./crates.csv", sep=",")
    # Dictionary to hold all crates
    crates = {}

    # Create crates from .csv file
    for _, row in df.iterrows():
        crate_name = row['crate']
        item = Item(name=row['name'], rarity=row['rarity'], item_type=row['type'])

        if crate_name not in crates:
            crates[crate_name] = Crate(crate_name)

        crates[crate_name].add_item(item)

    st.session_state["crates"] = crates

    # Select crate type
    with col2: 
        
        with st.container(border=True):
            # Allow users to adjust finish chance
            if "finish_chance" not in st.session_state:
                st.session_state["finish_chance"] = 0.01
            st.session_state["finish_chance"] = st.slider("Finish Chance", min_value=0.0, max_value=1.0, value=st.session_state["finish_chance"], step=0.01)

        with st.container(border=True):
            if "crate_type" not in st.session_state:
                st.session_state["crate_type"] = list(crates.keys())[0]  # Default to the first crate
            st.session_state["crate_type"] = st.selectbox("Select a crate to open:", list(crates.keys()), index=list(crates.keys()).index(st.session_state["crate_type"]))

            if "num_crates" not in st.session_state:
                st.session_state["num_crates"] = 1
            st.session_state["num_crates"] = st.number_input("Number of crates to open:", min_value=1, value=st.session_state["num_crates"])

            if "show_odds" not in st.session_state:
                st.session_state["show_odds"] = True
            st.session_state["show_odds"] = st.selectbox("Display Odds by default:",[True,False],index=[True,False].index(st.session_state["show_odds"]))
    # Counter for OR-Bucks and crates opened
    if 'crates_opened' not in st.session_state:
        st.session_state['crates_opened'] = 0
    if 'or_bucks_spent' not in st.session_state:
        st.session_state['or_bucks_spent'] = 0

    # Rarity and type counters
    if 'rarity_counts' not in st.session_state:
        st.session_state['rarity_counts'] = {
            'Finish': 0,
            'Legendary': 0,
            'Epic': 0,
            'Rare': 0,
            'Common': 0
        }

    if 'type_counts' not in st.session_state:
        st.session_state['type_counts'] = {
            'Cosmetic': 0,
            'Tool': 0,
            'Furniture': 0,
            'Gesture': 0
        }

    # Crate counts
    if 'crate_counts' not in st.session_state:
        st.session_state['crate_counts'] = {crate: 0 for crate in crates.keys()}
    
    mixer.init()
    audio_path = path.join(audio_directory, audio[0])
    mixer.music.load(audio_path)
    mixer.music.play()
    st.button("Roll Crates", use_container_width=True, on_click=submit)

def submit():
    st.session_state.calc = False

    st.session_state.buttonDis = False
