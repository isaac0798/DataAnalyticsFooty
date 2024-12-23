import sys
import os
import json
import shutil
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

''' create folder for game '''
dirs = args[0].split('/')
gamePicturePath = f'./MatchGeneratorResults/{dirs[1]}/{dirs[2]}'

if not os.path.exists(gamePicturePath):
  os.makedirs(gamePicturePath)
  print("Folder %s created!" % gamePicturePath)
else:
  print("Folder %s already exists" % gamePicturePath)
  shutil.rmtree(gamePicturePath)
  os.makedirs(gamePicturePath)

''' generate image for each event timestamp_player_type_id'''
for event in match_data:
  if 'location' not in event:
    continue

  ''' Create Image '''
  im = Image.new(mode="RGB", size=(int(maxX), int(maxY)), color=(0, 102, 0))
  draw = ImageDraw.Draw(im)
  draw.text((0, 0), f"{event['timestamp']}_{event['player']['id']}_{event['type']['id']}_{event['id']}")

  startLocation = event['location']
  startLocationX = startLocation[0] * 10
  startLocationY = startLocation[1] * 10

  print (startLocationX, startLocationY)

  draw.circle([startLocationX, startLocationY], 2, fill=(255, 255, 255, 255))

  im.save(f"{gamePicturePath}/{event['timestamp']}_{event['player']['id']}_{event['type']['id']}_{event['id']}.png")

print (maxX, maxY)


''' use 3rd party software to make all images into a video'''