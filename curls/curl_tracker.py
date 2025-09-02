import os, time, json, math
import requests

API_URL_TOWERS = os.getenv("API_URL_TOWERS", "https://selection-drone.charginglead.workers.dev/towers")
API_URL_TARGETS = os.getenv("API_URL_TARGETS", "https://selection-drone.charginglead.workers.dev/target")
API_URL_STATUS = os.getenv("API_URL_STATUS", "https://selection-drone.charginglead.workers.dev/status")


OUTPUT_JSON_PATH = "curl_positions.json"


