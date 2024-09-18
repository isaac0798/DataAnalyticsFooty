import json
import streamlit as st
import pandas as pd
import numpy as np

def foo():
    st.write("Stoke vs Leiceiser - 15/16")
    with open('./match_data.json') as f:
        match_data = json.load(f)
        print('hi')
        st.write("Pass Counter")

        players_who_passed = {}
        for match_event in match_data:
            if match_event["type"]["name"] != "Pass":
                continue

            if match_event["player"]["name"] in players_who_passed:
                players_who_passed[match_event["player"]["name"]] = players_who_passed[match_event["player"]["name"]] + 1
            else:
                players_who_passed[match_event["player"]["name"]] = 1

        print(players_who_passed)
        st.write(pd.DataFrame({
            'Players': list(players_who_passed.keys()),
            'Passes': [players_who_passed[key] for key in players_who_passed.keys()]
        }))

foo();
