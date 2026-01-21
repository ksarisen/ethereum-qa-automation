import os
import json
import random
from datetime import datetime
from zoneinfo import ZoneInfo
from hexbytes import HexBytes

from src.logger import logger

def generate_random_amount(min_eth, max_eth):
    amount = round(random.uniform(min_eth, max_eth), 6)

    return amount

def save_artifact(artifact: dict, folder="artifacts"):
    os.makedirs("artifacts", exist_ok = True)
    filename = f"artifacts/tx_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, "w") as f:
        json.dump(artifact, f, indent = 2)

    logger.info(f"Artifact saved: {filename}")

def is_duplicate_tx(tx_hash, folder="artifacts"):
    if not os.path.exists(folder):
        return False

    for file in os.listdir(folder):
        if not file.endswith(".json"):
            continue

        try:
            with open(os.path.join(folder, file)) as f:
                data = json.load(f)
                if data.get("tx_hash") == tx_hash:
                    return True
        except:
            continue

    return False

def get_timestamp_tr():
    return datetime.now(ZoneInfo("Europe/Istanbul")).isoformat()

def normalize_for_json(obj):
    if isinstance(obj, HexBytes):
        return obj.hex()
    elif isinstance(obj, dict):
        return {k: normalize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [normalize_for_json(i) for i in obj]
    else:
        return obj
