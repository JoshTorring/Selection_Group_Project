import time, json, os, tempfile
from api_client import get_all, APIError

TOWERS_URL  = "https://selection-drone.charginglead.workers.dev/towers"
TARGETS_URL = "https://selection-drone.charginglead.workers.dev/target"
STATUS_URL  = "https://selection-drone.charginglead.workers.dev/status"


TOKEN = os.getenv("Sait-Selection-2025", None)  

OUTPUT_JSON_PATH = "curl_positions.json"

POLL_PERIOD_SEC = 2.0


def write_snapshot(snapshot: dict, path: str):
    """Atomically write snapshot dict to JSON file."""
    dir_ = os.path.dirname(path) or "."
    with tempfile.NamedTemporaryFile("w", delete=False, dir=dir_, encoding="utf-8") as tmp:
        json.dump(snapshot, tmp, ensure_ascii=False, indent=2)
        tmp_path = tmp.name
    os.replace(tmp_path, path)


def main():
    print(f"Polling API every {POLL_PERIOD_SEC}s → writing {OUTPUT_JSON_PATH}")

    while True:
        loop_start = time.time()
        try:
            snapshot = get_all(TOWERS_URL, TARGETS_URL, STATUS_URL, token=TOKEN)

            snapshot["ts"] = time.time()

            write_snapshot(snapshot, OUTPUT_JSON_PATH)

            print(f"[OK] snapshot written with {len(snapshot.get('status', {}).get('drones', []))} drones")
        except APIError as e:
            print("API failure:", e)

        elapsed = time.time() - loop_start
        time.sleep(max(0.0, POLL_PERIOD_SEC - elapsed))


if __name__ == "__main__":
    main()
