"""
app.py — AgriTech AI Platform
Author : Daniel Oyanogbezina
Day 11 : Added /api/diseases endpoints
Day 13 : Added /api/journal endpoints, offline first farm journal
Day 24 : Added /api/activity endpoints, offline first farm activity log
Day 25 : Added /api/expenses endpoints, offline first cost tracker
Day 26 : Added /api/profit endpoints, profit calculator
"""

import sys
import os
import urllib.request
import json as json_lib
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS

from advisory import (
    SUPPORTED_CROPS,
    CROP_ADVICE,
    get_calendar,
    MONTH_NAMES,
    NIGERIAN_STATES,
    REGION_RAINFALL,
    get_state_list,
    CROP_DISEASES,
    SEVERITY_COLORS,
    get_diseases,
    get_all_diseases,
)
from predictor import predict_and_advise, MODEL_LOADED
from database import log_prediction, get_analytics
from journal import (
    add_entry as journal_add,
    get_entries as journal_list,
    delete_entry as journal_delete,
    get_stats as journal_stats,
)
from activity import (
    add_activity as activity_add,
    get_activities as activity_list,
    delete_activity as activity_delete,
    get_activity_stats as activity_stats,
)
from expenses import (
    add_expense as expense_add,
    get_expenses as expense_list,
    delete_expense as expense_delete,
    get_expense_stats as expense_stats,
)
from profit import (
    get_profit_summary as profit_summary,
    calculate_profit as profit_calc,
)

app = Flask(__name__)
CORS(app)


def error_response(message: str, code: int = 400):
    return jsonify({"success": False, "error": message}), code


def ok_response(data: dict):
    return jsonify({"success": True, **data})


# ── 1: Home ────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return ok_response({
        "name": "AgriTech AI Platform API",
        "version": "1.6.0",
        "author": "Daniel Oyanogbezina",
        "mission": "AI-powered farming advice for Nigerian farmers",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "GET /api/crops": "List supported crops",
            "POST /api/predict": "Predict yield + advice",
            "GET /api/calendar/<crop>": "Monthly crop calendar",
            "GET /api/advice/<crop>": "Full advice for a crop",
            "GET /api/weather/<state>": "Rainfall for a state",
            "GET /api/states": "List Nigerian states",
            "GET /api/analytics": "Dashboard analytics",
            "GET /api/diseases/<crop>": "Diseases for a crop",
            "GET /api/diseases": "All disease counts",
            "GET /api/journal": "List journal entries",
            "POST /api/journal": "Save a journal entry",
            "DELETE /api/journal/<id>": "Delete a journal entry",
            "GET /api/activity": "List farm activities",
            "POST /api/activity": "Save a farm activity",
            "DELETE /api/activity/<id>": "Delete a farm activity",
            "GET /api/expenses": "List expenses and spend summary",
            "POST /api/expenses": "Save a farm expense",
            "DELETE /api/expenses/<id>": "Delete a farm expense",
            "GET /api/profit": "Profit summary with expense totals by crop",
            "POST /api/profit": "Calculate profit for a crop",
        },
        "supported_crops": SUPPORTED_CROPS,
    })


# ── 2: Health ──────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return ok_response({
        "status": "online",
        "model_loaded": MODEL_LOADED,
        "timestamp": datetime.datetime.now().isoformat(),
        "server": "AgriTech AI Platform v1.6",
    })


# ── 3: List crops ──────────────────────────────────────────
@app.route("/api/crops", methods=["GET"])
def list_crops():
    crops_info = []
    for crop in SUPPORTED_CROPS:
        info = CROP_ADVICE[crop]
        crops_info.append({
            "crop": crop,
            "season": info["season"],
            "planting_months": info["planting_months"],
            "harvest_months": info["harvest_months"],
        })
    return ok_response({"crops": crops_info})


# ── 4: Predict yield ───────────────────────────────────────
@app.route("/api/predict", methods=["POST"])
def predict():
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")
    try:
        result = predict_and_advise(body)
        try:
            log_prediction(body, result)
        except Exception:
            pass
        return ok_response(result)
    except Exception as e:
        return error_response(f"Prediction failed: {e}")


# ── 5: Crop calendar ───────────────────────────────────────
@app.route("/api/calendar/<crop>", methods=["GET"])
def crop_calendar(crop):
    crop = crop.capitalize()
    if crop not in SUPPORTED_CROPS:
        return error_response(f"Unsupported crop: {crop}", 404)
    return ok_response(get_calendar(crop))


# ── 6: Crop advice ─────────────────────────────────────────
@app.route("/api/advice/<crop>", methods=["GET"])
def crop_advice(crop):
    crop = crop.capitalize()
    if crop not in SUPPORTED_CROPS:
        return error_response(f"Unsupported crop: {crop}", 404)
    return ok_response(CROP_ADVICE[crop])


# ── 7: Weather by state ────────────────────────────────────
@app.route("/api/weather/<state>", methods=["GET"])
def weather(state):
    state = state.title()
    if state not in NIGERIAN_STATES:
        return error_response(f"Unknown state: {state}", 404)
    return ok_response({
        "state": state,
        "rainfall_mm": REGION_RAINFALL.get(state, 0),
        "months": MONTH_NAMES,
    })


# ── 8: List states ─────────────────────────────────────────
@app.route("/api/states", methods=["GET"])
def states():
    return ok_response({"states": get_state_list()})


# ── 9: Analytics ───────────────────────────────────────────
@app.route("/api/analytics", methods=["GET"])
def analytics():
    try:
        data = get_analytics()
        return ok_response(data)
    except Exception as e:
        return error_response(f"Analytics failed: {e}")


# ── 10: Diseases for a crop ────────────────────────────────
@app.route("/api/diseases/<crop>", methods=["GET"])
def diseases_for_crop(crop):
    crop = crop.capitalize()
    if crop not in SUPPORTED_CROPS:
        return error_response(f"Unsupported crop: {crop}", 404)
    return ok_response({"crop": crop, "diseases": get_diseases(crop)})


# ── 11: All diseases ───────────────────────────────────────
@app.route("/api/diseases", methods=["GET"])
def all_diseases():
    counts = get_all_diseases()
    return ok_response({"diseases": counts, "total": sum(counts.values())})


# ── 12: Journal list and save ──────────────────────────────
@app.route("/api/journal", methods=["GET", "POST"])
def journal():
    if request.method == "GET":
        limit = request.args.get("limit", 100)
        return ok_response({"entries": journal_list(limit), "stats": journal_stats()})
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")
    try:
        entry = journal_add(body)
        return ok_response({"entry": entry})
    except Exception as e:
        return error_response(f"Could not save journal entry: {e}")


# ── 13: Journal delete ─────────────────────────────────────
@app.route("/api/journal/<entry_id>", methods=["DELETE"])
def journal_delete_one(entry_id):
    ok = journal_delete(entry_id)
    if not ok:
        return error_response("Journal entry not found.", 404)
    return ok_response({"deleted": entry_id})


# ── 14: Activity list and save ─────────────────────────────
@app.route("/api/activity", methods=["GET", "POST"])
def activity():
    if request.method == "GET":
        limit = request.args.get("limit", 100)
        return ok_response({
            "activities": activity_list(limit),
            "stats": activity_stats(),
        })
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")
    try:
        entry = activity_add(body)
        return ok_response({"entry": entry})
    except Exception as e:
        return error_response(f"Could not save activity: {e}")


# ── 15: Activity delete ────────────────────────────────────
@app.route("/api/activity/<activity_id>", methods=["DELETE"])
def activity_delete_one(activity_id):
    ok = activity_delete(activity_id)
    if not ok:
        return error_response("Activity not found.", 404)
    return ok_response({"deleted": activity_id})


# ── 16: Expense list and save ──────────────────────────────
@app.route("/api/expenses", methods=["GET", "POST"])
def expenses():
    if request.method == "GET":
        limit = request.args.get("limit", 100)
        return ok_response({
            "expenses": expense_list(limit),
            "stats": expense_stats(),
        })
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")
    try:
        entry = expense_add(body)
        return ok_response({"entry": entry})
    except Exception as e:
        return error_response(f"Could not save expense: {e}")


# ── 17: Expense delete ─────────────────────────────────────
@app.route("/api/expenses/<expense_id>", methods=["DELETE"])
def expense_delete_one(expense_id):
    ok = expense_delete(expense_id)
    if not ok:
        return error_response("Expense not found.", 404)
    return ok_response({"deleted": expense_id})


# ── 18: Profit summary and calculation ─────────────────────
@app.route("/api/profit", methods=["GET", "POST"])
def profit():
    if request.method == "GET":
        return ok_response(profit_summary())
    body = request.get_json(silent=True)
    if not body:
        return error_response("Request body must be JSON.")
    try:
        result = profit_calc(
            crop=body.get("crop", "Cassava"),
            yield_kg=body.get("yield_kg", 0),
            price_per_kg=body.get("price_per_kg", 0),
            total_cost=body.get("total_cost", 0),
        )
        return ok_response(result)
    except Exception as e:
        return error_response(f"Could not calculate profit: {e}")


# ── Error handlers ─────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return error_response(
        "Endpoint not found. Visit / for all endpoints.", 404)


@app.errorhandler(405)
def method_not_allowed(e):
    return error_response("Method not allowed.", 405)


@app.errorhandler(500)
def server_error(e):
    return error_response("Internal server error.", 500)


# ── Run ────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" AgriTech AI Platform — Farmer Advisory API v1.6")
    print(" Author: Daniel Oyanogbezina")
    print("=" * 60)
    print(f" Model loaded : {MODEL_LOADED}")
    print(f" Supported crops : {SUPPORTED_CROPS}")
    print(f" Nigerian states : {len(NIGERIAN_STATES)}")
    print(f" Diseases loaded : {sum(get_all_diseases().values())}")
    print()
    print(" Routes (19 total):")
    print(" GET http://127.0.0.1:5001/")
    print(" GET http://127.0.0.1:5001/health")
    print(" GET http://127.0.0.1:5001/api/crops")
    print(" POST http://127.0.0.1:5001/api/predict")
    print(" GET http://127.0.0.1:5001/api/calendar/<crop>")
    print(" GET http://127.0.0.1:5001/api/advice/<crop>")
    print(" GET http://127.0.0.1:5001/api/weather/<state>")
    print(" GET http://127.0.0.1:5001/api/states")
    print(" GET http://127.0.0.1:5001/api/analytics")
    print(" GET http://127.0.0.1:5001/api/diseases/<crop>")
    print(" GET http://127.0.0.1:5001/api/diseases")
    print(" GET http://127.0.0.1:5001/api/journal")
    print(" POST http://127.0.0.1:5001/api/journal")
    print(" DELETE http://127.0.0.1:5001/api/journal/<id>")
    print(" GET http://127.0.0.1:5001/api/activity")
    print(" POST http://127.0.0.1:5001/api/activity")
    print(" DELETE http://127.0.0.1:5001/api/activity/<id>")
    print(" GET http://127.0.0.1:5001/api/expenses <- Day 25")
    print(" POST http://127.0.0.1:5001/api/expenses <- Day 25")
    print(" DELETE http://127.0.0.1:5001/api/expenses/<id> <- Day 25")
    print(" GET http://127.0.0.1:5001/api/profit <- NEW Day 26")
    print(" POST http://127.0.0.1:5001/api/profit <- NEW Day 26")
    print()
    print(" Press CTRL+C to stop")
    print("=" * 60 + "\n")
    app.run(host="127.0.0.1", port=5001, debug=True)