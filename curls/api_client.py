from typing import Any, Dict, Optional
import requests

DEFAULT_TIMEOUT = 8.0

class APIError(RuntimeError):
    pass

def _headers(token: Optional[str]) -> Dict[str, str]:
    return {"Authorization": token} if token else {}

def fetch_json(url: str, token: Optional[str] = None, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    try:
        resp = requests.get(url, headers=_headers(token), timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, dict):
            raise APIError(f"Expected JSON object at {url}, got {type(data).__name__}")
        return data
    except requests.RequestException as e:
        raise APIError(f"HTTP error for {url}: {e}") from e
    except ValueError as e:
        raise APIError(f"Invalid JSON from {url}: {e}") from e

def get_towers(url: str, token: Optional[str] = None, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    data = fetch_json(url, token, timeout)
    if "towers" not in data:
        raise APIError(f"'towers' key missing from {url}")
    return data

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
