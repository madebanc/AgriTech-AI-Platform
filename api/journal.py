"""
AgriTech AI Platform — Farm Journal Storage
Day 13 of 365. Offline first journal for Nigerian farmers.

Each entry is one farm record saved by a farmer.
Phone stores entries in localStorage when offline,
then syncs them here when online. No old code is changed.
"""

import json
import os
import uuid
from datetime import datetime

JOURNAL_FILE = os.path.join(os.path.dirname(__file__), "journal_data.json")


def _now_iso():
    return datetime.utcnow().isoformat() + "Z"


def load_entries():
    if not os.path.exists(JOURNAL_FILE):
        return []
    try:
        with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_entries(entries):
    with open(JOURNAL_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def add_entry(payload):
    entries = load_entries()
    entry = {
        "id": str(uuid.uuid4())[:8],
        "farmer_name": str(payload.get("farmer_name", "")).strip()[:80],
        "farm_name": str(payload.get("farm_name", "")).strip()[:80],
        "crop": str(payload.get("crop", "Cassava")).strip()[:40],
        "state": str(payload.get("state", "")).strip()[:40],
        "size_hectares": float(payload.get("size_hectares", 0) or 0),
        "planting_date": str(payload.get("planting_date", "")).strip()[:20],
        "notes": str(payload.get("notes", "")).strip()[:500],
        "prediction_id": str(payload.get("prediction_id", "")).strip()[:40],
        "source": str(payload.get("source", "online")).strip()[:20],
        "created_at": _now_iso(),
    }
    if not entry["farm_name"]:
        entry["farm_name"] = "My Farm"
    if entry["size_hectares"] < 0:
        entry["size_hectares"] = 0
    entries.insert(0, entry)
    save_entries(entries)
    return entry


def get_entries(limit=50):
    entries = load_entries()
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 50
    limit = max(1, min(limit, 200))
    return entries[:limit]


def delete_entry(entry_id):
    entries = load_entries()
    kept = [e for e in entries if e.get("id") != entry_id]
    if len(kept) == len(entries):
        return False
    save_entries(kept)
    return True


def get_stats():
    entries = load_entries()
    crops = {}
    for e in entries:
        crop = e.get("crop", "Unknown")
        crops[crop] = crops.get(crop, 0) + 1
    return {
        "total_entries": len(entries),
        "by_crop": crops,
    }