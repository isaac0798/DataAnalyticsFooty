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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS type (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
    ''')
    
    conn.commit()
    
    for event in match_data:
        if 'player' not in event:
            continue
        
        if 'location' not in event:
            continue

        eventType = event['type']['name'].lower()

        cursor.execute('''
          INSERT OR IGNORE INTO players (id, name)
          VALUES (?, ?)
        ''', (
          event['player']['id'],
          event['player']['name']
        ))

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
            ))

cursor.close()