
import time, json, os, requests
TOWERS_URL  = "https://selection-drone.charginglead.workers.dev/towers"
TARGETS_URL = "https://selection-drone.charginglead.workers.dev/target"
STATUS_URL  = "https://selection-drone.charginglead.workers.dev/status"

TOKEN = os.getenv("API_TOKEN", "Bearer sait-selection-2025")

OUTPUT_JSON_PATH = "curl_snapshot.json"

POLL_PERIOD_SEC = 2.0


def fetch(url: str, token: str | None = None) -> dict | list:
    headers = {"Authorization": token} if token else {}
    r = requests.get(url, headers=headers, timeout=8)
    r.raise_for_status()
    return r.json()


def main():
    print(f"Polling every {POLL_PERIOD_SEC}s → {OUTPUT_JSON_PATH}")
    while True:
        loop_start = time.time()
        try:
            towers  = fetch(TOWERS_URL, TOKEN)
            targets = fetch(TARGETS_URL, TOKEN)
            status  = fetch(STATUS_URL, TOKEN)

            snapshot = {
                "ts": time.time(),
                "towers": towers,
                "targets": targets,
                "status": status,
            }

            with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(snapshot, f, ensure_ascii=False, indent=2)

            print(f"[OK] Snapshot written at {time.ctime()}")
        except Exception as e:
            print("[ERR]", e)

        elapsed = time.time() - loop_start
        time.sleep(max(0.0, POLL_PERIOD_SEC - elapsed))


if __name__ == "__main__":
    main()
