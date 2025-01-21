import os
import streamlit as st
from supabase import create_client, Client
from st_supabase_connection import SupabaseConnection, execute_query
from PIL import Image, ImageDraw
from arrowedLine import arrowedLine

url: str = "https://iokzkglewkuojahttfig.supabase.co"
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlva3prZ2xld2t1b2phaHR0ZmlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc0NTAzNzMsImV4cCI6MjA1MzAyNjM3M30.l8qfDDjmK1XF8dWOvN0gxxRRWVTOI0CtPNqhzT9fLWs'

st_supabase_client = st.connection(
    name="supabase",
    type=SupabaseConnection,
    ttl=None,
)

conn = st.connection("supabase",type=SupabaseConnection, ttl=None, url=url, key=key)

rows = conn.table("players").select("*").execute()

playerSelected = st.selectbox(
  "Pick a player",
  rows.data,
  index=None,
  placeholder="Select player...",
)

if playerSelected == None:
  st.write('Select a Player 👀')

st.write(playerSelected['id'])

event_types = conn.table("type").select("*").execute()

typeSeleceted = st.selectbox(
  "pick an event",
  event_types.data
)

events = conn.table("event").select("*").eq('player_id', playerSelected['id']).eq('type_id', typeSeleceted['id']).execute()

selected_event = st.dataframe(events.data, on_select="rerun", selection_mode="single-row")

event = selected_event.selection.rows

if len(event) == 0:
  st.write('pick an event')

st.write(events.data[event[0]])

ev = events.data[event[0]]

im = Image.new(mode="RGB", size=(1200, 800), color=(0, 102, 0)) #size is pitch * 2 * 10
draw = ImageDraw.Draw(im)
draw.text((0, 0), f"{ev['timestamp']}_{ev['player_id']}_{ev['type_id']}_{ev['uuid']}")
draw.circle([ev['location_x']*10, ev['location_y']]*10, 2, fill=(255, 255, 255, 255))

draw.circle([ev['end_location_x']*10, ev['end_location_y']]*10, 2, fill=(255, 255, 255, 255))
draw.line([(ev['location_x']*10, ev['location_y']*10), (ev['end_location_x']*10, ev['end_location_y']*10)], fill=(255, 255, 255, 255), width=1)

im = arrowedLine(im, (ev['location_x']*10, ev['location_y']*10), (ev['end_location_x']*10, ev['end_location_y']*10), 1, (255, 255, 255))

st.image(im)