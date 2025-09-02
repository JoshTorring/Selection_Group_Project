import math
import json
import requests
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

    # Send command to drone using direction as heading
    drone_id = "drone-04"
    heading = direction  # already 0–360 with 0 = north
    # simple speed logic: slow down when close
    speed = 1.0 if distance > 10 else 0.1

    cmd_payload = {
        "id": drone_id,
        "heading": heading,
        "speed": speed
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
