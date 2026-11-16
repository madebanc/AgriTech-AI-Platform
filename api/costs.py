"""
AgriTech AI Platform — Farm Cost Tracker Storage
Day 25 of 365. Offline first money book for Nigerian farmers.
"""

import json
import os
import uuid
from datetime import datetime

COSTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "costs_data.json")

ALLOWED_KINDS = ["spent", "earned"]
ALLOWED_CATEGORIES = [
    "seed",
    "fertilizer",
    "labour",
    "spray",
    "transport",
    "sales",
    "other",
]

def _now_iso():
    return datetime.utcnow().isoformat() + "Z"

def load_records():
    if not os.path.exists(COSTS_FILE):
        return []
    try:
        with open(COSTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, OSError):
        return []

def save_records(records):
    with open(COSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

def add_record(payload):
    records = load_records()
    kind = str(payload.get("kind", "spent")).strip().lower()[:10]
    if kind not in ALLOWED_KINDS:
        kind = "spent"
    category = str(payload.get("category", "other")).strip().lower()[:20]
    if category not in ALLOWED_CATEGORIES:
        category = "other"
    try:
        amount = float(payload.get("amount", 0) or 0)
    except (TypeError, ValueError):
        amount = 0
    if amount < 0:
        amount = 0
    entry = {
        "id": str(uuid.uuid4())[:8],
        "farmer_name": str(payload.get("farmer_name", "")).strip()[:80],
        "farm_name": str(payload.get("farm_name", "")).strip()[:80],
        "crop": str(payload.get("crop", "Cassava")).strip()[:40],
        "kind": kind,
        "category": category,
        "amount": round(amount, 2),
        "record_date": str(payload.get("record_date", "")).strip()[:20],
        "notes": str(payload.get("notes", "")).strip()[:500],
        "source": str(payload.get("source", "online")).strip()[:20],
        "created_at": _now_iso(),
    }
    if not entry["farm_name"]:
        entry["farm_name"] = "My Farm"
    if not entry["record_date"]:
        entry["record_date"] = datetime.utcnow().strftime("%Y-%m-%d")
    records.insert(0, entry)
    save_records(records)
    return entry

def get_records(limit=200):
    records = load_records()
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 200
    limit = max(1, min(limit, 500))
    return records[:limit]

def delete_record(record_id):
    records = load_records()
    kept = [r for r in records if r.get("id") != record_id]
    if len(kept) == len(records):
        return False
    save_records(kept)
    return True

def get_costs_stats():
    records = load_records()
    total_spent = 0.0
    total_earned = 0.0
    by_category = {}
    for r in records:
        amt = float(r.get("amount", 0) or 0)
        if r.get("kind") == "earned":
            total_earned += amt
        else:
            total_spent += amt
        c = r.get("category", "other")
        by_category[c] = round(by_category.get(c, 0) + amt, 2)
    return {
        "total_records": len(records),
        "total_spent": round(total_spent, 2),
        "total_earned": round(total_earned, 2),
        "balance": round(total_earned - total_spent, 2),
        "by_category": by_category,
    }