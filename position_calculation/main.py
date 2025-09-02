import math
from curl_tracker import get_API
from position_calculation import calculate_drone_position

# Main loop

flying = True

while flying:
  data = curl_tracker.get_API()
  print(data)
  
  # get Data from api


  # calculate drone position
  

  # calculate direction change needed
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

direction, distance = calc_bearing(target_loc, current_position)
  # decide if we need to drop the bomb
if direction < 1:
   # Drop the bomb!
   pass

  # send commands to drone
    # Either change heading or drop
