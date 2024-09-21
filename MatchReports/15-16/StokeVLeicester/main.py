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

            plyr = match_event["player"]["name"];
            if plyr in players_who_passed:
                players_who_passed[plyr]['count'] = players_who_passed[plyr]['count'] + 1
                players_who_passed[plyr]['passes'].append(
                        {
                                "location": match_event["location"],
                                "end_location": match_event["pass"]["end_location"]
                        }
                        )
            else:
                players_who_passed[plyr] = {
                        "count": 1,
                        "passes": [{
                                "location": match_event["location"],
                                "end_location": match_event["pass"]["end_location"]
                            }]
                        }

        pass_counter = pd.DataFrame({
            'Players': list(players_who_passed.keys()),
            'Passes': [players_who_passed[key] for key in players_who_passed.keys()]
        })

        option = st.selectbox(
            'Which number do you like best?',
             pass_counter['Players'])

        'Passes: ', players_who_passed[option]['count']

        pitch = Image.new("RGB", (1500,600), "green")

        passes = []

        for x in (players_who_passed[option]['passes']):
            passes.append([(x['location'][0] * 5, x['location'][1] * 10), (x['end_location'][0] * 10, x['end_location'][1] * 10)])

        print(passes)
        for p in passes:
            draw = ImageDraw.Draw(pitch)
            draw.line(p, width=1,fill="white")
        pitch.save('./pitch.png')

        st.image('./pitch.png')

foo();
