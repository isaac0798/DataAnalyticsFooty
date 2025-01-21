import sys
import os
import json
import sqlite3
from supabase import create_client, Client
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
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
    """ 

    cursor.execute('''
      INSERT OR IGNORE INTO type (id, name)
      VALUES (?, ?)
    ''', (
      event['type']['id'],
      event['type']['name']
    ))

    if eventType not in event:
        print(f'cannot find event details: {eventType}')
        cursor.execute('''
            INSERT INTO event (uuid, type_id, player_id, timestamp, location_x, location_y, end_location_x, end_location_y)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event['id'],
            event['type']['id'],
            event['player']['id'],
            event['timestamp'],
            event['location'][0],
            event['location'][1],
            event['location'][0],
            event['location'][1]  
        ))
    else:
        print('found event')
        end_location_x = event['location'][0]
        end_location_y = event['location'][1] 
        
        if eventType in event and 'end_location' in event[eventType]:
            end_location_x = event[eventType]['end_location'][0]
            end_location_y = event[eventType]['end_location'][1]
        
        cursor.execute('''
            INSERT INTO event (uuid, type_id, player_id, timestamp, location_x, location_y, end_location_x, end_location_y)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event['id'],
            event['type']['id'],
            event['player']['id'],
            event['timestamp'],
            event['location'][0],
            event['location'][1],
            end_location_x,
            end_location_y
        ))  """