import os, time, json, math
import requests

API_URL_TOWERS = os.getenv("API_URL_TOWERS", "https://selection-drone.charginglead.workers.dev/towers")
API_URL_TARGETS = os.getenv("API_URL_TARGETS", "https://selection-drone.charginglead.workers.dev/target")
API_URL_STATUS = os.getenv("API_URL_STATUS", "https://selection-drone.charginglead.workers.dev/status")


OUTPUT_JSON_PATH = "curl_positions.json"

#!/usr/bin/env python3
import os, time, json, math, requests
import numpy as np

API_URL_TOWERS = os.getenv("API_URL_TOWERS", "https://selection-drone.charginglead.workers.dev/towers")
API_URL_TARGETS = os.getenv("API_URL_TARGETS", "https://selection-drone.charginglead.workers.dev/target")
API_URL_STATUS  = os.getenv("API_URL_STATUS",  "https://selection-drone.charginglead.workers.dev/status")
MIN_RX_DB = 10.0
N = 2.0                # path-loss exponent per your model
POLL_SEC = 1


def estimate_position(towers, readings, n=2.0, max_iter=30, tol=1e-6):
    t_by_id = {str(t["id"]): t for t in towers}
    xs, ys, ds, w = [], [], [], []
    used_ids = []
    for r in readings:
        if float(r["rx_db"]) < MIN_RX_DB:
            continue
        tid = str(r["id"])
        if tid not in t_by_id: 
            continue
        t = t_by_id[tid]
        pt = float(t.get("tx_db", t.get("transmit_power")))
        d  = rx_to_range(pt, float(r["rx_db"]), n=n)
        xs.append(float(t["x"])); ys.append(float(t["y"])); ds.append(d)
        # weight higher RSSI more
        w.append(10.0**(float(r["rx_db"])/10.0))
        used_ids.append(tid)
    if len(ds) < 3:
        raise RuntimeError(f"Need ≥3 towers ≥{MIN_RX_DB} dB; got {len(ds)}")
    xs, ys, ds, w = map(np.array, (xs, ys, ds, w))
    W = np.diag(w / max(w.max(), 1e-9))

    # initial guess: inverse-distance weighted centroid
    w0 = 1.0 / np.maximum(ds, 1e-6)
    x = float(np.average(xs, weights=w0)); y = float(np.average(ys, weights=w0))

    for _ in range(max_iter):
        dx, dy = x - xs, y - ys
        ri = np.hypot(dx, dy); ri = np.where(ri < 1e-6, 1e-6, ri)
        res = ri - ds
        J = np.column_stack((dx/ri, dy/ri))
        JT_W = J.T @ W
        H = JT_W @ J
        g = JT_W @ res
        try:
            step = -np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            step = -np.linalg.solve(H + 1e-6*np.eye(2), g)
        x_new, y_new = x + step[0], y + step[1]
        if math.hypot(x_new - x, y_new - y) < tol:
            x, y = x_new, y_new; break
        x, y = x_new, y_new

    dx, dy = x - xs, y - ys
    ri = np.hypot(dx, dy)
    rmse = float(np.sqrt(np.mean((ri - ds)**2)))
    return {"x": float(x), "y": float(y), "rmse": rmse, "used_ids": used_ids}

def fetch_json(url):
    r = requests.get(url, timeout=10); r.raise_for_status(); return r.json()

def parse_towers(j):
    arr = j.get("towers", j)
    out = []
    for t in arr:
        out.append({
            "id": str(t.get("id") or t.get("tower_id")),
            "x": float(t["x"]), "y": float(t["y"]),
            "tx_db": float(t.get("tx_db", t.get("transmit_power")))
        })
    return out

def parse_status_groups(j):
    """Return dict {drone_id: [ {id, rx_db}, ... ] } from flexible schemas."""
    if isinstance(j, dict) and "readings" in j:
        groups = {}
        for r in j["readings"]:
            did = str(r.get("drone_id","unknown"))
            groups.setdefault(did, []).append({"id": str(r["id"]), "rx_db": float(r["rx_db"])})
        return groups
    if isinstance(j, dict) and "drones" in j:
        groups = {}
        for d in j["drones"]:
            did = str(d["id"])
            groups[did] = [{"id": str(r["id"]), "rx_db": float(r["rx_db"])} for r in d.get("readings",[])]
        return groups
    if isinstance(j, list):
        return {"unknown": [{"id": str(r["id"]), "rx_db": float(r["rx_db"])} for r in j]}
    return {}

def rx_to_range(tx_db, rx_db, n=2.0):
    """
    Estimate distance from transmit and received power using the path-loss model:
    rx_db = tx_db - 10 * n * log10(d)
    => d = 10 ** ((tx_db - rx_db) / (10 * n))
    """
    return 10 ** ((tx_db - rx_db) / (10.0 * n))

def bearing_deg(dx, dy):
    # 0° = +x (east), increases counterclockwise
    ang = math.degrees(math.atan2(dy, dx))
    return (ang + 360.0) % 360.0

def main():
    towers = parse_towers(fetch_json(API_URL_TOWERS))
    print(f"Loaded {len(towers)} towers")

    while True:
        try:
            target = fetch_json(API_URL_TARGETS)  # expect {x, y} or {target:{x,y}}
            tgt = target.get("target", target)
            tx, ty = float(tgt["x"]), float(tgt["y"])

            status = fetch_json(API_URL_STATUS)
            groups = parse_status_groups(status)
            if not groups:
                print("No readings yet.")
                time.sleep(POLL_SEC); continue

            for drone_id, readings in groups.items():
                try:
                    est = estimate_position(towers, readings, n=N)
                    dx = tx - est["x"]; dy = ty - est["y"]
                    dist = math.hypot(dx, dy)
                    brg  = bearing_deg(dx, dy)
                    print(f"[{time.strftime('%H:%M:%S')}] {drone_id}: "
                          f"pos=({est['x']:.2f},{est['y']:.2f})±{est['rmse']:.2f}  "
                          f"→ target Δ=({dx:.2f},{dy:.2f})  dist={dist:.2f}  bearing={brg:.1f}°  "
                          f"towers={','.join(est['used_ids'])}")
                except Exception as e:
                    print(f"[{time.strftime('%H:%M:%S')}] {drone_id}: unable to localize — {e}")
        except Exception as e:
            print(f"Fetch error: {e}")

        time.sleep(POLL_SEC)

if __name__ == "__main__":
    main()
