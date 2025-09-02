import math
import json
from curl_tracker import get_API
from position_calculation import calculate_drone_position

def calc_bearing(target_loc: dict, current_position: dict):
    """
    Takes in dictionaries for target location and current position, both
    in { "x": x, "y": y} and returns floats of direction (in degrees) and distance.
    """
    tx, ty = target_loc["x"], target_loc["y"]
    dx, dy = current_position["x"], current_position["y"]

    delta_x = tx - dx
    delta_y = ty - dy
    distance = math.sqrt((delta_x **2) + (delta_y **2))
    direction = math.degrees(math.atan2(delta_y, delta_x))
    if direction < 0:
        direction += 360

    return(direction, distance)
# Main loop

flying = True

while flying:
  get_API()
  with open('curl_snapshot.json') as f:
    d = json.load(f)
  position = calculate_drone_position(d["status"])
  x, y = position["x"], position["y"]
  print(x, y)
  target_loc = d["targets"]
  direction, distance = calc_bearing(target_loc, position)
  print(f" direction, distance: {direction, distance}")
  

if direction < 1:
   # Drop the bomb!
   pass

  # send commands to drone
    # Either change heading or drop
