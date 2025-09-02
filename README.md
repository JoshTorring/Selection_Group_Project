# Drone 4 - SAIT Selection Group Project

# Group Challenge

<img width="959" height="914" alt="image" src="https://github.com/user-attachments/assets/909da1d9-40e9-4927-bf83-ef482a153826" />

## Outline

You are given a highly important mission to hit a target with a series of one way attack drones. The drones are operating in a highly communications and GNSS denied environment. 
You have been given an API that receives short burst data from the drones and can be sent commands, you have been asked to implement a mission planning tool that:

  - Tracks the current position of one or more drones.
  
  - Works out the next heading the drone(s) should fly in order to reach their target.
  
  - Drops the payload accurately once the target is reached.
  
  - Produces a visualisation of the drone’s flight path over time.

We’re not just looking for code — we’re looking for how you:

  - Approach a problem with incomplete information
  
  - Break down and assign tasks as a team
  
  - Communicate your solution clearly

## Simulation Environment

The world is a simple 2D map with x and y coordinates.

Altitude is ignored — you only need to plan movements in 2D space.

Drones update their position on each status check, you can command the drone by giving it a heading and speed value. The heading will drift over time due to inteference so make sure you keep updating it.

Once you think you're near the target send the drone the drop payload command. You will then receive a score and battle damage assessment from J2

The target location can be retrieved via the api, the target will change during the challenge so make sure you keep checking it.

Cell towers are also placed on the map and provide a signal strength value depending on the drone’s distance.

## Cell Tower Power Calculation

Each tower broadcasts a signal, and the signal power from a tower is calculated as:

Received power = Transmit Power - (10 x 2.0 x log10(distance from the drone)

receive_power ​= transmit_power - (10 * 2.0 * math.log10(distance))

Where:
P_received = received power (dB)
P_transmit = transmit power (dB)
d = distance between the tower and the drone

You will be given the cell towers locations and known transmit powers, you need to use these to work out the drones location.

Drones only report towers with receive powers above 10 dB

## API

### /towers -> returns list of cell towers, locations and transmit powers

    { id: "A", position: { x: 20, y: 80 }, tx_power: 45 },
    { id: "B", position: { x: 70, y: 30 }, tx_power: 60 },
    { id: "C", position: { x: 90, y: 90 }, tx_power: 45 },
    { id: "D", position: { x: 0, y: 120 }, tx_power: 45 },
    { id: "E", position: { x: 130, y: 110 }, tx_power: 45 },
    { id: "F", position: { x: 30, y: 40 }, tx_power: 60 },
    { id: "G", position: { x: 160, y: 80 }, tx_power: 45 },
    { id: "H", position: { x: -10, y: -20 }, tx_power: 60 },
    { id: "I", position: { x: -10, y: -20 }, tx_power: 60 },
    { id: "J", position: { x: -20, y: -30 }, tx_power: 60 },
    { id: "K", position: { x: 10, y: -20 }, tx_power: 60 },
    { id: "L", position: { x: 20, y: -10 }, tx_power: 60 },
    { id: "M", position: { x: 30, y: 0 }, tx_power: 60 },
    { id: "N", position: { x: 60, y: 60 }, tx_power: 60 },
    { id: "O", position: { x: 90, y: 30 }, tx_power: 60 }

### /target -> returns the current target location

i.e

curl --location 'https://selection-drone.charginglead.workers.dev/target'

response:
    
    {
        "x": 111,
        "y": 101
    }

### /status → returns the current drones states and tower signals they can see

  i.e

  curl --location 'https://selection-drone.charginglead.workers.dev/status'

  response:

    [
      {
          "id": "drone-01",
          "signals": [
              {
                  "tower_id": "A",
                  "rx_power": 12.447274948966943
              },
              {
                  "tower_id": "B",
                  "rx_power": 30.969100130080562
              }
          ]
      }
    ]

### /command → send a new heading and/or speed for the drone. The max speed for the drone is 1, the minimum speed is 0.1. The heading is between 0 and 360 with 0 being north or positive on the y axis

  i.e
  
  curl --location --request GET 'https://selection-drone.charginglead.workers.dev/command' \
  --header 'Content-Type: application/json' \
  --data '{
      "id": "drone-01",
      "heading": 90,
      "speed": 0.4
  }'

  response:

  HTTP 200 "Command accepted"

### /reset?drone_id=<DRONE_ID>  → reset the drone to the original start point

  i.e

  curl --location 'https://selection-drone.charginglead.workers.dev/reset?drone_id=drone-01'

  response:

  HTTP 200 "Drone reset"

### /drop?drone_id=<DRONE_ID> -> Commands the drone specified to drop the payload

  i.e:

  curl --location 'https://selection-drone.charginglead.workers.dev/drop?drone_id=drone-01'

  response:

    {"drop_location":{"x":79.44554435175532,"y":86.39037881475089},"distance_to_target":3.6063545229002467,"score":48613,"bda":"Eh I guess it'll do"}
      
    
