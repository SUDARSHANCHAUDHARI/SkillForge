
import json
import os

DEFAULTS = {
    "path": "./skills",
    "threshold": 0.8,
    "ignore": [],
}

RC_FILE = ".skillforgerc"


def load_config() -> dict:
    config = DEFAULTS.copy()
    rc_path = os.path.join(os.getcwd(), RC_FILE)
    if os.path.isfile(rc_path):
        try:
            with open(rc_path, encoding="utf-8") as f:
                overrides = json.load(f)
            config.update(overrides)
        except (OSError, json.JSONDecodeError) as e:
            print(f"⚠ Could not read {RC_FILE}: {e}")
    return config
