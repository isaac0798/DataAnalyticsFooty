import json
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw

def foo():
    st.write("Stoke vs Leiceister - 15/16")
    with open('./match_data.json') as f:
        match_data = json.load(f)
        st.write("Pass Counter")

        players_who_passed = {}
        for match_event in match_data:
            if match_event["type"]["name"] != "Pass":
                continue

            if match_event["player"]["name"] in players_who_passed:
                players_who_passed[match_event["player"]["name"]] = players_who_passed[match_event["player"]["name"]] + 1
            else:
                players_who_passed[match_event["player"]["name"]] = 1

        pass_counter = pd.DataFrame({
            'Players': list(players_who_passed.keys()),
            'Passes': [players_who_passed[key] for key in players_who_passed.keys()]
        })

        option = st.selectbox(
            'Which number do you like best?',
             pass_counter['Players'])

        'Passes: ', players_who_passed[option]

        pitch = Image.new("RGB", (1500,600), "green")
        pitch.save('./pitch.png')

        st.image('./pitch.png')

foo();
