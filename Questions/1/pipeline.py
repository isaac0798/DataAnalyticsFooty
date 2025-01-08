import sys
import os
import json
import sqlite3

args = sys.argv[1:]
print(args[0])

json_file = open(args[0])
match_data = json.load(json_file)

# Connect to the db
with sqlite3.connect('./Questions/1/example.db') as conn:
    cursor = conn.cursor()

    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event (
            id INTEGER PRIMARY KEY,
            uuid TEXT NOT NULL,
            type_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            location_x REAL NOT NULL,
            location_y REAL NOT NULL,
            end_location_x REAL NOT NULL,
            end_location_y REAL NOT NULL
        );
    ''')
    
    conn.commit()
    
    for event in match_data:
        if 'player' not in event:
            continue
        
        if 'location' not in event:
            continue

        eventType = event['type']['name'].lower()

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
                event['location'][0],  # Default to same as start location if no end location
                event['location'][1]   # Default to same as start location if no end location
            ))
        else:
            print('found event')
            end_location_x = event['location'][0]  # Default values
            end_location_y = event['location'][1]  # Default values
            
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
            ))

cursor.close()