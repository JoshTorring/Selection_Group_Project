import json
import math

drone_dummy_status = [
  {
    "id": "drone-01",
    "signals": [
      {
        "tower_id": "A",
        "rx_power": 11.5079430272114
      },
      {
        "tower_id": "B",
        "rx_power": 28.7472986820898
      },
      {
        "tower_id": "F",
        "rx_power": 43.814336777736
      },
      {
        "tower_id": "H",
        "rx_power": 23.0818000894258
      },
      {
        "tower_id": "I",
        "rx_power": 23.0818000894258
      },
      {
        "tower_id": "J",
        "rx_power": 21.4937037288011
      },
      {
        "tower_id": "K",
        "rx_power": 24.4770566057093
      },
      {
        "tower_id": "L",
        "rx_power": 26.5845559156563
      },
      {
        "tower_id": "M",
        "rx_power": 29.121536861986
      },
      {
        "tower_id": "N",
        "rx_power": 28.7841051246103
      },
      {
        "tower_id": "O",
        "rx_power": 24.9717389915962
      }
    ]
  },
  {
    "id": "drone-02",
    "signals": [
      {
        "tower_id": "A",
        "rx_power": 12.3055442860036
      },
      {
        "tower_id": "B",
        "rx_power": 30.201779313304
      },
      {
        "tower_id": "C",
        "rx_power": 11.7838152704289
      },
      {
        "tower_id": "F",
        "rx_power": 29.7285956193536
      },
      {
        "tower_id": "H",
        "rx_power": 19.7437054241532
      },
      {
        "tower_id": "I",
        "rx_power": 19.7437054241532
      },
      {
        "tower_id": "J",
        "rx_power": 18.6287423323746
      },
      {
        "tower_id": "K",
        "rx_power": 20.7977271582576
      },
      {
        "tower_id": "L",
        "rx_power": 22.2061243526368
      },
      {
        "tower_id": "M",
        "rx_power": 23.8592392468309
      },
      {
        "tower_id": "N",
        "rx_power": 49.2965659355261
      },
      {
        "tower_id": "O",
        "rx_power": 27.2846222132088
      }
    ]
  },
  {
    "id": "drone-03",
    "signals": [
      {
        "tower_id": "A",
        "rx_power": 12.6541014613293
      },
      {
        "tower_id": "B",
        "rx_power": 30.6567819299921
      },
      {
        "tower_id": "C",
        "rx_power": 10.1223340271157
      },
      {
        "tower_id": "F",
        "rx_power": 32.709030166572
      },
      {
        "tower_id": "H",
        "rx_power": 20.592636831636
      },
      {
        "tower_id": "I",
        "rx_power": 20.592636831636
      },
      {
        "tower_id": "J",
        "rx_power": 19.371781776942
      },
      {
        "tower_id": "K",
        "rx_power": 21.7255818749704
      },
      {
        "tower_id": "L",
        "rx_power": 23.2890519619016
      },
      {
        "tower_id": "M",
        "rx_power": 25.1467726789951
      },
      {
        "tower_id": "N",
        "rx_power": 37.6868419191283
      },
      {
        "tower_id": "O",
        "rx_power": 26.8690132176806
      }
    ]
  },
  {
    "id": "drone-04",
    "signals": [
      {
        "tower_id": "A",
        "rx_power": 12.194243298574
      },
      {
        "tower_id": "B",
        "rx_power": 29.893469580698
      },
      {
        "tower_id": "C",
        "rx_power": 12.2789099239468
      },
      {
        "tower_id": "F",
        "rx_power": 29.0956057257888
      },
      {
        "tower_id": "H",
        "rx_power": 19.5317086585292
      },
      {
        "tower_id": "I",
        "rx_power": 19.5317086585292
      },
      {
        "tower_id": "J",
        "rx_power": 18.4419960683248
      },
      {
        "tower_id": "K",
        "rx_power": 20.5624857792912
      },
      {
        "tower_id": "L",
        "rx_power": 21.9324635443913
      },
      {
        "tower_id": "M",
        "rx_power": 23.5342732247535
      },
      {
        "tower_id": "N",
        "rx_power": 58.6672853487751
      },
      {
        "tower_id": "O",
        "rx_power": 27.2781805940989
      }
    ]
  },
  {
    "id": "drone-05",
    "signals": [
      {
        "tower_id": "A",
        "rx_power": 12.6167747773437
      },
      {
        "tower_id": "B",
        "rx_power": 30.706199327829
      },
      {
        "tower_id": "F",
        "rx_power": 33.6113704350997
      },
      {
        "tower_id": "H",
        "rx_power": 20.8221389953753
      },
      {
        "tower_id": "I",
        "rx_power": 20.8221389953753
      },
      {
        "tower_id": "J",
        "rx_power": 19.570865536715
      },
      {
        "tower_id": "K",
        "rx_power": 21.9819386784897
      },
      {
        "tower_id": "L",
        "rx_power": 23.5925756872029
      },
      {
        "tower_id": "M",
        "rx_power": 25.5138861461249
      },
      {
        "tower_id": "N",
        "rx_power": 36.2132275511936
      },
      {
        "tower_id": "O",
        "rx_power": 26.756254938814
      }
    ]
  },
  {
    "id": "drone-06",
    "signals": [
      {
        "tower_id": "A",
        "rx_power": 10.9064173895266
      },
      {
        "tower_id": "B",
        "rx_power": 27.7213010142499
      },
      {
        "tower_id": "F",
        "rx_power": 40.0546172173205
      },
      {
        "tower_id": "H",
        "rx_power": 23.9523127883621
      },
      {
        "tower_id": "I",
        "rx_power": 23.9523127883621
      },
      {
        "tower_id": "J",
        "rx_power": 22.2146181183932
      },
      {
        "tower_id": "K",
        "rx_power": 25.4221325176808
      },
      {
        "tower_id": "L",
        "rx_power": 27.7235763528884
      },
      {
        "tower_id": "M",
        "rx_power": 30.4156627469648
      },
      {
        "tower_id": "N",
        "rx_power": 27.3042189482108
      },
      {
        "tower_id": "O",
        "rx_power": 24.2779316758612
      }
    ]
  }
]

towerData = [
    { "id": "A", "position": { "x": 20, "y": 80 }, "tx_power": 45 },
    { "id": "B", "position": { "x": 70, "y": 30 }, "tx_power": 60 },
    { "id": "C", "position": { "x": 90, "y": 90 }, "tx_power": 45 },
    { "id": "D", "position": { "x": 0, "y": 120 }, "tx_power": 45 },
    { "id": "E", "position": { "x": 130, "y": 110 }, "tx_power": 45 },
    { "id": "F", "position": { "x": 30, "y": 40 }, "tx_power": 60 },
    { "id": "G", "position": { "x": 160, "y": 80 }, "tx_power": 45 },
    { "id": "H", "position": { "x": -10, "y": -20 }, "tx_power": 60 },
    { "id": "I", "position": { "x": -10, "y": -20 }, "tx_power": 60 },
    { "id": "J", "position": { "x": -20, "y": -30 }, "tx_power": 60 },
    { "id": "K", "position": { "x": 10, "y": -20 }, "tx_power": 60 },
    { "id": "L", "position": { "x": 20, "y": -10 }, "tx_power": 60 },
    { "id": "M", "position": { "x": 30, "y": 0 }, "tx_power": 60 },
    { "id": "N", "position": { "x": 60, "y": 60 }, "tx_power": 60 },
    { "id": "O", "position": { "x": 90, "y": 30 }, "tx_power": 60 }
]

def get_tx_power(tower_id, data):
    for tower in data:
        if tower["id"] == tower_id:
            return tower["tx_power"]
    return None

def get_tower_pos(tower_id, data):
    for tower in data:
        if tower["id"] == tower_id:
            return tower["position"]

def main(drone_status):
    tower_data_formatted = {}

    for drone in drone_status:
        if drone["id"] == "drone-04":
            for tower in drone["signals"]:
                transmit_power = get_tx_power(tower["tower_id"], towerData)
                tower_data_formatted[tower["tower_id"]] = {
                    "distance": 10 ** ((transmit_power - tower["rx_power"]) / 20),
                    "position": get_tower_pos(tower["tower_id"], towerData)
                }
    print(tower_data_formatted)

    positions = [(v["position"]["x"], v["position"]["y"]) for v in tower_data_formatted.values()]
    distances = [v["distance"] for v in tower_data_formatted.values()]

    def cost(x, y):
        """Sum of squared errors between predicted and measured distances"""
        err = 0.0
        for (px, py), d in zip(positions, distances):
            predicted = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
            err += (predicted - d) ** 2
        return err

    # Start at centroid
    x: float = sum(px for px, _ in positions) / len(positions)
    y: float = sum(py for _, py in positions) / len(positions)

    # Simple gradient descent
    lr = 0.01  # learning rate
    for _ in range(5000):  # iterations
        grad_x = grad_y = 0.0
        for (px, py), d in zip(positions, distances):
            dx = x - px
            dy = y - py
            dist = (dx * dx + dy * dy) ** 0.5 + 1e-9
            diff = dist - d
            grad_x += 2 * diff * (dx / dist)
            grad_y += 2 * diff * (dy / dist)
        x -= lr * grad_x
        y -= lr * grad_y

    print(f"Estimated drone position: ({x}, {y})")
    print(f"Final cost: {cost(x, y):.6f}")

    return {
        "x": x,
        "y": y
        }


if __name__ == "__main__":
    main(drone_status)

