import sys
import json
from PIL import Image, ImageDraw

args = sys.argv[1:]
print(args[0])

json_file = open(args[0])
match_data = json.load(json_file)

maxX = 0.0
maxY = 0.0

for event in match_data:
  ''' Grab pitch size based off kick off location '''
  if event['minute'] == 0 and event['second'] == 0 and 'location' in event:
    maxX = event['location'][0] * 2 * 10
    maxY = event['location'][1] * 2 * 10

''' draw pitch image with basic dimensions green'''
im = Image.new(mode="RGB", size=(int(maxX), int(maxY)), color=(0, 102, 0))
im.save('./MatchGenerator/field.png')

''' generate image for each event timestamp_player_type_id'''

''' use 3rd party software to make all images into a video'''