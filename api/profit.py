"""AgriTech AI — Profit Calculator (Day 26 of 365).

Combines recorded farm expenses with expected yield and selling price to
calculate profit or loss per crop.  All monetary values are in Nigerian Naira.
"""

import json
import os
from datetime import datetime, timezone

DATA_FILE = os.path.join(os.path.dirname(__file__), "expenses_data.json")

# Estimated market prices per kg for Nigerian crops (₦/kg).  These are
# rough 2026 averages for fresh produce in local markets; the user can
# override any value from the frontend.
MARKET_PRICES = {
    "Cassava": 200,
    "Maize": 300,
    "Yam": 500,
    "Rice": 600,
    "Groundnut": 700,
    "Cocoa": 2500,
}

CROPS = ["Cassava", "Maize", "Yam", "Rice", "Groundnut", "Cocoa"]


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def get_expense_totals_by_crop():
    """Return a dict mapping crop name -> total expense amount in naira."""
    expenses = load_expenses()
    totals = {}
    for e in expenses:
        crop = e.get("crop", "Unknown")
        amount = float(e.get("amount_ngn", 0) or 0)
        totals[crop] = totals.get(crop, 0) + amount
    return totals


def calculate_profit(crop, yield_kg, price_per_kg, total_cost):
    """Calculate profit metrics for a single crop.

    Returns a dict with revenue, cost, profit, profit_margin_pct, and
    a human-readable verdict.
    """
    yield_kg = float(yield_kg or 0)
    price_per_kg = float(price_per_kg or 0)
    total_cost = float(total_cost or 0)

    revenue = yield_kg * price_per_kg
    profit = revenue - total_cost
    margin = (profit / revenue * 100) if revenue > 0 else 0.0

    if revenue == 0 and total_cost == 0:
        verdict = "No data yet"
    elif profit > 0:
        verdict = "Profit"
    elif profit < 0:
        verdict = "Loss"
    else:
        verdict = "Break even"

    return {
        "crop": crop,
        "yield_kg": round(yield_kg, 2),
        "price_per_kg": round(price_per_kg, 2),
        "revenue": round(revenue, 2),
        "total_cost": round(total_cost, 2),
        "profit": round(profit, 2),
        "profit_margin_pct": round(margin, 2),
        "verdict": verdict,
    }


def get_profit_summary():
    """Return expense totals grouped by crop plus market price reference."""
    totals = get_expense_totals_by_crop()
    rows = []
    for crop in CROPS:
        cost = totals.get(crop, 0)
        rows.append({
            "crop": crop,
            "total_cost": round(cost, 2),
            "market_price_per_kg": MARKET_PRICES.get(crop, 0),
        })
    # Include any crops in expenses that aren't in the standard list
    for crop, cost in totals.items():
        if crop not in CROPS:
            rows.append({
                "crop": crop,
                "total_cost": round(cost, 2),
                "market_price_per_kg": 0,
            })
    return {
        "success": True,
        "crops": rows,
        "market_prices": MARKET_PRICES,
        "total_expenses": round(sum(totals.values()), 2),
        "generated_at": _now_iso(),
    }