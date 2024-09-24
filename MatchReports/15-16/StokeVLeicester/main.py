import json
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
                                "end_location": match_event["pass"]["end_location"],
                                "outcome": match_event["pass"]["outcome"]["name"] if 'outcome' in match_event["pass"] else "Complete"
                        }
                        )
            else:
                players_who_passed[plyr] = {
                        "count": 1,
                        "passes": [{
                                "location": match_event["location"],
                                "end_location": match_event["pass"]["end_location"],
                                "outcome": match_event["pass"]["outcome"]["name"] if 'outcome' in match_event["pass"] else "Complete"
                            }]
                        }

        pass_counter = pd.DataFrame({
            'Players': list(players_who_passed.keys()),
            'Passes': [players_who_passed[key] for key in players_who_passed.keys()]
        })

        option = st.selectbox(
            'Player Options:',
             pass_counter['Players'])

        'Passes: ', players_who_passed[option]

        pitch = Image.new("RGB", (120,100), "green")

        passes = []

        for x in (players_who_passed[option]['passes']):
            passes.append([(x['location'][0], x['location'][1]), (x['end_location'][0], x['end_location'][1])])

        for p in passes:
            draw = ImageDraw.Draw(pitch)
            draw.line(p, width=1,fill="white")
        pitch.save('./pitch.png')

        players = tuple(players_who_passed.keys())
        completed_passes = []
        incomplete_passes = []

        for player in players_who_passed.keys():
            if player != option:
                continue

            completedPassses = 0
            incompletedPasses = 0

            for p in players_who_passed[player]['passes']:
                if p['outcome'] == 'Complete':
                    completedPassses += 1
                elif p['outcome'] == 'Incomplete':
                    incompletedPasses += 1
            
            completed_passes.append(completedPassses)
            incomplete_passes.append(incompletedPasses)


        weight_counts = {
            "Complete": np.array(completed_passes),
            "Incomplete": np.array(incomplete_passes),
        }
        width = 0.5

        fig, ax = plt.subplots()
        bottom = np.zeros(1)

        for boolean, weight_count in weight_counts.items():
            print(boolean)
            print(weight_count)
            p = ax.bar(option, weight_count, width, label=boolean, bottom=bottom)
            bottom += weight_count

        ax.set_title("Number of passes")
        ax.legend(loc="upper right")
        st.pyplot(fig)

        st.image('./pitch.png')

foo();
