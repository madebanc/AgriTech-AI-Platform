"""
AgriTech AI Platform — Farm Activity Log Storage
Day 24 of 365. Offline first activity log for Nigerian farmers.
"""

import json
import os
import uuid
from datetime import datetime

ACTIVITY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "activity_data.json")

ALLOWED_TYPES = [
    "planted",
    "weeded",
    "sprayed",
    "fertilised",
    "harvested",
    "irrigated",
    "note",
]


def _now_iso():
    return datetime.utcnow().isoformat() + "Z"


def load_activities():
    if not os.path.exists(ACTIVITY_FILE):
        return []
    try:
        with open(ACTIVITY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, OSError):
        return []


def save_activities(activities):
    with open(ACTIVITY_FILE, "w", encoding="utf-8") as f:
        json.dump(activities, f, indent=2, ensure_ascii=False)


def add_activity(payload):
    activities = load_activities()
    activity_type = str(payload.get("activity_type", "note")).strip().lower()[:20]
    if activity_type not in ALLOWED_TYPES:
        activity_type = "note"
    entry = {
        "id": str(uuid.uuid4())[:8],
        "farmer_name": str(payload.get("farmer_name", "")).strip()[:80],
        "farm_name": str(payload.get("farm_name", "")).strip()[:80],
        "crop": str(payload.get("crop", "Cassava")).strip()[:40],
        "activity_type": activity_type,
        "activity_date": str(payload.get("activity_date", "")).strip()[:20],
        "quantity": str(payload.get("quantity", "")).strip()[:80],
        "notes": str(payload.get("notes", "")).strip()[:500],
        "source": str(payload.get("source", "online")).strip()[:20],
        "created_at": _now_iso(),
    }
    if not entry["farm_name"]:
        entry["farm_name"] = "My Farm"
    if not entry["activity_date"]:
        entry["activity_date"] = datetime.utcnow().strftime("%Y-%m-%d")
    activities.insert(0, entry)
    save_activities(activities)
    return entry


def get_activities(limit=100):
    activities = load_activities()
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 100
    limit = max(1, min(limit, 200))
    return activities[:limit]


def delete_activity(activity_id):
    activities = load_activities()
    kept = [a for a in activities if a.get("id") != activity_id]
    if len(kept) == len(activities):
        return False
    save_activities(kept)
    return True


def get_activity_stats():
    activities = load_activities()
    by_type = {}
    for a in activities:
        t = a.get("activity_type", "note")
        by_type[t] = by_type.get(t, 0) + 1
    return {
        "total_activities": len(activities),
        "by_type": by_type,
    }