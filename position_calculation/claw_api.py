#!/usr/bin/env python3
"""
Demo: trigger an action when a drone comes close to a target point on a 2D map.

- Drone moves at constant speed 1 (arbitrary units).
- Target is at coordinate (tx, ty).
- When distance < threshold, trigger open_claw().
"""

import math
import time

# Target position
tx, ty = 5.0, 5.0
# Start position
x, y = 0.0, 0.0
# Drone speed (units per second)
speed = 1.0
# Direction (to target for simplicity)
heading = math.atan2(ty - y, tx - x)
# Distance threshold to trigger action
threshold = 0.5

def open_claw():
    # Placeholder action
    print(">>> CLAW OPENED <<<")

while True:
    # Move drone
    x += math.cos(heading) * speed * 0.5   # step = 0.5s
    y += math.sin(heading) * speed * 0.5

    # Compute distance to target
    dist = math.hypot(tx - x, ty - y)
    print(f"Drone at ({x:.2f}, {y:.2f}), dist={dist:.2f}")

    if dist <= threshold:
        open_claw()
        break

    time.sleep(0.5)
