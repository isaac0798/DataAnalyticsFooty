import sys
import os
import json
import shutil
import cv2
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
gamePicturePath = f'./MatchGeneratorResults/{dirs[1]}/{dirs[2]}/images'

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

  ''' get location event '''
  startLocation = event['location']
  startLocationX = startLocation[0] * 10
  startLocationY = startLocation[1] * 10

  draw.circle([startLocationX, startLocationY], 2, fill=(255, 255, 255, 255))

  ''' get end location event '''
  eventType = event['type']['name'].lower()

  if eventType not in event:
    print('cannot find event details')
    draw.text((0, 10), f"cannot find event details: {eventType}")
  else:
    if 'end_location' in event[eventType]:
      endLocation = event[eventType]['end_location']
      endLocationX = endLocation[0] * 10
      endLocationY = endLocation[1] * 10

      draw.circle([endLocationX, endLocationY], 2, fill=(255, 255, 255, 255))
    else:
      print('No end location f')
      draw.text((0, 10), f"No end location f")

  im.save(f"{gamePicturePath}/{event['timestamp']}_{event['player']['id']}_{event['type']['id']}_{event['id']}.png")


video_name = 'output_video.mp4'

images = [img for img in os.listdir(gamePicturePath) if img.endswith(".png")]

first_image = cv2.imread(os.path.join(gamePicturePath, images[0]))
height, width, _ = first_image.shape

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name, fourcc, 20, (width, height))

for image in images:
    img_path = os.path.join(gamePicturePath, image)
    frame = cv2.imread(img_path)
    video.write(frame)

video.release()
cv2.destroyAllWindows()