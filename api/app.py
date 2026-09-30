"""
app.py
AgriTech AI Platform — Flask REST API
Author : Daniel Oyanogbezina
Purpose: Exposes the farmer advisory tool as HTTP endpoints
         so any phone, app, or website can call the AI

Run:   python3 api/app.py
Test:  curl http://127.0.0.1:5001/health
"""

import sys
import os
import urllib.request
import json as json_lib

# Make sure Python can find advisory.py and predictor.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask      import Flask, request, jsonify
from flask_cors import CORS
import datetime

from advisory  import (
    SUPPORTED_CROPS, CROP_ADVICE,
    get_calendar, MONTH_NAMES, NIGERIAN_STATES, REGION_RAINFALL, get_state_list
)
from predictor import predict_and_advise, MODEL_LOADED

# ── App setup ─────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)   # allows browser apps and mobile apps to call this API

# ── Helper ────────────────────────────────────────────────────────────
def error_response(message: str, code: int = 400):
    return jsonify({"success": False, "error": message}), code


def ok_response(data: dict):
    return jsonify({"success": True, **data})


# ─────────────────────────────────────────────────────────────────────
# ENDPOINT 1 — Home
# GET /
# Returns API information and all available endpoints
# ─────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return ok_response({
        "name":    "AgriTech AI Platform API",
        "version": "1.0.0",
        "author":  "Daniel Oyanogbezina",
        "mission": "AI-powered farming advice for Nigerian farmers",
        "endpoints": {
            "GET  /":                     "This page — API information",
            "GET  /health":               "Check if server is running",
            "GET  /api/crops":            "List all supported crops",
            "POST /api/predict":          "Predict yield + get advice",
            "GET  /api/calendar/<crop>":  "Monthly crop action calendar",
            "GET  /api/advice/<crop>":    "Full advice for a crop",
        },
        "supported_crops": SUPPORTED_CROPS,
    })


# ─────────────────────────────────────────────────────────────────────
# ENDPOINT 2 — Health check
# GET /health
# Used by monitoring tools and mobile apps to confirm the server is up
# ─────────────────────────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return ok_response({
        "status":       "online",
        "model_loaded": MODEL_LOADED,
        "timestamp":    datetime.datetime.now().isoformat(),
        "server":       "AgriTech AI Platform v1.0",
    })


# ─────────────────────────────────────────────────────────────────────
# ENDPOINT 3 — List crops
# GET /api/crops
# Returns all crops the model and knowledge base support
# ─────────────────────────────────────────────────────────────────────
@app.route("/api/crops", methods=["GET"])
def list_crops():
    crops_info = []
    for crop in SUPPORTED_CROPS:
        info = CROP_ADVICE[crop]
        crops_info.append({
            "crop":         crop,
            "season":       info["season"],
            "harvest_time": info["harvest"],
            "market_tip":   info["market_tip"],
            "price_range_ngn_per_ton": {
                "low":  info["price_range"][0],
                "high": info["price_range"][1],
            },
        })
    return ok_response({
        "count":  len(crops_info),
        "crops":  crops_info,
    })


# ─────────────────────────────────────────────────────────────────────
# ENDPOINT 4 — Predict yield + get full advice  ★ MAIN ENDPOINT ★
# POST /api/predict
# Body (JSON):
#   {
#     "crop":           "Cassava",        required
#     "rainfall_mm":    1200,             required
#     "soil_ph":        6.2,              required
#     "fertilizer_kg":  100,              required
#     "improved_seeds": true,             required
#     "irrigation":     false,            required
#     "farm_size_ha":   3.5              required
#   }
# ─────────────────────────────────────────────────────────────────────
@app.route("/api/predict", methods=["POST"])
def predict():

    # ── Parse request body ──
    body = request.get_json(silent=True)
    if not body:
        return error_response(
            "Request body must be JSON. "
            "Set Content-Type: application/json header."
        )

    # ── Required fields check ──
    required = [
        "crop", "rainfall_mm", "soil_ph",
        "fertilizer_kg", "improved_seeds",
        "irrigation", "farm_size_ha",
    ]
    missing = [f for f in required if f not in body]
    if missing:
        return error_response(
            f"Missing required fields: {missing}. "
            f"All fields are required: {required}"
        )

    # ── Type coercion (handles strings from mobile forms) ──
    try:
        crop           = str(body["crop"])
        rainfall_mm    = float(body["rainfall_mm"])
        soil_ph        = float(body["soil_ph"])
        fertilizer_kg  = float(body["fertilizer_kg"])
        improved_seeds = bool(body["improved_seeds"])
        irrigation     = bool(body["irrigation"])
        farm_size_ha   = float(body["farm_size_ha"])
    except (ValueError, TypeError) as e:
        return error_response(f"Invalid field type: {e}")

    # ── Call prediction engine ──
    result = predict_and_advise(
        crop           = crop,
        rainfall_mm    = rainfall_mm,
        soil_ph        = soil_ph,
        fertilizer_kg  = fertilizer_kg,
        improved_seeds = improved_seeds,
        irrigation     = irrigation,
        farm_size_ha   = farm_size_ha,
    )

    # ── Return error from predictor if any ──
    if "error" in result:
        return error_response(result["error"])

    return ok_response({"result": result})


# ─────────────────────────────────────────────────────────────────────
# ENDPOINT 5 — Crop calendar
# GET /api/calendar/<crop>
# GET /api/calendar/<crop>?month=9   (optional month override)
# Returns what to do this month, last month, and next month
# ─────────────────────────────────────────────────────────────────────
@app.route("/api/calendar/<crop>", methods=["GET"])
def crop_calendar(crop):
    crop = crop.strip().title()
    if crop not in SUPPORTED_CROPS:
        return error_response(
            f"Crop '{crop}' not supported. "
            f"Supported: {SUPPORTED_CROPS}"
        )

    # Allow optional ?month=N query parameter for testing
    try:
        month = int(request.args.get("month",
                    datetime.datetime.now().month))
        if not 1 <= month <= 12:
            return error_response("month must be between 1 and 12")
    except ValueError:
        return error_response("month must be an integer (1-12)")

    calendar = get_calendar(crop, month)
    return ok_response({"calendar": calendar})


# ─────────────────────────────────────────────────────────────────────
# ENDPOINT 6 — Full crop advice (no prediction)
# GET /api/advice/<crop>
# Returns all static advice for a crop without needing farm inputs
# ─────────────────────────────────────────────────────────────────────
@app.route("/api/advice/<crop>", methods=["GET"])
def crop_advice(crop):
    crop = crop.strip().title()
    if crop not in SUPPORTED_CROPS:
        return error_response(
            f"Crop '{crop}' not supported. "
            f"Supported: {SUPPORTED_CROPS}"
        )

    info = CROP_ADVICE[crop]
    return ok_response({
        "crop":   crop,
        "advice": {
            "season":        info["season"],
            "soil_ph":       info["soil_ph"],
            "spacing":       info["spacing"],
            "harvest":       info["harvest"],
            "fertilizer":    info["fertilizer"],
            "water_need":    info["water_need"],
            "disease_watch": info["disease_watch"],
            "market_tip":    info["market_tip"],
            "price_range_ngn_per_ton": {
                "low":  info["price_range"][0],
                "high": info["price_range"][1],
            },
        },
    })


# ─────────────────────────────────────────────────────────────────────
# Error handlers — return JSON errors, not HTML pages
# ─────────────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return error_response(
        f"Endpoint not found. Visit / for a list of endpoints.", 404
    )


@app.errorhandler(405)
def method_not_allowed(e):
    return error_response(
        "Method not allowed. Check GET vs POST for this endpoint.", 405
    )


@app.errorhandler(500)
def server_error(e):
    return error_response("Internal server error.", 500)


# ─────────────────────────────────────────────────────────────────────
# ENDPOINT 7 — State weather data
# GET /api/weather/<state>
# Returns real rainfall data for a Nigerian state
# Uses Open-Meteo API (free, no API key needed)
# ─────────────────────────────────────────────────────────────────────
@app.route("/api/weather/<state>", methods=["GET"])
def get_state_weather(state):
    """
    Fetches real current weather data for a Nigerian state.
    Returns annual rainfall estimate based on recent data.
    Farmer selects state → rainfall fills automatically.
    """
    # Find state in our database
    state_title = state.strip().title()

    # Try to find the state (flexible matching)
    matched_state = None
    for s in NIGERIAN_STATES:
        if s.lower() == state.lower() or \
           s.lower().replace(" ", "") == state.lower().replace(" ", ""):
            matched_state = s
            break

    if not matched_state:
        return error_response(
            f"State '{state}' not found. "
            f"Use /api/states for the full list."
        )

    coords    = NIGERIAN_STATES[matched_state]
    lat, lon  = coords["lat"], coords["lon"]
    region    = coords["region"]

    # Fetch real weather from Open-Meteo (free, no key)
    try:
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&daily=precipitation_sum"
            f"&timezone=Africa%2FLagos"
            f"&past_days=30"
            f"&forecast_days=1"
        )

        req      = urllib.request.Request(
            weather_url,
            headers={"User-Agent": "AgriTechAI/1.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw      = resp.read().decode()
            wdata    = json_lib.loads(raw)

        # Sum last 30 days of rainfall
        daily_rain   = wdata.get("daily", {}).get("precipitation_sum", [])
        rain_30_days = sum(r for r in daily_rain if r is not None)

        # Extrapolate to annual estimate
        annual_estimate = round(rain_30_days * 12)

        # Apply regional adjustment
        # (30-day window may not represent full season)
        regional_typical = REGION_RAINFALL[region]
        blended = round((annual_estimate * 0.4) + (regional_typical * 0.6))

        return ok_response({
            "state":            matched_state,
            "region":           region,
            "coordinates":      {"lat": lat, "lon": lon},
            "weather": {
                "rainfall_30_days_mm":    round(rain_30_days, 1),
                "annual_estimate_mm":     annual_estimate,
                "recommended_input_mm":   blended,
                "source":                 "Open-Meteo + regional data",
            },
            "farming_context": {
                "typical_annual_mm": regional_typical,
                "note": (
                    "Use recommended_input_mm as your rainfall value. "
                    "This blends recent weather with historical regional data."
                ),
            },
        })

    except Exception as e:
        # Fallback to regional average if API fails
        regional_typical = REGION_RAINFALL[region]
        return ok_response({
            "state":    matched_state,
            "region":   region,
            "weather": {
                "recommended_input_mm": regional_typical,
                "source":               "regional historical average (live data unavailable)",
            },
            "farming_context": {
                "typical_annual_mm": regional_typical,
                "note": "Live weather unavailable. Using historical regional average.",
            },
        })


# ─────────────────────────────────────────────────────────────────────
# ENDPOINT 8 — List all Nigerian states
# GET /api/states
# ─────────────────────────────────────────────────────────────────────
@app.route("/api/states", methods=["GET"])
def list_states():
    """Returns all supported Nigerian states"""
    return ok_response({
        "count":  len(NIGERIAN_STATES),
        "states": get_state_list(),
    })


# ─────────────────────────────────────────────────────────────────────
# Run the server
# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  AgriTech AI Platform — Farmer Advisory API")
    print("  Author: Daniel Oyanogbezina")
    print("=" * 60)
    print(f"  Model loaded     : {MODEL_LOADED}")
    print(f"  Supported crops  : {SUPPORTED_CROPS}")
    print()
    print("  Endpoints:")
    print("  GET  http://127.0.0.1:5001/")
    print("  GET  http://127.0.0.1:5001/health")
    print("  GET  http://127.0.0.1:5001/api/crops")
    print("  POST http://127.0.0.1:5001/api/predict")
    print("  GET  http://127.0.0.1:5001/api/calendar/<crop>")
    print("  GET  http://127.0.0.1:5001/api/advice/<crop>")
    print()
    print("  Press CTRL+C to stop")
    print("=" * 60 + "\n")

    app.run(host="127.0.0.1", port=5001, debug=True)# Day 8 redeployment trigger
