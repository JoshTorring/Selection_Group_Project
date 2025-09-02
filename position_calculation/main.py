import math
import json
import requests
from curl_tracker import get_API
from position_calculation import calculate_drone_position

def math_to_compass(math_heading: float) -> float:
    """
    Convert math heading (0° = +x axis (east), CCW positive)
    to compass heading (0° = north, CW positive).
    """
    compass = (90 - math_heading) % 360
    return compass

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
    math_heading = math.degrees(math.atan2(delta_y, delta_x))
    compass_heading = math_to_compass(math_heading)
    return compass_heading, distance
# Main loop

flying = True

while flying:
    get_API()
    with open('curl_snapshot.json') as f:
        d = json.load(f)
    position = calculate_drone_position(d["status"])
    #x, y = position["x"], position["y"]
    #print(x, y)
    target_loc = d["targets"]
    direction, distance = calc_bearing(target_loc, position)
    print(f" direction, distance: {direction, distance}")

    drone_id = "drone-04"

 
    speed = 1.0 if distance > 2 else 0.1
    offset = 0
    if speed != 1:
      offset = distance % 1
        

    cmd_payload = {
        "id": drone_id,
        "heading": direction,
        "speed": speed + offset
    }

    try:
        resp = requests.post(
            "https://selection-drone.charginglead.workers.dev/command",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer sait-selection-2025"
            },
            json=cmd_payload,
            timeout=5
        )
        print("Command response:", resp.status_code, resp.text)
    except Exception as e:
        print("Command error:", e)

    # Trigger drop if within 1 unit distance
    if distance <= 0.08:
        try:
            drop_url = f"https://selection-drone.charginglead.workers.dev/drop?drone_id={drone_id}"
            drop_resp = requests.post(
                drop_url,
                headers={"Authorization": "Bearer sait-selection-2025"},
                timeout=5
            )
            print("Drop response:", drop_resp.status_code, drop_resp.text)
        except Exception as e:
            print("Drop error:", e)
