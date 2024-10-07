import json
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from typing import List, Optional
from uuid import UUID
from datetime import datetime

def foo():
    '''
        GOAL:
            -match statistics
                -total passes
                -total shots
                -dribbles
                -goals


    '''
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

class PlayPattern:
    id: int
    name: str

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name


class BallReceipt:
    outcome: PlayPattern

    def __init__(self, outcome: PlayPattern) -> None:
        self.outcome = outcome


class Carry:
    end_location: List[float]

    def __init__(self, end_location: List[float]) -> None:
        self.end_location = end_location


class Clearance:
    body_part: PlayPattern
    left_foot: bool

    def __init__(self, body_part: PlayPattern, left_foot: bool) -> None:
        self.body_part = body_part
        self.left_foot = left_foot


class Duel:
    type: PlayPattern

    def __init__(self, type: PlayPattern) -> None:
        self.type = type


class Lineup:
    player: PlayPattern
    position: PlayPattern
    jersey_number: int

    def __init__(self, player: PlayPattern, position: PlayPattern, jersey_number: int) -> None:
        self.player = player
        self.position = position
        self.jersey_number = jersey_number


class Tactics:
    formation: int
    lineup: List[Lineup]

    def __init__(self, formation: int, lineup: List[Lineup]) -> None:
        self.formation = formation
        self.lineup = lineup


class Pass:
    recipient: PlayPattern
    length: float
    angle: float
    height: PlayPattern
    end_location: List[float]
    body_part: Optional[PlayPattern]
    type: Optional[PlayPattern]
    outcome: Optional[PlayPattern]
    aerial_won: Optional[bool]

    def __init__(self, recipient: PlayPattern, length: float, angle: float, height: PlayPattern, end_location: List[float], body_part: Optional[PlayPattern], type: Optional[PlayPattern], outcome: Optional[PlayPattern], aerial_won: Optional[bool]) -> None:
        self.recipient = recipient
        self.length = length
        self.angle = angle
        self.height = height
        self.end_location = end_location
        self.body_part = body_part
        self.type = type
        self.outcome = outcome
        self.aerial_won = aerial_won


class MatchEvent:
    id: UUID
    index: Optional[int]
    period: Optional[int]
    timestamp: Optional[datetime]
    minute: Optional[int]
    second: Optional[int]
    type: Optional[PlayPattern]
    possession: Optional[int]
    possession_team: Optional[PlayPattern]
    play_pattern: Optional[PlayPattern]
    team: Optional[PlayPattern]
    duration: Optional[float]
    tactics: Optional[Tactics]
    related_events: Optional[List[UUID]]
    player: Optional[PlayPattern]
    position: Optional[PlayPattern]
    location: Optional[List[float]]
    welcome_pass: Optional[Pass]
    carry: Optional[Carry]
    ball_receipt: Optional[BallReceipt]
    under_pressure: Optional[bool]
    duel: Optional[Duel]
    counterpress: Optional[bool]
    out: Optional[bool]
    clearance: Optional[Clearance]

    def __init__(self, id: UUID, index: int, period: int, timestamp: datetime, minute: int, second: int, type: PlayPattern, possession: int, possession_team: PlayPattern, play_pattern: PlayPattern, team: PlayPattern, duration: Optional[float], tactics: Optional[Tactics], related_events: Optional[List[UUID]], player: Optional[PlayPattern], position: Optional[PlayPattern], location: Optional[List[float]], welcome_pass: Optional[Pass], carry: Optional[Carry], ball_receipt: Optional[BallReceipt], under_pressure: Optional[bool], duel: Optional[Duel], counterpress: Optional[bool], out: Optional[bool], clearance: Optional[Clearance]) -> None:
        self.id = id
        self.index = index
        self.period = period
        self.timestamp = timestamp
        self.minute = minute
        self.second = second
        self.type = type
        self.possession = possession
        self.possession_team = possession_team
        self.play_pattern = play_pattern
        self.team = team
        self.duration = duration
        self.tactics = tactics
        self.related_events = related_events
        self.player = player
        self.position = position
        self.location = location
        self.welcome_pass = welcome_pass
        self.carry = carry
        self.ball_receipt = ball_receipt
        self.under_pressure = under_pressure
        self.duel = duel
        self.counterpress = counterpress
        self.out = out
        self.clearance = clearance


def run():
    st.write('Stoke vs Leicester')

    with open('./match_data.json') as f:
        match_data = json.load(f)

    for match_event in match_data:
        print(match_event)
        pass
run()
