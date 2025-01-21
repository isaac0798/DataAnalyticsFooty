import sys
import os
import json
import sqlite3
from supabase import create_client, Client
from dotenv import load_dotenv, dotenv_values 

load_dotenv()

args = sys.argv[1:]
print(args[0])

json_file = open(args[0])
match_data = json.load(json_file)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
    
for event in match_data:
    if 'player' not in event:
        continue
    
    if 'location' not in event:
        continue

    eventType = event['type']['name'].lower()

    response = (
      supabase.table("players")
        .upsert({"id": event['player']['id'], "name": event['player']['name']}, on_conflict="id")
        .execute()
    )

    response = (
      supabase.table("type")
        .upsert({"id": event['type']['id'], "name": event['type']['name']}, on_conflict="id")
        .execute()
    )

    if eventType not in event:
        print(f'cannot find event details: {eventType}')

        response = (
          supabase.table("event")
            .upsert({
              "uuid": event['id'],
              "type_id": event['type']['id'],
              "player_id": event['player']['id'],
              "timestamp": event['timestamp'],
              "location_x": event['location'][0],
              "location_y": event['location'][1],
              "end_location_x": event['location'][0],
              "end_location_y": event['location'][1]
            }, on_conflict="uuid").execute()
        )
    else:
        print('found event')
        end_location_x = event['location'][0]
        end_location_y = event['location'][1] 
        
        if eventType in event and 'end_location' in event[eventType]:
            end_location_x = event[eventType]['end_location'][0]
            end_location_y = event[eventType]['end_location'][1]
        
        response = (
          supabase.table("event")
            .upsert({
              "uuid": event['id'],
              "type_id": event['type']['id'],
              "player_id": event['player']['id'],
              "timestamp": event['timestamp'],
              "location_x": event['location'][0],
              "location_y": event['location'][1],
              "end_location_x": end_location_x,
              "end_location_y": end_location_y
            }, on_conflict="uuid").execute()
        )