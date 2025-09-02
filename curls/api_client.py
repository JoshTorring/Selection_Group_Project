from typing import Any, Dict, Optional
import requests

DEFAULT_TIMEOUT = 8.0

class APIError(RuntimeError):
    pass

def _headers(token: Optional[str]) -> Dict[str, str]:
    return {"Authorization": token} if token else {}

def fetch_json(url: str, token: Optional[str] = None, timeout: float = DEFAULT_TIMEOUT):
    try:
        resp = requests.get(url, headers=_headers(token), timeout=timeout)
        resp.raise_for_status()
        return resp.json()  # may be dict OR list
    except requests.RequestException as e:
        raise APIError(f"HTTP error for {url}: {e}") from e
    except ValueError as e:
        raise APIError(f"Invalid JSON from {url}: {e}") from e

def get_towers(url: str, token: Optional[str] = None, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    data = fetch_json(url, token, timeout)

    if isinstance(data, dict) and "towers" in data:
        return data

    if isinstance(data, list):
        towers_dict: Dict[str, Dict[str, float]] = {}
        for i, t in enumerate(data):
            if not isinstance(t, dict):
                continue
            tid = str(t.get("id") or t.get("tower_id") or t.get("name") or f"T{i}")
            x = t.get("x", t.get("X", t.get("lon", t.get("lng"))))
            y = t.get("y", t.get("Y", t.get("lat")))
            pt = t.get("pt_db", t.get("tx_db", t.get("power", t.get("pt"))))
            if x is not None and y is not None and pt is not None:
                towers_dict[tid] = {"x": float(x), "y": float(y), "pt_db": float(pt)}
        if not towers_dict:
            raise APIError(f"Couldn't normalize towers list from {url}")
        return {"towers": towers_dict}

    raise APIError(f"Unexpected towers payload type from {url}: {type(data).__name__}")

def get_targets(url: str, token: Optional[str] = None, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    data = fetch_json(url, token, timeout)
    if not any(k in data for k in ("target", "targets")):
        raise APIError(f"No 'target' or 'targets' field in {url}")
    return data

def get_status(url: str, token: Optional[str] = None, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    data = fetch_json(url, token, timeout)
    if "drones" not in data:
        raise APIError(f"'drones' key missing from {url}")
    return data

def get_all(towers_url: str, targets_url: str, status_url: str,
            token: Optional[str] = None, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    towers = get_towers(towers_url, token, timeout)
    targets = get_targets(targets_url, token, timeout)
    status  = get_status(status_url,  token, timeout)
    return {"towers": towers, "targets": targets, "status": status}
