"""
expenses.py — Day 25: Farm Cost Tracker
Author : Daniel Oyanogbezina
Stores farm expenses in expenses_data.json
Also provides a spend summary for the cost tracker page.
"""
import json
import os
import uuid
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "expenses_data.json")

CATEGORIES = [
    "seeds", "fertilizer", "pesticide", "labour",
    "fuel", "irrigation", "transport", "storage", "other",
]


def _now_iso():
    return datetime.datetime.now().isoformat()


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_expenses(entries):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def add_expense(body):
    if not isinstance(body, dict):
        raise ValueError("Expense must be a JSON object")
    amount = body.get("amount_ngn", body.get("amount"))
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError("amount must be a number")
    if amount <= 0:
        raise ValueError("amount must be greater than zero")
    category = str(body.get("category", "other")).strip().lower()
    if category not in CATEGORIES:
        category = "other"
    entry = {
        "id": uuid.uuid4().hex[:8],
        "farmer_name": str(body.get("farmer_name", "")).strip(),
        "farm_name": str(body.get("farm_name", "My Farm")).strip() or "My Farm",
        "crop": str(body.get("crop", "")).strip(),
        "category": category,
        "item": str(body.get("item", "")).strip(),
        "amount_ngn": amount,
        "expense_date": str(
            body.get("expense_date") or datetime.date.today().isoformat()
        ),
        "notes": str(body.get("notes", "")).strip(),
        "created_at": _now_iso(),
    }
    entries = load_expenses()
    entries.insert(0, entry)
    save_expenses(entries)
    return entry


def get_expenses(limit=100):
    entries = load_expenses()
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 100
    return entries[:max(1, min(limit, 500))]


def delete_expense(entry_id):
    entries = load_expenses()
    kept = [e for e in entries if e.get("id") != entry_id]
    if len(kept) == len(entries):
        return False
    save_expenses(kept)
    return True


def get_expense_stats(entries=None):
    entries = load_expenses() if entries is None else entries
    total = 0.0
    by_category = {}
    for e in entries:
        amount = float(e.get("amount_ngn", 0) or 0)
        total += amount
        cat = e.get("category", "other")
        by_category[cat] = round(by_category.get(cat, 0) + amount, 2)
    return {
        "total_spent_ngn": round(total, 2),
        "entry_count": len(entries),
        "by_category": by_category,
        "categories": CATEGORIES,
    }